from src.o1.direct import Direct
from src.o1.hitl.o1 import Hitl
from src.o1.atomic.o1 import Atomic


def get_method(name: str):
    if name == "direct":
        return Direct
    elif name == "hitl":
        return Hitl
    elif name == "atomic":
        return Atomic
    else:
        raise ValueError(f"Unknown method {name}")
