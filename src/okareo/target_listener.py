"""TargetListener: a custom Target answered on its own channel, with no Run.

``ModelUnderTest.listen_on_target_channel`` starts one. It answers whatever
Okareo sends the Target (a session opened, a turn's messages, a session ended)
for as long as it runs, with no Run submitted and no Run watched: it ends only
when ``stop`` is called, or when its connection to NATS is gone for good. A
process that serves a Target, such as okareo-vision's runner, holds one and
waits on it.
"""

from __future__ import annotations

import threading
from typing import Optional


class TargetListener:
    """A listener on one Target's own channel (``channel``)."""

    def __init__(
        self,
        stop_event: threading.Event,
        thread: threading.Thread,
        stats: dict,
        channel: str,
    ) -> None:
        self.channel = channel
        self._stop_event, self._thread, self._stats = stop_event, thread, stats

    def is_listening(self) -> bool:
        """Whether it is still connected and answering."""
        return self._thread.is_alive() and not self._stats.get("closed")

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Block until the listener ends, or ``timeout`` seconds pass; whether it ended."""
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def stop(self, timeout: float = 5.0) -> None:
        """Stop answering and close the connection, waiting at most ``timeout`` seconds."""
        self._stop_event.set()
        self._thread.join(timeout)

    def describe(self) -> str:
        """Its state in a few words: connected or not, and how often the connection dropped."""
        return (
            f"connected: {'yes' if self.is_listening() else 'no'} "
            f"(disconnects {self._stats.get('disconnects', 0)}, "
            f"reconnects {self._stats.get('reconnects', 0)}, "
            f"answered {self._stats.get('turns_answered', 0)})"
        )
