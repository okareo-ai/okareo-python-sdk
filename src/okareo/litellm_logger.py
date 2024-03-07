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
            input_obj={"input": kwargs["messages"]},
            input_datetime=str(start_time),
            result_obj={"result": response_obj},
            result_datetime=str(end_time),
            context_token=self.context_token,
        )
