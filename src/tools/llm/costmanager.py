from typing import NamedTuple
import logging
from prettytable import PrettyTable

from src.utils import Singleton


log = logging.getLogger(__name__)


# $x / 1M tokens
TOKEN_COSTS = {
    "fastapi": {"prompt": 0.0, "completion": 0.0},
    "vllm": {"prompt": 0.0, "completion": 0.0},
    "ollama": {"prompt": 0.0, "completion": 0.0},
    "gpt-3.5-turbo-instruct": {"prompt": 1.5, "completion": 2.0},
    "gpt-4-turbo": {"prompt": 10.0, "completion": 30.0},
    "gpt-4": {"prompt": 30.0, "completion": 60.0},
    "gpt-4-32k": {"prompt": 60.0, "completion": 120.0},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.6},
    "gpt-4o": {"prompt": 5.0, "completion": 15.0},
    "text-embedding-ada-002": {"prompt": 0.4, "completion": 0.0},
}


class Costs(NamedTuple):
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    total_budget: float


class CostManager:
    """计算使用接口的开销"""
    def __init__(self, name: str):
        self.name = name
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0

    def update_cost(self, prompt_tokens, completion_tokens, model):
        """
        Update the total cost, prompt tokens, and completion tokens.

        Args:
        prompt_tokens (int): The number of tokens used in the prompt.
        completion_tokens (int): The number of tokens used in the completion.
        model (str): The model used for the API call.
        """
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        cost = (
                       prompt_tokens * TOKEN_COSTS[model]["prompt"]
                       + completion_tokens * TOKEN_COSTS[model]["completion"]
               ) / 1000 / 1000
        self.total_cost += cost
        # log.info(
        #     f"{self.name} cost | "
        #     f"Total cost: ${self.total_cost:.3f} | "
        #     f"Current cost: ${cost:.3f}"
        # )
        # log.info(
        #     f"{self.name} tokens | "
        #     f"Total tokens: prompt: {self.total_prompt_tokens}, completion: {self.total_completion_tokens} | "
        #     f"Current tokens: prompt: {prompt_tokens}, completion: {completion_tokens}"
        # )

        return self.total_completion_tokens

    def get_costs(self) -> Costs:
        """Get all costs"""
        return Costs(
            self.total_prompt_tokens,
            self.total_completion_tokens,
            self.total_cost,
            self.total_budget,
        )


class CostManagers(metaclass=Singleton):
    def __init__(self):
        self.cost_managers: dict[str, CostManager] = {}

    def manager(self, name: str) -> CostManager:
        if name not in self.cost_managers:
            self.cost_managers[name] = CostManager(name)
        return self.cost_managers[name]

    def update_cost(self, prompt_tokens, completion_tokens, model, name: str = "all"):
        self.manager("all").update_cost(prompt_tokens, completion_tokens, model)
        if name != "all":
            self.manager(name).update_cost(prompt_tokens, completion_tokens, model)

    def show_cost(self):
        table = PrettyTable()
        table.field_names = ["Name", "prompt tokens", "completion tokens", "cost"]
        for name, cost_manager in self.cost_managers.items():
            cost = cost_manager.get_costs()
            table.add_row([name, cost.total_prompt_tokens, cost.total_completion_tokens, cost.total_cost])
        log.info(f"cost table:\n{table}")
