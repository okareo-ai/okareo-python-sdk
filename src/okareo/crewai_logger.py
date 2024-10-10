import datetime
import json
import random
import string
import uuid
from typing import Any, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider
from opentelemetry.trace import Status, StatusCode

from okareo import Okareo


class CrewAISpanProcessor(SpanProcessor):
    def __init__(self, config: dict[str, Any]) -> None:
        if "api_key" not in config:
            raise ValueError("api_key is required in the config")

        self.okareo = Okareo(
            config["api_key"],
        )
        self.session_id = str(config.get("context_token", uuid.uuid4()))
        self.tags = config.get("tags", [])
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        self.mut_name = config.get("mut_name", f"crewai-chat-{random_suffix}")
        
        self.registered_model = self.okareo.register_model(
            name=self.mut_name,
            tags=self.tags
        )

    def _format_span_data(self, span: ReadableSpan) -> dict:
        if span.attributes is None:
            return {}
        return {
            k: self.safe_loads(v)
            for k, v in span.attributes.items()
            if self.is_serializable(self.safe_loads(v))
        }

    def _get_timestamp_iso(self, epoch_ns: Any) -> str:
        return datetime.datetime.fromtimestamp(epoch_ns / 1e9, tz=datetime.timezone.utc).isoformat()

    def on_end(self, span: ReadableSpan) -> None:
        if span.instrumentation_info.name != "crewai.telemetry":
            return

        try:
            span_data = self._format_span_data(span)
            result_obj = {
                "log_type": span.name,
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
            }

            self.registered_model.add_data_point(
                input_obj=span_data,
                input_datetime=self._get_timestamp_iso(span.start_time),
                result_obj=json.dumps(result_obj),
                result_datetime=self._get_timestamp_iso(span.end_time),
                context_token=self.session_id,
                tags=self.tags,
            )
        except Exception as e:
            import traceback
            print(f"Error adding data point: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())

    @staticmethod
    def safe_loads(data: Any) -> Any:
        try:
            return json.loads(data)
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
        provider.add_span_processor(CrewAISpanProcessor(logger_config))
        trace.set_tracer_provider(provider)
