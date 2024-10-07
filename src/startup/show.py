import os
import logging

from aiohttp.web_routedef import static
from omegaconf import DictConfig
from tqdm import tqdm
import pandas as pd
from prettytable import PrettyTable
import asyncio

from src.startup.builder import RunBuilder
from src.utils import Logger
from src.tools.llm import CostManagers, LLMApi


log = logging.getLogger(__name__)


@RunBuilder.register_module("show")
class ShowRunner:
    def __init__(self, cfg: DictConfig):
        log.info("Initializing TmpRunner")
        self.cfg = cfg
        self.logger = Logger(cfg)
        self.base_path = "log/o1"

    def run(self):
        baseline_path = "1006_223438-seed0-direct-math"
        baseline = self.read_evaluate(os.path.join(self.base_path, baseline_path, "evaluate.csv"))
        baseline_right, baseline_wrong = self.static(baseline)
        qwq_paths = [
            "1006_230104-seed0-atomic-math",
            "1006_232419-seed0-atomic-math"
        ]
        for qwq_path in qwq_paths:
            self.compare(baseline_right, baseline_wrong, qwq_path)

    @staticmethod
    def read_evaluate(csv_path: str):
        eval_df = pd.read_csv(csv_path)
        id2acc = {}
        for i, row in eval_df.iterrows():
            if row["id"] == "mean":
                continue
            id2acc[int(float(row["id"]))] = int(row["acc"])
        return id2acc

    @staticmethod
    def static(id2acc: dict):
        right, wrong = [], []
        for id, acc in id2acc.items():
            if acc == 1:
                right.append(id)
            else:
                wrong.append(id)
        right.sort()
        wrong.sort()
        return right, wrong

    @staticmethod
    def _compare(baseline_right, baseline_wrong, qwq_right, qwq_wrong):
        table = PrettyTable()
        table.field_names = ["", "Baseline", "qwq"]
        table.add_row(["√", len(baseline_right), len(qwq_right)])
        table.add_row(["×", len(baseline_wrong), len(qwq_wrong)])
        log.info(f"num of √ or ×: \n{table}")

        table = PrettyTable()
        table.field_names = ["", "num", "id_list"]
        baseline_wrong_qwq_right = [id for id in baseline_wrong if id in qwq_right]
        baseline_wrong_qwq_right.sort()
        table.add_row(["baseline × qwq √", len(baseline_wrong_qwq_right), baseline_wrong_qwq_right])
        baseline_right_qwq_wrong = [id for id in baseline_right if id in qwq_wrong]
        baseline_right_qwq_wrong.sort()
        table.add_row(["baseline √ qwq ×", len(baseline_right_qwq_wrong), baseline_right_qwq_wrong])
        log.info(f"compare: \n{table}")

    def compare(self, baseline_right, baseline_wrong, qwq_path: str):
        qwq = self.read_evaluate(os.path.join(self.base_path, qwq_path, "evaluate.csv"))
        qwq_right, qwq_wrong = self.static(qwq)
        self._compare(baseline_right, baseline_wrong, qwq_right, qwq_wrong)