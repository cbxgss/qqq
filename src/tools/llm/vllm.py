import os
import logging
import openai

from src.tools.llm.costmanager import CostManagers


log = logging.getLogger(__name__)


class vLLM:
    def __init__(self):
        self.client = openai.OpenAI(api_key="EMPTY", base_url="http://localhost:8003/v1")
        self.async_client = openai.AsyncOpenAI(api_key="EMPTY", base_url="http://localhost:8003/v1")
        self.cost_manager = CostManagers()

    def ask_message(self, messages: list[dict[str, str]], temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = self.client.chat.completions.create(
            messages=messages,
            model="vllm",
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, "vllm", cost_name)
        return content

    async def aask_message(self, messages: list[dict[str, str]], temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = await self.async_client.chat.completions.create(
            messages=messages,
            model="vllm",
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, "vllm", cost_name)
        return content
