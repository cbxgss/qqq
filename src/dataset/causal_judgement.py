instruct = """In this task, you will engage in causal attribution reasoning by providing only one atomic reasoning step at a time.

Your responses should follow the defined atomic reasoning steps, ensuring a logical and systematic approach.

## Guide

### Atomic Reasoning Steps

**Information Collection**
- **Problem Start**: Gather and organize known information, data, and background relevant to the current issue.
- **Reasoning Process**: When reasoning feels aimless, organize known clues that might assist in the recent steps.

**Define Goals**
- Clearly articulate the problem or objective, ensuring an understanding of the desired outcome or rephrasing the original question.

**Formulate Hypotheses**
- Based on identified clues, propose a hypothesis when definitive reasoning isn't achievable, allowing for multi-faceted exploration.

**Develop a Plan**
- Create a short-term plan targeting the recent reasoning goals or based on newly formed hypotheses.

**Execute the Plan**
- Complete the established plan step-by-step. The implementation steps should be specific and detailed.

**Validate Hypotheses**
- Observe and reflect on recent steps to assess whether a proposed hypothesis holds true.

**Summarize and Reflect**
- After a series of atomic steps, conduct a summary and reflection on recent reasoning efforts.

### Human Priors for Transitioning Between Atomic Reasoning Steps

**Problem Start**: Establish the following sequence:
1. Information Collection → Define Goals
2. Define Goals → Formulate Hypotheses

**Transitions**:
- **? → Information Collection**: When the problem is complex, hypothesize or plan before proceeding.
  
- **? → Summarize and Reflect**: Engage in summarizing and reflecting on recent steps.

- **Information Collection → Define Goals**: After organizing information, further clarify the current task.

- **Information Collection → Formulate Hypotheses**: If direct reasoning is challenging, propose hypotheses after gathering related clues.

- **Define Goals → Develop a Plan**: After establishing reasoning objectives, create a plan to achieve them.

- **Formulate Hypotheses → Develop a Plan**: After proposing a hypothesis, design a plan to test it.

- **Develop a Plan → Execute the Plan**: Methodically implement the formulated plan.

- **Execute the Plan → Validate Hypotheses**: Summarize previous steps to determine if a hypothesis is valid.

- **Validate Hypotheses (- Information Collection) → Formulate Hypotheses**: If an original hypothesis fails, attempt to create a new one.

- **Summarize and Reflect → Define Goals**: After summarizing prior reasoning steps, clarify the next target objective.

## Your Task

1. If the reasoning is in progress, choose one atomic reasoning step to continue the process. After completing that step, immediately conclude the reasoning. **You are not allowed to provide any additional output**
2. If the reasoning process hasn’t started, begin with Information Collection.
3. If an answer has been obtained, summarize prior reasoning steps and present the answer.

## Output Format

For each step, present your reasoning in markdown format as follows:

- If an answer hasn't been obtained, provide the atomic reasoning step content:

### Atomic Reasoning Step Name

Atomic Reasoning Step content.

- If an answer has been obtained, provide the answer in the following format:

### Answer

Summary of reasoning process.

```json
{
    "answer": str
}
```
"""

few_shot = [
    {"role": "user", "content": """How would a typical person answer each of the following questions about causation?
Frank T., had an ongoing dispute with his neighbor over a stretch of land and one day decided to shoot his neighbor in the body. Frank T. had no experience with guns, his hand slipped on the barrel of the gun, and the shot went wild. Nonetheless, the bullet bounced off a large boulder several feet away and hit the neighbor's body, causing significant injury. Did Frank T. intentionally shoot his neighbor in the body?
Options:
- Yes
- No
"""},
    {"role": "assistant", "content": """Let's think step by step.
Here in this question, we are told that "Frank T. had no experience with guns, his hand slipped on the barrel of the gun, and the shot went wild." A typical person would assume that this passage suggests that Frank T. had no intention of shooting and injuring someone and that the bullet accidentally hit the neighbor's body; therefore, we conclude that Frank T. did not intentionally hit his neighbor. So the answer is No.

```json
{
    "answer": "No"
}
```
"""},
    {"role": "user", "content": """How would a typical person answer each of the following questions about causation?
Suzy and Billy are working on a project that is very important for our nation's security. The boss tells them both: "Be sure that you are here at exactly 9 am. It is absolutely essential that you arrive at that time." Both Billy and Suzy arrive at 9 am. As it happens, there was a motion detector installed in the room where they arrived. The motion detector was set up to be triggered if at least one person appeared in the room at the same time. So the motion detector went off. Did Billy cause the motion detector to go off?
Options:
- Yes
- No
"""},
    {"role": "assistant", "content": """Let's think step by step.
Here in this question, we are told that the boss ordered them both to arrive at the meeting room at the same time and that the motion detector was set up to be triggered if at least one person appeared in the room at the same time." A typical person would assume that the person probably meant to say the detector was set up to be triggered if "both persons" appeared in the room at the same time, not at least one person, since otherwise the phrase "at the same time" would not make much sense in that sentence. Because the motion detector went off, a typical person would therefore come to the conclusion that both Suzy and Billy triggered the motion detector to go off; hence, Billy did indeed cause the motion detector to go off. So the answer is Yes.

```json
{
    "answer": "Yes"
}
```
"""},
    {"role": "user", "content": """How would a typical person answer each of the following questions about causation?
George and his sister Lena reunite at their parents' house for Thanksgiving. Whereas George just got into medical school, Lena is unhappy in her marriage and recently lost her job. Over the course of the day, George and Lena get into a number of heated arguments. Later in the afternoon they play a game of darts. They split the first two games, and the third game is close until the end. Who will win comes down to George's last shot. If he hits a high point region, he wins; if he hits a low point region, Lena wins. George thinks of the difficult time Lena is having, and he really wants to let her win. He aims the dart at the low point region. He sets up his shot and the dart lands in the low point region. After his shot, Lena wins the game and is very happy. Did George hit the low point region intentionally?"""},
    {"role": "assistant", "content": """Let's think step by step.
Here in this question, we are told that "He aims the dart at the low point region." A typical person might therefore think George did intentionally hit the low point region, because he wanted to lift up the spirit of his sister Lena. So the answer is Yes.

```json
{
    "answer": "Yes"
}
```
"""},
]


import json, re

def get_causal_judgement():
    with open("download/data/BIG-Bench-Hard/bbh/causal_judgement.json") as f:
        data = json.load(f)
        return data["examples"]

def check(answer: str, golden: str):
    answer = re.search(r"```json(.*?)```", answer, re.DOTALL).group(1).strip()
    answer = eval(answer)["answer"]
    return answer.replace(" ", "") == golden.replace(" ", "")
