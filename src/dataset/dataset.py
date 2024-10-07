class Item:
    def __init__(self, id, question:str, golden_answers:list[str], metadata:dict):
        self.id = id
        self.question: str = question
        self.golden_answers: list[str] = golden_answers
        self.metadata: dict = metadata

    def __getattr__(self, attr_name):
        if attr_name in ['id','question','golden_answers','metadata']:
            return super().__getattribute__(attr_name)
        else:
            raise AttributeError(f"Attribute `{attr_name}` not found")


class Dataset:
    def __init__(self, name, data: list[Item]):
        self.name = name
        self.data: list[Item] = data

    @property
    def question(self):
        return [item.question for item in self.data]
    @property
    def golden_answers(self):
        return [item.golden_answers for item in self.data]
    @property
    def id(self):
        return [item.id for item in self.data]

    def get_batch_data(self, attr_name:str, batch_size: int):
        for i in range(0, len(self.data), batch_size):
            batch_items = self.data[i:i+batch_size]
            yield [item[attr_name] for item in batch_items]

    def __getattr__(self, attr_name):
        return [item.__getattr__(attr_name) for item in self.data]

    def __getitem__(self, index) -> Item:
        return self.data[index]

    def __len__(self):
        return len(self.data)
