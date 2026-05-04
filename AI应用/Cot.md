# 第一章：CoT（思维链）深度解析与扩展实践

**CoT (Chain of Thought)** 是 AI Agent 规划器（Planner）中最基础也是最核心的静态规划技术。本章将深入探讨其核心原理、高级变体、工程实践，以及在 LangChain 生态中的落地方式。

## 1.1 核心原理：为什么 CoT 有效？

CoT 不仅仅是提示词工程（Prompt Engineering），它在本质上改变了模型的推理模式：

- **认知对齐：** 让模型模仿人类“分步推理”的过程，激活训练阶段习得的中间推理能力。
- **计算展开：** 将单步直接预测（Direct Prediction）转化为多步条件预测。通过增加推理路径的长度，为模型提供了更多的“计算空间”，每步上下文更聚焦，从而减少“跳步”或“忽略前提”的错误。
- **可解释性：** 透明的中间推理过程不仅方便开发者进行调试，也能显著提升最终用户对 AI 输出结果的信任度。

------

## 1.2 Zero-shot CoT —— “让我们一步步思考”

这是最简单、最通用的实现方式。只需在提示末尾加入魔法语句 `"Let's think step by step"` 或中文“请逐步思考”。

Python

```
def zero_shot_cot(question):
    prompt = f"问题：{question}\n让我们一步步思考。"
    response = client.chat.completions.create(
        model="gpt-4-turbo", # 建议使用推理能力较强的模型
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

- **优点：** 无需示例，通用性极强。
- **局限：** 对于逻辑极其复杂的任务或参数量较小的模型，效果提升有限，且推理格式难以严格控制。

------

## 1.3 Few-shot CoT —— 手把手教模型思考

通过提供 2~3 个带有完整推理步骤的示例，强制模型模仿特定的逻辑链条。

**示例模板：**

> **示例 1:**
>
> **问题：** 罗杰有 5 个网球，又买 2 罐每罐 3 个，共几个？
>
> **推理：** 原来有 5 个，新买了 2 × 3 = 6 个，总数是 5 + 6 = 11 个。
>
> **答案：** 11
>
> **现在请回答：**
>
> **问题：** {用户问题}
>
> **推理：**

------

## 1.4 Auto-CoT：自动化示例生成

Few-shot 的效果高度依赖示例的质量。**Auto-CoT** 通过自动化流程避免了人工挑选示例的偏差。

**工作流程：**

1. **聚类：** 将待处理的问题集进行语义聚类。
2. **采样：** 从每个簇中选取代表性问题。
3. **生成：** 使用 Zero-shot CoT 生成推理链。
4. **过滤：** 配合简单启发式规则过滤错误的推理。
5. **构建：** 将生成的（问题, 推理, 答案）作为 Few-shot 示例喂给最终模型。

------

## 1.5 Self-Consistency：多路径推理与投票

单一的推理路径偶尔会进入“死胡同”。**Self-Consistency（自一致性）** 借鉴了集成学习的思想。

**核心逻辑：**

1. 对同一问题设置 `temperature > 0`。
2. 并行采样生成多条不同的推理路径（如 5-10 条）。
3. 对各路径给出的最终答案进行**多数投票（Majority Voting）**。

Python

```
def self_consistency_cot(question, n_paths=5):
    answers = []
    for _ in range(n_paths):
        # 内部调用带示例的 CoT 推理函数
        cot_output = few_shot_cot(question) 
        ans = extract_answer(cot_output) # 提取答案的辅助函数
        answers.append(ans)
    # 选取出现次数最多的答案
    return max(set(answers), key=answers.count) 
```

- **成效：** 尤其在数学推理和逻辑题中，该策略可将准确率额外提升 5%~10%。

------

## 1.6 从 CoT 到 ReAct：迈向动态交互

CoT 是“纯思考”的静态过程。若引导模型在推理过程中输出可执行的“动作标记”（Action Token），并由外部系统执行反馈，CoT 就演化成了 **ReAct**。

**示例推理流：**

- **思考：** 我需要查询 2024 年奥运会乒乓球冠军。
- **搜索：** `2024年奥运会乒乓球男单冠军` —— *（此时程序挂起，调用搜索工具并返回结果）*
- **结果：** 樊振东获得冠军。
- **思考：** 目标已达成，给出最终回答。

------

## 1.7 LangChain 中的工程落地

### 1.7.1 使用 FewShotPromptTemplate 构建 CoT

通过 LangChain 的模板功能，可以标准化推理过程：

Python

```
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

template = """逐步推理回答问题。
示例：
问题：进水量10，出水量6，容量200，已有50，多久满？
推理：净进水为 10-6=4；需增加 200-50=150；时间为 150/4=37.5。答案：37.5

现在：
问题：{question}
推理："""

prompt = PromptTemplate(input_variables=["question"], template=template)
chain = LLMChain(llm=llm, prompt=prompt)
```

### 1.7.2 构建多步链（SequentialChain）

对于复杂任务，可以将 CoT 拆解为多个原子步骤：

1. **Step 1:** 数据提取链（提取问题中的核心数值）。
2. **Step 2:** 逻辑推理链（基于提取的数据进行分步计算）。

------

## 1.8 进阶：CoT 微调与蒸馏

当 Prompt Engineering 达到瓶颈时，可以通过数据手段提升模型推理本能。

- **数据集构建：** 使用 Auto-CoT 批量生成数据，人工修正后形成 `Question -> Reasoning -> Answer` 三元组。
- **微调（Fine-tuning）：** 使用 LoRA/QLoRA 训练 Llama 3 或 Mistral，使其在不加提示词的情况下也能自发进行推理。
- **蒸馏（Distillation）：** 用 GPT-4 生成高质量推理链数据，训练轻量化的小模型，实现生产环境的低延迟部署。

------

## 1.9 常见陷阱与最佳实践

| **陷阱**       | **最佳实践**                                                 |
| -------------- | ------------------------------------------------------------ |
| **Token 浪费** | 约束推理长度，或在最终输出前进行“摘要式”压缩。               |
| **算术错误**   | 推理链中涉及计算时，强制引导模型调用 `Calculator` 工具。     |
| **指令遗忘**   | 使用 Few-shot 示例固化格式，并降低 `temperature`（除 Self-Consistency 外）。 |
| **自我矛盾**   | 采用 Self-Consistency 投票机制或双模型校验。                 |

------

# 第二章：总结与展望

### 1. 规划范式回顾

在 Agent 的设计中，Planner 是核心。目前主流的四种范式包括：

- **CoT：** 纯推理，适合内部知识充足的闭环任务。
- **ReAct：** 推理与行动交替，适合需要实时获取外部信息的交互任务。
- **Plan-and-Solve：** 先制定完整计划再逐一执行，适合长链路任务。
- **ToT（思维树）：** 树状探索，适合需要多路径回溯的决策任务。

### 2. 实践建议

在实际应用中，**CoT 与 ReAct 往往是结合使用的**：

- **高层规划：** 使用 Plan-and-Solve 拆解大目标。
- **中间推理：** 在每个执行步骤中嵌套 CoT 以保证逻辑严密。
- **工具交互：** 当遇到知识盲区时，自动转入 ReAct 模式。

通过这种弹性架构，可以构建出既有深度思考能力、又能与现实环境灵活交互的强大 AI Agent。