# 运行逻辑

代码位置: `src/o1/hitl/o1.py`

将推理拆分为多个step，每个step都调用一次llm

输入包括
- 原始问题
- 以往的推理步骤
- 人类指导 (需要输入)

旨在通过人类指导，引导模型一步一步推理，明确当下这一step需要做什么

# 人类指导

模拟人类的原子推理，比如：澄清目标、提出猜想、自我检查、规划等多种类型的思考，通过一句 guidance, 指导模型进行下一步推理

下面是在 0-cipher case 中，原子推理的一些举例：
- 前提结构化(整理现有信息成半结构化形式 eg: 1encode example, 2decode example, 3 str to decode)
- insight发现任务结构化（前提1，2，Q：发现1，2间的联系）
- 任务约简（验证1个单词的关系）
- 提出多个假设（提出若干猜想，一般第二个是对的，即长度关系2：1）
- 逐个验证（开始逐个验证）
- 验证任务结构化（前提1，2->长度关系2：1）
- 计算单词数量（step by step）
- 得到初步验证结果
- 推广验证（与任务约简对应）
- 返回验证结果（statement 4：长度2：1）
- 关系发现任务结构化（前提1，2，4，Q：发现1，2间的具体关系）
- 任务约简（发现首个字母之间的映射关系）
- 提出多个假设（一般第二个是对的）
- 逐个验证（开始逐个验证）
- 验证任务结构化（前提1，2->asc码均值）
- 推广验证（step by step）
- 返回验证结果（statement5：asc码均值）
- 解码任务结构化（前提3，4，5做解码）
- step by step解码
- 回答（...）

可大致划分为以下几类原子推理：
- information_collection：整理现有信息成半结构化形式
- goal：澄清目标、问题转换、明确短期任务
- insight_extraction：观察现有信息，发现隐藏信息
- hypotheses_formulate：当解题思路不明确时，提出可能的解题思路或假设
- hypotheses_validate：判断之前提出的假设是否正确
- plan：当解题思路明确时，规划解题步骤 / 提出假设后，规划验证步骤
- execute：一步一步执行规划好的步骤
- check：检查之前的推理是否有错误

# 代码运行

## 参数设置

1. 数据集
   `config/dataset/o1case.yaml` 的 case，可选值: [0, 1, 2, 3, 4, 5, 6, 7]，分别对应 [openai 官方](https://openai.com/index/learning-to-reason-with-llms/) 给出的 8 个 case
2. LLM
   - 需要在项目根目录下，写一个 `.env` 文件，内容
   ```
    OPENAI_API_KEY=...
    OPENAI_API_BASE=https://openai.arnotho.com/v1
    ```
   - 如果选用我们本地的llama模型，可以修改 `config/main.yaml` 中的 `llm` 为 `ollama`

## 运行

```shell
python main.py
```

每个 step 有两次输入：
1. 输入 guidance, 有三种输入情况:
   - `-1`: 结束推理
   - `int`: 使用内置的原子推理类型(运行时这里会打印所有已有的推理类型, 每种内置类型都有固定的 prompt(路径: `src/o1/hitl/agent/infer`) 来指导)
   - `str`: 一句话，表示这一步用户手动输入 string 来指导 (PS: 手动输入的指导要比使用固定 prompt 的效果更好)
2. 输入 y / 其他字符, 如果输入 y 则表示接受这次推理的输出，否则表示拒绝（即不把这次的输出加到推理历史中），并且重新载入所有内置原子推理类型的 prompt

## log

在 `log/o1` 下
- `llm/` 下记录每次调用llm的输入输出
- `output/` 下
  - `xxx.md`: 记录每个问题的整个推理过程
  - `xxx.json`: 里面的 `trace` 里记录接受的推理步骤中，对应的 `guidance` 和这一步的推理

# What to do

1. 选择 case 运行，通过指导llm进行每个step的推理，找到能得到正确解题过程和结果的 推理路径 和 指导集合
2. 确定
   - LLM 能实现 information_collection, hypotheses_formulate 等原子推理
   - 使用以上的原子推理类型，能够得到正确的解题过程和结果
3. 如果不能，对 `guidance` 集合抽象，得到需要引入的原子推理类型
