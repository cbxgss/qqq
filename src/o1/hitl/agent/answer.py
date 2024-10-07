answer_user = """Question:
{question}

Your reasoning steps:
{inference}
"""

answer_system = """Your task is to summarize the reasoning process and provide the final answer.

Your output format should be:

### Summary

Summary of reasoning process.

### Answer

```json
{
    "answer": str
}
```
"""
