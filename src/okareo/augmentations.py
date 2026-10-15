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


# The ``type`` each strategy class takes in a plan entry: its key on Augmentation.
_PLAN_TYPES: dict[type, str] = {
    CAPAugmentation: "cap",
    DirectedSpeechAugmentation: "directed_speech",
    NoiseAugmentation: "noise",
    SecondarySpeakerAugmentation: "secondary_speaker",
    BackchannelAugmentation: "backchannel",
    BargeInAugmentation: "barge_in",
    DropoutAugmentation: "dropout",
}


@_attrs_define
class Augmentation(_DictSerializable):
    """Container for voice simulation augmentation strategy config.

    Configure it one of two ways:

    - **One strategy** for the whole run: set one strategy field. ``noise``
      may be combined with one other strategy.
    - **A per-turn plan**: ``plan`` maps the caller's turn number (counted
      from 1, the same turns ``start_at_turn`` counts) to the augmentations
      for that turn, using the same strategy classes. Only ``noise``, which is
      run-wide, may be set beside it.

    In a plan:

    - The turn key is the turn, so entries don't take ``start_at_turn`` or
      ``end_at_turn``, and ``probability`` defaults to 1.0.
    - Entries that shape the caller's own line (``cap``, ``dropout``, and
      ``directed_speech`` / ``secondary_speaker`` without ``interrupt``) apply
      first. Interruptions (``barge_in``, ``backchannel``, and the speaker
      kinds with ``interrupt=True``) then play in listed order over the
      agent's reply, best effort: one that can't land is skipped and
      reported. A turn holds at most 6 interruptions, counting each
      ``count``.
    - Interruptions start 200-600 ms into the agent's reply by default. Real
      agents usually need later offsets.
    - ``CAPAugmentation.pause_ms`` is run-wide and can't be set in an entry.
    - ``None`` or ``[]`` for a turn means no augmentation on it.

    Example:
        ``Augmentation(noise=NoiseAugmentation(profile="cafeteria", snr_db=10))``

        A per-turn plan::

            Augmentation(plan={
                1: [BargeInAugmentation(utterance="Can I refill my prescription?")],
                2: [
                    BackchannelAugmentation(utterance="OK, good."),
                    BargeInAugmentation(utterance="No thank you."),
                ],
            })
    """

    cap: CAPAugmentation | None = None
    directed_speech: DirectedSpeechAugmentation | None = None
    noise: NoiseAugmentation | None = None
    secondary_speaker: SecondarySpeakerAugmentation | None = None
    backchannel: BackchannelAugmentation | None = None
    barge_in: BargeInAugmentation | None = None
    dropout: DropoutAugmentation | None = None
    plan: Mapping[int, Sequence[AugmentationConfig] | None] | None = None

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
    """The wire shape: ``{"<turn>": [{"type": ..., <fields>}, ...] | None}``."""
    if not isinstance(plan, Mapping):
        raise TypeError(
            "Augmentation.plan must map turn numbers to lists of augmentations."
        )
    turns: dict[int, Any] = {}
    for raw_turn, entries in plan.items():
        turn = _plan_turn(raw_turn)
        if turn in turns:
            raise ValueError(f"Augmentation.plan lists turn {turn} twice.")
        if entries is None:
            turns[turn] = None
        elif isinstance(entries, (list, tuple)):
            turns[turn] = [_plan_entry_dict(turn, entry) for entry in entries]
        else:
            raise TypeError(
                f"Augmentation.plan turn {turn} must be a list of augmentations, "
                "or None for none."
            )
    return {str(turn): turns[turn] for turn in sorted(turns)}


def _plan_turn(raw_turn: Any) -> int:
    turn = (
        int(raw_turn) if isinstance(raw_turn, str) and raw_turn.isdigit() else raw_turn
    )
    if isinstance(turn, bool) or not isinstance(turn, int) or turn < 1:
        raise ValueError(
            f"Invalid Augmentation.plan turn {raw_turn!r}: turns are the caller's "
            "turns, counted from 1."
        )
    return turn


def _plan_entry_dict(turn: int, entry: Any) -> dict[str, Any]:
    entry_type = next(
        (_PLAN_TYPES[cls] for cls in type(entry).__mro__ if cls in _PLAN_TYPES),
        None,
    )
    if entry_type is None:
        raise TypeError(
            f"Augmentation.plan turn {turn} entries must be augmentation configs "
            f"such as BargeInAugmentation, not {type(entry).__name__}."
        )
    if entry_type == "noise":
        raise ValueError(
            "NoiseAugmentation is run-wide: set Augmentation(noise=...) beside "
            f"the plan, not in turn {turn}."
        )
    body = entry.to_dict()
    window = [key for key in ("start_at_turn", "end_at_turn") if key in body]
    if window:
        raise ValueError(
            f"Augmentation.plan entries don't take {' / '.join(window)}: the "
            f"turn key ({turn}) is the turn."
        )
    if entry_type == "cap" and "pause_ms" in body:
        raise ValueError(
            f"cap pause_ms can't be set in a plan entry (turn {turn}): it sets a "
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
)
