from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriverStepSchema")


@_attrs_define
class DriverStepSchema:
    """One scripted step: exactly one of message / dtmf / end_conversation (checked by the
    steps validator), with an optional reason on end_conversation. Unknown keys are a 422.

        Attributes:
            message (None | str | Unset): Words the Driver says, verbatim.
            dtmf (None | str | Unset): Keys the Driver presses (0-9, A-D, *, #, w); voice only.
            silence (bool | None | Unset): true: the Driver says nothing this turn and listens for the Target's next
                segment; voice only.
            end_conversation (None | str | Unset): Closing words; the Driver says them and ends the call.
            reason (None | str | Unset): Why the script ended the call (with end_conversation only).
            turn (int | None | Unset): Reserved; rejected today.
    """

    message: None | str | Unset = UNSET
    dtmf: None | str | Unset = UNSET
    silence: bool | None | Unset = UNSET
    end_conversation: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    turn: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        dtmf: None | str | Unset
        if isinstance(self.dtmf, Unset):
            dtmf = UNSET
        else:
            dtmf = self.dtmf

        silence: bool | None | Unset
        if isinstance(self.silence, Unset):
            silence = UNSET
        else:
            silence = self.silence

        end_conversation: None | str | Unset
        if isinstance(self.end_conversation, Unset):
            end_conversation = UNSET
        else:
            end_conversation = self.end_conversation

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        turn: int | None | Unset
        if isinstance(self.turn, Unset):
            turn = UNSET
        else:
            turn = self.turn

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if dtmf is not UNSET:
            field_dict["dtmf"] = dtmf
        if silence is not UNSET:
            field_dict["silence"] = silence
        if end_conversation is not UNSET:
            field_dict["end_conversation"] = end_conversation
        if reason is not UNSET:
            field_dict["reason"] = reason
        if turn is not UNSET:
            field_dict["turn"] = turn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_dtmf(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dtmf = _parse_dtmf(d.pop("dtmf", UNSET))

        def _parse_silence(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        silence = _parse_silence(d.pop("silence", UNSET))

        def _parse_end_conversation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        end_conversation = _parse_end_conversation(d.pop("end_conversation", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_turn(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        turn = _parse_turn(d.pop("turn", UNSET))

        driver_step_schema = cls(
            message=message,
            dtmf=dtmf,
            silence=silence,
            end_conversation=end_conversation,
            reason=reason,
            turn=turn,
        )

        return driver_step_schema
