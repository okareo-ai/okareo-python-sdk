from __future__ import annotations

import json
import logging
import random
import string
import threading
import traceback
import uuid
from typing import TYPE_CHECKING, Any, Callable, TypeVar

import autogen  # type: ignore
from autogen.logger.base_logger import BaseLogger  # type: ignore
from autogen.logger.logger_utils import get_current_ts, to_dict  # type: ignore
from openai import AzureOpenAI, OpenAI
from openai.types.chat import ChatCompletion

from okareo import Okareo

if TYPE_CHECKING:
    from autogen import Agent

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def agent_obj_to_name(agent: Agent) -> str:  # type: ignore
    return agent.name if isinstance(agent, Agent) else agent  # type: ignore


def safe_serialize(obj: Any) -> str:
    def default(o: Any) -> str:
        if hasattr(o, "to_json"):
            return str(o.to_json())
        elif callable(o):
            return f"<function {o.__name__}>"
        else:
            return f"<<non-serializable: {type(o).__qualname__}>>"

    return json.dumps(obj, default=default)


class OkareoLogger(BaseLogger):  # type: ignore
    def __init__(
        self,
        config: dict[str, Any],
    ) -> None:
        assert "api_key" in config, "api_key is required in the config"
        api_key = config["api_key"]
        base_path = config.get("base_path", None)

        if base_path and len(base_path) > 0:
            self.okareo = Okareo(api_key, base_path=base_path)
        else:
            self.okareo = Okareo(api_key)

        self.session_id = str(uuid.uuid4())

        random_str = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        self.mut_name = config.get("mut_name", f"autogen-chat-{random_str}")
        self.tags = config.get("tags", [])
        self.registered_model = self.okareo.register_model(
            name=self.mut_name, tags=self.tags
        )

        # set default logging options
        self._log_chat_completion = config.get("log_chat_completion", True)
        self._log_function_use = config.get("log_function_use", True)
        self._log_new_agent = config.get("log_new_agent", False)
        self._log_event = config.get("log_event", False)
        self._log_new_wrapper = config.get("log_new_wrapper", False)
        self._log_new_client = config.get("log_new_client", False)
        self._log_types = [
            "chat_completion",
            "function_use",
            "new_agent",
            "event",
            "new_wrapper",
            "new_client",
        ]

    def start(self) -> str:
        """Start the logger and return the session_id."""
        try:
            print(f"[Okareo] Started new session with Session ID: {self.session_id}")
            print(f"[Okareo] Logging data points under mut_name '{self.mut_name}'.")
            print("[Okareo] Logging the following events:")
            for log_type in self._log_types:
                if getattr(self, f"_log_{log_type}"):
                    print(f"[Okareo] - {log_type}")
        except Exception as e:
            print(f"[Okareo] Failed to start logging: {e}")
        return self.session_id

    def log_chat_completion(
        self,
        invocation_id: uuid.UUID,
        client_id: int,
        wrapper_id: int,
        source: Any,  # TODO: str | Agent,
        request: dict[str, float | str | list[dict[str, str]]],
        response: str | ChatCompletion,
        is_cached: int,
        cost: float,
        start_time: str,
    ) -> None:
        """
        Log a chat completion.
        """
        if self._log_chat_completion:
            thread_id = threading.get_ident()
            source_name = None
            if isinstance(source, str):
                source_name = getattr(source, "name", "unknown")
            else:
                source_name = source.name
            try:
                response_dict = json.loads(
                    safe_serialize(
                        response if isinstance(response, str) else response.model_dump()
                    )
                )
                self.registered_model.add_data_point_async(
                    input_obj=request,
                    input_datetime=start_time,
                    result_obj=json.dumps(
                        {
                            "log_type": "chat_completion",
                            "invocation_id": invocation_id,
                            "client_id": client_id,
                            "wrapper_id": wrapper_id,
                            "response": response_dict,
                            "is_cached": is_cached,
                            "cost": cost,
                            "thread_id": thread_id,
                            "source_name": source_name,
                        }
                    ),
                    result_datetime=get_current_ts(),
                    context_token=self.session_id,
                    tags=self.tags,
                )
            except Exception:
                tb = traceback.format_exc()
                line_number = tb.splitlines()[-3].split(",")[1].strip().split()[1]
                print(
                    f"[Okareo AutogenLogger] Failed to log chat completion (Line {line_number}): {tb}"
                )
        else:
            pass

    def log_new_agent(
        self, agent: Any, init_args: dict[str, Any]  # TODO: ConversableAgent,
    ) -> None:
        """
        Log a new agent instance.
        """
        if self._log_new_agent:
            thread_id = threading.get_ident()

            try:
                # make init_args['chat_messages'] serializable
                if (
                    "chat_messages" in init_args
                    and init_args["chat_messages"] is not None
                ):
                    init_args["chat_messages"] = {
                        agent_obj_to_name(k): agent_obj_to_name(v)
                        for k, v in init_args["chat_messages"].items()
                    }
                self.registered_model.add_data_point_async(
                    result_obj=json.dumps(
                        {
                            "log_type": "new_agent",
                            "agent_id": id(agent),
                            "agent_name": (
                                agent.name
                                if hasattr(agent, "name") and agent.name is not None
                                else ""
                            ),
                            "wrapper_id": to_dict(
                                agent.client.wrapper_id
                                if hasattr(agent, "client") and agent.client is not None
                                else ""
                            ),
                            "session_id": self.session_id,
                            "current_time": get_current_ts(),
                            "agent_type": type(agent).__name__,
                            "args": safe_serialize(init_args),
                            "thread_id": thread_id,
                        }
                    ),
                    result_datetime=get_current_ts(),
                    context_token=self.session_id,
                    tags=self.tags,
                )
            except Exception:
                tb = traceback.format_exc()
                line_number = tb.splitlines()[-3].split(",")[1].strip().split()[1]
                print(
                    f"[Okareo AutogenLogger] Failed to log new agent (Line {line_number}): {tb}"
                )
        else:
            pass

    def log_event(
        self, source: Any, name: str, **kwargs: dict[str, Any]  # TODO: str | Agent,
    ) -> None:
        """
        Log an event from an agent or a string source.
        """
        if self._log_event:

            # This takes an object o as input and returns a string. If the object o cannot be serialized, instead of raising an error,
            # it returns a string indicating that the object is non-serializable, along with its type's qualified name obtained using __qualname__.
            json_args = json.dumps(
                kwargs,
                default=lambda o: f"<<non-serializable: {type(o).__qualname__}>>",
            )
            thread_id = threading.get_ident()

            if isinstance(source, Agent):
                try:
                    self.registered_model.add_data_point_async(
                        result_obj=json.dumps(
                            {
                                "log_type": "event",
                                "source_id": id(source),
                                "source_name": (
                                    str(source.name)
                                    if hasattr(source, "name")
                                    else source
                                ),
                                "event_name": name,
                                "agent_module": source.__module__,
                                "agent_class": source.__class__.__name__,
                                "json_state": json_args,
                                "timestamp": get_current_ts(),
                                "thread_id": thread_id,
                            }
                        ),
                        result_datetime=get_current_ts(),
                        context_token=self.session_id,
                        tags=self.tags,
                    )
                except Exception as e:
                    print(f"[Okareo AutogenLogger] Failed to log event: {e}")
            else:
                try:
                    self.registered_model.add_data_point_async(
                        result_obj=json.dumps(
                            {
                                "log_type": "event",
                                "source_id": id(source),
                                "source_name": (
                                    str(source.name)
                                    if hasattr(source, "name")
                                    else source
                                ),
                                "event_name": name,
                                "json_state": json_args,
                                "timestamp": get_current_ts(),
                                "thread_id": thread_id,
                            }
                        ),
                        result_datetime=get_current_ts(),
                        context_token=self.session_id,
                        tags=self.tags,
                    )
                except Exception as e:
                    print(f"[Okareo AutogenLogger] Failed to log event: {e}")
        else:
            pass

    def log_new_wrapper(
        self,
        wrapper: Any,  # TODO: OpenAIWrapper
        init_args: dict[str, Any],  # TODO: dict[str, LLMConfig | list[LLMConfig]]
    ) -> None:
        """
        Log a new wrapper instance.
        """
        if self._log_new_wrapper:
            thread_id = threading.get_ident()
            try:
                self.registered_model.add_data_point_async(
                    result_obj=json.dumps(
                        {
                            "log_type": "new_wrapper",
                            "wrapper_id": id(wrapper),
                            "session_id": self.session_id,
                            "json_state": safe_serialize(init_args),
                            "timestamp": get_current_ts(),
                            "thread_id": thread_id,
                        }
                    ),
                    result_datetime=get_current_ts(),
                    context_token=self.session_id,
                    tags=self.tags,
                )
            except Exception:
                tb = traceback.format_exc()
                line_number = tb.splitlines()[-3].split(",")[1].strip().split()[1]
                print(
                    f"[Okareo AutogenLogger] Failed to log new wrapper (Line {line_number}): {tb}"
                )
        else:
            pass

    def log_new_client(
        self,
        client: AzureOpenAI | OpenAI,
        wrapper: Any,  # TODO: OpenAIWrapper
        init_args: dict[str, Any],
    ) -> None:
        """
        Log a new client instance.
        """
        if self._log_new_client:
            thread_id = threading.get_ident()

            try:
                self.registered_model.add_data_point_async(
                    result_obj=json.dumps(
                        {
                            "log_type": "new_client",
                            "client_id": id(client),
                            "wrapper_id": id(wrapper),
                            "session_id": self.session_id,
                            "class": type(client).__name__,
                            "json_state": json.dumps(init_args),
                            "timestamp": get_current_ts(),
                            "thread_id": thread_id,
                        }
                    ),
                    result_datetime=get_current_ts(),
                    context_token=self.session_id,
                    tags=self.tags,
                )
            except Exception as e:
                print(f"[Okareo AutogenLogger] Failed to log new client: {e}")
        else:
            pass

    def log_function_use(
        self,
        source: Any,  # TODO: str | Agent
        function: F,
        args: dict[str, Any],
        returns: Any,
    ) -> None:
        """
        Log a registered function(can be a tool) use from an agent or a string source.
        """
        if self._log_function_use:
            thread_id = threading.get_ident()

            try:
                self.registered_model.add_data_point_async(
                    result_obj=json.dumps(
                        {
                            "log_type": "new_client",
                            "source_id": id(source),
                            "source_name": (
                                str(source.name) if hasattr(source, "name") else source
                            ),
                            "agent_module": source.__module__,
                            "agent_class": source.__class__.__name__,
                            "timestamp": get_current_ts(),
                            "thread_id": thread_id,
                            "input_args": safe_serialize(args),
                            "returns": safe_serialize(returns),
                        }
                    ),
                    result_datetime=get_current_ts(),
                    context_token=self.session_id,
                    tags=self.tags,
                )
            except Exception as e:
                print(f"[Okareo AutogenLogger] Failed to log function use: {e}")
        else:
            pass

    def get_connection(self) -> None:
        """Method is intentionally left blank because there is no specific connection needed for the OkareoLogger."""

    def stop(self) -> None:
        """Close the file handler and remove it from the logger."""
        print(f"[Okareo] Finished logging Session ID: {self.session_id}")
        print(
            f"[Okareo] Logged data points for autogen chat under mut_name '{self.mut_name}'."
        )
        print(f"[Okareo] View data points at {self.registered_model.app_link}.")


class AutogenLogger:
    def __init__(
        self,
        config: dict[str, Any],
    ) -> None:
        self.logger = OkareoLogger(config)

    def __enter__(self) -> None:
        # start logging
        autogen.runtime_logging.start(logger=self.logger)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # stop logging
        autogen.runtime_logging.stop()
