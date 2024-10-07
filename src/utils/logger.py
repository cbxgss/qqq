import os
import pandas as pd
import json
from omegaconf import DictConfig

from src.utils.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg

    def mkdir(self, path: str):
        path = os.path.join(self.cfg.log_config.base_log_dir, path)
        os.makedirs(path, exist_ok=True)

    def save_csv(self, file_path: str, csv: pd.DataFrame):
        csv_path = os.path.join(self.cfg.log_config.base_log_dir, file_path)
        csv.to_csv(csv_path, index=False)

    def save_json(self, file_path: str, json_data: dict):
        json_path = os.path.join(self.cfg.log_config.base_log_dir, file_path)
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    def save_md(self, file_path: str, content: str):
        md_path = os.path.join(self.cfg.log_config.base_log_dir, file_path)
        with open(md_path, "w") as f:
            f.write(content)

    def save_message(self, file_path: str, message: list[dict[str, str]]):
        md_content = ""
        for m in message:
            role, content = m["role"], m["content"]
            md_content += f"# role: {role}\n"
            md_content += f"{content}\n"
        self.save_md(file_path, md_content)
