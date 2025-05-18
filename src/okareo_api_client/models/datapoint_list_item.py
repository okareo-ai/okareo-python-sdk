import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
    from ..models.datapoint_list_item_checks_type_0 import DatapointListItemChecksType0
    from ..models.datapoint_list_item_input_tools_type_0_item import DatapointListItemInputToolsType0Item
    from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
    from ..models.datapoint_list_item_result_embeddings_type_0_item import DatapointListItemResultEmbeddingsType0Item
    from ..models.datapoint_list_item_result_tool_calls_type_0_item import DatapointListItemResultToolCallsType0Item
    from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0


T = TypeVar("T", bound="DatapointListItem")


@_attrs_define
class DatapointListItem:
    """
    Attributes:
        id (UUID):
        tags (Union[None, Unset, list[str]]):
        input_ (Union[Unset, Any]):
        input_datetime (Union[Unset, datetime.datetime]):
        result (Union[Unset, Any]):
        result_datetime (Union[Unset, datetime.datetime]):
        feedback (Union[None, Unset, float]):
        error_message (Union[None, Unset, str]):
        error_code (Union[None, Unset, str]):
        error_type (Union[None, Unset, str]):
        context_token (Union[None, Unset, str]):
        time_created (Union[Unset, datetime.datetime]):
        model_metadata (Union['DatapointListItemModelMetadataType0', Any, None, Unset]):
        project_id (Union[None, UUID, Unset]):
        mut_id (Union[None, UUID, Unset]):
        test_run_id (Union[None, UUID, Unset]):
        group_id (Union[None, UUID, Unset]):
        scenario_data_point_id (Union[None, UUID, Unset]):
        latency (Union[None, Unset, int]):
        input_tokens (Union[None, Unset, int]):
        output_tokens (Union[None, Unset, int]):
        source (Union[None, Unset, str]):
        temperature (Union[None, Unset, str]):
        input_tools (Union[None, Unset, list['DatapointListItemInputToolsType0Item']]):
        result_tool_calls (Union[None, Unset, list['DatapointListItemResultToolCallsType0Item']]):
        result_embeddings (Union[None, Unset, list['DatapointListItemResultEmbeddingsType0Item']]):
        checks (Union['DatapointListItemChecksType0', None, Unset]):
        agent_metadata (Union['DatapointListItemAgentMetadataType0', Any, None, Unset]):
        provider (Union[None, Unset, str]):
        total_search_count (Union[None, Unset, int]):
        total_datapoint_count (Union[None, Unset, int]):
        request_model_name (Union[None, Unset, str]):
        response_model_name (Union[None, Unset, str]):
        cost (Union[None, Unset, float]):
        status (Union[None, Unset, str]):  Default: ''.
        failed_checks (Union[None, Unset, list[str]]): Array of failed check names
        resolved (Union[None, Unset, bool]): Manual marking from user on resolved status Default: False.
        user_metadata (Union['DatapointListItemUserMetadataType0', Any, None, Unset]): User-provided metadata provided
            as context to the completion call.
    """

    id: UUID
    tags: Union[None, Unset, list[str]] = UNSET
    input_: Union[Unset, Any] = UNSET
    input_datetime: Union[Unset, datetime.datetime] = UNSET
    result: Union[Unset, Any] = UNSET
    result_datetime: Union[Unset, datetime.datetime] = UNSET
    feedback: Union[None, Unset, float] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    error_code: Union[None, Unset, str] = UNSET
    error_type: Union[None, Unset, str] = UNSET
    context_token: Union[None, Unset, str] = UNSET
    time_created: Union[Unset, datetime.datetime] = UNSET
    model_metadata: Union["DatapointListItemModelMetadataType0", Any, None, Unset] = UNSET
    project_id: Union[None, UUID, Unset] = UNSET
    mut_id: Union[None, UUID, Unset] = UNSET
    test_run_id: Union[None, UUID, Unset] = UNSET
    group_id: Union[None, UUID, Unset] = UNSET
    scenario_data_point_id: Union[None, UUID, Unset] = UNSET
    latency: Union[None, Unset, int] = UNSET
    input_tokens: Union[None, Unset, int] = UNSET
    output_tokens: Union[None, Unset, int] = UNSET
    source: Union[None, Unset, str] = UNSET
    temperature: Union[None, Unset, str] = UNSET
    input_tools: Union[None, Unset, list["DatapointListItemInputToolsType0Item"]] = UNSET
    result_tool_calls: Union[None, Unset, list["DatapointListItemResultToolCallsType0Item"]] = UNSET
    result_embeddings: Union[None, Unset, list["DatapointListItemResultEmbeddingsType0Item"]] = UNSET
    checks: Union["DatapointListItemChecksType0", None, Unset] = UNSET
    agent_metadata: Union["DatapointListItemAgentMetadataType0", Any, None, Unset] = UNSET
    provider: Union[None, Unset, str] = UNSET
    total_search_count: Union[None, Unset, int] = UNSET
    total_datapoint_count: Union[None, Unset, int] = UNSET
    request_model_name: Union[None, Unset, str] = UNSET
    response_model_name: Union[None, Unset, str] = UNSET
    cost: Union[None, Unset, float] = UNSET
    status: Union[None, Unset, str] = ""
    failed_checks: Union[None, Unset, list[str]] = UNSET
    resolved: Union[None, Unset, bool] = False
    user_metadata: Union["DatapointListItemUserMetadataType0", Any, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_checks_type_0 import DatapointListItemChecksType0
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        id = str(self.id)

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        input_ = self.input_

        input_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.input_datetime, Unset):
            input_datetime = self.input_datetime.isoformat()

        result = self.result

        result_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.result_datetime, Unset):
            result_datetime = self.result_datetime.isoformat()

        feedback: Union[None, Unset, float]
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        else:
            feedback = self.feedback

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        error_code: Union[None, Unset, str]
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        error_type: Union[None, Unset, str]
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        else:
            error_type = self.error_type

        context_token: Union[None, Unset, str]
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

        time_created: Union[Unset, str] = UNSET
        if not isinstance(self.time_created, Unset):
            time_created = self.time_created.isoformat()

        model_metadata: Union[Any, None, Unset, dict[str, Any]]
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET
        elif isinstance(self.model_metadata, DatapointListItemModelMetadataType0):
            model_metadata = self.model_metadata.to_dict()
        else:
            model_metadata = self.model_metadata

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        mut_id: Union[None, Unset, str]
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        test_run_id: Union[None, Unset, str]
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        group_id: Union[None, Unset, str]
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        elif isinstance(self.group_id, UUID):
            group_id = str(self.group_id)
        else:
            group_id = self.group_id

        scenario_data_point_id: Union[None, Unset, str]
        if isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        elif isinstance(self.scenario_data_point_id, UUID):
            scenario_data_point_id = str(self.scenario_data_point_id)
        else:
            scenario_data_point_id = self.scenario_data_point_id

        latency: Union[None, Unset, int]
        if isinstance(self.latency, Unset):
            latency = UNSET
        else:
            latency = self.latency

        input_tokens: Union[None, Unset, int]
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        output_tokens: Union[None, Unset, int]
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        temperature: Union[None, Unset, str]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        input_tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.input_tools, Unset):
            input_tools = UNSET
        elif isinstance(self.input_tools, list):
            input_tools = []
            for input_tools_type_0_item_data in self.input_tools:
                input_tools_type_0_item = input_tools_type_0_item_data.to_dict()
                input_tools.append(input_tools_type_0_item)

        else:
            input_tools = self.input_tools

        result_tool_calls: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.result_tool_calls, Unset):
            result_tool_calls = UNSET
        elif isinstance(self.result_tool_calls, list):
            result_tool_calls = []
            for result_tool_calls_type_0_item_data in self.result_tool_calls:
                result_tool_calls_type_0_item = result_tool_calls_type_0_item_data.to_dict()
                result_tool_calls.append(result_tool_calls_type_0_item)

        else:
            result_tool_calls = self.result_tool_calls

        result_embeddings: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.result_embeddings, Unset):
            result_embeddings = UNSET
        elif isinstance(self.result_embeddings, list):
            result_embeddings = []
            for result_embeddings_type_0_item_data in self.result_embeddings:
                result_embeddings_type_0_item = result_embeddings_type_0_item_data.to_dict()
                result_embeddings.append(result_embeddings_type_0_item)

        else:
            result_embeddings = self.result_embeddings

        checks: Union[None, Unset, dict[str, Any]]
        if isinstance(self.checks, Unset):
            checks = UNSET
        elif isinstance(self.checks, DatapointListItemChecksType0):
            checks = self.checks.to_dict()
        else:
            checks = self.checks

        agent_metadata: Union[Any, None, Unset, dict[str, Any]]
        if isinstance(self.agent_metadata, Unset):
            agent_metadata = UNSET
        elif isinstance(self.agent_metadata, DatapointListItemAgentMetadataType0):
            agent_metadata = self.agent_metadata.to_dict()
        else:
            agent_metadata = self.agent_metadata

        provider: Union[None, Unset, str]
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        total_search_count: Union[None, Unset, int]
        if isinstance(self.total_search_count, Unset):
            total_search_count = UNSET
        else:
            total_search_count = self.total_search_count

        total_datapoint_count: Union[None, Unset, int]
        if isinstance(self.total_datapoint_count, Unset):
            total_datapoint_count = UNSET
        else:
            total_datapoint_count = self.total_datapoint_count

        request_model_name: Union[None, Unset, str]
        if isinstance(self.request_model_name, Unset):
            request_model_name = UNSET
        else:
            request_model_name = self.request_model_name

        response_model_name: Union[None, Unset, str]
        if isinstance(self.response_model_name, Unset):
            response_model_name = UNSET
        else:
            response_model_name = self.response_model_name

        cost: Union[None, Unset, float]
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        failed_checks: Union[None, Unset, list[str]]
        if isinstance(self.failed_checks, Unset):
            failed_checks = UNSET
        elif isinstance(self.failed_checks, list):
            failed_checks = self.failed_checks

        else:
            failed_checks = self.failed_checks

        resolved: Union[None, Unset, bool]
        if isinstance(self.resolved, Unset):
            resolved = UNSET
        else:
            resolved = self.resolved

        user_metadata: Union[Any, None, Unset, dict[str, Any]]
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET
        elif isinstance(self.user_metadata, DatapointListItemUserMetadataType0):
            user_metadata = self.user_metadata.to_dict()
        else:
            user_metadata = self.user_metadata

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_checks_type_0 import DatapointListItemChecksType0
        from ..models.datapoint_list_item_input_tools_type_0_item import DatapointListItemInputToolsType0Item
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_result_embeddings_type_0_item import (
            DatapointListItemResultEmbeddingsType0Item,
        )
        from ..models.datapoint_list_item_result_tool_calls_type_0_item import DatapointListItemResultToolCallsType0Item
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

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

        def _parse_feedback(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_error_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_error_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_type = _parse_error_type(d.pop("error_type", UNSET))

        def _parse_context_token(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

        _time_created = d.pop("time_created", UNSET)
        time_created: Union[Unset, datetime.datetime]
        if isinstance(_time_created, Unset):
            time_created = UNSET
        else:
            time_created = isoparse(_time_created)

        def _parse_model_metadata(data: object) -> Union["DatapointListItemModelMetadataType0", Any, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metadata_type_0 = DatapointListItemModelMetadataType0.from_dict(data)

                return model_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemModelMetadataType0", Any, None, Unset], data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        def _parse_project_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_mut_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_test_run_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

        def _parse_group_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_id_type_0 = UUID(data)

                return group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        group_id = _parse_group_id(d.pop("group_id", UNSET))

        def _parse_scenario_data_point_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_data_point_id_type_0 = UUID(data)

                return scenario_data_point_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scenario_data_point_id = _parse_scenario_data_point_id(d.pop("scenario_data_point_id", UNSET))

        def _parse_latency(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        latency = _parse_latency(d.pop("latency", UNSET))

        def _parse_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_input_tools(data: object) -> Union[None, Unset, list["DatapointListItemInputToolsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_tools_type_0 = []
                _input_tools_type_0 = data
                for input_tools_type_0_item_data in _input_tools_type_0:
                    input_tools_type_0_item = DatapointListItemInputToolsType0Item.from_dict(
                        input_tools_type_0_item_data
                    )

                    input_tools_type_0.append(input_tools_type_0_item)

                return input_tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DatapointListItemInputToolsType0Item"]], data)

        input_tools = _parse_input_tools(d.pop("input_tools", UNSET))

        def _parse_result_tool_calls(
            data: object,
        ) -> Union[None, Unset, list["DatapointListItemResultToolCallsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_tool_calls_type_0 = []
                _result_tool_calls_type_0 = data
                for result_tool_calls_type_0_item_data in _result_tool_calls_type_0:
                    result_tool_calls_type_0_item = DatapointListItemResultToolCallsType0Item.from_dict(
                        result_tool_calls_type_0_item_data
                    )

                    result_tool_calls_type_0.append(result_tool_calls_type_0_item)

                return result_tool_calls_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DatapointListItemResultToolCallsType0Item"]], data)

        result_tool_calls = _parse_result_tool_calls(d.pop("result_tool_calls", UNSET))

        def _parse_result_embeddings(
            data: object,
        ) -> Union[None, Unset, list["DatapointListItemResultEmbeddingsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                result_embeddings_type_0 = []
                _result_embeddings_type_0 = data
                for result_embeddings_type_0_item_data in _result_embeddings_type_0:
                    result_embeddings_type_0_item = DatapointListItemResultEmbeddingsType0Item.from_dict(
                        result_embeddings_type_0_item_data
                    )

                    result_embeddings_type_0.append(result_embeddings_type_0_item)

                return result_embeddings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["DatapointListItemResultEmbeddingsType0Item"]], data)

        result_embeddings = _parse_result_embeddings(d.pop("result_embeddings", UNSET))

        def _parse_checks(data: object) -> Union["DatapointListItemChecksType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                checks_type_0 = DatapointListItemChecksType0.from_dict(data)

                return checks_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemChecksType0", None, Unset], data)

        checks = _parse_checks(d.pop("checks", UNSET))

        def _parse_agent_metadata(data: object) -> Union["DatapointListItemAgentMetadataType0", Any, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_metadata_type_0 = DatapointListItemAgentMetadataType0.from_dict(data)

                return agent_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemAgentMetadataType0", Any, None, Unset], data)

        agent_metadata = _parse_agent_metadata(d.pop("agent_metadata", UNSET))

        def _parse_provider(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_total_search_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_search_count = _parse_total_search_count(d.pop("total_search_count", UNSET))

        def _parse_total_datapoint_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_datapoint_count = _parse_total_datapoint_count(d.pop("total_datapoint_count", UNSET))

        def _parse_request_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        request_model_name = _parse_request_model_name(d.pop("request_model_name", UNSET))

        def _parse_response_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        response_model_name = _parse_response_model_name(d.pop("response_model_name", UNSET))

        def _parse_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_failed_checks(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                failed_checks_type_0 = cast(list[str], data)

                return failed_checks_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        failed_checks = _parse_failed_checks(d.pop("failed_checks", UNSET))

        def _parse_resolved(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        resolved = _parse_resolved(d.pop("resolved", UNSET))

        def _parse_user_metadata(data: object) -> Union["DatapointListItemUserMetadataType0", Any, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_metadata_type_0 = DatapointListItemUserMetadataType0.from_dict(data)

                return user_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatapointListItemUserMetadataType0", Any, None, Unset], data)

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
