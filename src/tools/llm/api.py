import logging

from src.utils.singleton import Singleton
from src.utils.logger import Logger
from src.tools.llm.OpenAI import LLMOpenAI, OPENAI_MODELS
from src.tools.llm.fast import LLMFastapi
from src.tools.llm.vllm import vLLM
from src.tools.llm.ollama import Ollama


log = logging.getLogger(__name__)


class LLMApi(metaclass=Singleton):
    def __init__(self):
        self.openai = LLMOpenAI()
        self.fastapi = LLMFastapi()
        self.vllm = vLLM()
        self.ollama = Ollama()
        self.llm2api = {
            "openai": self.openai,
            "fastapi": self.fastapi,
            "vllm": self.vllm,
            "ollama": self.ollama,
        }
        self.cnt = 0
        self.logger = Logger()

    async def aask_message(self, messages: list[dict[str, str]], llm: str, temperature: float, cost_name: str, path) -> str:
        cnt = self.cnt
        self.cnt += 1
        self.logger.save_message(f"{path}/{cnt}_message.md", messages)
        if llm in OPENAI_MODELS:
            rsp = await self.openai.aask_message(messages, llm, temperature, cost_name)
        elif llm == "fastapi":
            rsp = await self.fastapi.aask_message(messages, cost_name)
        elif llm == "vllm":
            rsp = await self.vllm.aask_message(messages, temperature, cost_name)
        elif llm == "ollama":
            rsp = await self.ollama.aask_message(messages, temperature, cost_name)
        else:
            raise ValueError(f"Unknown llm: {llm}")
        self.logger.save_md(f"{path}/{cnt}_response.md", rsp)
        return rsp
