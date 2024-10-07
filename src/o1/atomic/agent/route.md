## Background Knowledge and Role Introduction

When solving complex problems, we break the reasoning process down into multiple steps, each belonging to a specific atomic reasoning type. This approach makes the reasoning process clearer and more efficient.

Based on the following input, think step by step and choose the next atomic reasoning type to proceed. In each step, select one atomic reasoning type and continue to advance the reasoning.

Additionally, determine if the current reasoning steps have already arrived at a conclusive answer. If so, output "None" for the route.

Input:
- Question: The origin question you need to answer.
- Reasoning Memory: Previous reasoning steps.

Available atomic reasoning types:
1. information_collection: Organize known information into a structured format.
2. goal: Clarify the next short-term goal or perform problem equivalence transformation to simplify the problem.
3. insight_extraction: When the problem-solving direction is unclear, observe the known information to uncover potential insights.
4. hypotheses_formulate: Propose a possible approach or hypothesis for solving the problem.
5. hypotheses_validate: Observe the process of validating the hypothesis and conclude whether the previously proposed hypothesis is valid.
6. plan: Specify a clear plan to solve the problem or validate the proposed hypothesis.
7. execute: Follow the specified plan, executing step by step.
8. check: Review previous reasoning steps for any errors.

The following are some experiences of how humans use different atomic reasoning types to solve problems when reasoning:
- When encountering a problem, the first step is to organize the information in the problem, structure the known information to better understand the problem.
- After organizing the information, clarify the next short-term goal or transform the problem into an equivalent form to make it easier to solve.
- If the direction of solving the problem is unclear and a definite method to solve the problem cannot be found, first observe the known information, try to find potential clues or insights from it, then try to propose hypotheses that may be helpful, and then find a solution by validating these hypotheses.
- If the direction of solving the problem is clear, a detailed plan can be formulated to solve the problem step by step.
- If a hypothesis is proposed, a plan needs to be specified to validate the hypothesis first, and then the hypothesis needs to be validated step by step according to the plan.
- If the result of a step of reasoning does not meet expectations, or if the current reasoning encounters difficulties, you can review the previous reasoning steps to check for errors or missing information.

## Output Format

Please consider the current question and reasoning steps, think about the next step in the reasoning process, and output in the following format:

```json
{
    "guide": "What should the next step be?(Do not include any escape characters (\\) in the generated string)",
    "route": "chosen atomic reasoning type (str of [{{reasoning_types}}]) or None if the answer is conclusive"
}
```

Note：Your output will be processed with the json.dumps () function, so please make sure that the output format is correct.
