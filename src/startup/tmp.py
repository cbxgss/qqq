system = """Your task is to extract valuable insights from the question context.

## Input

- question: the question context you need to extract insights from.

## Guide

You should follow the steps below to complete the task:

1. List all the known conditions in the original question one by one, ensuring that all relevant conditions are systematically covered, and no sentence or segment is missed.
    - premise 1: ...
    - premise 2: ...
    ...
2. Then analyze them together, try to explore the relationship between them, and obtain some valuable insight.
    - Your extracted insight must be clear and specific, not overly simple conclusions or vague directions.
        - insight 1: ...
        - insight 2: ...
        ...
"""

user = """Question: 
{question}
"""


import os
import logging
from omegaconf import DictConfig
from tqdm import tqdm
import pandas as pd
from prettytable import PrettyTable
import asyncio

from src.startup.builder import RunBuilder
from src.utils import Logger
from src.tools.llm import CostManagers, LLMApi


log = logging.getLogger(__name__)


@RunBuilder.register_module("tmp")
class TmpRunner:
    def __init__(self, cfg: DictConfig):
        log.info("Initializing TmpRunner")
        self.cfg = cfg
        self.logger = Logger(cfg)
        self.logger.mkdir("output")
        self.logger.mkdir("llm")
        self.dataset = [
            {
                "id": 0,
                "input": """original message: oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz
decoded message: THERE ARE THREE RS IN STRAWBERRY

Use the example above to decode:

original message: oyfjdnisdr rtqwainr acxz mynzbhhx
""",
                "target": "Think step by step",
            }
        ]

    def run(self):
        asyncio.run(self.aprocess_all())

    async def aprocess_all(self):
        message = [
            {"role": "system", "content": system},
            {"role": "user", "content": user.format(question=self.dataset[0]["input"])},
        ]
        rsp = await LLMApi().aask_message(message, self.cfg.llm, "all", "llm")
        log.info(rsp)
        self.logger.save_md("output/tmp.md", rsp)
