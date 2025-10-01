import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="VoiceUploadResponse")


@_attrs_define
class VoiceUploadResponse:
    """
    Attributes:
        file_id (str): Unique identifier for the uploaded audio.
        file_url (str): Link to access the uploaded audio file.
        time_created (datetime.datetime): Timestamp indicating when audio file was created.
    """

    file_id: str
    file_url: str
    time_created: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id
        file_url = self.file_url
        time_created = self.time_created.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_id": file_id,
                "file_url": file_url,
                "time_created": time_created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("file_id")

        file_url = d.pop("file_url")

        time_created = isoparse(d.pop("time_created"))

        voice_upload_response = cls(
            file_id=file_id,
            file_url=file_url,
            time_created=time_created,
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
