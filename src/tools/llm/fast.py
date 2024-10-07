from typing import List
from openai.types.chat.chat_completion import ChatCompletion
import requests
import aiohttp

from src.tools.llm.costmanager import CostManagers


class LLMFastapi:
    def __init__(self):
        self.cost_manager = CostManagers()

    def ask_message(self, messages: List[dict], cost_name: str = "all"):
        response = requests.post("http://localhost:8003/ask_message/", json=messages, proxies=None)
        response = ChatCompletion(**response.json())
        content = response.choices[0].message.content
        self.cost_manager.update_cost(response.usage.prompt_tokens, response.usage.completion_tokens, "fastapi", cost_name)
        return content

    async def aask_message(self, messages: List[dict], cost_name: str = "all"):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8003/ask_message/", json=messages) as response:
                data = await response.json()
                response = ChatCompletion(**data)
                content = response.choices[0].message.content
                self.cost_manager.update_cost(response.usage.prompt_tokens, response.usage.completion_tokens, "fastapi", cost_name)
                return content
