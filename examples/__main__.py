import os

from okareo import Okareo

API_KEY = os.environ["API_KEY"]


def main() -> None:
    okareo = Okareo(API_KEY)
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


if __name__ == "__main__":
    main()
