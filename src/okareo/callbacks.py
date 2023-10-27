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
        self.okareo = Okareo(api_key or os.environ["API_KEY"])
        self.inputs: Dict[str, Any] = {}
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

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = ...,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        print(f"\n\n\033[1m> Entering new {class_name} chain...\033[0m")

        if not self.registered_model:
            self.registered_model = self.okareo.register_model(
                name=class_name, tags=["langchain"]
            )
        self.inputs = {
            "input": inputs,
            "kwargs": kwargs,
            "serialized": serialized,
        }

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        print("\n\033[1m> Finished chain.\033[0m")
        print("Output: ", outputs)

        assert self.registered_model
        self.registered_model.add_data_point(
            input_obj={"in-json": self.inputs},
            result_obj={
                "result-json": {
                    "outputs": outputs,
                    "kwargs": kwargs,
                }
            },
            context_token=self.context_token,
            tags=["langchain"],
        )

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain errors."""
        print("\n\033[1m> Chain error\033[0m")
        assert self.registered_model
        self.registered_model.add_data_point(
            input_obj={"in-json": self.inputs},
            result_obj={},
            context_token=self.context_token,
            tags=["langchain"],
            error_message=str(error),
        )

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> Any:
        """Run on arbitrary text."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
