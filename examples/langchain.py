import sys

# move the current working directory to the end position
sys.path = sys.path[1:] + sys.path[:1]
from langchain.chains import LLMChain  # noqa: E402
from langchain.llms import OpenAI  # noqa: E402
from langchain.prompts import PromptTemplate  # noqa: E402

from okareo.callbacks import CallbackHandler  # noqa: E402


def main() -> None:
    print("Running a LangChain example showcasing Okareo custom callback handler")
    handler = CallbackHandler()
    llm = OpenAI()
    prompt = PromptTemplate.from_template("1 + {number} = ")

    # Constructor callback: First, let's explicitly set the StdOutCallbackHandler when initializing our chain
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
    chain.run(number=2)
    chain.run(number=6)
    chain.run(number=12)

    print("Done")


if __name__ == "__main__":
    main()
