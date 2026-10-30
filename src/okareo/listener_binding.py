"""A custom multiturn Target's use of the Run's NATS connection: its ``bind_listener`` and the release it returns.

A Target opts in by defining ``bind_listener(nc, invoke_id)`` on its class
(``BindsListener``). The SDK's custom-model listener calls it once per Run, on
the listener's own event loop, after its ``invoke.<invoke_id>`` subscription is
flushed and before the Run starts; it returns None, or a release
(``ListenerRelease``) that the listener runs before it closes the connection.

``ListenerBinding`` is that call and that release for one Run. A bind that
raises, returns something that is not a release, or, as a coroutine, runs past
``LISTENER_BIND_TIMEOUT_SECONDS`` is a ``ListenerBindError``. A release that
raises or, as a coroutine, runs past ``LISTENER_RELEASE_TIMEOUT_SECONDS`` is
logged, never raised. The time limits apply to coroutines only: a plain-function
``bind_listener`` or release runs on the listener's loop and blocks it until it
returns.
"""

import asyncio
import inspect
from typing import TYPE_CHECKING, Awaitable, Callable, Optional, Protocol, Union, cast

from okareo.error import ListenerBindError

if TYPE_CHECKING:
    from nats.aio.client import Client as NATS

# The method a Target defines to be handed the Run's NATS connection.
# okareo.model_under_test re-exports it: its presence there tells a caller
# (okareo-vision's client relay) that this SDK calls it.
LISTENER_BIND_HOOK = "bind_listener"
# How long a coroutine bind_listener, and a coroutine release, may take. A plain
# function is not cut off: it runs on the listener's loop until it returns.
LISTENER_BIND_TIMEOUT_SECONDS = 30.0
LISTENER_RELEASE_TIMEOUT_SECONDS = 30.0

ListenerRelease = Callable[[], Optional[Awaitable[None]]]
"""What ``bind_listener`` returns when it bound something: a function or a
coroutine function, no arguments, that lets go of everything it started."""


class BindsListener(Protocol):
    """A custom multiturn Target that is handed the Run's NATS connection."""

    def bind_listener(
        self, nc: "NATS", invoke_id: str
    ) -> Union[Optional[ListenerRelease], Awaitable[Optional[ListenerRelease]]]:
        """Use ``nc`` (subscribe, publish, start tasks on the listener's loop)
        for the Run whose id on NATS is ``invoke_id``; None, or the release."""


class _OutOfTime(Exception):
    """The Target's coroutine did not finish in its time and was cancelled."""


class _EndedCancelled(Exception):
    """The Target's coroutine ended cancelled: a task it cancelled and awaited."""


class ListenerBinding:
    """One Run's call of a Target's ``bind_listener``, and the release it holds until the listener stops."""

    def __init__(self, target: BindsListener, log: Callable[[str], None]) -> None:
        self._target = target
        self._log = log
        self._release: Optional[Callable[[], object]] = None

    @classmethod
    def for_target(
        cls, target: object, log: Callable[[str], None]
    ) -> Optional["ListenerBinding"]:
        """A binding for ``target`` when its class defines ``bind_listener``; None otherwise.

        The hook is read off the class, not the instance, so an object whose
        ``__getattr__`` answers any name (a proxy, a Target forwarding to a
        client) is not taken as opted in. ``log`` writes one line, already
        labelled with the listener it belongs to."""
        if inspect.getattr_static(type(target), LISTENER_BIND_HOOK, None) is None:
            return None
        if not callable(getattr(target, LISTENER_BIND_HOOK)):
            return None
        return cls(cast(BindsListener, target), log)

    async def bind(self, nc: "NATS", invoke_id: str) -> None:
        """Hand the Target ``nc`` and ``invoke_id``, and hold the release it returns.

        The release is held the moment ``bind_listener`` returns, so whatever
        fails after it, ``release`` still lets go. Any failure of the bind
        itself is a ``ListenerBindError`` saying what happened, caused by the
        Target's own exception when there is one."""
        try:
            bound = await self._finished(
                self._target.bind_listener(nc, invoke_id), LISTENER_BIND_TIMEOUT_SECONDS
            )
        except _OutOfTime:
            raise ListenerBindError(
                f"the Target's {LISTENER_BIND_HOOK} did not return within "
                f"{LISTENER_BIND_TIMEOUT_SECONDS:.0f}s"
            ) from None
        except _EndedCancelled as e:
            raise ListenerBindError(
                f"the Target's {LISTENER_BIND_HOOK} ended cancelled"
            ) from e.__cause__
        except Exception as e:
            raise ListenerBindError(
                f"the Target's {LISTENER_BIND_HOOK} failed: {type(e).__name__}: {e}"
            ) from e
        if bound is None:
            return
        if not callable(bound):
            raise ListenerBindError(
                f"the Target's {LISTENER_BIND_HOOK} returned a {type(bound).__name__}; "
                "it returns None, or a callable that releases what it bound"
            )
        self._release = bound
        self._log(f"the Target is using the Run's NATS connection ({LISTENER_BIND_HOOK})")

    async def release(self) -> None:
        """Run the release ``bind_listener`` returned, once, if it returned one.

        Never raises: the listener is stopping either way and its connection
        still has to close, so a release that fails, ends cancelled or runs out
        of time is logged."""
        release, self._release = self._release, None
        if release is None:
            return
        closing = "closing NATS anyway"
        try:
            await self._finished(release(), LISTENER_RELEASE_TIMEOUT_SECONDS)
        except _OutOfTime:
            self._log(
                f"the Target's {LISTENER_BIND_HOOK} release did not finish within "
                f"{LISTENER_RELEASE_TIMEOUT_SECONDS:.0f}s; {closing}"
            )
        except _EndedCancelled:
            self._log(f"the Target's {LISTENER_BIND_HOOK} release ended cancelled; {closing}")
        except Exception as e:
            self._log(
                f"the Target's {LISTENER_BIND_HOOK} release failed "
                f"({type(e).__name__}: {e}); {closing}"
            )

    async def _finished(self, returned: object, seconds: float) -> object:
        """``returned``, or, when it is awaitable, what it ends with, waited for at most ``seconds``.

        Past that it is cancelled and ``_OutOfTime`` is raised, kept apart from
        a timeout the Target raises itself (nats-py's ``TimeoutError`` is
        asyncio's), which is raised as it is. A cancellation that arrives when
        the result is read is the Target's own (the listener is already past
        the wait), so it is ``_EndedCancelled``, an ordinary exception; a
        cancellation of the listener, during the wait, still propagates."""
        if not inspect.isawaitable(returned):
            return returned
        pending = asyncio.ensure_future(returned)
        done, _ = await asyncio.wait({pending}, timeout=seconds)
        if not done:
            pending.cancel()
            await asyncio.gather(pending, return_exceptions=True)
            raise _OutOfTime()
        try:
            return pending.result()
        except asyncio.CancelledError as e:
            raise _EndedCancelled() from e

