instruct = """Recommend movies similar to the given list of movies.

The output must end with:
```json
{
    "answer": str
}
```
"""

few_shot = [
    {"role": "user", "content": """Find a movie similar to Star Wars Episode IV - A New Hope, Indiana Jones and the Last Crusade, Star Wars Episode V - The Empire Strikes Back, The Big Lebowski:
Options:
(A) Tetsuo
(B) the Ironman
(C) The Princess Bride
(D) The Barkley Marathons The Race That Eats Its Young
(E) Bug
"""},
    {"role": "assistant", "content": """Let's think step by step.
- Star Wars Episode IV - A New Hope (action, adventure, fantasy; 1977)
- Indiana Jones and the Last Crusade (action, adventure; 1989)
- Star Wars Episode V - The Empire Strikes Back (action, adventure, fantasy; 1980)
- The Big Lebowski (action, drama, comedy; 1998)
These are all famous classic American movies produced before 2000. Amongst all the options, the only movie similar to these ones seems to be The Princess Bride (1987). So the answer is (C).

```json
{
    "answer": "(C)"
}
```
"""},
    {"role": "user", "content": """Find a movie similar to Twister, The Silence of the Lambs, Independence Day, Braveheart:
Options:
(A) They Shoot Horses
(B) Don't They
(C) Forrest Gump
(D) The Salton Sea
(E) Extreme Days
"""},
    {"role": "assistant", "content": """Let's think step by step.
- Twister (action, adventure, thriller; 1996)
- The Silence of the Lambs (crime, drama, thriller; 1991)
- Independence Day (action, science-fiction, drama; 1996)
- Braveheart (biography, drama, epic; 1995)
These are all famous Hollywood movies produced around the 1990s. Amongst all the options, the only movie similar to these ones seems to be Forrest Gump (comedy, drama, romance; 1994). So the answer is (C).

```json
{
    "answer": "(C)"
}
```
"""},
    {"role": "user", "content":  """Find a movie similar to Minority Report, Total Recall, Inside Out, Forrest Gump:
Options:
(A) Phenomena
(B) Lilting
(C) Catwoman
(D) Edge of Tomorrow
"""},
    {"role": "assistant", "content": """Let's think step by step.
- Minority Report (action, crime, mystery; 2002)
- Total Recall (action, adventure, science-fiction; 2012)
- Inside Out (animation, family, comedy; 2015)
- Forrest Gump (comedy, drama, romance; 1994)
These are all famous movies produced in the past few decades.Amongst all the options, the only movie similar to these ones seems to be Edge of Tomorrow (action, adventure, crime, mystery; 2014), as it is also a science-fiction movie and features Tom Cruise. So the answer is (D).

```json
{
    "answer": "(D)"
}
```
"""},
]


import json, re

def get_movie_recommendation():
    with open("download/data/BIG-Bench-Hard/bbh/movie_recommendation.json") as f:
        data = json.load(f)
        return data["examples"]

def check(answer: str, golden: str):
    answer = re.search(r"```json(.*?)```", answer, re.DOTALL).group(1).strip()
    answer = eval(answer)["answer"]
    return answer.replace(" ", "") == golden.replace(" ", "")
