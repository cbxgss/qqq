import datasets

from src.dataset.dataset import Dataset, Item


def get_gsm8k():
    gsm8k = datasets.load_dataset("openai/gsm8k", "main", cache_dir='download/data')
    gsm8k_test = gsm8k['test']
    data: list[Item] = []
    for i, item in enumerate(gsm8k_test):
        question, golden_answers = item['question'], [item['answer']]
        data.append(Item(id=i, question=question, golden_answers=golden_answers, metadata={}))
    dataset = Dataset(name="gsm8k", data=data)
    return dataset
