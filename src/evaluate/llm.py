import asyncio
from tqdm import tqdm

from src.tools.llm import LLMApi


# Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy
# https://aclanthology.org/2023.findings-emnlp.620
system_prompt = """In the following task, you are given a Question, a model Prediction for the Question, and a Ground-truth Answer to the Question. You should decide whether the model Prediction implies the Ground-truth Answer.
"""

user_prompt = """Question:
{question}

Prediction:
{response}

Ground-truth Answer
{golden_answer}

Does the Prediction imply the Ground-truth Answer? Output Yes or No:
"""


async def allm_score(question: str, response: str, golden_answer: str, llm: str, path):
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt.format(question=question, response=response, golden_answer=golden_answer)}
    ]
    while True:
        llm_e = await LLMApi().aask_message(message, llm, 0.0, "evaluate", path)
        if "Yes" in llm_e:
            return 1.0
        elif "No" in llm_e:
            return 0.0


async def allm_evaluate(question: str, response: str, golden_answers: list[str], llm, path):
    task = [allm_score(question, response, golden_answer, llm, path) for golden_answer in golden_answers]
    scores = await asyncio.gather(*task)
    return max(scores)
