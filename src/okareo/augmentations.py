"""Voice simulation augmentation payload wrappers.

Import these from ``okareo.augmentations`` and pass them into
``Okareo.run_simulation(..., augmentation=...)``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from attrs import asdict as _attrs_asdict
from attrs import define as _attrs_define


class _DictSerializable:
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@_attrs_define
class AugmentationConfig(_DictSerializable):
    """Base helper for simulation augmentation payload wrappers.

    Subclasses are thin JSON shapers for ``simulation_params["augmentation"]``.
    They serialize only the fields you set.
    """

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in _attrs_asdict(self).items()
            if value is not None
        }


def _check_utterance_or_prompt(
    kind: str, utterance: str | None, prompt: str | None
) -> None:
    if utterance is not None and prompt is not None:
        raise ValueError(
            f"{kind} takes prompt or utterance, not both: utterance for exact "
            "words, prompt to have them written by the LLM."
        )


@_attrs_define
class CAPAugmentation(AugmentationConfig):
    """Concurrent-ask augmentation config.

    Arguments:
        probability: Probability that the driver emits an extra follow-up message.
        pause_ms: Pause duration in milliseconds before emitting the
            follow-up message. Run-wide, so not valid in a plan entry.
        consecutive_messages: How many messages the caller sends back to back
            when CAP fires, from 2 to 4. Defaults to 2 server-side.
    """

    probability: float | None = None
    pause_ms: int | None = None
    consecutive_messages: int | None = None


@_attrs_define
class DirectedSpeechAugmentation(AugmentationConfig):
    """Directed-speech augmentation config.

    Arguments:
        probability: Probability that directed speech is injected for a given
            opportunity.
        prompt: Optional independent prompt for the directed speech content.
        utterance: Exact words for the remark, spoken as given with no LLM
            call; voice and filters still apply. Not with ``prompt``.
        lpf_cutoff_hz: Low-pass filter cutoff used for off-mic speech.
        gain_db: Gain reduction applied to off-mic speech.
        start_at_turn: First turn this may fire on. Turns are counted as the
            CALLER's own turns -- the turns Okareo's simulated caller takes,
            not the agent's replies. Counting begins once the agent has said
            something, so ringing, dial tone, hold music and an empty greeting
            do not advance it. Not the transcript's turn numbering: on a call
            that takes a while to get going, the window opens later in the
            transcript than the number alone suggests. Defaults to 1
            server-side, i.e. the first turn of the conversation proper.
        end_at_turn: Last turn this may fire on, counted the same way.
            Defaults to unbounded. Set it equal to ``start_at_turn`` to narrow
            the window to a single turn -- but a window is only a window: the
            ``probability`` above is still drawn inside it, so pair a one-turn
            window with ``probability=1.0`` to actually fire on that turn.
        interrupt: Play the remark over the agent's next reply instead of
            in the caller's turn. The caller says their line as usual; the
            remark then overlaps the agent's reply to it and does not take a
            turn. Needs a connection that can interrupt the agent, as barge-in
            does. Defaults to off server-side.
        min_offset_ms: With ``interrupt``: earliest delay, after the agent
            starts speaking, before the remark plays. Defaults to 200
            server-side, as on barge-in. Only valid with ``interrupt``.
        max_offset_ms: With ``interrupt``: latest such delay; at least
            ``min_offset_ms``. Defaults to 600 server-side, as on barge-in.
            Only valid with ``interrupt``.
        seed: Optional seed that makes the probability and offset draws
            reproducible.
    """

    probability: float | None = None
    prompt: str | None = None
    lpf_cutoff_hz: int | None = None
    gain_db: float | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None
    interrupt: bool | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    seed: int | None = None
    utterance: str | None = None

    def __attrs_post_init__(self) -> None:
        _check_utterance_or_prompt("directed_speech", self.utterance, self.prompt)


@_attrs_define
class NoiseAugmentation(AugmentationConfig):
    """Background noise augmentation config.

    Arguments:
        probability: Probability that background noise is applied during a run.
        profile: Noise profile name, e.g. ``"cafeteria"`` or ``"traffic"``.
        snr_db: Target signal-to-noise ratio in dB.
    """

    probability: float | None = None
    profile: str | None = None
    snr_db: float | None = None


@_attrs_define
class SecondarySpeakerAugmentation(AugmentationConfig):
    """Secondary-speaker augmentation config.

    Arguments:
        probability: Probability that a secondary-speaker segment is injected
            for a given opportunity.
        voice: Voice identifier for the secondary speaker.
        prompt: Optional independent prompt for the secondary speaker.
        utterance: Exact words for the secondary speaker, spoken as given with
            no LLM call; voice and filters still apply. Not with ``prompt``.
        lpf_cutoff_hz: Optional low-pass filter cutoff applied only to
            the secondary speaker audio.
        gain_db: Optional gain adjustment applied only to the
            secondary speaker audio.
        inter_speaker_pause_ms: Optional pause inserted between the primary
            and secondary speaker audio segments. Not valid with ``interrupt``,
            where the remark is timed from the agent's speech instead.
        start_at_turn: First turn this may fire on. Turns are counted as the
            CALLER's own turns -- the turns Okareo's simulated caller takes,
            not the agent's replies. Counting begins once the agent has said
            something, so ringing, dial tone, hold music and an empty greeting
            do not advance it. Not the transcript's turn numbering: on a call
            that takes a while to get going, the window opens later in the
            transcript than the number alone suggests. Defaults to 1
            server-side, i.e. the first turn of the conversation proper.
        end_at_turn: Last turn this may fire on, counted the same way.
            Defaults to unbounded. Set it equal to ``start_at_turn`` to narrow
            the window to a single turn -- but a window is only a window: the
            ``probability`` above is still drawn inside it, so pair a one-turn
            window with ``probability=1.0`` to actually fire on that turn.
        interrupt: Play the remark over the agent's next reply instead of
            in the caller's turn. The caller says their line as usual; the
            remark then overlaps the agent's reply to it and does not take a
            turn. Needs a connection that can interrupt the agent, as barge-in
            does. Defaults to off server-side.
        min_offset_ms: With ``interrupt``: earliest delay, after the agent
            starts speaking, before the remark plays. Defaults to 200
            server-side, as on barge-in. Only valid with ``interrupt``.
        max_offset_ms: With ``interrupt``: latest such delay; at least
            ``min_offset_ms``. Defaults to 600 server-side, as on barge-in.
            Only valid with ``interrupt``.
        seed: Optional seed that makes the probability and offset draws
            reproducible.
    """

    probability: float | None = None
    voice: str | None = None
    prompt: str | None = None
    lpf_cutoff_hz: int | None = None
    gain_db: float | None = None
    inter_speaker_pause_ms: int | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None
    interrupt: bool | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    seed: int | None = None
    utterance: str | None = None

    def __attrs_post_init__(self) -> None:
        _check_utterance_or_prompt("secondary_speaker", self.utterance, self.prompt)


@_attrs_define
class BackchannelAugmentation(AugmentationConfig):
    """Backchannel injection augmentation config.

    Arguments:
        probability: Probability that a short backchannel is injected.
        utterance: Optional backchannel text override, e.g. ``"mm-hmm"``.
        min_offset_ms: Minimum delay before the injection fires.
        max_offset_ms: Maximum delay before the injection fires.
        start_at_turn: First turn this may fire on. Turns are counted as the
            CALLER's own turns -- the turns Okareo's simulated caller takes,
            not the agent's replies. Counting begins once the agent has said
            something, so ringing, dial tone, hold music and an empty greeting
            do not advance it. Not the transcript's turn numbering: on a call
            that takes a while to get going, the window opens later in the
            transcript than the number alone suggests. Defaults to 1
            server-side, i.e. the first turn of the conversation proper.
        end_at_turn: Last turn this may fire on, counted the same way.
            Defaults to unbounded. Set it equal to ``start_at_turn`` to narrow
            the window to a single turn -- but a window is only a window: the
            ``probability`` above is still drawn inside it, so pair a one-turn
            window with ``probability=1.0`` to actually fire on that turn.
        count: Plan entries only: how many times the backchannel plays in its
            turn. The offset window applies before the first play and again
            between plays. Defaults to 1 server-side.
    """

    probability: float | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None
    count: int | None = None


@_attrs_define
class BargeInAugmentation(AugmentationConfig):
    """Barge-in injection augmentation config.

    Arguments:
        probability: Probability that a barge-in interruption is injected.
        replacement_text: Older name for ``utterance``. Ignored server-side
            outside a plan; inside a plan it is sent as ``utterance``. Use
            ``utterance``.
        prompt: Prompt the LLM writes the interruption from.
        utterance: Exact words for the interruption, spoken as given with no
            LLM call. Not with ``prompt``.
        min_offset_ms: Minimum delay before the injection fires.
        max_offset_ms: Maximum delay before the injection fires.
        start_at_turn: First turn this may fire on. Turns are counted as the
            CALLER's own turns -- the turns Okareo's simulated caller takes,
            not the agent's replies. Counting begins once the agent has said
            something, so ringing, dial tone, hold music and an empty greeting
            do not advance it. Not the transcript's turn numbering: on a call
            that takes a while to get going, the window opens later in the
            transcript than the number alone suggests. Defaults to 1
            server-side, i.e. the first turn of the conversation proper.
        end_at_turn: Last turn this may fire on, counted the same way.
            Defaults to unbounded. Set it equal to ``start_at_turn`` to narrow
            the window to a single turn -- but a window is only a window: the
            ``probability`` above is still drawn inside it, so pair a one-turn
            window with ``probability=1.0`` to actually fire on that turn.
        count: Plan entries only: how many times the barge-in plays in its
            turn, each landing on the agent's answer to the one before.
            Defaults to 1 server-side.
    """

    probability: float | None = None
    replacement_text: str | None = None
    prompt: str | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None
    count: int | None = None

    def __attrs_post_init__(self) -> None:
        # Not ``replacement_text``: callers send it beside ``prompt`` and the
        # server ignores it outside a plan. Inside one it is checked as
        # ``utterance`` (see ``_plan_entry_dict``).
        _check_utterance_or_prompt("barge_in", self.utterance, self.prompt)


@_attrs_define
class DropoutAugmentation(AugmentationConfig):
    """Dropout augmentation config.

    Arguments:
        probability: Probability (0-1) that the driver drops an entire turn:
            nothing is said and the target hears silence for that turn.
        start_at_turn: First turn this may fire on. Turns are counted as the
            CALLER's own turns -- the turns Okareo's simulated caller takes,
            not the agent's replies. Counting begins once the agent has said
            something, so ringing, dial tone, hold music and an empty greeting
            do not advance it. Not the transcript's turn numbering: on a call
            that takes a while to get going, the window opens later in the
            transcript than the number alone suggests. Defaults to 1
            server-side, i.e. the first turn of the conversation proper.
        end_at_turn: Last turn this may fire on, counted the same way.
            Defaults to unbounded. Set it equal to ``start_at_turn`` to narrow
            the window to a single turn -- but a window is only a window: the
            ``probability`` above is still drawn inside it, so pair a one-turn
            window with ``probability=1.0`` to actually fire on that turn.
    """

    probability: float | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None


@_attrs_define
class OffMicAugmentation(AugmentationConfig):
    """Off-mic augmentation config: the caller's own line, said turned away
    from the phone.

    The driver still writes and says its line, prompt-written or a scripted
    step's words alike; it reaches the agent muffled and quieter through a
    low-pass filter and a gain cut. Nothing else is said.

    Arguments:
        probability: Probability (0-1) that a turn's line is said off-mic.
        lpf_cutoff_hz: Low-pass filter cutoff, above 0 and up to 20000 Hz.
            Defaults to 800 server-side.
        gain_db: Gain applied to the line, from -40 to 0 dB. Defaults to -8
            server-side.
        start_at_turn: First turn this may fire on, counted as the caller's
            own turns, as for ``DropoutAugmentation``. Not in a plan entry.
        end_at_turn: Last turn this may fire on, counted the same way. Not in
            a plan entry.
        seed: Seed for the probability draws.
    """

    probability: float | None = None
    lpf_cutoff_hz: float | None = None
    gain_db: float | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None
    seed: int | None = None


# The ``type`` each strategy class takes in a plan entry: its key on Augmentation.
_PLAN_TYPES: dict[type, str] = {
    CAPAugmentation: "cap",
    DirectedSpeechAugmentation: "directed_speech",
    NoiseAugmentation: "noise",
    SecondarySpeakerAugmentation: "secondary_speaker",
    BackchannelAugmentation: "backchannel",
    BargeInAugmentation: "barge_in",
    DropoutAugmentation: "dropout",
    OffMicAugmentation: "off_mic",
}

# A plan key: a turn (2 or "2"), a range ("2-4" or (2, 4)), or a turn to the
# end of the call ("5-" or (5, None)).
PlanKey = int | str | tuple[int, int | None]


@_attrs_define
class Augmentation(_DictSerializable):
    """Container for voice simulation augmentation strategy config.

    Configure it one of two ways:

    - **One strategy** for the whole run: set one strategy field. ``noise``
      may be combined with one other strategy.
    - **A per-turn plan**: ``plan`` maps the caller's turns (counted from 1,
      the same turns ``start_at_turn`` counts) to the augmentations played on
      them, using the same strategy classes. Only ``noise``, which is
      run-wide, may be set beside it.

    A plan key is a turn (``2`` or ``"2"``), a range (``"2-4"`` or
    ``(2, 4)``), or a turn to the end of the call (``"5-"`` or ``(5, None)``).
    A key's entries play on every turn it covers, and keys can't overlap.

    Each turn has two slots, and each takes one augmentation:

    - **What the caller says**: ``cap``, ``dropout``, ``off_mic``, and
      ``directed_speech`` / ``secondary_speaker`` without ``interrupt``. These
      shape or follow the caller's own line.
    - **The agent's reply**: ``barge_in``, ``backchannel``, and the speaker
      kinds with ``interrupt=True``. These play over the reply, best effort:
      one that can't land is reported as missed. ``count`` repeats a
      barge-in or backchannel, up to 6 plays per turn.

    ``dropout`` leaves the caller silent, so it takes the whole turn. The
    server refuses a plan over these limits with a 400 that names the turn and
    the slot.

    Also in a plan:

    - Entries don't take ``start_at_turn`` or ``end_at_turn`` (the key sets
      the turns), and ``probability`` defaults to 1.0, drawn on each turn.
    - Interruptions start 200-600 ms into the agent's reply by default. Real
      agents usually need later offsets.
    - ``CAPAugmentation.pause_ms`` is run-wide and can't be set in an entry.
    - ``None`` or ``[]`` for a key means no augmentation on its turns.

    Example:
        ``Augmentation(noise=NoiseAugmentation(profile="cafeteria", snr_db=10))``

        A per-turn plan::

            Augmentation(plan={
                1: [BargeInAugmentation(utterance="Can I refill my prescription?")],
                "2-3": [
                    OffMicAugmentation(),
                    BackchannelAugmentation(utterance="OK, good."),
                ],
                "5-": [BargeInAugmentation(prompt="Ask to speak to a pharmacist.")],
            })
    """

    cap: CAPAugmentation | None = None
    directed_speech: DirectedSpeechAugmentation | None = None
    noise: NoiseAugmentation | None = None
    secondary_speaker: SecondarySpeakerAugmentation | None = None
    backchannel: BackchannelAugmentation | None = None
    barge_in: BargeInAugmentation | None = None
    dropout: DropoutAugmentation | None = None
    off_mic: OffMicAugmentation | None = None
    plan: Mapping[PlanKey, Sequence[AugmentationConfig] | None] | None = None

    def __attrs_post_init__(self) -> None:
        # Refuse a bad config when it is built, not when the run is submitted.
        self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        fields = _attrs_asdict(self, recurse=False)
        plan = fields.pop("plan")
        out = {
            key: value.to_dict() for key, value in fields.items() if value is not None
        }
        if plan is None:
            for key in ("barge_in", "backchannel"):
                if "count" in out.get(key, {}):
                    raise ValueError(
                        f"{key} count only applies inside a plan, where it sets "
                        "how many times the entry plays in its turn."
                    )
            return out
        beside = sorted(set(out) - {"noise"})
        if beside:
            raise ValueError(
                f"Augmentation.plan can't be combined with {', '.join(beside)}: "
                "only noise (run-wide) sits beside a plan. Put these in the plan."
            )
        out["plan"] = _plan_to_dict(plan)
        return out


def _plan_to_dict(
    plan: Mapping[Any, Sequence[AugmentationConfig] | None],
) -> dict[str, Any]:
    """The wire shape: ``{"<key>": [{"type": ..., <fields>}, ...] | None}``, with
    keys as ``"2"``, ``"2-4"`` or ``"5-"`` in turn order."""
    if not isinstance(plan, Mapping):
        raise TypeError("Augmentation.plan must map turns to lists of augmentations.")
    boxes: list[tuple[tuple[int, int | None], Any]] = []
    for raw_key, entries in plan.items():
        box = _plan_range(raw_key)
        key = _plan_key(box)
        clash = next((b for b, _ in boxes if _overlap(b, box)), None)
        if clash is not None:
            raise ValueError(
                f"Augmentation.plan keys {_plan_key(clash)!r} and {key!r} both "
                f"cover turn {max(box[0], clash[0])}; keys can't overlap."
            )
        if entries is None:
            boxes.append((box, None))
        elif isinstance(entries, (list, tuple)):
            boxes.append((box, [_plan_entry_dict(key, entry) for entry in entries]))
        else:
            raise TypeError(
                f"Augmentation.plan key {key!r} must be a list of augmentations, "
                "or None for none."
            )
    return {
        _plan_key(box): entries for box, entries in sorted(boxes, key=lambda b: b[0][0])
    }


def _is_turn(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _plan_range(raw_key: Any) -> tuple[int, int | None]:
    """A plan key as (first turn, last turn); the last is None to the end of the call."""
    start: Any = raw_key
    end: Any = raw_key
    if isinstance(raw_key, tuple) and len(raw_key) == 2:
        start, end = raw_key
    elif isinstance(raw_key, str):
        first, dash, last = raw_key.strip().partition("-")
        start = int(first) if first.isdigit() else None
        if not dash:
            end = start
        elif last == "":
            end = None
        else:
            end = int(last) if last.isdigit() else None
            start = start if end is not None else None
    if not _is_turn(start) or not (end is None or (_is_turn(end) and end >= start)):
        raise ValueError(
            f"Invalid Augmentation.plan key {raw_key!r}: use a caller turn counted "
            'from 1 (2 or "2"), a range ("2-4" or (2, 4)), or a turn to the end '
            'of the call ("5-" or (5, None)).'
        )
    return start, end


def _plan_key(box: tuple[int, int | None]) -> str:
    start, end = box
    if end is None:
        return f"{start}-"
    return str(start) if end == start else f"{start}-{end}"


def _overlap(a: tuple[int, int | None], b: tuple[int, int | None]) -> bool:
    a_end = float("inf") if a[1] is None else a[1]
    b_end = float("inf") if b[1] is None else b[1]
    return a[0] <= b_end and b[0] <= a_end


def _plan_entry_dict(key: str, entry: Any) -> dict[str, Any]:
    entry_type = next(
        (_PLAN_TYPES[cls] for cls in type(entry).__mro__ if cls in _PLAN_TYPES),
        None,
    )
    if entry_type is None:
        raise TypeError(
            f"Augmentation.plan key {key!r} entries must be augmentation configs "
            f"such as BargeInAugmentation, not {type(entry).__name__}."
        )
    if entry_type == "noise":
        raise ValueError(
            "NoiseAugmentation is run-wide: set Augmentation(noise=...) beside "
            f"the plan, not under key {key!r}."
        )
    body = entry.to_dict()
    window = [key for key in ("start_at_turn", "end_at_turn") if key in body]
    if window:
        raise ValueError(
            f"Augmentation.plan entries don't take {' / '.join(window)}: the "
            f"key ({key}) sets the turns."
        )
    if entry_type == "cap" and "pause_ms" in body:
        raise ValueError(
            f"cap pause_ms can't be set in a plan entry (key {key!r}): it sets a "
            "run-wide pause, which can't vary by turn."
        )
    if entry_type == "barge_in" and "replacement_text" in body:
        # Inside a plan the older name means exact words, as on the server.
        if "utterance" in body:
            raise ValueError(
                "barge_in takes utterance or replacement_text, not both; use "
                "utterance."
            )
        body["utterance"] = body.pop("replacement_text")
        _check_utterance_or_prompt("barge_in", body["utterance"], body.get("prompt"))
    return {"type": entry_type, **body}


__all__ = (
    "Augmentation",
    "CAPAugmentation",
    "DirectedSpeechAugmentation",
    "NoiseAugmentation",
    "SecondarySpeakerAugmentation",
    "BackchannelAugmentation",
    "BargeInAugmentation",
    "DropoutAugmentation",
    "OffMicAugmentation",
)
