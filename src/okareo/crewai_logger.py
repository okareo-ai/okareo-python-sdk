import datetime
import json
import random
import string
import traceback
import uuid
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider

from okareo import Okareo

def get_agent_names(json_data):
    data = json.loads(json_data)
    agents = data.get('crew_agents', [])
    agent_names = [agent['role'] for agent in agents]
    return agent_names

def find_agent_role(json_data, id_prefix):
    data = json.loads(json_data)
    
    for task in data["crew_tasks"]:
        if task["id"].startswith(id_prefix):
            role = task["agent_role"]
            return role
    return None

class CrewAISpanProcessor(SpanProcessor):
    def __init__(self, config: dict[str, Any]) -> None:
        if "api_key" not in config:
            raise ValueError("api_key is required in the config")

        self.okareo = Okareo(
            config["api_key"],
        )
        self.context_id = str(config.get("context_token", uuid.uuid4()))
        self.tags = config.get("tags", [])
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        self.group_name = config.get("group_name", f"crewai-chat-{random_suffix}")

        self.group = self.okareo.create_group(
            name=self.group_name, tags=self.tags, source={"log_source": "crewai"}
        )
        self.created_obj = {}
        self.cur_model = None

    def _format_span_data(self, span: ReadableSpan) -> dict:
        if span.attributes is None:
            return {}
        formatted_data = {
            k: self.safe_loads(v)
            for k, v in span.attributes.items()
            if self.is_serializable(self.safe_loads(v))
        }
        return formatted_data

    def _get_timestamp_iso(self, epoch_ns: Any) -> str:
        timestamp = datetime.datetime.fromtimestamp(
            epoch_ns / 1e9, tz=datetime.timezone.utc
        ).isoformat()
        return timestamp

    def on_end(self, span: ReadableSpan) -> None:
        if span.instrumentation_info.name != "crewai.telemetry":
            return

        try:
            if span.name == "Crew Created":
                self.created_obj = self._format_span_data(span)
            
                agent_names = get_agent_names(json.dumps(self.created_obj))
                self.models = []
                for agent_name in agent_names:
                    model = self.okareo.register_model(name=agent_name)
                    self.models.append(model)
                    self.okareo.add_model_to_group(self.group, model)
            models_to_add = []
            span_data = self._format_span_data(span)
            if span.name == "Crew Created":
                models_to_add = self.models
            elif span.name == "Task Created":
                role = find_agent_role(json.dumps(self.created_obj), span_data.get("task_id"))
                self.cur_model = self.okareo.register_model(name=role)
                models_to_add = [self.cur_model]
            else:
                models_to_add = [self.cur_model] 

            result_obj = {
                "log_type": span.name,
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
            }
            for cur_model in models_to_add:
                cur_model.add_data_point(
                    input_obj=span_data,
                    input_datetime=self._get_timestamp_iso(span.start_time),
                    result_obj=json.dumps(result_obj),
                    result_datetime=self._get_timestamp_iso(span.end_time),
                    context_token=self.context_id,
                    tags=self.tags,
                    group_id=self.group.get('id'),
                )
        except Exception as e:
            pass

    @staticmethod
    def safe_loads(data: Any) -> Any:
        try:
            loaded_data = json.loads(data)
            return loaded_data
        except (json.JSONDecodeError, TypeError):
            return data

    @staticmethod
    def is_serializable(obj: Any) -> bool:
        if isinstance(obj, (str, int, float, bool, type(None))):
            return True
        if isinstance(obj, dict):
            return all(CrewAISpanProcessor.is_serializable(v) for v in obj.values())
        if isinstance(obj, (list, tuple)):
            return all(CrewAISpanProcessor.is_serializable(item) for item in obj)
        return False


class CrewAILogger:
    def __init__(self, logger_config: dict[str, Any]):
        provider = TracerProvider()
        span_processor = CrewAISpanProcessor(logger_config)
        provider.add_span_processor(span_processor)
        trace.set_tracer_provider(provider)
