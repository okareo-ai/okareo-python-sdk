import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
    from ..models.datapoint_list_item_checks import DatapointListItemChecks
    from ..models.datapoint_list_item_input_tools_item import DatapointListItemInputToolsItem
    from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
    from ..models.datapoint_list_item_result_embeddings_item import DatapointListItemResultEmbeddingsItem
    from ..models.datapoint_list_item_result_tool_calls_item import DatapointListItemResultToolCallsItem
    from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0


T = TypeVar("T", bound="DatapointListItem")


@_attrs_define
class DatapointListItem:
    """
    Attributes:
        id (str):
        tags (Union[Unset, List[str]]):
        input_ (Union[Unset, Any]):
        input_datetime (Union[Unset, datetime.datetime]):
        result (Union[Unset, Any]):
        result_datetime (Union[Unset, datetime.datetime]):
        feedback (Union[Unset, float]):
        error_message (Union[Unset, str]):
        error_code (Union[Unset, str]):
        error_type (Union[Unset, str]):
        context_token (Union[Unset, str]):
        time_created (Union[Unset, datetime.datetime]):
        model_metadata (Union['DatapointListItemModelMetadataType0', Any, Unset]):
        project_id (Union[Unset, str]):
        mut_id (Union[Unset, str]):
        test_run_id (Union[Unset, str]):
        test_data_point_id (Union[Unset, str]):
        group_id (Union[Unset, str]):
        scenario_data_point_id (Union[Unset, str]):
        latency (Union[Unset, int]):
        input_tokens (Union[Unset, int]):
        output_tokens (Union[Unset, int]):
        source (Union[Unset, str]):
        temperature (Union[Unset, str]):
        input_tools (Union[Unset, List['DatapointListItemInputToolsItem']]):
        result_tool_calls (Union[Unset, List['DatapointListItemResultToolCallsItem']]):
        result_embeddings (Union[Unset, List['DatapointListItemResultEmbeddingsItem']]):
        checks (Union[Unset, DatapointListItemChecks]):
        agent_metadata (Union['DatapointListItemAgentMetadataType0', Any, Unset]):
        provider (Union[Unset, str]):
        total_search_count (Union[Unset, int]):
        total_datapoint_count (Union[Unset, int]):
        request_model_name (Union[Unset, str]):
        response_model_name (Union[Unset, str]):
        cost (Union[Unset, float]):
        status (Union[Unset, str]):  Default: ''.
        failed_checks (Union[Unset, List[str]]): Array of failed check names
        resolved (Union[Unset, bool]): Manual marking from user on resolved status
        user_metadata (Union['DatapointListItemUserMetadataType0', Any, Unset]): User-provided metadata provided as
            context to the completion call.
    """

    id: str
    tags: Union[Unset, List[str]] = UNSET
    input_: Union[Unset, Any] = UNSET
    input_datetime: Union[Unset, datetime.datetime] = UNSET
    result: Union[Unset, Any] = UNSET
    result_datetime: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[Unset, float] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_type: Union[Unset, str] = UNSET
    context_token: Union[Unset, str] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    model_metadata: Union["DatapointListItemModelMetadataType0", Any, Unset] = UNSET
    project_id: Union[Unset, str] = UNSET
    mut_id: Union[Unset, str] = UNSET
    test_run_id: Union[Unset, str] = UNSET
    test_data_point_id: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET
    scenario_data_point_id: Union[Unset, str] = UNSET
    latency: Union[Unset, int] = UNSET
    input_tokens: Union[Unset, int] = UNSET
    output_tokens: Union[Unset, int] = UNSET
    source: Union[Unset, str] = UNSET
    temperature: Union[Unset, str] = UNSET
    input_tools: Union[Unset, List["DatapointListItemInputToolsItem"]] = UNSET
    result_tool_calls: Union[Unset, List["DatapointListItemResultToolCallsItem"]] = UNSET
    result_embeddings: Union[Unset, List["DatapointListItemResultEmbeddingsItem"]] = UNSET
    checks: Union[Unset, "DatapointListItemChecks"] = UNSET
    agent_metadata: Union["DatapointListItemAgentMetadataType0", Any, Unset] = UNSET
    provider: Union[Unset, str] = UNSET
    total_search_count: Union[Unset, int] = UNSET
    total_datapoint_count: Union[Unset, int] = UNSET
    request_model_name: Union[Unset, str] = UNSET
    response_model_name: Union[Unset, str] = UNSET
    cost: Union[Unset, float] = UNSET
    status: Union[Unset, str] = ""
    failed_checks: Union[Unset, List[str]] = UNSET
    resolved: Union[Unset, bool] = False
    user_metadata: Union["DatapointListItemUserMetadataType0", Any, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        id = self.id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        input_ = self.input_
        input_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.input_datetime, Unset):
            input_datetime = self.input_datetime.isoformat()

        result = self.result
        result_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.result_datetime, Unset):
            result_datetime = self.result_datetime.isoformat()

        feedback = self.feedback
        error_message = self.error_message
        error_code = self.error_code
        error_type = self.error_type
        context_token = self.context_token
        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        model_metadata: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET

        elif isinstance(self.model_metadata, DatapointListItemModelMetadataType0):
            model_metadata = UNSET
            if not isinstance(self.model_metadata, Unset):
                model_metadata = self.model_metadata.to_dict()

        else:
            model_metadata = self.model_metadata

        project_id = self.project_id
        mut_id = self.mut_id
        test_run_id = self.test_run_id
        test_data_point_id = self.test_data_point_id
        group_id = self.group_id
        scenario_data_point_id = self.scenario_data_point_id
        latency = self.latency
        input_tokens = self.input_tokens
        output_tokens = self.output_tokens
        source = self.source
        temperature = self.temperature
        input_tools: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.input_tools, Unset):
            input_tools = []
            for input_tools_item_data in self.input_tools:
                input_tools_item = input_tools_item_data.to_dict()

                input_tools.append(input_tools_item)

        result_tool_calls: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.result_tool_calls, Unset):
            result_tool_calls = []
            for result_tool_calls_item_data in self.result_tool_calls:
                result_tool_calls_item = result_tool_calls_item_data.to_dict()

                result_tool_calls.append(result_tool_calls_item)

        result_embeddings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.result_embeddings, Unset):
            result_embeddings = []
            for result_embeddings_item_data in self.result_embeddings:
                result_embeddings_item = result_embeddings_item_data.to_dict()

                result_embeddings.append(result_embeddings_item)

        checks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks.to_dict()

        agent_metadata: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.agent_metadata, Unset):
            agent_metadata = UNSET

        elif isinstance(self.agent_metadata, DatapointListItemAgentMetadataType0):
            agent_metadata = UNSET
            if not isinstance(self.agent_metadata, Unset):
                agent_metadata = self.agent_metadata.to_dict()

        else:
            agent_metadata = self.agent_metadata

        provider = self.provider
        total_search_count = self.total_search_count
        total_datapoint_count = self.total_datapoint_count
        request_model_name = self.request_model_name
        response_model_name = self.response_model_name
        cost = self.cost
        status = self.status
        failed_checks: Union[Unset, List[str]] = UNSET
        if not isinstance(self.failed_checks, Unset):
            failed_checks = self.failed_checks

        resolved = self.resolved
        user_metadata: Union[Any, Dict[str, Any], Unset]
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET

        elif isinstance(self.user_metadata, DatapointListItemUserMetadataType0):
            user_metadata = UNSET
            if not isinstance(self.user_metadata, Unset):
                user_metadata = self.user_metadata.to_dict()

        else:
            user_metadata = self.user_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if tags is not UNSET:
            field_dict["tags"] = tags
        if input_ is not UNSET:
            field_dict["input"] = input_
        if input_datetime is not UNSET:
            field_dict["input_datetime"] = input_datetime
        if result is not UNSET:
            field_dict["result"] = result
        if result_datetime is not UNSET:
            field_dict["result_datetime"] = result_datetime
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if context_token is not UNSET:
            field_dict["context_token"] = context_token
        if time_created is not UNSET:
            field_dict["time_created"] = time_created
        if model_metadata is not UNSET:
            field_dict["model_metadata"] = model_metadata
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if mut_id is not UNSET:
            field_dict["mut_id"] = mut_id
        if test_run_id is not UNSET:
            field_dict["test_run_id"] = test_run_id
        if test_data_point_id is not UNSET:
            field_dict["test_data_point_id"] = test_data_point_id
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if scenario_data_point_id is not UNSET:
            field_dict["scenario_data_point_id"] = scenario_data_point_id
        if latency is not UNSET:
            field_dict["latency"] = latency
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if source is not UNSET:
            field_dict["source"] = source
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if input_tools is not UNSET:
            field_dict["input_tools"] = input_tools
        if result_tool_calls is not UNSET:
            field_dict["result_tool_calls"] = result_tool_calls
        if result_embeddings is not UNSET:
            field_dict["result_embeddings"] = result_embeddings
        if checks is not UNSET:
            field_dict["checks"] = checks
        if agent_metadata is not UNSET:
            field_dict["agent_metadata"] = agent_metadata
        if provider is not UNSET:
            field_dict["provider"] = provider
        if total_search_count is not UNSET:
            field_dict["total_search_count"] = total_search_count
        if total_datapoint_count is not UNSET:
            field_dict["total_datapoint_count"] = total_datapoint_count
        if request_model_name is not UNSET:
            field_dict["request_model_name"] = request_model_name
        if response_model_name is not UNSET:
            field_dict["response_model_name"] = response_model_name
        if cost is not UNSET:
            field_dict["cost"] = cost
        if status is not UNSET:
            field_dict["status"] = status
        if failed_checks is not UNSET:
            field_dict["failed_checks"] = failed_checks
        if resolved is not UNSET:
            field_dict["resolved"] = resolved
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_checks import DatapointListItemChecks
        from ..models.datapoint_list_item_input_tools_item import DatapointListItemInputToolsItem
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_result_embeddings_item import DatapointListItemResultEmbeddingsItem
        from ..models.datapoint_list_item_result_tool_calls_item import DatapointListItemResultToolCallsItem
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        d = src_dict.copy()
        id = d.pop("id")

        tags = cast(List[str], d.pop("tags", UNSET))

        input_ = d.pop("input", UNSET)

        _input_datetime = d.pop("input_datetime", UNSET)
        input_datetime: Union[Unset, datetime.datetime]
        if isinstance(_input_datetime, Unset):
            input_datetime = UNSET
        else:
            input_datetime = isoparse(_input_datetime)

        result = d.pop("result", UNSET)

        _result_datetime = d.pop("result_datetime", UNSET)
        result_datetime: Union[Unset, datetime.datetime]
        if isinstance(_result_datetime, Unset):
            result_datetime = UNSET
        else:
            result_datetime = isoparse(_result_datetime)

        feedback = d.pop("feedback", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_code = d.pop("error_code", UNSET)

        error_type = d.pop("error_type", UNSET)

        context_token = d.pop("context_token", UNSET)

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        def _parse_model_metadata(data: object) -> Union["DatapointListItemModelMetadataType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _model_metadata_type_0 = data
                model_metadata_type_0: Union[Unset, DatapointListItemModelMetadataType0]
                if isinstance(_model_metadata_type_0, Unset):
                    model_metadata_type_0 = UNSET
                else:
                    model_metadata_type_0 = DatapointListItemModelMetadataType0.from_dict(_model_metadata_type_0)

                return model_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemModelMetadataType0", Any, Unset], data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        project_id = d.pop("project_id", UNSET)

        mut_id = d.pop("mut_id", UNSET)

        test_run_id = d.pop("test_run_id", UNSET)

        test_data_point_id = d.pop("test_data_point_id", UNSET)

        group_id = d.pop("group_id", UNSET)

        scenario_data_point_id = d.pop("scenario_data_point_id", UNSET)

        latency = d.pop("latency", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        source = d.pop("source", UNSET)

        temperature = d.pop("temperature", UNSET)

        input_tools = []
        _input_tools = d.pop("input_tools", UNSET)
        for input_tools_item_data in _input_tools or []:
            input_tools_item = DatapointListItemInputToolsItem.from_dict(input_tools_item_data)

            input_tools.append(input_tools_item)

        result_tool_calls = []
        _result_tool_calls = d.pop("result_tool_calls", UNSET)
        for result_tool_calls_item_data in _result_tool_calls or []:
            result_tool_calls_item = DatapointListItemResultToolCallsItem.from_dict(result_tool_calls_item_data)

            result_tool_calls.append(result_tool_calls_item)

        result_embeddings = []
        _result_embeddings = d.pop("result_embeddings", UNSET)
        for result_embeddings_item_data in _result_embeddings or []:
            result_embeddings_item = DatapointListItemResultEmbeddingsItem.from_dict(result_embeddings_item_data)

            result_embeddings.append(result_embeddings_item)

        _checks = d.pop("checks", UNSET)
        checks: Union[Unset, DatapointListItemChecks]
        if isinstance(_checks, Unset):
            checks = UNSET
        else:
            checks = DatapointListItemChecks.from_dict(_checks)

        def _parse_agent_metadata(data: object) -> Union["DatapointListItemAgentMetadataType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _agent_metadata_type_0 = data
                agent_metadata_type_0: Union[Unset, DatapointListItemAgentMetadataType0]
                if isinstance(_agent_metadata_type_0, Unset):
                    agent_metadata_type_0 = UNSET
                else:
                    agent_metadata_type_0 = DatapointListItemAgentMetadataType0.from_dict(_agent_metadata_type_0)

                return agent_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemAgentMetadataType0", Any, Unset], data)

        agent_metadata = _parse_agent_metadata(d.pop("agent_metadata", UNSET))

        provider = d.pop("provider", UNSET)

        total_search_count = d.pop("total_search_count", UNSET)

        total_datapoint_count = d.pop("total_datapoint_count", UNSET)

        request_model_name = d.pop("request_model_name", UNSET)

        response_model_name = d.pop("response_model_name", UNSET)

        cost = d.pop("cost", UNSET)

        status = d.pop("status", UNSET)

        failed_checks = cast(List[str], d.pop("failed_checks", UNSET))

        resolved = d.pop("resolved", UNSET)

        def _parse_user_metadata(data: object) -> Union["DatapointListItemUserMetadataType0", Any, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _user_metadata_type_0 = data
                user_metadata_type_0: Union[Unset, DatapointListItemUserMetadataType0]
                if isinstance(_user_metadata_type_0, Unset):
                    user_metadata_type_0 = UNSET
                else:
                    user_metadata_type_0 = DatapointListItemUserMetadataType0.from_dict(_user_metadata_type_0)

                return user_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemUserMetadataType0", Any, Unset], data)

        user_metadata = _parse_user_metadata(d.pop("user_metadata", UNSET))

        datapoint_list_item = cls(
            id=id,
            tags=tags,
            input_=input_,
            input_datetime=input_datetime,
            result=result,
            result_datetime=result_datetime,
            feedback=feedback,
            error_message=error_message,
            error_code=error_code,
            error_type=error_type,
            context_token=context_token,
            time_created=time_created,
            model_metadata=model_metadata,
            project_id=project_id,
            mut_id=mut_id,
            test_run_id=test_run_id,
            test_data_point_id=test_data_point_id,
            group_id=group_id,
            scenario_data_point_id=scenario_data_point_id,
            latency=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            source=source,
            temperature=temperature,
            input_tools=input_tools,
            result_tool_calls=result_tool_calls,
            result_embeddings=result_embeddings,
            checks=checks,
            agent_metadata=agent_metadata,
            provider=provider,
            total_search_count=total_search_count,
            total_datapoint_count=total_datapoint_count,
            request_model_name=request_model_name,
            response_model_name=response_model_name,
            cost=cost,
            status=status,
            failed_checks=failed_checks,
            resolved=resolved,
            user_metadata=user_metadata,
        )

        datapoint_list_item.additional_properties = d
        return datapoint_list_item

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
