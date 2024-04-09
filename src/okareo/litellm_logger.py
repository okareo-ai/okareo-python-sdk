import os
from typing import Any, List, Optional

import dotenv
from litellm.integrations.custom_logger import CustomLogger  # type: ignore
from openai._models import BaseModel as OpenAIObject

from okareo import Okareo

dotenv.load_dotenv()


class LiteLLMLogger(CustomLogger):  # type: ignore
    def __init__(
        self,
        api_key: str,
        mut_name: str,
        context_token: str,
        tags: Optional[List[str]] = None,
        host_address: Optional[str] = None,
    ) -> None:
        if host_address and len(host_address) > 0:
            self.okareo = Okareo(api_key, base_path=host_address)
        else:
            self.okareo = Okareo(api_key)

        self.context_token = context_token
        self.registered_model = self.okareo.register_model(name=mut_name, tags=tags)

    def log_success_event(
        self, kwargs: Any, response_obj: Any, start_time: Any, end_time: Any
    ) -> None:
        self.registered_model.add_data_point_async(
            input_obj=self.parse_input_obj(kwargs),
            input_datetime=str(start_time),
            result_obj=self.parse_response_obj(kwargs, response_obj),
            result_datetime=str(end_time),
            context_token=self.context_token,
        )

    async def async_log_success_event(
        self, kwargs: Any, response_obj: Any, start_time: Any, end_time: Any
    ) -> None:
        self.registered_model.add_data_point_async(
            input_obj=self.parse_input_obj(kwargs),
            input_datetime=str(start_time),
            result_obj=self.parse_response_obj(kwargs, response_obj),
            result_datetime=str(end_time),
            context_token=self.context_token,
        )

    def parse_input_obj(self, kwargs: Any) -> dict:
        input_data = {}
        for idx, value in enumerate(kwargs["messages"]):
            input_data[str(idx)] = value
        return {"input": input_data}

    def parse_response_obj(self, kwargs: Any, response_obj: Any) -> Any:
        try:
            if isinstance(response_obj, OpenAIObject):
                formatted_response = dict(response_obj.model_dump())
            else:
                formatted_response = {"raw_response": response_obj}
        except Exception as e:
            formatted_response = {"exception": str(e), "raw_response": response_obj}

        return formatted_response


class LiteLLMProxyLogger(LiteLLMLogger):
    def __init__(
        self,
        api_key: Optional[str] = None,
        mut_name: Optional[str] = None,
        context_token: Optional[str] = None,
        tags: Optional[List[str]] = None,
        host_address: Optional[str] = None,
    ) -> None:
        if not api_key:
            api_key = os.getenv("OKAREO_API_KEY", "")
        if not mut_name:
            mut_name = os.getenv("OKAREO_MUT_NAME", "")
        if not tags:
            tags_str = os.getenv("OKAREO_MUT_TAGS", "")
            if tags_str and len(tags_str) > 0:
                tags = tags_str.split(",")
        if not context_token:
            context_token = os.getenv("OKAREO_CONTEXT_TOKEN", "")

        super().__init__(
            api_key=api_key,
            mut_name=mut_name,
            context_token=context_token,
            tags=tags,
            host_address=host_address,
        )


litellm_proxy_handler = LiteLLMProxyLogger(mut_name="litellm_proxy_handler")
