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
        lpf_cutoff_hz: Low-pass filter cutoff used for off-mic speech.
        gain_db: Gain reduction applied to off-mic speech.
    """

    probability: float | None = None
    prompt: str | None = None
    lpf_cutoff_hz: int | None = None
    gain_db: float | None = None


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
        probability: Probability that a short backchannel is injected.
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
        probability: Probability that a barge-in interruption is injected.
        replacement_text: Text to use for the interruption utterance.
        prompt: Optional independent prompt for the barge-in content.
        utterance: Optional direct text override for the injected content.
        min_offset_ms: Minimum delay before the injection fires.
        max_offset_ms: Maximum delay before the injection fires.
    """

    probability: float | None = None
    replacement_text: str | None = None
    prompt: str | None = None
    utterance: str | None = None
    min_offset_ms: int | None = None
    max_offset_ms: int | None = None


@_attrs_define
class Augmentation(_DictSerializable):
    """Container for voice simulation augmentation strategy config.

    Configure one primary strategy at a time. ``noise`` may be combined with
    one additional strategy.

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
