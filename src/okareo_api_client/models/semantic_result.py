from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SemanticResult")


@_attrs_define
class SemanticResult:
    """
    Attributes:
        document_sentences (List[str]):
        summary_sentences (List[str]):
        scores (List[List[str]]):
    """

    document_sentences: List[str]
    summary_sentences: List[str]
    scores: List[List[str]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_sentences = self.document_sentences

        summary_sentences = self.summary_sentences

        scores = []
        for scores_item_data in self.scores:
            scores_item = scores_item_data

            scores.append(scores_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document_sentences": document_sentences,
                "summary_sentences": summary_sentences,
                "scores": scores,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_sentences = cast(List[str], d.pop("document_sentences"))

        summary_sentences = cast(List[str], d.pop("summary_sentences"))

        scores = []
        _scores = d.pop("scores")
        for scores_item_data in _scores:
            scores_item = cast(List[str], scores_item_data)

            scores.append(scores_item)

        semantic_result = cls(
            document_sentences=document_sentences,
            summary_sentences=summary_sentences,
            scores=scores,
        )

        semantic_result.additional_properties = d
        return semantic_result

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
