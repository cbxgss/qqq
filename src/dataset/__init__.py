from src.dataset.dataset import Dataset, Item


def get_dataset(name: str) -> Dataset:
    if name == "dyck_languages":
        from src.dataset.dyck_languages import get_dyck_languages
        return get_dyck_languages()
    elif name == "geometric_shapes":
        from src.dataset.geometric_shapes import get_geometric_shapes
        return get_geometric_shapes()
    elif name == "movie_recommendation":
        from src.dataset.movie_recommendation import get_movie_recommendation
        return get_movie_recommendation()
    elif name == "causal_judgement":
        from src.dataset.causal_judgement import get_causal_judgement
        return get_causal_judgement()
    elif name == "gsm8k":
        from src.dataset.gsm8k import get_gsm8k
        return get_gsm8k()
    elif name == "math":
        from src.dataset.competition_math import get_math
        return get_math()
    elif name == "o1case":
        from src.dataset.o1 import get_o1case
        return get_o1case()
    else:
        raise ValueError(f"Unknown dataset {name}")


def get_instruct(name: str) -> str:
    if name == "dyck_languages":
        from src.dataset.dyck_languages import instruct
        return instruct
    elif name == "geometric_shapes":
        from src.dataset.geometric_shapes import instruct
        return instruct
    elif name == "movie_recommendation":
        from src.dataset.movie_recommendation import instruct
        return instruct
    elif name == "causal_judgement":
        from src.dataset.causal_judgement import instruct
        return instruct
    else:
        raise ValueError(f"Unknown dataset {name}")


def get_few_shot(name: str) -> list:
    if name == "dyck_languages":
        from src.dataset.dyck_languages import few_shot
        return few_shot
    elif name == "geometric_shapes":
        from src.dataset.geometric_shapes import few_shot
        return few_shot
    elif name == "movie_recommendation":
        from src.dataset.movie_recommendation import few_shot
        return few_shot
    elif name == "causal_judgement":
        from src.dataset.causal_judgement import few_shot
        return few_shot
    else:
        raise ValueError(f"Unknown dataset {name}")
