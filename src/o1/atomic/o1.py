from omegaconf import DictConfig
import logging

from src.utils.logger import Logger
from src.o1.atomic.struct import CoT
from src.o1.atomic.agent import Agent, system, route_user, user, answer_system, answer_user, ID2NAME, NAME2ID

log = logging.getLogger(__name__)


class Atomic:
    def __init__(self, cfg: DictConfig, logger: Logger):
        self.cfg = cfg
        self.logger = logger
        self.infers: dict = {
            k: Agent(cfg, logger, v, system(v), user) for k, v in ID2NAME.items()
        }
        self.router = Agent(cfg, logger, "router", system("route"), route_user, out_json=True)
        self.answer = Agent(cfg, logger, "answer", answer_system, answer_user)

    async def aanswer(self, id, question: str):
        cot = CoT()
        trace = {}
        for step in range(1, self.cfg.method.max_step):
            # router
            router = await self.router.arun(id, question=question, reason_memory=cot.recent_memory())
            guide, action = router["guide"], router["route"]
            trace[step] = {
                "router": {
                    "guide": guide,
                    "action": action
                }
            }
            if "None" in action:
                break
            action = NAME2ID[action]
            # atomic reasoning step
            rsp = await self.infers[action].arun(id,
                                                 question=question,
                                                 reason_memory=cot.recent_memory(),
                                                 guidance=guide
            )
            cot += rsp
            self.logger.save_md(f"output/{id}.md", str(cot))
        rsp = await self.answer.arun(id, question=question, inference=cot)
        cot += rsp
        self.logger.save_md(f"output/{id}.md", str(cot))
        return rsp, trace
