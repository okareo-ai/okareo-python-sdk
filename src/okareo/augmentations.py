"""Voice simulation augmentation payload wrappers.

Import these from ``okareo.augmentations`` and pass them into
``Okareo.run_simulation(..., augmentation=...)``.
"""

from __future__ import annotations

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
    They do not perform server-side validation locally; they only serialize the
    fields you set.
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
        pause_ms: Optional illustrative pause hint included in the public SDK
            contract. The current server accepts this field but does not yet use
            it to change runtime behavior.
    """

    probability: float | None = None
    pause_ms: int | None = None


@_attrs_define
class DirectedSpeechAugmentation(AugmentationConfig):
    """Directed-speech augmentation config.

    Arguments:
        probability: Optional illustrative field in the public SDK contract. The
            current server accepts it but does not yet use it to change runtime
            behavior.
        lpf_cutoff_hz: Low-pass filter cutoff used for off-mic speech.
        gain_db: Gain reduction applied to off-mic speech.
    """

    probability: float | None = None
    lpf_cutoff_hz: int | None = None
    gain_db: float | None = None


@_attrs_define
class NoiseAugmentation(AugmentationConfig):
    """Background noise augmentation config.

    Arguments:
        probability: Optional illustrative field included in the public SDK
            contract.
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
        probability: Optional illustrative field in the public SDK contract. The
            current server accepts it but does not yet use it to change runtime
            behavior.
        voice: Voice identifier for the secondary speaker.
        prompt: Optional independent prompt for the secondary speaker.
        lpf_cutoff_hz: Optional low-pass filter cutoff applied only to
            the secondary speaker audio.
        gain_db: Optional gain adjustment applied only to the
            secondary speaker audio.
        inter_speaker_pause_ms: Optional pause inserted between the primary
            and secondary speaker audio segments.
    """

    probability: float | None = None
    voice: str | None = None
    prompt: str | None = None
    lpf_cutoff_hz: int | None = None
    gain_db: float | None = None
    inter_speaker_pause_ms: int | None = None


@_attrs_define
class BackchannelAugmentation(AugmentationConfig):
    """Backchannel injection augmentation config.

    Arguments:
        probability: Chance of injecting a short non-turn-consuming backchannel.
        utterance: Optional backchannel text override, e.g. ``"mm-hmm"``.
        min_offset_ms: Minimum delay before the injection fires.
        max_offset_ms: Maximum delay before the injection fires.
    """

    probability: float | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None


@_attrs_define
class BargeInAugmentation(AugmentationConfig):
    """Barge-in injection augmentation config.

    Arguments:
        probability: Chance of injecting a turn-consuming interruption.
        replacement_text: Public contract field for the replacement utterance.
        utterance: Optional low-level override for the injected text. When both
            are provided, the server currently prefers ``utterance``.
        min_offset_ms: Minimum delay before the injection fires.
        max_offset_ms: Maximum delay before the injection fires.
    """

    probability: float | None = None
    replacement_text: str | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None


@_attrs_define
class Augmentation(_DictSerializable):
    """Container for voice simulation augmentation strategy config.

    Pass exactly one strategy at a time to match the current server-side
    single-strategy limitation.

    Example:
        ``Augmentation(noise=NoiseAugmentation(profile="cafeteria", snr_db=10))``
    """

    cap: CAPAugmentation | None = None
    directed_speech: DirectedSpeechAugmentation | None = None
    noise: NoiseAugmentation | None = None
    secondary_speaker: SecondarySpeakerAugmentation | None = None
    backchannel: BackchannelAugmentation | None = None
    barge_in: BargeInAugmentation | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value.to_dict()
            for key, value in _attrs_asdict(self, recurse=False).items()
            if value is not None
        }


__all__ = (
    "Augmentation",
    "CAPAugmentation",
    "DirectedSpeechAugmentation",
    "NoiseAugmentation",
    "SecondarySpeakerAugmentation",
    "BackchannelAugmentation",
    "BargeInAugmentation",
)
