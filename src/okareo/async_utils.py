import collections
import threading
import time
from abc import abstractmethod
from typing import Any, Callable, Deque, Tuple, Union

from okareo_api_client.client import Client

_DEFAULT_MAX_QUEUE_SIZE = 2048
_DEFAULT_SCHEDULE_DELAY_MILLIS = 1000
_DEFAULT_MAX_BATCH_SIZE = 512
_DEFAULT_ASYNC_CALL_RETRIES = 5


class AsyncProcessorMixin:
    def __init__(self, name: str = "AsyncProcessor") -> None:
        self.queue: Deque[Tuple[Callable, Any]] = collections.deque(
            [], _DEFAULT_MAX_QUEUE_SIZE
        )
        self.done = False
        self._data_dropped = False
        self.worker_thread = threading.Thread(
            name=name, target=self.worker, daemon=True
        )
        self.condition = threading.Condition(threading.Lock())
        self.worker_thread.start()

    @abstractmethod
    def get_client(self) -> Client:
        """Return API Client instance"""

    @abstractmethod
    def get_api_key(self) -> str:
        """Get Okareo API key to use"""

    def async_call(self, func: Callable, data: Any) -> bool:
        if len(self.queue) == _DEFAULT_MAX_QUEUE_SIZE:
            if not self._data_dropped:
                print("Queue is full, data points might get dropped.")
            self._data_dropped = True
        self.queue.append((func, data))

        if len(self.queue) >= int(_DEFAULT_MAX_BATCH_SIZE):
            with self.condition:
                self.condition.notify()
        return True

    def _perform_call(self, func: Callable, data: Any) -> Union[Any, None]:
        attempts = 0
        while attempts < _DEFAULT_ASYNC_CALL_RETRIES:
            try:
                return func(
                    client=self.get_client(),
                    api_key=self.get_api_key(),
                    json_body=data,
                )

            except Exception as e:
                print("Error performing async call", e)
                attempts += 1
            # .1, .2, .4, .8, 1.6, 3.2, ...
            time.sleep(0.1 * 2 ** (attempts - 1))
        return None

    def worker(self) -> None:
        timeout = _DEFAULT_SCHEDULE_DELAY_MILLIS / 1e3

        while not self.done:
            with self.condition:
                if self.done:
                    break  # if flag has changed
                if not self.queue:
                    self.condition.wait(timeout)

            idx = 0
            entries = []
            while idx < _DEFAULT_MAX_BATCH_SIZE and self.queue:
                entries.append(self.queue.popleft())

            for entry in entries:
                func, data = entry
                self._perform_call(func, data)

    def flush(self) -> None:
        # signal the worker thread to finish and then wait for it
        print("Shutting down")
        self.done = True
        with self.condition:
            self.condition.notify_all()
        self.worker_thread.join()
