import os
import logging
import openai

from src.tools.llm.costmanager import CostManagers


log = logging.getLogger(__name__)


OPENAI_MODELS = [
    "gpt-3.5-turbo-instruct",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4o-mini",
    "gpt-4o",
    "text-embedding-ada-002",
]


class LLMOpenAI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))
        self.async_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))
        self.cost_manager = CostManagers()

    def ask_message(self, messages: list[dict[str, str]], model: str, temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = self.client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, model, cost_name)
        return content

    async def aask_message(self, messages: list[dict[str, str]], model: str, temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = await self.async_client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, model, cost_name)
        return content
