import logging
from omegaconf import DictConfig
import re, json

from src.utils.logger import Logger
from src.tools.llm import LLMApi


log = logging.getLogger(__name__)


class Agent:
    def __init__(self, cfg: DictConfig, logger: Logger, name: str, system: str, user: str, out_json: bool = False):
        self.cfg = cfg
        self.logger = logger
        self.name = name
        self.system = system
        self.user = user
        self.out_json = out_json

    async def arun(self, id, **placeholder):
        messages = self.get_messages(**placeholder)
        if self.out_json:
            rsp = await self.agenerate_json(messages, self.cfg.llm, 0.0, self.name, f"llm/{id}")
        else:
            rsp = await self.agenerate(messages, self.cfg.llm, 0.0, self.name, f"llm/{id}")
        return rsp

    def fill_user_prompt(self, **kwargs):
        return self.user.format(**kwargs)

    def get_messages(self, **kwargs):
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.fill_user_prompt(**kwargs)},
        ]

    async def agenerate(self, message: list[dict[str, str]], llm: str, temperature: float, cost_name: str, path) -> str:
        return await LLMApi().aask_message(message, llm, temperature, cost_name, path)

    async def agenerate_json(self, message: list[dict[str, str]], llm: str, temperature: float, cost_name: str, path) -> dict:
        while True:
            out = await self.agenerate(message, llm, temperature, cost_name, path)
            try:
                out = re.search(r"```json\n(.*)\n```", out, re.DOTALL).group(1)
                out = out.replace("\\", "")
                out_json = json.loads(out)
                return out_json
            except Exception as e:
                log.error(f"json error: {e} when decode {out}")
