"""Deliver queued API calls from a background thread that starts on the first call.

The thread starts when the first call is queued, not when the object is built, so an
object that never queues anything costs no thread. ``close()`` (or leaving a ``with``
block) delivers what is queued and stops the thread without printing. Problems go to
this module's logger, never to stdout.
"""

import collections
import logging
import threading
import time
from abc import abstractmethod
from types import TracebackType
from typing import Any, Callable, Deque, List, Optional, Tuple, Type, TypeVar, Union

from okareo_api_client.client import Client

_DEFAULT_MAX_QUEUE_SIZE = 2048
_DEFAULT_SCHEDULE_DELAY_MILLIS = 1000
_DEFAULT_MAX_BATCH_SIZE = 512
_DEFAULT_ASYNC_CALL_RETRIES = 5
# How long close() waits for the worker to deliver what is queued. Past it, close()
# returns and the daemon thread finishes delivering on its own, then exits.
_CLOSE_JOIN_TIMEOUT_SECONDS = 5.0

_ProcessorT = TypeVar("_ProcessorT", bound="AsyncProcessorMixin")

# Never stdout: a stdio MCP server speaks its protocol there, and a stray line breaks it.
logger = logging.getLogger(__name__)


class AsyncProcessorMixin:
    def __init__(self, name: str = "AsyncProcessor") -> None:
        self.queue: Deque[Tuple[Callable, Any]] = collections.deque(
            [], _DEFAULT_MAX_QUEUE_SIZE
        )
        self.done = False
        self._data_dropped = False
        self._worker_name = name
        # Started by the first async_call; None until then.
        self.worker_thread: Optional[threading.Thread] = None
        # Guards starting the worker, queueing, and setting done, so a call that
        # races close() is either queued before the worker drains or refused.
        self.condition = threading.Condition(threading.Lock())

    def __enter__(self: _ProcessorT) -> _ProcessorT:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    @abstractmethod
    def get_client(self) -> Client:
        """Return API Client instance"""

    @abstractmethod
    def get_api_key(self) -> str:
        """Get Okareo API key to use"""

    def async_call(self, func: Callable, data: Any) -> bool:
        """Queue one call for the worker. False once close() or flush() has run."""
        with self.condition:
            if self.done:
                return False
            if self.worker_thread is None:
                self.worker_thread = threading.Thread(
                    name=self._worker_name, target=self.worker, daemon=True
                )
                self.worker_thread.start()
            if len(self.queue) == _DEFAULT_MAX_QUEUE_SIZE:
                if not self._data_dropped:
                    logger.warning("Queue is full, data points might get dropped.")
                self._data_dropped = True
            self.queue.append((func, data))

            if len(self.queue) >= int(_DEFAULT_MAX_BATCH_SIZE):
                self.condition.notify()
        return True

    def close(self) -> None:
        """Deliver what is queued, then stop the worker thread. Prints nothing.

        Waits up to a few seconds for the delivery; safe to call more than once,
        and on an object that never queued anything (it has no thread to stop).
        """
        self._stop(join_timeout=_CLOSE_JOIN_TIMEOUT_SECONDS)

    def flush(self) -> None:
        """Print "Shutting down", deliver what is queued, then stop the worker thread.

        Waits with no time limit. close() does the same without printing.
        """
        print("Shutting down")
        self._stop(join_timeout=None)

    def worker(self) -> None:
        """The worker thread's loop: send queued calls in batches until close()
        or flush(), then send whatever is still queued."""
        timeout = _DEFAULT_SCHEDULE_DELAY_MILLIS / 1e3

        while not self.done:
            with self.condition:
                if self.done:
                    break  # if flag has changed
                if not self.queue:
                    self.condition.wait(timeout)
            self._deliver_batch()

        # close() or flush() set done: deliver everything queued before it.
        while self.queue:
            self._deliver_batch()

    def _stop(self, join_timeout: Optional[float]) -> None:
        with self.condition:
            self.done = True
            thread = self.worker_thread
            self.condition.notify_all()
        if thread is not None and thread is not threading.current_thread():
            thread.join(join_timeout)

    def _deliver_batch(self) -> None:
        entries: List[Tuple[Callable, Any]] = []
        while len(entries) < _DEFAULT_MAX_BATCH_SIZE and self.queue:
            entries.append(self.queue.popleft())

        for entry in entries:
            func, data = entry
            self._perform_call(func, data)

    def _perform_call(self, func: Callable, data: Any) -> Union[Any, None]:
        attempts = 0
        while attempts < _DEFAULT_ASYNC_CALL_RETRIES:
            try:
                return func(
                    client=self.get_client(),
                    api_key=self.get_api_key(),
                    body=data,
                )

            except Exception:
                attempts += 1
                logger.warning(
                    "Error performing async call (attempt %d of %d)",
                    attempts,
                    _DEFAULT_ASYNC_CALL_RETRIES,
                    exc_info=True,
                )
            # .1, .2, .4, .8, 1.6, 3.2, ...
            time.sleep(0.1 * 2 ** (attempts - 1))
        return None
