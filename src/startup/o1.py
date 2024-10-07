import logging
from omegaconf import DictConfig
from tqdm import tqdm
import pandas as pd
import asyncio

from src.startup.builder import RunBuilder
from src.utils import Logger
from src.tools.llm.costmanager import CostManagers
from src.dataset import get_dataset, Item
from src.o1 import get_method
from src.evaluate import allm_evaluate


log = logging.getLogger(__name__)


@RunBuilder.register_module("o1")
class O1Runner:
    def __init__(self, cfg: DictConfig):
        log.info("Initializing O1Runner")
        self.cfg = cfg
        self.logger = Logger(cfg)
        self.logger.mkdir("output")
        self.method = get_method(cfg.method.name)(cfg, self.logger)
        self.dataset = get_dataset(cfg.dataset.name)

    def run(self):
        asyncio.run(self.aprocess_all())

    async def aprocess_all(self):
        data = self.dataset[self.cfg.dataset.case]
        self.logger.mkdir(f"llm/{data.id}")
        response, trace = await self.method.aanswer(data.id, data.question)
        out = {
            "id": data.id,
            "question": data.question,
            "response": response,
            "golden_answers": data.golden_answers,
            "trace": trace,
        }
        self.logger.save_json(f"output/{data.id}.json", out)
