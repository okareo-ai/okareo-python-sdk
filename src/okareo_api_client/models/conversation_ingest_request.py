from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conversation_audio import ConversationAudio
    from ..models.conversation_ingest_request_metadata import ConversationIngestRequestMetadata
    from ..models.conversation_turn import ConversationTurn


T = TypeVar("T", bound="ConversationIngestRequest")


@_attrs_define
class ConversationIngestRequest:
    """Request payload for ingesting voice conversations.

    Attributes:
        call_id (str): Platform-specific call identifier
        context_token (None | str | Unset): Optional context token for correlation. Defaults to call_id if not provided.
        conversation_start_at (datetime.datetime | None | Unset): Absolute conversation start timestamp in UTC. Use this
            with per-turn timestamp_ms values to derive wall-clock message times.
        audio (ConversationAudio | None | Unset): Audio reference for the conversation. Prefer URL or voice_file_id over
            inline base64.
        recording_url (None | str | Unset): Legacy compatibility field. Prefer audio={type:'url', url: ...}.
        recording_bytes_b64 (None | str | Unset): Legacy compatibility field. Prefer audio={type:'inline_b64',
            inline_b64: ...}.
        transcript (list[ConversationTurn] | None | Unset): Pre-parsed transcript as a list of turns. Optional for
            audio-only sources.
        diarization (bool | Unset): When transcript is absent, run diarization + ASR on the audio before creating the
            datapoint. Default: True.
        metadata (ConversationIngestRequestMetadata | Unset): Platform-specific metadata
        tags (list[str] | Unset): Tags for monitor matching
        first_turn (str | Unset): For audio-only diarization: 'user' or 'assistant' spoke first Default: 'assistant'.
    """

    call_id: str
    context_token: None | str | Unset = UNSET
    conversation_start_at: datetime.datetime | None | Unset = UNSET
    audio: ConversationAudio | None | Unset = UNSET
    recording_url: None | str | Unset = UNSET
    recording_bytes_b64: None | str | Unset = UNSET
    transcript: list[ConversationTurn] | None | Unset = UNSET
    diarization: bool | Unset = True
    metadata: ConversationIngestRequestMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    first_turn: str | Unset = "assistant"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conversation_audio import ConversationAudio

        call_id = self.call_id

        context_token: None | str | Unset
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

        conversation_start_at: None | str | Unset
        if isinstance(self.conversation_start_at, Unset):
            conversation_start_at = UNSET
        elif isinstance(self.conversation_start_at, datetime.datetime):
            conversation_start_at = self.conversation_start_at.isoformat()
        else:
            conversation_start_at = self.conversation_start_at

        audio: dict[str, Any] | None | Unset
        if isinstance(self.audio, Unset):
            audio = UNSET
        elif isinstance(self.audio, ConversationAudio):
            audio = self.audio.to_dict()
        else:
            audio = self.audio

        recording_url: None | str | Unset
        if isinstance(self.recording_url, Unset):
            recording_url = UNSET
        else:
            recording_url = self.recording_url

        recording_bytes_b64: None | str | Unset
        if isinstance(self.recording_bytes_b64, Unset):
            recording_bytes_b64 = UNSET
        else:
            recording_bytes_b64 = self.recording_bytes_b64

        transcript: list[dict[str, Any]] | None | Unset
        if isinstance(self.transcript, Unset):
            transcript = UNSET
        elif isinstance(self.transcript, list):
            transcript = []
            for transcript_type_0_item_data in self.transcript:
                transcript_type_0_item = transcript_type_0_item_data.to_dict()
                transcript.append(transcript_type_0_item)

        else:
            transcript = self.transcript

        diarization = self.diarization

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        first_turn = self.first_turn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
            }
        )
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if conversation_start_at is not UNSET:
            field_dict["conversation_start_at"] = conversation_start_at
        if audio is not UNSET:
            field_dict["audio"] = audio
        if recording_url is not UNSET:
            field_dict["recording_url"] = recording_url
        if recording_bytes_b64 is not UNSET:
            field_dict["recording_bytes_b64"] = recording_bytes_b64
        if transcript is not UNSET:
            field_dict["transcript"] = transcript
        if diarization is not UNSET:
            field_dict["diarization"] = diarization
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if first_turn is not UNSET:
            field_dict["first_turn"] = first_turn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conversation_audio import ConversationAudio
        from ..models.conversation_ingest_request_metadata import ConversationIngestRequestMetadata
        from ..models.conversation_turn import ConversationTurn

        d = dict(src_dict)
        call_id = d.pop("call_id")

        def _parse_context_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

        def _parse_conversation_start_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                conversation_start_at_type_0 = isoparse(data)

                return conversation_start_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        conversation_start_at = _parse_conversation_start_at(d.pop("conversation_start_at", UNSET))

        def _parse_audio(data: object) -> ConversationAudio | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audio_type_0 = ConversationAudio.from_dict(data)

                return audio_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ConversationAudio | None | Unset, data)

        audio = _parse_audio(d.pop("audio", UNSET))

        def _parse_recording_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recording_url = _parse_recording_url(d.pop("recording_url", UNSET))

        def _parse_recording_bytes_b64(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recording_bytes_b64 = _parse_recording_bytes_b64(d.pop("recording_bytes_b64", UNSET))

        def _parse_transcript(data: object) -> list[ConversationTurn] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                transcript_type_0 = []
                _transcript_type_0 = data
                for transcript_type_0_item_data in _transcript_type_0:
                    transcript_type_0_item = ConversationTurn.from_dict(transcript_type_0_item_data)

                    transcript_type_0.append(transcript_type_0_item)

                return transcript_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ConversationTurn] | None | Unset, data)

        transcript = _parse_transcript(d.pop("transcript", UNSET))

        diarization = d.pop("diarization", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ConversationIngestRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ConversationIngestRequestMetadata.from_dict(_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        first_turn = d.pop("first_turn", UNSET)

        conversation_ingest_request = cls(
            call_id=call_id,
            context_token=context_token,
            conversation_start_at=conversation_start_at,
            audio=audio,
            recording_url=recording_url,
            recording_bytes_b64=recording_bytes_b64,
            transcript=transcript,
            diarization=diarization,
            metadata=metadata,
            tags=tags,
            first_turn=first_turn,
        )

        conversation_ingest_request.additional_properties = d
        return conversation_ingest_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
