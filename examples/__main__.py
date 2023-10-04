import os

from okareo import Okareo

API_KEY = os.environ["API_KEY"]


def main() -> None:
    okareo = Okareo(API_KEY)
    print("Generations: ", okareo.get_generations())


if __name__ == "__main__":
    main()
