from omegaconf import DictConfig
import logging

from src.utils.logger import Logger
from src.tools.llm import LLMApi


log = logging.getLogger(__name__)


class Direct:
    def __init__(self, cfg: DictConfig, logger: Logger):
        self.cfg = cfg
        self.logger = logger

    async def aanswer(self, id, question: str):
        trace = {}
        messages = [
            {"role": "system", "content": """Your task is to solve the following math problem step by step.
"""},
            {"role": "user", "content": question},
        ]
        rsp = await LLMApi().aask_message(messages, self.cfg.llm, 0.0, "generate", f"llm/{id}")
        self.logger.save_md(f"output/{id}.md", rsp)
        return rsp, trace
