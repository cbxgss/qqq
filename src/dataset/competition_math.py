import os
import json

from src.dataset.dataset import Dataset, Item


def get_math():
    base_path = "download/data/hendrycks/competition_math/data/MATH"
    splits = ["train", "test"]
    categories = ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory", "prealgebra", "precalculus"]
    split, category = splits[1], categories[0]

    path = f"{base_path}/{split}/{category}"
    # 列举path 下所有json文件
    json_files = [f for f in os.listdir(path) if f.endswith('.json')]
    data: list[Item] = []
    for file in json_files:
        with open(f"{path}/{file}", 'r') as f:
            item = json.load(f)
            question, golden_answers = item['problem'], [item['solution']]
            metadata = {"level": item['level'], "type": item['type']}
            data.append(Item(id=len(data), question=question, golden_answers=golden_answers, metadata=metadata))
    dataset = Dataset(name=f"math-{split}-{category}", data=data)
    return dataset
