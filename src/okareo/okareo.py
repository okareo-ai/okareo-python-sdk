import functools
from typing import Callable, List, Union

from typing_extensions import ParamSpec, TypeVar

from okareo_api_client.api_config import HTTPException
from okareo_api_client.models import GenerationList, ModelUnderTestSchema
from okareo_api_client.services.None_service import (
    get_generations_v0_generations_get,
    register_model_v0_register_model_post,
)

from .common import API_CONFIG
from .model_under_test import ModelUnderTest

T = TypeVar("T")
P = ParamSpec("P")


class Okareo:
    """A class for interacting with Okareo API"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_generations(self) -> Union[List[GenerationList], None]:
        """Get a list of generations"""
        data = get_generations_v0_generations_get(
            self.api_key, api_config_override=API_CONFIG
        )
        if isinstance(data, HTTPException):
            print(f"Unexpected {data=}, {type(data)=}")
            raise
        return data

    def register_model(
        self,
        name: str,
        tags: Union[List[str], None] = None,
        project_id: Union[int, None] = None,
    ) -> ModelUnderTest:
        if tags is None:
            tags = []
        data = {"name": name, "tags": tags}
        if project_id is not None:
            data["project_id"] = project_id  # type: ignore
        registered_model = register_model_v0_register_model_post(
            self.api_key,
            ModelUnderTestSchema.model_validate(data, strict=True),
            api_config_override=API_CONFIG,
        )
        return ModelUnderTest(self.api_key, registered_model)

    def instrument(self, tags: Union[List[str], None] = None) -> Callable:
        def decorator_instrument(func: Callable[P, T]) -> Callable[P, T]:
            @functools.wraps(func)
            def wrapper_instrument(*args: P.args, **kwargs: P.kwargs) -> T:
                # do something before
                result = func(*args, **kwargs)
                # add result data point
                mut = kwargs["model"]
                if not mut:
                    print(f"Model under test not provided {kwargs=}")
                    raise

                mut.add_data_point(  # type: ignore
                    kwargs["input"],
                    result,
                    kwargs["feedback"],
                    kwargs["context_token"],
                    tags=tags,
                )

                return result

            return wrapper_instrument

        return decorator_instrument
