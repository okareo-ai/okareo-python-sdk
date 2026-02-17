from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
    from ..models.datapoint_list_item_checks import DatapointListItemChecks
    from ..models.datapoint_list_item_checks_metadata import DatapointListItemChecksMetadata
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
        tags (list[str] | Unset):
        input_ (Any | Unset):
        input_datetime (datetime.datetime | None | Unset):
        result (Any | Unset):
        result_datetime (datetime.datetime | None | Unset):
        feedback (float | None | Unset):
        error_message (None | str | Unset):
        error_code (None | str | Unset):
        error_type (None | str | Unset):
        context_token (None | str | Unset):
        time_created (datetime.datetime | None | Unset):
        model_metadata (Any | DatapointListItemModelMetadataType0 | None | Unset):
        project_id (None | Unset | UUID):
        mut_id (None | Unset | UUID):
        test_run_id (None | Unset | UUID):
        test_data_point_id (None | Unset | UUID):
        group_id (None | Unset | UUID):
        scenario_data_point_id (None | Unset | UUID):
        latency (int | None | Unset):
        input_tokens (int | None | Unset):
        output_tokens (int | None | Unset):
        source (None | str | Unset):
        temperature (None | str | Unset):
        input_tools (list[DatapointListItemInputToolsType0Item] | None | Unset):
        result_tool_calls (list[DatapointListItemResultToolCallsType0Item] | None | Unset):
        result_embeddings (list[DatapointListItemResultEmbeddingsType0Item] | None | Unset):
        checks (DatapointListItemChecks | Unset):
        checks_metadata (DatapointListItemChecksMetadata | Unset):
        agent_metadata (Any | DatapointListItemAgentMetadataType0 | None | Unset):
        provider (None | str | Unset):
        total_search_count (int | None | Unset):
        total_datapoint_count (int | None | Unset):
        request_model_name (None | str | Unset):
        response_model_name (None | str | Unset):
        cost (float | None | Unset):
        status (str | Unset):  Default: ''.
        failed_checks (list[str] | Unset): Array of failed check names
        resolved (bool | Unset): Manual marking from user on resolved status Default: False.
        user_metadata (Any | DatapointListItemUserMetadataType0 | None | Unset): User-provided metadata provided as
            context to the completion call.
        otel_trace_id (None | str | Unset): OpenTelemetry Trace ID
        otel_span_id (None | str | Unset): OpenTelemetry Span ID
    """

    id: UUID
    tags: list[str] | Unset = UNSET
    input_: Any | Unset = UNSET
    input_datetime: datetime.datetime | None | Unset = UNSET
    result: Any | Unset = UNSET
    result_datetime: datetime.datetime | None | Unset = UNSET
    feedback: float | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_type: None | str | Unset = UNSET
    context_token: None | str | Unset = UNSET
    time_created: datetime.datetime | None | Unset = UNSET
    model_metadata: Any | DatapointListItemModelMetadataType0 | None | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    mut_id: None | Unset | UUID = UNSET
    test_run_id: None | Unset | UUID = UNSET
    test_data_point_id: None | Unset | UUID = UNSET
    group_id: None | Unset | UUID = UNSET
    scenario_data_point_id: None | Unset | UUID = UNSET
    latency: int | None | Unset = UNSET
    input_tokens: int | None | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    source: None | str | Unset = UNSET
    temperature: None | str | Unset = UNSET
    input_tools: list[DatapointListItemInputToolsType0Item] | None | Unset = UNSET
    result_tool_calls: list[DatapointListItemResultToolCallsType0Item] | None | Unset = UNSET
    result_embeddings: list[DatapointListItemResultEmbeddingsType0Item] | None | Unset = UNSET
    checks: DatapointListItemChecks | Unset = UNSET
    checks_metadata: DatapointListItemChecksMetadata | Unset = UNSET
    agent_metadata: Any | DatapointListItemAgentMetadataType0 | None | Unset = UNSET
    provider: None | str | Unset = UNSET
    total_search_count: int | None | Unset = UNSET
    total_datapoint_count: int | None | Unset = UNSET
    request_model_name: None | str | Unset = UNSET
    response_model_name: None | str | Unset = UNSET
    cost: float | None | Unset = UNSET
    status: str | Unset = ""
    failed_checks: list[str] | Unset = UNSET
    resolved: bool | Unset = False
    user_metadata: Any | DatapointListItemUserMetadataType0 | None | Unset = UNSET
    otel_trace_id: None | str | Unset = UNSET
    otel_span_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        id = str(self.id)

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        input_ = self.input_

        input_datetime: None | str | Unset
        if isinstance(self.input_datetime, Unset):
            input_datetime = UNSET
        elif isinstance(self.input_datetime, datetime.datetime):
            input_datetime = self.input_datetime.isoformat()
        else:
            input_datetime = self.input_datetime

        result = self.result

        result_datetime: None | str | Unset
        if isinstance(self.result_datetime, Unset):
            result_datetime = UNSET
        elif isinstance(self.result_datetime, datetime.datetime):
            result_datetime = self.result_datetime.isoformat()
        else:
            result_datetime = self.result_datetime

        feedback: float | None | Unset
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        else:
            feedback = self.feedback

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        error_type: None | str | Unset
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        else:
            error_type = self.error_type

        context_token: None | str | Unset
        if isinstance(self.context_token, Unset):
            context_token = UNSET
        else:
            context_token = self.context_token

        time_created: None | str | Unset
        if isinstance(self.time_created, Unset):
            time_created = UNSET
        elif isinstance(self.time_created, datetime.datetime):
            time_created = self.time_created.isoformat()
        else:
            time_created = self.time_created

        model_metadata: Any | dict[str, Any] | None | Unset
        if isinstance(self.model_metadata, Unset):
            model_metadata = UNSET
        elif isinstance(self.model_metadata, DatapointListItemModelMetadataType0):
            model_metadata = self.model_metadata.to_dict()
        else:
            model_metadata = self.model_metadata

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        mut_id: None | str | Unset
        if isinstance(self.mut_id, Unset):
            mut_id = UNSET
        elif isinstance(self.mut_id, UUID):
            mut_id = str(self.mut_id)
        else:
            mut_id = self.mut_id

        test_run_id: None | str | Unset
        if isinstance(self.test_run_id, Unset):
            test_run_id = UNSET
        elif isinstance(self.test_run_id, UUID):
            test_run_id = str(self.test_run_id)
        else:
            test_run_id = self.test_run_id

        test_data_point_id: None | str | Unset
        if isinstance(self.test_data_point_id, Unset):
            test_data_point_id = UNSET
        elif isinstance(self.test_data_point_id, UUID):
            test_data_point_id = str(self.test_data_point_id)
        else:
            test_data_point_id = self.test_data_point_id

        group_id: None | str | Unset
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        elif isinstance(self.group_id, UUID):
            group_id = str(self.group_id)
        else:
            group_id = self.group_id

        scenario_data_point_id: None | str | Unset
        if isinstance(self.scenario_data_point_id, Unset):
            scenario_data_point_id = UNSET
        elif isinstance(self.scenario_data_point_id, UUID):
            scenario_data_point_id = str(self.scenario_data_point_id)
        else:
            scenario_data_point_id = self.scenario_data_point_id

        latency: int | None | Unset
        if isinstance(self.latency, Unset):
            latency = UNSET
        else:
            latency = self.latency

        input_tokens: int | None | Unset
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        output_tokens: int | None | Unset
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        source: None | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        temperature: None | str | Unset
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        input_tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.input_tools, Unset):
            input_tools = UNSET
        elif isinstance(self.input_tools, list):
            input_tools = []
            for input_tools_type_0_item_data in self.input_tools:
                input_tools_type_0_item = input_tools_type_0_item_data.to_dict()
                input_tools.append(input_tools_type_0_item)

        else:
            input_tools = self.input_tools

        result_tool_calls: list[dict[str, Any]] | None | Unset
        if isinstance(self.result_tool_calls, Unset):
            result_tool_calls = UNSET
        elif isinstance(self.result_tool_calls, list):
            result_tool_calls = []
            for result_tool_calls_type_0_item_data in self.result_tool_calls:
                result_tool_calls_type_0_item = result_tool_calls_type_0_item_data.to_dict()
                result_tool_calls.append(result_tool_calls_type_0_item)

        else:
            result_tool_calls = self.result_tool_calls

        result_embeddings: list[dict[str, Any]] | None | Unset
        if isinstance(self.result_embeddings, Unset):
            result_embeddings = UNSET
        elif isinstance(self.result_embeddings, list):
            result_embeddings = []
            for result_embeddings_type_0_item_data in self.result_embeddings:
                result_embeddings_type_0_item = result_embeddings_type_0_item_data.to_dict()
                result_embeddings.append(result_embeddings_type_0_item)

        else:
            result_embeddings = self.result_embeddings

        checks: dict[str, Any] | Unset = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks.to_dict()

        checks_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.checks_metadata, Unset):
            checks_metadata = self.checks_metadata.to_dict()

        agent_metadata: Any | dict[str, Any] | None | Unset
        if isinstance(self.agent_metadata, Unset):
            agent_metadata = UNSET
        elif isinstance(self.agent_metadata, DatapointListItemAgentMetadataType0):
            agent_metadata = self.agent_metadata.to_dict()
        else:
            agent_metadata = self.agent_metadata

        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        else:
            provider = self.provider

        total_search_count: int | None | Unset
        if isinstance(self.total_search_count, Unset):
            total_search_count = UNSET
        else:
            total_search_count = self.total_search_count

        total_datapoint_count: int | None | Unset
        if isinstance(self.total_datapoint_count, Unset):
            total_datapoint_count = UNSET
        else:
            total_datapoint_count = self.total_datapoint_count

        request_model_name: None | str | Unset
        if isinstance(self.request_model_name, Unset):
            request_model_name = UNSET
        else:
            request_model_name = self.request_model_name

        response_model_name: None | str | Unset
        if isinstance(self.response_model_name, Unset):
            response_model_name = UNSET
        else:
            response_model_name = self.response_model_name

        cost: float | None | Unset
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        status = self.status

        failed_checks: list[str] | Unset = UNSET
        if not isinstance(self.failed_checks, Unset):
            failed_checks = self.failed_checks

        resolved = self.resolved

        user_metadata: Any | dict[str, Any] | None | Unset
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET
        elif isinstance(self.user_metadata, DatapointListItemUserMetadataType0):
            user_metadata = self.user_metadata.to_dict()
        else:
            user_metadata = self.user_metadata

        otel_trace_id: None | str | Unset
        if isinstance(self.otel_trace_id, Unset):
            otel_trace_id = UNSET
        else:
            otel_trace_id = self.otel_trace_id

        otel_span_id: None | str | Unset
        if isinstance(self.otel_span_id, Unset):
            otel_span_id = UNSET
        else:
            otel_span_id = self.otel_span_id

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
        if checks_metadata is not UNSET:
            field_dict["checks_metadata"] = checks_metadata
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
        if otel_trace_id is not UNSET:
            field_dict["otel_trace_id"] = otel_trace_id
        if otel_span_id is not UNSET:
            field_dict["otel_span_id"] = otel_span_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.datapoint_list_item_agent_metadata_type_0 import DatapointListItemAgentMetadataType0
        from ..models.datapoint_list_item_checks import DatapointListItemChecks
        from ..models.datapoint_list_item_checks_metadata import DatapointListItemChecksMetadata
        from ..models.datapoint_list_item_input_tools_type_0_item import DatapointListItemInputToolsType0Item
        from ..models.datapoint_list_item_model_metadata_type_0 import DatapointListItemModelMetadataType0
        from ..models.datapoint_list_item_result_embeddings_type_0_item import (
            DatapointListItemResultEmbeddingsType0Item,
        )
        from ..models.datapoint_list_item_result_tool_calls_type_0_item import DatapointListItemResultToolCallsType0Item
        from ..models.datapoint_list_item_user_metadata_type_0 import DatapointListItemUserMetadataType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        tags = cast(list[str], d.pop("tags", UNSET))

        input_ = d.pop("input", UNSET)

        def _parse_input_datetime(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_datetime_type_0 = isoparse(data)

                return input_datetime_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        input_datetime = _parse_input_datetime(d.pop("input_datetime", UNSET))

        result = d.pop("result", UNSET)

        def _parse_result_datetime(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_datetime_type_0 = isoparse(data)

                return result_datetime_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        result_datetime = _parse_result_datetime(d.pop("result_datetime", UNSET))

        def _parse_feedback(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("error_code", UNSET))

        def _parse_error_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_type = _parse_error_type(d.pop("error_type", UNSET))

        def _parse_context_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        context_token = _parse_context_token(d.pop("context_token", UNSET))

        def _parse_time_created(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_created_type_0 = isoparse(data)

                return time_created_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        time_created = _parse_time_created(d.pop("time_created", UNSET))

        def _parse_model_metadata(data: object) -> Any | DatapointListItemModelMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_metadata_type_0 = DatapointListItemModelMetadataType0.from_dict(data)

                return model_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointListItemModelMetadataType0 | None | Unset, data)

        model_metadata = _parse_model_metadata(d.pop("model_metadata", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_mut_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mut_id_type_0 = UUID(data)

                return mut_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        mut_id = _parse_mut_id(d.pop("mut_id", UNSET))

        def _parse_test_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_run_id_type_0 = UUID(data)

                return test_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        test_run_id = _parse_test_run_id(d.pop("test_run_id", UNSET))

        def _parse_test_data_point_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                test_data_point_id_type_0 = UUID(data)

                return test_data_point_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        test_data_point_id = _parse_test_data_point_id(d.pop("test_data_point_id", UNSET))

        def _parse_group_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_id_type_0 = UUID(data)

                return group_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        group_id = _parse_group_id(d.pop("group_id", UNSET))

        def _parse_scenario_data_point_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scenario_data_point_id_type_0 = UUID(data)

                return scenario_data_point_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        scenario_data_point_id = _parse_scenario_data_point_id(d.pop("scenario_data_point_id", UNSET))

        def _parse_latency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latency = _parse_latency(d.pop("latency", UNSET))

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_temperature(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_input_tools(data: object) -> list[DatapointListItemInputToolsType0Item] | None | Unset:
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
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DatapointListItemInputToolsType0Item] | None | Unset, data)

        input_tools = _parse_input_tools(d.pop("input_tools", UNSET))

        def _parse_result_tool_calls(data: object) -> list[DatapointListItemResultToolCallsType0Item] | None | Unset:
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
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DatapointListItemResultToolCallsType0Item] | None | Unset, data)

        result_tool_calls = _parse_result_tool_calls(d.pop("result_tool_calls", UNSET))

        def _parse_result_embeddings(data: object) -> list[DatapointListItemResultEmbeddingsType0Item] | None | Unset:
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
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DatapointListItemResultEmbeddingsType0Item] | None | Unset, data)

        result_embeddings = _parse_result_embeddings(d.pop("result_embeddings", UNSET))

        _checks = d.pop("checks", UNSET)
        checks: DatapointListItemChecks | Unset
        if isinstance(_checks, Unset):
            checks = UNSET
        else:
            checks = DatapointListItemChecks.from_dict(_checks)

        _checks_metadata = d.pop("checks_metadata", UNSET)
        checks_metadata: DatapointListItemChecksMetadata | Unset
        if isinstance(_checks_metadata, Unset):
            checks_metadata = UNSET
        else:
            checks_metadata = DatapointListItemChecksMetadata.from_dict(_checks_metadata)

        def _parse_agent_metadata(data: object) -> Any | DatapointListItemAgentMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_metadata_type_0 = DatapointListItemAgentMetadataType0.from_dict(data)

                return agent_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointListItemAgentMetadataType0 | None | Unset, data)

        agent_metadata = _parse_agent_metadata(d.pop("agent_metadata", UNSET))

        def _parse_provider(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_total_search_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_search_count = _parse_total_search_count(d.pop("total_search_count", UNSET))

        def _parse_total_datapoint_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_datapoint_count = _parse_total_datapoint_count(d.pop("total_datapoint_count", UNSET))

        def _parse_request_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        request_model_name = _parse_request_model_name(d.pop("request_model_name", UNSET))

        def _parse_response_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        response_model_name = _parse_response_model_name(d.pop("response_model_name", UNSET))

        def _parse_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cost = _parse_cost(d.pop("cost", UNSET))

        status = d.pop("status", UNSET)

        failed_checks = cast(list[str], d.pop("failed_checks", UNSET))

        resolved = d.pop("resolved", UNSET)

        def _parse_user_metadata(data: object) -> Any | DatapointListItemUserMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_metadata_type_0 = DatapointListItemUserMetadataType0.from_dict(data)

                return user_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Any | DatapointListItemUserMetadataType0 | None | Unset, data)

        user_metadata = _parse_user_metadata(d.pop("user_metadata", UNSET))

        def _parse_otel_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        otel_trace_id = _parse_otel_trace_id(d.pop("otel_trace_id", UNSET))

        def _parse_otel_span_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        otel_span_id = _parse_otel_span_id(d.pop("otel_span_id", UNSET))

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
            checks_metadata=checks_metadata,
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
            otel_trace_id=otel_trace_id,
            otel_span_id=otel_span_id,
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
