instruct = """Correctly close a Dyck-n word.

The output must end with:
```json
{
    "answer": str
}
```
"""

few_shot = [
    {"role": "user", "content": """Complete the rest of the sequence, making sure that the parentheses are closed properly. Input: [ { [
"""},
    {"role": "assistant", "content": """Let's think step by step.
We should process each input one by one and keep track of the stack configuration.
0: empty stack
1: [ ; stack: [
2: { ; stack: [ {
3: [ ; stack: [ { [
Now, we have reached the end. The final stack is "[ { [".
We will need to pop out "[", "{", "[" one by one in that order.
So, we need "]", "}", "]". So the answer is ] } ].

```json
{
    "answer": "] } ]"
}
```
"""},
    {"role": "user", "content": """Complete the rest of the sequence, making sure that the parentheses are closed properly. Input: < > ( ( [ [ ( { } ) [ < > ] ]
"""},
    {"role": "assistant", "content": """Let's think step by step.
We should process each input one by one and keep track of the stack configuration.
0: empty stack
1: < ; stack: <
2: > ; stack: empty
3: ( ; stack: (
4: ( ; stack: ( (
5: [ ; stack: ( ( [
6: [ ; stack: ( ( [ [
7: ( ; stack: ( ( [ [ (
8: { ; stack: ( ( [ [ ( {
9: } ; stack: ( ( [ [ (
10: ) ; stack: ( ( [ [
11: [ ; stack: ( ( [ [ [
12: < ; stack: ( ( [ [ [ <
13: > ; stack: ( ( [ [ [
14: ] ; stack: ( ( [ [
15: ] ; stack: ( ( [
Now, we have reached the end. The final stack is "( ( [".
We will need to pop out "[", "(", "(" one by one in that order.
So, we need "]", ")", ")". So the answer is ] ) ).

```json
{
    "answer": "] ) )"
}
```
"""},
    {"role": "user", "content": """Complete the rest of the sequence, making sure that the parentheses are closed properly. Input: < [ < [ { < [ ] < { } > > } ] > { { ( ) } { < [ < > ] > }
"""},
    {"role": "assistant", "content": """Let's think step by step.
We should process each input one by one and keep track of the stack configuration.
0: empty stack
1: < ; stack: <
2: [ ; stack: < [
3: < ; stack: < [ <
4: [ ; stack: < [ < [
5: { ; stack: < [ < [ {
6: < ; stack: < [ < [ { <
7: [ ; stack: < [ < [ { < [
8: ] ; stack: < [ < [ { <
9: < ; stack: < [ < [ { < <
10: { ; stack: < [ < [ { < < {
11: } ; stack: < [ < [ { < <
12: > ; stack: < [ < [ { <
13: > ; stack: < [ < [ {
14: } ; stack: < [ < [
15: ] ; stack: < [ <
16: > ; stack: < [
17: { ; stack: < [ {
18: { ; stack: < [ { {
19: ( ; stack: < [ { { (
20: ) ; stack: < [ { {
21: } ; stack: < [ {
22: { ; stack: < [ { {
23: < ; stack: < [ { { <
24: [ ; stack: < [ { { < [
25: < ; stack: < [ { { < [ <
26: > ; stack: < [ { { < [
27: ] ; stack: < [ { { <
28: > ; stack: < [ { {
29: } ; stack: < [ {
Now, we have reached the end. The final stack is "< [ {".
We will need to pop out "{", "[", "<" one by one in that order.
So, we need "}", "]", ">". So the answer is } ] >.

```json
{
    "answer": "} ] >"
}
```
"""},
]


import json, re

def get_dyck_languages():
    with open("download/data/BIG-Bench-Hard/bbh/dyck_languages.json") as f:
        data = json.load(f)
        return data["examples"]

def check(answer: str, golden: str):
    answer = re.search(r"```json(.*?)```", answer, re.DOTALL).group(1).strip()
    answer = eval(answer)["answer"]
    return answer.replace(" ", "") == golden.replace(" ", "")
