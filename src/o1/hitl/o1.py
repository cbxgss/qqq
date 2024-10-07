from omegaconf import DictConfig
import logging
import re

from src.utils.logger import Logger
from src.tools.llm import CostManagers
from src.o1.hitl.struct import CoT
from src.o1.hitl.agent import Agent, ID2NAME, system, user, user_guidance, answer_system, answer_user


log = logging.getLogger(__name__)


class Hitl:
    def __init__(self, cfg: DictConfig, logger: Logger):
        self.cfg = cfg
        self.logger = logger
        self.infers: dict = {
            k: Agent(cfg, logger, v, system(v), user) for k, v in ID2NAME.items()
        }
        self.infer = Agent(cfg, logger, name="infer", system=system("infer"), user=user_guidance)
        self.answer = Agent(cfg, logger, "answer", answer_system, answer_user)

    async def aanswer(self, id, question: str):
        log.info(f"question: \n{question}")
        cot = CoT()
        trace = {}
        for step in range(1, self.cfg.method.max_step):
            guidance = self.get_guidance()
            if "-1" in guidance:
                break
            action = re.findall(r"-?\d+", guidance)
            if len(action) > 0:
                action = int(action[0])
                rsp = await self.infers[action].arun(id,
                                                     question=question,
                                                     reason_memory=cot.recent_memory()
                )
            else:
                rsp = await self.infer.arun(id,
                                        question=question,
                                        reason_memory=cot.recent_memory(),
                                        guidance=guidance
                )
            CostManagers().show_cost()
            log.info(f"\n{rsp}")
            save = input("y: 保存当前推理, else: 重新进行当前step推理: ")
            if save == "y":
                trace[step] = {
                    "guidance": guidance,
                    "inference": rsp
                }
                cot += rsp
                self.logger.save_md(f"output/{id}.md", str(cot))
            else:
                self.infers: dict = {
                    k: Agent(self.cfg, self.logger, v, system(v), user) for k, v in ID2NAME.items()
                }
        rsp = await self.answer.arun(id, question=question, inference=cot)
        cot += rsp
        self.logger.save_md(f"output/{id}.md", str(cot))
        cot.clear()
        return rsp, trace

    @staticmethod
    def get_guidance():
        print(ID2NAME)
        return input("输入 guidance, -1 表示结束推理: int 表示走对应的原子推理: ")

    def summary(self, cot: CoT, summary_li: list[str]):
        cot.memory_summary += summary_li
        self.logger.save_md("summary.md", cot.long_term_memory())
        return cot.long_term_memory()
