### Background Knowledge and Role Introduction

You are solving a complicated problem. This problem is very complicated, so don't try to solve it in one step.

Now, what you should do in this step is as follows:

### Input

The input for this step includes:

- Question: The question you need to answer.
- Long-term Reasoning Memory: A summarized version of long-term reasoning memories, which is less complete but more concise than the original content.
- Recent Original Reasoning Memory: The original, detailed reasoning content, which is comprehensive but lengthy.
- Human Guidance: Instructions for transitioning between atomic reasoning steps.

### Current Task

Your primary task is to summarize the content in the Recent Original Reasoning Memory.

Each step should be clearly identified, starting with "###". When summarizing, retain the same format, ensuring each summary step also begins with "###".

Aim to condense the information into a single paragraph of approximately 100 words per step, focusing on the key points and maintaining clarity without breaking into multiple paragraphs.

### Output Format

For this step, present your reasoning in json format as follows:

```json
[
    "#### ...\n\nsummary content",
    "#### ...\n\nsummary content"
]
```

Don't output any other information in this step. Only focus on clarifying the goal of the current task and the next step.
