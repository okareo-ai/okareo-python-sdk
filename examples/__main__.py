import os
import time

from okareo import Okareo
from okareo.model_under_test import ModelUnderTest

API_KEY = os.environ["API_KEY"]
okareo = Okareo(API_KEY)


def main() -> None:
    print("Generations: ", okareo.get_generations())
    registered_model = okareo.register_model(
        name="Example Model", tags=["testing", "example"]
    )

    registered_model.add_data_point(
        input_obj={"in-json": "input data"},
        result_obj={"result-json": "result data"},
        feedback=1,
        context_token="token-123",
        tags=["a", "b", "c"],
    )

    input_ = "model input"
    print("running context wrapper example")
    with registered_model.instrument(
        input_obj={"in-json": input_},
        feedback=1,
        context_token="token-123",
        tags=["a", "b", "c"],
    ) as data_point:
        print("Run inference inside context wrapper")
        result = simulate_inference(input_)
        data_point.set_result_obj(result)

    print("running decorated function example")
    decorated_simulate_inference(
        model=registered_model,
        feedback=1,
        context_token="token-123",
        input_={"in-json": input_},
    )


def simulate_inference(input_: str) -> dict:
    print("Starting ML task simulation...")
    time.sleep(4)
    print("[COMPLETE] ML task simulation")
    return {"result": "example-result"}


@okareo.instrument(tags=["a", "b", "c"])
def decorated_simulate_inference(
    input_: dict, model: ModelUnderTest, feedback: int, context_token: str
) -> dict:
    print("Starting decorated ML task simulation...")
    time.sleep(4)
    print("[COMPLETE] decorated ML task simulation")
    return {"result": "example-result"}


if __name__ == "__main__":
    main()
