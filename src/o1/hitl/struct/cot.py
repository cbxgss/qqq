class CoT:
    def __init__(self):
        self.memory_raw = []
        self.memory_summary = []

    def __add__(self, other: str):
        self.memory_raw.append(other)
        return self

    def __str__(self):
        chain = self.memory_summary + self.memory_raw[len(self.memory_summary):]
        return "None" if len(chain) == 0 else "\n\n".join(chain)

    def long_term_memory(self):
        return "None" if len(self.memory_summary) == 0 else "\n\n".join(self.memory_summary)

    def recent_memory(self):
        recent_cot = self.memory_raw[len(self.memory_summary):]
        return "None" if len(recent_cot) == 0 else "\n\n".join(recent_cot)

    def clear(self):
        self.memory_raw = []
        self.memory_summary = []
