from typing import Any, List, Optional

from litellm.integrations.custom_logger import CustomLogger  # type: ignore

from okareo import Okareo


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
        return kwargs["original_response"]


class LiteLLMLoggerOpenAI(LiteLLMLogger):
    def __init__(
        self,
        api_key: str,
        mut_name: str,
        context_token: str,
        tags: Optional[List[str]] = None,
        host_address: Optional[str] = None,
    ) -> None:
        super().__init__(
            api_key=api_key,
            mut_name=mut_name,
            context_token=context_token,
            tags=tags,
            host_address=host_address,
        )
