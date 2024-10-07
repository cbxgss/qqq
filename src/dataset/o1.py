from src.dataset.dataset import Dataset, Item


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# https://openai.com/index/learning-to-reason-with-llms/
def get_o1case():
    base_path = "src/dataset/o1"
    data = [
        Item(id=i, question=read_file(f"{base_path}/{i}.md"), golden_answers=["https://openai.com/index/learning-to-reason-with-llms/"], metadata={})
        for i in range(8)
    ]
    dataset = Dataset(name="o1case", data=data)
    return dataset
