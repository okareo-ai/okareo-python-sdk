"""Voice simulation augmentation payload wrappers.

Import these from ``okareo.augmentations`` and pass them into
``Okareo.run_simulation(..., augmentation=...)``.
"""

from __future__ import annotations

import warnings
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


@_attrs_define
class CAPAugmentation(AugmentationConfig):
    """Concurrent-ask augmentation config.

    Arguments:
        probability: Probability that the driver emits an extra follow-up message.
        pause_ms: Pause duration in milliseconds before emitting the
            follow-up message.
    """

    probability: float | None = None
    pause_ms: int | None = None


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
    """

    probability: float | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None


@_attrs_define
class BargeInAugmentation(AugmentationConfig):
    """Barge-in injection augmentation config.

    Arguments:
        probability: Probability that a barge-in interruption is injected.
        replacement_text: Deprecated: ignored by Okareo, and to be removed in a
            future release. Setting it warns (``FutureWarning``). Use
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
    """

    probability: float | None = None
    replacement_text: str | None = None
    prompt: str | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None
    start_at_turn: int | None = None
    end_at_turn: int | None = None

    def __attrs_post_init__(self) -> None:
        if self.replacement_text is not None:
            warnings.warn(
                "BargeInAugmentation.replacement_text is ignored by Okareo and will "
                "be removed in a future release. Use utterance for exact words, or "
                "prompt to have them generated.",
                FutureWarning,
                stacklevel=3,
            )


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
class Augmentation(_DictSerializable):
    """Container for voice simulation augmentation strategy config.

    Configure it one of two ways:

    - **One strategy** for the whole run: set one strategy field. ``noise``
      may be combined with one other strategy.
    - **A per-turn plan**: ``plan`` maps the caller's turns (counted from 1,
      the same turns ``start_at_turn`` counts) to the augmentations played on
      them, using the same strategy classes. Only ``noise`` may be set
      beside it.

    A plan key is a turn (``2`` or ``"2"``), a range (``"2-4"``), or a turn
    to the end of the call (``"5-"``). A key's augmentations play on every
    turn it covers, and keys can't overlap.

    Each turn takes one augmentation on what the caller says (``cap``,
    ``dropout``, or ``directed_speech`` / ``secondary_speaker`` without
    ``interrupt``) and one on the agent's reply (``barge_in``, ``backchannel``, or the speaker kinds with
    ``interrupt=True``). ``dropout`` takes the whole turn. In a plan entry,
    ``probability`` defaults to 1.0 and the key replaces ``start_at_turn`` /
    ``end_at_turn``. Okareo refuses a plan that breaks these rules, with a
    message that names the turn.

    Example:
        ``Augmentation(noise=NoiseAugmentation(profile="cafeteria", snr_db=10))``

        A per-turn plan::

            Augmentation(plan={
                1: [BargeInAugmentation(utterance="Can I refill my prescription?")],
                "2-3": [BackchannelAugmentation(utterance="mm-hmm")],
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
    plan: Mapping[int | str, Sequence[AugmentationConfig] | None] | None = None

    def to_dict(self) -> dict[str, Any]:
        fields = _attrs_asdict(self, recurse=False)
        plan = fields.pop("plan")
        out = {
            key: value.to_dict() for key, value in fields.items() if value is not None
        }
        if plan is not None:
            out["plan"] = _plan_to_dict(plan)
        return out


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


def _plan_to_dict(
    plan: Mapping[Any, Sequence[AugmentationConfig] | None],
) -> dict[str, Any]:
    """The wire shape: ``{"<key>": [{"type": ..., <fields>}, ...] | None}``.
    Keys are sent as strings; Okareo validates them."""
    out: dict[str, Any] = {}
    for raw_key, entries in plan.items():
        key = str(raw_key).strip()
        if key in out:
            raise ValueError(f"Augmentation.plan lists key {key!r} twice.")
        out[key] = (
            None if entries is None else [_plan_entry_dict(key, e) for e in entries]
        )
    return out


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
    return {"type": entry_type, **entry.to_dict()}


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
