import datetime
import importlib.metadata
import json
import logging
import random
import string
import uuid
from typing import Any, Collection, Optional

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor, TracerProvider
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper  # type: ignore

from okareo import Okareo

logging.basicConfig(level=logging.FATAL)


def get_agent_names(json_data: Any) -> Any:
    data = json.loads(json_data)
    agents = data.get("crew_agents", [])
    agent_names = [agent["role"] for agent in agents]
    return agent_names


def find_agent_role(json_data: Any, id_prefix: Any) -> Any:
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
        base_path = config.get("base_path", None)
        api_key = config["api_key"]

        if base_path and len(base_path) > 0:
            self.okareo = Okareo(api_key, base_path=base_path)
        else:
            self.okareo = Okareo(api_key)
        self.is_context_set = "context_token" in config
        self.context_id = str(config.get("context_token", uuid.uuid4()))
        self.tags = config.get("tags", [])
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        self.group_name = config.get("group_name", f"crewai-chat-{random_suffix}")

        self.group = self.okareo.create_group(
            name=self.group_name, tags=self.tags, source={"log_source": "crewai"}
        )
        self.created_obj: Any = {}
        self.cur_model: Any = None
        self.total_task_count = 0
        self.task_count = 0

    def _format_span_data(self, span: ReadableSpan) -> dict:
        if span.attributes is None:
            return {}
        formatted_data = {
            k: self.safe_loads(v)
            for k, v in span.attributes.items()
            if self.is_serializable(self.safe_loads(v))
        }
        if "openai.message_get" in formatted_data:
            formatted_data["openai.message_get"] = self.safe_loads(
                formatted_data["openai.message_get"]
            )
        return formatted_data

    def _get_timestamp_iso(self, epoch_ns: Any) -> str:
        timestamp = datetime.datetime.fromtimestamp(
            epoch_ns / 1e9, tz=datetime.timezone.utc
        ).isoformat()
        return timestamp

    def on_end(self, span: ReadableSpan) -> None:
        if span.name == "Crew Created":
            self.task_count = 0
            self.total_task_count = 0
            if not self.is_context_set:
                self.context_id = str(uuid.uuid4())
            self.created_obj = self._format_span_data(span)
            self.total_task_count = len(self.created_obj["crew_tasks"])

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
            role = find_agent_role(
                json.dumps(self.created_obj), span_data.get("task_id")
            )
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
            if cur_model:
                cur_model.add_data_point(
                    input_obj=span_data,
                    input_datetime=self._get_timestamp_iso(span.start_time),
                    result_obj=json.dumps(result_obj),
                    result_datetime=self._get_timestamp_iso(span.end_time),
                    context_token=self.context_id,
                    tags=self.tags,
                    group_id=self.group.get("id"),
                )
        if span.name == "Task Execution":
            self.task_count += 1
            if self.task_count == self.total_task_count:
                self.okareo.create_trace_eval(self.group, self.context_id)

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


def completion_wrapper(version: Any, tracer: Any) -> Any:
    def wrapper(wrapped: Any, instance: Any, args: Any, kwargs: Any) -> Any:
        with tracer.start_as_current_span("litellm.completion") as span:
            span.set_attribute("litellm.version", version)

            model = kwargs.get("model") or args[0] if args else None
            if model:
                span.set_attribute("litellm.model", model)

            messages = kwargs.get("messages")
            if messages:
                messages_json = json.dumps(messages, indent=2)
                span.set_attribute("messages", messages_json)

            try:
                result = wrapped(*args, **kwargs)

                if isinstance(result, dict):
                    usage = result.get("usage", {})
                    span.set_attribute(
                        "litellm.completion_tokens",
                        usage.get("completion_tokens"),
                    )
                    span.set_attribute(
                        "litellm.prompt_tokens",
                        usage.get("prompt_tokens"),
                    )
                    span.set_attribute(
                        "litellm.total_tokens",
                        usage.get("total_tokens"),
                    )

                return result
            except Exception as e:
                span.record_exception(e)

                raise

    return wrapper


class LiteLLMInstrumentation(BaseInstrumentor):  # type: ignore
    def instrumentation_dependencies(self) -> Collection[str]:
        return ["litellm >= 1.48.0", "opentelemetry-api >= 1.0.0"]

    def _instrument(self, **kwargs: Any) -> None:
        tracer_provider: Optional[TracerProvider] = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        version: str = importlib.metadata.version("litellm")
        wrap_function_wrapper(
            "litellm",
            "completion",
            completion_wrapper(version, tracer),
        )

        wrap_function_wrapper(
            "litellm",
            "text_completion",
            completion_wrapper(version, tracer),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass


def chat_completions_create(version: Any, tracer: Any) -> Any:
    def wrapper(wrapped: Any, instance: Any, args: Any, kwargs: Any) -> Any:
        with tracer.start_as_current_span("openai.chat.completions.create") as span:
            span.set_attribute("openai.version", version)

            model = kwargs.get("model")
            if model:
                span.set_attribute("openai.model", model)

            messages = kwargs.get("messages")
            span.set_attribute("openai.message_get", json.dumps(messages))

            try:
                result = wrapped(*args, **kwargs)

                if hasattr(result, "usage"):
                    span.set_attribute(
                        "openai.completion_tokens", result.usage.completion_tokens
                    )
                    span.set_attribute(
                        "openai.prompt_tokens", result.usage.prompt_tokens
                    )
                    span.set_attribute("openai.total_tokens", result.usage.total_tokens)

                return result
            except Exception as e:
                span.record_exception(e)
                raise

    return wrapper


class OpenAIInstrumentation(BaseInstrumentor):  # type: ignore
    def instrumentation_dependencies(self) -> Collection[str]:
        return ["openai >= 0.27.0", "opentelemetry-api >= 1.0.0"]

    def _instrument(self, **kwargs: Any) -> None:
        tracer_provider: Optional[TracerProvider] = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        version: str = importlib.metadata.version("openai")

        wrap_function_wrapper(
            "openai.resources.chat.completions",
            "Completions.create",
            chat_completions_create(version, tracer),
        )
        wrap_function_wrapper(
            "openai.resources.chat.completions",
            "AsyncCompletions.create",
            chat_completions_create(version, tracer),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass


class CrewAILogger:
    _instance = None
    _provider = None

    def __new__(cls, *args, **kwargs) -> Any:  # type: ignore
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, logger_config: dict[str, Any]) -> None:
        self.logger_config: Any = logger_config
        self.span_processor: Any = None

    def start(self) -> None:
        if CrewAILogger._provider is None:
            CrewAILogger._provider = TracerProvider()
            trace.set_tracer_provider(CrewAILogger._provider)
            LiteLLMInstrumentation().instrument(
                tracer_provider=CrewAILogger._provider, skip_dep_check=True
            )
            OpenAIInstrumentation().instrument(
                tracer_provider=CrewAILogger._provider, skip_dep_check=True
            )

        if self.span_processor is None:
            self.span_processor = CrewAISpanProcessor(self.logger_config)
            CrewAILogger._provider.add_span_processor(self.span_processor)

    def stop(self) -> None:
        if self.span_processor:
            self.span_processor.shutdown()
            self.span_processor = None
        # Note: We're not removing the span processor from the TracerProvider
        # as there's no built-in method to do so.

    def __enter__(self) -> "CrewAILogger":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

    def __del__(self) -> None:
        self.stop()
