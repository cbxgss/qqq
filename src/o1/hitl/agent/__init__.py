from src.o1.hitl.agent.base import Agent
from src.o1.hitl.agent.infer import ID2STEP
from src.o1.hitl.agent.answer import answer_system, answer_user


user = """## Question:
{question}

## Reasoning Memory:
{reason_memory}

## Human Guidance:
{guidance}
"""


def system(name: str) -> str:
    base_path = "src/o1/hitl/agent"
    if name in ["route", "summary"]:
        with open(f"{base_path}/{name}.md", 'r') as file:
            return file.read()
    elif name in ID2STEP:
        with open(f"{base_path}/infer/{ID2STEP[name][0]}.md", 'r') as file:
            return file.read()
    else:
        raise ValueError(f"Invalid name: {name}")
