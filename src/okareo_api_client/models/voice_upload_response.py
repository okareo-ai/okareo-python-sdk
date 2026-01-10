import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="VoiceUploadResponse")


@_attrs_define
class VoiceUploadResponse:
    """
    Attributes:
        file_id (str): Unique identifier for the uploaded audio.
        file_url (str): Link to access the uploaded audio file.
        file_duration (float): Duration of the audio file in milliseconds.
        time_created (datetime.datetime): Timestamp indicating when audio file was created.
        datapoint_id (Union[Unset, str]): ID of the created datapoint. Only present when transcribe=True.
        message (Union[Unset, str]): Status message from transcription. Only present when transcribe=True.
    """

    file_id: str
    file_url: str
    file_duration: float
    time_created: datetime.datetime
    datapoint_id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id
        file_url = self.file_url
        file_duration = self.file_duration
        time_created = self.time_created.isoformat()
        datapoint_id = self.datapoint_id
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
                "file_url": file_url,
                "file_duration": file_duration,
                "time_created": time_created,
            }
        )
        if datapoint_id is not UNSET:
            field_dict["datapoint_id"] = datapoint_id
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("file_id")

        file_url = d.pop("file_url")

        file_duration = d.pop("file_duration")

        time_created = isoparse(d.pop("time_created"))

        datapoint_id = d.pop("datapoint_id", UNSET)

        message = d.pop("message", UNSET)

        voice_upload_response = cls(
            file_id=file_id,
            file_url=file_url,
            file_duration=file_duration,
            time_created=time_created,
            datapoint_id=datapoint_id,
            message=message,
        )

        voice_upload_response.additional_properties = d
        return voice_upload_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
