import random
import string
import sys

# move the current working directory to the end position
sys.path = sys.path[1:] + sys.path[:1]
from langchain.chains import LLMChain  # noqa: E402
from langchain.chains import SimpleSequentialChain  # noqa: E402
from langchain.llms import OpenAI  # noqa: E402
from langchain.prompts import PromptTemplate  # noqa: E402

from okareo.callbacks import CallbackHandler  # noqa: E402


def main() -> None:
    print("Running a LangChain example showcasing Okareo custom callback handler")
    print("\nLet's assume that all the below chains are part of the same context")
    print("and instantaite the handler with single context token")

    context_token = "".join(random.choices(string.ascii_letters, k=10))
    print("Context Token =", context_token)
    handler = CallbackHandler(mut_name="langchain_example", context_token=context_token)

    llm = OpenAI(temperature=0, callbacks=[handler])
    prompt_add = PromptTemplate.from_template("1 + {number} = ")
    prompt_mul = PromptTemplate.from_template("2 * {number} = ")

    chain_add = LLMChain(llm=llm, prompt=prompt_add, callbacks=[handler])
    chain_mul = LLMChain(llm=llm, prompt=prompt_mul, callbacks=[handler])

    print("Individual chain run")
    chain_add.run(number=2)

    print("Composite sequential chain run")
    seq_chain = SimpleSequentialChain(chains=[chain_add, chain_mul], verbose=True)
    seq_chain.run("3")

    output = llm.predict("how are you?", callbacks=[handler])
    print("LLM chain output", output)

    print("Done")


if __name__ == "__main__":
    main()
