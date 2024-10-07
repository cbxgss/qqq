import logging
from omegaconf import DictConfig
from tqdm import tqdm
import pandas as pd
import asyncio

from src.startup.builder import RunBuilder
from src.utils import Logger
from src.tools.llm.costmanager import CostManagers
from src.dataset import get_dataset, Item
from src.o1 import Direct, get_method
from src.evaluate import allm_score, allm_evaluate


log = logging.getLogger(__name__)


@RunBuilder.register_module("benchmark")
class BenchmarkRunner:
    def __init__(self, cfg: DictConfig):
        log.info("Initializing BenchmarkRunner")
        self.cfg = cfg
        self.logger = Logger(cfg)
        self.logger.mkdir("output")
        self.method: Direct = get_method(cfg.method.name)(cfg, self.logger)
        self.dataset = get_dataset(cfg.dataset.name)
        self.evaluate_df = pd.DataFrame(columns=["id", "acc"])

    def run(self):
        asyncio.run(self.aprocess_all())

    async def arun_one(self, data: Item):
        log_dir = f"llm/{data.id}"
        self.logger.mkdir(log_dir)
        response, trace = await self.method.aanswer(data.id, data.question)
        acc = await allm_evaluate(data.question, response, data.golden_answers, self.cfg.llm, log_dir)
        self.evaluate_df.loc[len(self.evaluate_df)] = [data.id, acc]
        out = {
            "id": data.id,
            "question": data.question,
            "acc": acc,
            "response": response,
            "golden_answers": data.golden_answers,
            "trace": trace,
        }
        self.logger.save_json(f"output/{data.id}.json", out)

    async def arun_batch(self, data_batch: list[Item]):
        tasks = [self.arun_one(data) for data in data_batch]
        await asyncio.gather(*tasks)
        cost_manager = CostManagers()
        cost_manager.show_cost()
        log.info(self.evaluate_mean())

    async def aprocess_all(self):
        bs = self.cfg.batch_size
        with tqdm(range(0, len(self.dataset), bs), desc=f"batch_size: {bs}") as tbar:
            for data_i in tbar:
                if data_i > 100: continue
                batch_l, batch_r = data_i, min(data_i + bs, len(self.dataset))
                tbar.set_postfix_str(f"batch: [{batch_l}, {batch_r})")
                data_batch = self.dataset[batch_l:batch_r]
                await self.arun_batch(data_batch)
        self.evaluate_df = self.evaluate_df.sort_values(by="id")
        self.evaluate_df.loc[len(self.evaluate_df)] = self.evaluate_mean()
        self.logger.save_csv("evaluate.csv", self.evaluate_df)

    def evaluate_mean(self):
        return ['mean'] + self.evaluate_df[["acc"]].mean().tolist()
