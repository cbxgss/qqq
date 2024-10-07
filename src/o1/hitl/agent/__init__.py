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


def system(name: str) -> str:
    base_path = "src/o1/hitl/agent"
    if name == "infer" or name in NAME2ID:
        with open(f"{base_path}/infer/{name}.md", 'r') as file:
            return file.read()
    else:
        raise ValueError(f"Invalid name: {name}")
