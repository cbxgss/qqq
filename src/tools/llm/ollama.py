import os
import logging
import openai

from src.tools.llm.costmanager import CostManagers


log = logging.getLogger(__name__)


class Ollama:
    def __init__(self):
        self.client = openai.OpenAI(api_key="ollama", base_url="http://172.28.102.11:11434/v1")
        self.async_client = openai.AsyncOpenAI(api_key="ollama", base_url="http://172.28.102.11:11434/v1")
        self.cost_manager = CostManagers()

    def ask_message(self, messages: list[dict[str, str]], temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = self.client.chat.completions.create(
            messages=messages,
            model="qwen2.5",
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, "ollama", cost_name)
        return content

    async def aask_message(self, messages: list[dict[str, str]], temperature: float = 0.0, cost_name: str = "all") -> str:
        rsp = await self.async_client.chat.completions.create(
            messages=messages,
            model="qwen2.5",
            temperature=temperature,
        )
        content = rsp.choices[0].message.content
        self.cost_manager.update_cost(rsp.usage.prompt_tokens, rsp.usage.completion_tokens, "ollama", cost_name)
        return content
