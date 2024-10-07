from src.o1.atomic.agent.base import Agent
from src.o1.atomic.agent.infer import ID2NAME, NAME2ID
from src.o1.atomic.agent.answer import answer_system, answer_user


user = """## Question:
{question}

## Reasoning Memory:
{reason_memory}

## Guidance:
{guidance}
"""


route_user = """## Question:
{question}

## Reasoning Memory:
{reason_memory}
"""


def system(name: str) -> str:
    base_path = "src/o1/atomic/agent"
    if name == "route":
        with open(f"{base_path}/{name}.md", 'r') as file:
            content = file.read()
            reasoning_types = ", ".join([f"{k}" for k in NAME2ID.keys()])
            return content.replace("{{reasoning_types}}", reasoning_types)
    elif name in NAME2ID:
        with open(f"{base_path}/infer/{name}.md", 'r') as file:
            return file.read()
    else:
        raise ValueError(f"Invalid name: {name}")
