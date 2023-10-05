import os

from okareo import Okareo

API_KEY = os.environ["API_KEY"]


def main() -> None:
    okareo = Okareo(API_KEY)
    print("Generations: ", okareo.get_generations())
    okareo.add_data_point(
        input_={"in-json": "input data"},
        result={"result-json": "result data"},
        feedback=1,
        context_token="token-123",
        tags=["a", "b", "c"],
    )


if __name__ == "__main__":
    main()
