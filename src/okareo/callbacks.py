import logging
import os
import random
import string
from typing import Any, Dict, List, Optional
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult

from okareo.okareo import Okareo


class CallbackHandler(BaseCallbackHandler):
    """
    Base callback handler that can be used to handle callbacks
    from langchain.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        mut_name: Optional[str] = None,
        context_token: Optional[str] = None,
    ) -> None:
        """Initialize callback handler."""
        self.okareo = Okareo(api_key or os.environ["OKAREO_API_KEY"])
        self.inputs: List[Dict[str, Any]] = []
        self.context_token = context_token or "".join(
            random.choices(string.ascii_letters, k=10)
        )
        self.registered_model = None
        if mut_name:
            self.registered_model = self.okareo.register_model(
                name=mut_name, tags=["langchain"]
            )

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        logging.debug("on_llm_start", serialized, prompts, kwargs)
        self.inputs.append(
            {
                "prompts": prompts,
                "invocation_params": kwargs["invocation_params"],
            }
        )

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        logging.debug("on_llm_new_token", token, kwargs)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        logging.debug("on_llm_end", response, kwargs)
        model = self.registered_model
        if not model:
            model_name = (
                response.llm_output.get("model_name", "<unknown>")
                if response.llm_output
                else "<unknown>"
            )
            model = self.okareo.register_model(name=model_name, tags=["langchain"])
        model.add_data_point(
            input_obj=self.inputs.pop(),
            result_obj={
                "outputs": response.generations,
                "llm_output": response.llm_output,
            },
            context_token=self.context_token,
            tags=["langchain"],
        )

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        logging.debug("on_chain_start", serialized, inputs, kwargs)
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])

        if not self.registered_model:
            self.registered_model = self.okareo.register_model(
                name=class_name, tags=["langchain"]
            )
        self.inputs.append(
            {
                "template": serialized.get("kwargs", {})
                .get("prompt", {})
                .get("kwargs", {})
                .get("template", ""),
                "input": inputs,
                "tags": kwargs.get("tags", []),
            }
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        logging.debug("on_chain_end", outputs, kwargs)

        assert self.registered_model
        self.registered_model.add_data_point(
            input_obj=self.inputs.pop(),
            result_obj={
                "outputs": outputs,
                "tags": kwargs.get("tags", []),
            },
            context_token=self.context_token,
            tags=["langchain"],
        )

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain errors."""
        print("\n\033[1m> Chain error\033[0m")
        assert self.registered_model
        self.registered_model.add_data_point(
            input_obj=self.inputs.pop(),
            result_obj={},
            context_token=self.context_token,
            tags=["langchain"],
            error_message=str(error),
        )

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        logging.debug("on_tool_start", serialized, input_str, kwargs)

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        logging.debug("on_tool_end", output, kwargs)

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        logging.debug("on_agent_action", action, kwargs)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        logging.debug("on_agent_action", finish, kwargs)
