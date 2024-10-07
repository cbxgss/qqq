from src.o1.hitl.agent.base import Agent
from src.o1.hitl.agent.infer import ID2NAME, NAME2ID
from src.o1.hitl.agent.answer import answer_system, answer_user


user_guidance = """## Question:
{question}

## Reasoning Memory:
{reason_memory}

## Human Guidance:
{guidance}
"""

user = """## Question:
{question}

## Reasoning Memory:
{reason_memory}
"""

infer_system = """## Background Knowledge and Role Introduction

You are solving a complicated problem. This problem is very complicated, so don't try to solve it in one step.

Now, what you should do in this step is as follows:

## Input

The input for this step includes:

- Question: The question you need to answer.
- Reasoning Memory: The reasoning steps you have taken so far.
- Human Guidance: The guidance provided by the human.

Now, you need to reason based on the input and provide the output.

Don't output any other information in this step. Only focus on organizing the information from the question into a structured markdown format.
"""


def system(name: str) -> str:
    base_path = "src/o1/atomic/agent"
    if name == "infer":
        return infer_system
    if name in NAME2ID:
        with open(f"{base_path}/infer/{name}.md", 'r') as file:
            return file.read()
    else:
        raise ValueError(f"Invalid name: {name}")
