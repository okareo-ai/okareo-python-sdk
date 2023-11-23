from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_run_type import TestRunType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
    from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs


T = TypeVar("T", bound="TestRunPayloadV2")


@_attrs_define
class TestRunPayloadV2:
    """
    Attributes:
        mut_id (str):
        api_keys (TestRunPayloadV2ApiKeys):
        scenario_id (str):
        metrics_kwargs (Union[Unset, TestRunPayloadV2MetricsKwargs]):
        name (Union[Unset, str]):
        type (Union[Unset, TestRunType]): An enumeration. Default: TestRunType.MULTI_CLASS_CLASSIFICATION.
        calculate_metrics (Union[Unset, bool]):
        tags (Union[Unset, List[str]]):
        project_id (Union[Unset, str]):
    """

    mut_id: str
    api_keys: "TestRunPayloadV2ApiKeys"
    scenario_id: str
    metrics_kwargs: Union[Unset, "TestRunPayloadV2MetricsKwargs"] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, TestRunType] = TestRunType.MULTI_CLASS_CLASSIFICATION
    calculate_metrics: Union[Unset, bool] = False
    tags: Union[Unset, List[str]] = UNSET
    project_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mut_id = self.mut_id
        api_keys = self.api_keys.to_dict()

        scenario_id = self.scenario_id
        metrics_kwargs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metrics_kwargs, Unset):
            metrics_kwargs = self.metrics_kwargs.to_dict()

        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        calculate_metrics = self.calculate_metrics
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mut_id": mut_id,
                "api_keys": api_keys,
                "scenario_id": scenario_id,
            }
        )
        if metrics_kwargs is not UNSET:
            field_dict["metrics_kwargs"] = metrics_kwargs
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if calculate_metrics is not UNSET:
            field_dict["calculate_metrics"] = calculate_metrics
        if tags is not UNSET:
            field_dict["tags"] = tags
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_run_payload_v2_api_keys import TestRunPayloadV2ApiKeys
        from ..models.test_run_payload_v2_metrics_kwargs import TestRunPayloadV2MetricsKwargs

        d = src_dict.copy()
        mut_id = d.pop("mut_id")

        api_keys = TestRunPayloadV2ApiKeys.from_dict(d.pop("api_keys"))

        scenario_id = d.pop("scenario_id")

        _metrics_kwargs = d.pop("metrics_kwargs", UNSET)
        metrics_kwargs: Union[Unset, TestRunPayloadV2MetricsKwargs]
        if isinstance(_metrics_kwargs, Unset):
            metrics_kwargs = UNSET
        else:
            metrics_kwargs = TestRunPayloadV2MetricsKwargs.from_dict(_metrics_kwargs)

        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TestRunType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TestRunType(_type)

        calculate_metrics = d.pop("calculate_metrics", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        project_id = d.pop("project_id", UNSET)

        test_run_payload_v2 = cls(
            mut_id=mut_id,
            api_keys=api_keys,
            scenario_id=scenario_id,
            metrics_kwargs=metrics_kwargs,
            name=name,
            type=type,
            calculate_metrics=calculate_metrics,
            tags=tags,
            project_id=project_id,
        )

        test_run_payload_v2.additional_properties = d
        return test_run_payload_v2

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
