# 基础

## 1. pytorch基础

### 1.1隐藏层用Sequential的定义方式（更简单）

![image-20250119140506560](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250119140506560.png)

**另一种**方式

![image-20250119151647640](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250119151647640.png)



### 1.2两个向量的点积可以被看作衡量他们对齐程度的方法

![image-20250209135000556](../AppData/Roaming/Typora/typora-user-images/image-20250209135000556.png)

高维向量的方向对应了语义

### 1.3Transformer的目标是将这些向量不仅仅编码单个词，还要融合上下文语意

### 1.4logits分数

在深度学习中，logits 分数是指模型输出层的原始未经处理的分数或得分。这个概念主要用于神经网络模型，特别是那些用于分类任务的模型。Logits 代表了模型对每个类别的线性输出，它们是未经过任何激活函数处理的预测值

具体来说，在一个分类问题中，logits 是模型最后一层全连接层的输出，通常是没有经过 softmax 或者 sigmoid 激活函数的直接数值。这些数值可以是任意实数，并不代表概率。正值表示趋向于将样本分类到对应的类别，而负值则表示不倾向于将其分类到该类别。因此，logits 可以看作是对每个类别的置信度或者说是信心度量，但并不是直接的概率

例如，在二分类问题中，如果模型的最后一层输出为单个节点且没有激活函数，则输出值如 2.5 就是该样本被预测为正类的 logits 值。对于多分类问题，模型的最后一层可能有多个节点，每个节点对应一个类别。假设一个多分类模型的输出层包含五个节点，其输出向量为 [1.2, 3.1, -0.5, 4.8, 2.3]，那么这个向量就是该样本属于五个类别的 logits 值

为了将这些 logits 转换成更易于解释的形式，通常会应用 softmax 函数（对于多分类问题）或 sigmoid 函数（对于二分类问题）。Softmax 函数能够将 logits 转换为一个概率分布，使得每个类别的得分都在 0 到 1 之间，且所有类别的概率之和为 1。这样转换后的输出就可以被解释为模型对每个类别的预测概率

此外，在计算交叉熵损失时，logits 也是关键的部分。例如，在 PyTorch 中，BCEWithLogitsLoss 函数可以直接接受 logits 作为输入，并自动对其进行 sigmoid 处理来计算损失；而在使用 BCELoss 函数时，则需要先手动对 logits 应用 sigmoid 函数，然后才计算损失

总之，logits 在深度学习中扮演着重要的角色，特别是在分类任务中，因为它们提供了每个类别的原始得分信息，为后续的分类决策过程奠定了基础。理解 logits 的含义及其与激活函数的关系对于正确设计和训练神经网络模型至关重要。同时，logits 也常用于生成模型中，比如在大语言模型（LLM）的生成/推理过程中，logits 对应的是模型最后输出的一个张量，它包含了每个时间步长上词汇表中每个词的概率分布

。这种分布随后可能会通过采样方法（如 top-k 采样或 nucleus sampling）来选择下一个词，从而继续文本的生成过程。



### 1.5对矩阵点积的更好理解

这是一个非常好的问题！让我们通过分解矩阵运算的维度来详细理解这个梯度计算过程。首先明确几个关键维度：

假设：

- 输入数据维度：`batch_X` 的形状为 `(batch_size, 3)`（因为有3个特征）
- 误差项 `error` 形状为 `(batch_size, 1)`

**运算过程分解：**

1. **转置操作**：

   python

   复制

   ```
   batch_X.T  # 形状从 (40,3) 变为 (3,40)
   ```

2. **矩阵乘法**：

   python

   复制

   ```
   torch.matmul(batch_X.T, error)  # (3,40) × (40,1) = (3,1)
   ```

3. **结果解释**：

   python

   复制

   ```
   delta_w = 结果矩阵 / batch_size  # 最终形状保持 (3,1)
   ```

**具体计算逻辑**：

- **每个特征对应一个梯度**：输出矩阵的每个元素对应一个特征的梯度更新量

- **计算方式**：对于每个特征（即`batch_X.T`的每一行）：

  python

  复制

  ```
  delta_w[i] = sum(特征i在所有样本中的值 * 对应样本的误差) / batch_size
  ```

  这相当于对所有样本在该特征上的误差贡献进行加权平均

**示例说明**（假设 batch_size=2）：

python

复制

```
# 样本特征矩阵（2个样本，3个特征）
batch_X = [[x11, x12, x13],  # 样本1
           [x21, x22, x23]]  # 样本2

# 误差向量（2个样本的误差）
error = [e1, e2]

# 转置后的特征矩阵
batch_X.T = [[x11, x21],  # 特征1
             [x12, x22],  # 特征2
             [x13, x23]]  # 特征3

# 矩阵乘法结果：
delta_w = [
    x11*e1 + x21*e2,  # 特征1的梯度分量
    x12*e1 + x22*e2,  # 特征2的梯度分量
    x13*e1 + x23*e2   # 特征3的梯度分量
]
```

**关键理解点**：

1. 每个特征的梯度是该特征在所有样本中的值与对应误差的点积
2. 矩阵乘法自动完成了对所有样本的求和操作
3. 除以 batch_size 实现了对mini-batch的平均（对应SGD的随机梯度估计）

**为什么这样设计**：

1. **并行计算**：利用矩阵运算的并行性，一次性计算所有特征的梯度
2. **数值稳定性**：批量处理比逐样本更新更稳定
3. **数学等价性**：这实际上是对损失函数求导后梯度公式的矩阵表达形式

**补充说明**：

- 对于形状为 `(3,40)` 的 `batch_X.T` 和 `(40,1)` 的 `error`，矩阵乘法相当于：

  python

  复制

  ```
  for i in 0..2:  # 3个特征
      delta_w[i] = sum(batch_X[:,i] * error.flatten())
  ```

- 最终得到的 `delta_w` 形状是 `(3,1)`，可以直接用于更新 `w`（形状 `(3,)`）

这种设计确保了：

1. 每个特征独立计算其梯度
2. 充分利用了矩阵运算的并行优势
3. 严格对应逻辑回归的梯度公式：∇w = X^T(Sigmoid(Xw + b) - y)/N



### 1.6item()方法

在 PyTorch 中，`loss.item()` 的作用是从包含**单个标量值**的张量（Tensor）中提取其数值，并将其转换为 Python 的**基本数据类型**（如 `float`）。以下是详细解释和使用场景：

------

#### **1. 核心作用**

- **提取标量值**：
  当损失函数（如 `nn.CrossEntropyLoss()`）返回一个张量时，该张量可能包含梯度信息（`requires_grad=True`）。
  `loss.item()` 会返回张量中的**标量值**，并**丢弃梯度等额外信息**。
- **转换为 Python 类型**：
  返回的是一个 Python 数值（如 `float`），而非 PyTorch 张量，方便直接使用（例如打印、记录日志或参与数值计算）。













### 1.7之前的方法：

![image-20250121172613055](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250121172613055.png)

现在方法一：

![image-20250121172827337](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250121172827337.png)

方法二，用列表**（更多灵活性，但是更麻烦）**：

![image-20250121173141823](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250121173141823.png)







### 1.8 LayerNorm函数

![111045dd197522f5409e935ca842c652_720](C:\Users\hp\Documents\Tencent Files\1759751014\nt_qq\nt_data\Pic\2025-01\Thumb\111045dd197522f5409e935ca842c652_720.jpg)

### 1.9 Embedding参数

![1c48d54f13c3f1d54dbad08e6d882b6d_720](C:\Users\hp\Documents\Tencent Files\1759751014\nt_qq\nt_data\Pic\2025-01\Thumb\1c48d54f13c3f1d54dbad08e6d882b6d_720.jpg)

## 2. 深度学习的理解

### 2.1 深度学习与机器学习

```
机器学习要自己提取特征，深度学习它自己用特征提取器提取
```



## 3. 























# **大模型**

## 1. 基础

大模型最擅长的是检索，各种框架其实是把他的检索内容整理一下。它的本身能力不够，只是看起来很光鲜。

### 大模型流程

![image-20250131194035347](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131194035347.png)

transformer架构让大模型有了自己的思想，让它可以回答问题。

![image-20250131194512463](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131194512463.png)

![image-20250131194652620](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131194652620.png)

![image-20250131195807062](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131195807062.png)

### Agent

![image-20250131201748788](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131201748788.png)

![image-20250131202056421](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131202056421.png)

![image-20250131210809420](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131210809420.png)

![image-20250131211028307](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131211028307.png)

![image-20250131211619242](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131211619242.png)

![image-20250131213410331](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250131213410331.png)

### Agent相当于代理人，大脑还是llm

![image-20250202150316304](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250202150316304.png)

![image-20250202152409381](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250202152409381.png)

### self ask 不是通用框架，而是一些加上自问自答更好的模型需要

如下是self ask

![image-20250202153513963](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250202153513963.png)

![image-20250202154302706](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250202154302706.png)

模型能力定下后，Agent通过加入自我评估和反思等，进一步提高解决问题能力（简单的问题甚至可以不用工具）。

上述reflection进行反思（如果不反思，会导致逐渐偏离原问题）。





### 提示的重要性

![image-20250204225440045](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204225440045.png)

提示越冗余，结果越稳定



![image-20250204230855559](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204230855559.png)

### 少量样本不会改变模型本身，但是fine-tuning会改变本身

![image-20250204231302023](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204231302023.png)

### 各种器

![image-20250204231629321](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204231629321.png)

![image-20250204231831687](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204231831687.png)

![image-20250205120837204](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205120837204.png)

![image-20250205135451677](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205135451677.png)

![image-20250205142500570](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205142500570.png)

![image-20250205143000994](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205143000994.png)

![image-20250205143222475](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205143222475.png)

![image-20250205143511524](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205143511524.png)



### 提示词

提示词起到对大模型进行清洗和筛选的作用。





![image-20250205155552098](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205155552098.png)

给模型思考时间：1.给模型足够信息

​                               2.复杂的步骤中，分步骤引导模型

![image-20250205160914917](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205160914917.png)

from langchain.prompts import FewShotPromptTemplate, PromptTemplate

### 定义示例集合

examples = [
    {
        "input": "苹果",
        "output": "水果，常见颜色有红色、绿色。"
    },
    {
        "input": "汽车",
        "output": "交通工具，通常有四个轮子。"
    }
]





定义单个示例的格式

example_template = """
输入：{input}
输出：{output}
"""
example_prompt = PromptTemplate.from_template(example_template)







组合成 Few-Shot Prompt

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="根据示例回答问题：",
    suffix="输入：{noun}\n输出：",
    input_variables=["noun"],
)





使用 Prompt

filled_prompt = few_shot_prompt.format(noun="大象")
print(filled_prompt)







### AI知识库类应用所产生的工作流

![image-20250207145326563](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250207145326563.png)

![image-20250207150347171](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250207150347171.png)



## Langchain

### 链结构

![image-20250205144509184](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250205144509184.png)

多链结构，代码决定选择哪条链去解决问题最好？



### Langchain提示词模板



![image-20250204225702840](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204225702840.png)

![image-20250204230111157](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204230111157.png)

![image-20250204230630974](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20250204230630974.png)







### 历史记录模块

![image-20250209191745071](../AppData/Roaming/Typora/typora-user-images/image-20250209191745071.png)

说白了：就是把之前的聊天记录一并发给它





### Agent非常重要

![image-20250209192531641](../AppData/Roaming/Typora/typora-user-images/image-20250209192531641.png)

react:这里是reasoning and act

#### **1. 基本定义与核心组件**

RouterChain由两部分构成：
- **路由链（Router Chain）**：负责分析用户输入并选择目标子链，支持两种主要类型：
  - **LLMRouterChain**：基于大语言模型的推理能力，通过提示模板（Prompt Template）让LLM决定路由路径。
  - **EmbeddingRouterChain**：利用文本嵌入（Embedding）和向量数据库（如Chroma），通过相似性搜索匹配最相关的子链。
- **目标链（Destination Chains）**：多个预先定义的子链，每个子链专精于特定任务（如物理问答、诗歌生成等）。

此外，RouterChain通常与**MultiPromptChain**结合使用，后者负责整合路由链、子链和默认链（Default Chain），当输入无法匹配任何子链时启用默认链兜底。

---

#### **2. 工作原理**

1. **输入解析**：用户输入被传递给RouterChain。
2. **路由决策**：
   - **LLMRouterChain**：LLM根据预设的提示模板（包含子链描述）生成JSON格式的路由指令，包含目标链名称及可能的输入调整。
   - **EmbeddingRouterChain**：计算输入文本的向量表示，与各子链描述向量进行相似性匹配，选择最接近的子链。
3. **执行子链**：MultiPromptChain将输入传递给选中的子链，生成最终响应。
4. **默认处理**：若无匹配子链，则调用默认链（如通用对话链）处理。

### 注意RAG检索时和文本嵌入向量时的嵌入模型一定一样

不然会因为两者维度不同而犯错

### 用Chroma创建向量库如果用了client

那么检索的模型也要包含client

![image-20250617151606284](../AppData/Roaming/Typora/typora-user-images/image-20250617151606284.png)







## langchain基于向量的搜索索引

### **什么是基于向量的搜索索引？**

基于向量的搜索索引（Vector Search Index）是一种 **利用机器学习和数学方法**，将文本、图片、音频等 **高维数据** 转换成 **向量**（Vector），并存储在一个专门的数据结构中，使得我们可以通过相似性搜索（比如余弦相似度、欧几里得距离）来高效地查找最相关的内容。

------

#### **为什么需要向量搜索？**

传统的文本搜索（比如数据库的 SQL 查询、全文搜索）通常是 **基于关键字匹配** 的，也就是说：

- 只有当查询的关键词**完全匹配** 文本中的某个单词时，才能返回结果。
- 对于**含义相似但表达不同**的文本，传统方法无法很好地处理。

比如，假设你搜索：

> **"如何解决数组排序问题？"**

传统的关键词匹配可能只会找到包含 "**数组排序**" 这个词的文章，而不会找到 "**如何对列表进行排序**" 的内容，因为 "数组" 和 "列表" 虽然意思相近，但它们的关键词不同。

**基于向量的搜索** 则会利用 **深度学习的词嵌入技术（word embedding）**，把句子的含义转换成一个向量，即使查询语句的表述不同，仍然能找到意思相近的内容。

------

#### **向量搜索的核心概念**

1. **向量（Vector）**
   - 计算机不能直接理解文本，所以我们需要用**数值**表示文本。
   - 现代 NLP（自然语言处理）方法会把文本转换成一个高维向量。例如：
     - "苹果" 可能被表示为 `[0.12, 0.98, -0.33, ...]`
     - "橘子" 可能被表示为 `[0.13, 0.95, -0.30, ...]`
     - 由于这两个向量很相似，说明它们的意思也很接近。
2. **嵌入模型（Embedding Model）**
   - 负责把文本转换成向量，比如：
     - `OpenAIEmbeddings()`（OpenAI 提供的嵌入模型）
     - `Sentence-BERT`（基于 BERT 的句子向量模型）
     - `word2vec`（早期的词向量模型）
3. **相似性计算**
   - 计算查询文本与索引中的文本之间的相似度，常用方法：
     - **余弦相似度（Cosine Similarity）**：衡量两个向量的夹角，越接近 1 代表越相似。
     - **欧几里得距离（Euclidean Distance）**：衡量两个向量在空间中的直线距离，越小代表越相似。
4. **向量存储（Vector Store）**
   - 存储大量的文本向量，并支持高效检索，常见的向量数据库：
     - **FAISS**（Facebook AI 开源的向量搜索库，支持高效最近邻搜索）
     - **Chroma**（一个简单易用的向量数据库）
     - **Pinecone**（云端向量数据库）

------

#### **向量搜索的工作流程**

以你的代码为例，向量搜索的步骤如下：

1. **加载 PDF 文档**

   - `PyPDFLoader()` 解析 PDF 并提取文本。

2. **文本转换为向量**

   - ```
     OpenAIEmbeddings()
     ```

      处理文本，将其转换为向量。例如：

     - `"如何排序数组"` → `[0.12, 0.98, -0.33, ...]`
     - `"对列表进行排序的方法"` → `[0.13, 0.95, -0.30, ...]`
     - 由于它们的向量接近，即使关键词不同，搜索仍然可以匹配到正确的内容。

3. **存储向量索引**

   - `FAISS` 负责存储这些向量，并建立索引。

4. **查询**

   - 你输入一个查询（比如 `"如何高效排序数据"`）。
   - 这个查询会被 **转换成向量** 并与索引中的向量进行相似性比较。
   - 返回最相似的文本片段。



### 每个文本嵌入向量维度解释

每个文本的嵌入向量维度表示该文本在 **向量空间** 中的 **表示**。每个向量的维度是由嵌入模型决定的，通常越高维度的向量能表达越丰富的语义信息。在 OpenAI 的嵌入模型中，每个文本的嵌入通常是一个固定长度的向量，具体维度取决于模型。

#### 举个例子：

假设我们有两个文本：

1. **文本 1**："今天的天气很好，适合外出游玩。"
2. **文本 2**："外面的阳光明媚，温度适宜，非常适合运动。"

我们通过 OpenAI 的嵌入模型将这两个文本转换为嵌入向量。假设每个文本被嵌入为一个 512 维的向量（通常情况下，OpenAI 提供的嵌入模型会输出一个 512 维的向量，具体维度会根据模型而有所不同）。

- **文本 1 的嵌入向量**：`[0.123, -0.345, 0.567, ..., 0.987]`（共 512 个数值）
- **文本 2 的嵌入向量**：`[0.321, -0.432, 0.654, ..., -0.123]`（共 512 个数值）

#### 向量维度的作用：

- 这些嵌入向量的每个数字代表了文本在某一维度上的语义特征。例如，某些维度可能会捕捉到 **天气** 相关的词汇，而其他维度可能会关注 **活动** 或 **运动** 相关的语义。
- 嵌入向量的每个文本都被表示为一个固定长度的向量（在这个例子中是 512 维），该向量的不同维度会根据模型训练过程中所学到的语言规律来分配相应的语义信息。

#### 维度的作用：

- **文本相似度**：通过比较两个文本的嵌入向量，可以计算它们之间的相似度。如果两个文本的嵌入向量在向量空间中较为接近，则说明这两个文本的语义上较为相似。例如，`文本 1` 和 `文本 2` 的嵌入向量可能会有较高的相似度，因为它们讨论的是相似的主题：天气和适合外出活动。
- **文本聚类**：通过将多个文本嵌入为向量并进行聚类，可以将相似主题的文本分为一类，从而实现更高效的文本分类或信息检索。



### search搜索匹配向量

因为 Faiss 要求查询输入是 `(num_queries, dimension)` 形状的数组，所以`.reshape((1, embed_dim))` 把向量转换为 **二维格式**，

是的，`idx` 里存储的是 **最相似文本的索引（整数）**，也就是它们在 `texts` 列表中的位置编号（索引值）。

在 Faiss 中，`index_innerproduct.search(...)` 返回两个数组：

```
python


复制编辑
data, idx = index_innerproduct.search(query_embed[0].reshape((1, embed_dim)), topk)
```

- `data`：形状是 `(1, topk)`，包含 **匹配度分数**（通常是内积或 L2 距离）。
- `idx`：形状是 `(1, topk)`，包含 **最相似文本的索引（整数）**，这些索引可以用来访问 `texts` 中的原始文本



### 索引的不同

### **1. Faiss 索引（IndexFlatL2 / IndexFlatIP）**

**在 Faiss 中，"索引"（Index）指的是整个向量数据库**，它的作用是存储和查询向量。

- `index_L2 = faiss.IndexFlatL2(embed_dim)`
- `index_innerproduct = faiss.IndexFlatIP(embed_dim)`

这些是 **Faiss 索引对象**，用于存储向量数据，并执行相似性搜索。
👉 **它们是“数据库”本身，而不是具体的数据索引号。**

**添加数据到索引：**

```
python


复制编辑
index_innerproduct.add(np_embeddings)  
```

这行代码的作用是 **把 `np_embeddings`（所有文本的向量）添加到 Faiss 索引中**。
在这个过程中，Faiss **自动为每个向量分配一个整数索引编号**（从 `0` 开始）。

------

### **2. `idx` 里的索引（最相似文本的索引）**

```
python


复制编辑
data, idx = index_innerproduct.search(query_embed[0].reshape((1, embed_dim)), topk)
```

- `idx` 是 Faiss 进行相似性搜索后返回的结果。
- `idx` 里存储的是 **Faiss 索引中的向量编号（整数）**。
- 这些编号 **对应 `texts` 列表中的文本索引**







## RAG

### 过程

RAG过程展开如 下：（i）检索器最初接收输入查询并搜索相关信 息； (ii) 然后，通过特定的增强方法将原始查询和检 索结果输入生成器； (iii)最后，生成器产生期望的结 果。

#### 检索器

密集检索器和稀疏检索器是信息检索领域中两种常见的技术，它们在原理、特点和应用场景上存在显著差异：


密集检索器（Dense Retrieval）

1. 定义

密集检索器通过将文本（如文档和查询）映射到高维连续向量空间中，利用向量相似度（如余弦相似度）来检索相关文档。


2. 技术实现

密集检索通常依赖于深度学习模型，如BERT、GPT或其他预训练语言模型，将文本转换为密集的向量表示。这些向量能够捕捉文本的语义信息，即使查询和文档之间没有直接的词汇重叠，也能找到语义相关的文档。


3. 特点

• 语义匹配能力强：能够理解文本的深层语义，适合复杂语义检索场景。

• 计算需求高：需要大量的计算资源来训练和运行深度学习模型。

• 结果解释性低：向量的维度不直观，难以直接解释检索结果。


4. 应用场景

密集检索广泛应用于自然语言处理任务，如智能问答系统、内容推荐系统和语义搜索。


稀疏检索器（Sparse Retrieval）

1. 定义

稀疏检索器基于离散的关键词或短语来索引和检索数据。它将文本表示为稀疏向量，通常使用词袋模型（Bag of Words）或TF-IDF（词频-逆文档频率）来计算文档与查询的相关性。


2. 技术实现

稀疏检索通过统计文档中词的出现次数和逆文档频率来构建稀疏向量。例如，TF-IDF算法会为每个词分配权重，表示其在文档中的重要性。


3. 特点

• 高效率和可扩展性：适合处理大规模数据集，因为计算和存储成本较低。

• 强解释性：检索结果基于明确的词汇匹配，容易理解。

• 依赖关键词：效果高度依赖于查询词与文档中词的匹配度，无法解决术语不匹配问题。


4. 应用场景

稀疏检索常用于传统的搜索引擎、网页搜索和文档库检索等场景。


总结

• 密集检索器更适合需要理解复杂语义的场景，但计算成本较高。

• 稀疏检索器更适合大规模数据检索和对计算资源要求较低的场景，但语义理解能力较弱。

在实际应用中，两者也可以结合使用，例如先用密集检索快速缩小搜索范围，再用稀疏检索细化结果。

#### 可以做文章的地方

搜索方式

RAG的结构有很多种

我们将介绍增强所构建的 RAG 系统性能 的方法。我们根据现有方法的增强目标将其分为 5 组：输入、检索器、生成器、结果和整个管道。

两种确定检索必要性的方法：基于规则的方法和基于模 型的方法。

rag处理代码

检索到的表与查询连接起 来以生成答案

从多个源检索，包括知 识图谱、表格和数据库

在 NLP 领域，**实体**通常指的是文本中具有特定意义的名称或术语

几个从某些方面评估RAG的基准。 [318]提 出了一个RAG基准，从四个维度进行评估：（1） 噪声鲁棒性，测试LLM是否可以从噪声文档中提取 必要的信息； （2）消极拒绝，评估LLM在检索到 的内容不充分时是否可以拒绝回复； (3)信息整 合，检查LLM是否能够通过整合多个检索内容来获 取知识并做出反应； (4)反事实鲁棒性，确定LLM 是否可以识别检索到的内容中的反事实错误。

检索器和生成器之间的差距：由于检索器 和生成器的目标可能不一致，并且它们的潜在空间 可能不同，因此设计它们的交互需要精心设计和优 化。当前的方法要么解开检索和生成，要么在中间 阶段将它们集成。虽然前者更加模块化，但后者可 以从联合训练中受益，但会妨碍通用性。

冗长的上下 文：RAG（尤其是基于查询的 RAG）的主要缺点 之一是它极大地延长了上下文，使得上下文长度有 限的生成器不可行。此外，加长的上下文通常也会 减慢生成过程。

来 RAG 研究和应用的几个 潜在方向。1）增强方法的新颖设计：现有研究已 经探索了检索器和生成器之间的各种交互模式。然 而，由于这两个组件的目标不同，实际的增强过程 对最终的生成结果有重大影响。对更先进的增强基 础的研究有望充分释放 RAG 的潜力。2）灵活的 RAG 管道：RAG 系统正在逐步采用灵活的管道， 例如递归、自适应和迭代 RAG。除了对每个组件进 行适当的调整和精心设计之外，检索源、检索器、 生成器和 RAG 子系统的独特组合有望处理复杂的 任务并提高整体性能。



### 操作细节



#### 问题类型

![image-20250219170647636](../AppData/Roaming/Typora/typora-user-images/image-20250219170647636.png)



#### 脚本执行



这是脚本

![image-20250310145958384](../AppData/Roaming/Typora/typora-user-images/image-20250310145958384.png)

5. 脚本的作用和运行方式

- **作用**：

  1. **一键运行推理流程**：每次都手动输入长串命令。
  2. **固定路径和参数**：把所有需要的文件路径、模型路径、阈值、方法等都写死在脚本里，方便后期管理和复现实验。
  3. **可扩展性**：如果以后想对不同的数据集做推理，可以复制这个脚本，修改对应的标记（如`dataset=xxx`）即可快速使用。

- **运行方式**：

  1. 在命令行进入该脚本所在的目录，或者您可以将脚本放在任何您喜欢的位置，只需对应即可。

  2. 保证脚本具有执行权限：

     ```
     狂欢
     
     
     复制編輯
     chmod +x run_crag_inference.sh
     ```

  3. 执行脚本：

     ```
     狂欢
     
     
     复制編輯
     ./run_crag_inference.sh
     ```

     或者用

     ```
     sh run_crag_inference.sh
     ```

     也是可以的。

### 为什么需要加入正确和错误知识一起训练



**正确知识和错误知识的结合**有助于：

1. **训练模型区分正确和错误信息**（如QA、搜索引擎优化）。
2. **提高NLP模型的对比学习能力**（如BERT、GPT、SimCSE）。
3. **帮助处理有歧义的信息**（如推荐系统、信息检索）。
4. **用于文本分类或事实任务**（如假新闻检测）。

这类数据对于**提升AI在真实场景中的表现**非常重要，特别是**避免错误传播**。





### 相似性做文章的地方

![image-20250421205735441](../AppData/Roaming/Typora/typora-user-images/image-20250421205735441.png)

### 几个检索器特点

 🔚 总结对比



| 方法   | 是否语义理解 | 是否训练模型 | 适用场景       | 优点                   | 缺点           |
| ------ | ------------ | ------------ | -------------- | ---------------------- | -------------- |
| TF-IDF | ❌            | ❌            | 快速文本匹配   | 快、轻量、可解释       | 无法理解语义   |
| BM25   | ❌            | ❌            | 精准关键词搜索 | 检索准确、广泛应用     | 无语义理解能力 |
| BGE    | ✅            | ✅            | 多语言语义检索 | 支持多语言，语义理解强 | 占资源、黑盒性 |
| M3E    | ✅            | ✅            | 中文语义搜索   | 中文语义优秀，模型较小 | 英文不佳       |

------

如果你在做一个**检索系统（比如 RAG、FAQ 答题机器人）**：

- 🔍 对关键词匹配要求高，用 **BM25 或 TF-IDF**
- 🧠 追求语义匹配精度，推荐 **BGE**（多语言）或 **M3E**（中文）









# 项目

## 1.CRAG

### 1.解释

![image-20250314225733300](../AppData/Roaming/Typora/typora-user-images/image-20250314225733300.png)



代码解释

![image-20250314225558492](../AppData/Roaming/Typora/typora-user-images/image-20250314225558492.png)

### 2.tokenizer

train_data = tokenizer(
    data.content.to_list(),
    padding="max_length",
    max_length=512,
    truncation=True,
    return_tensors="pt"
)



    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForSequenceClassification.from_pretrained("t5-large", num_labels=1)



**5. 加载模型和数据**

```
python复制编辑    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForSequenceClassification.from_pretrained("t5-large", num_labels=1)
```

- 加载 `T5Tokenizer` 和 `T5ForSequenceClassification`（T5的分类版本，设置 `num_labels=1` 进行**回归任务**）。

```
python


复制编辑
    train_data, train_label = data_preprocess(train_file, tokenizer)
```

- 调用 `data_preprocess` 获取训练数据 `train_data` 和 `train_label`。

```
python复制编辑    batch_size = 12
    train = TensorDataset(train_data["input_ids"], train_data["attention_mask"], torch.tensor(train_label))
    train_dataloader = DataLoader(train, batch_size=batch_size, shuffle=True, sampler=None)
```

- 组装 `TensorDataset`，包括：
  - `input_ids`（输入的token ID）
  - `attention_mask`（注意力掩码）
  - `label`（标签）
- 用 `DataLoader` 生成批量数据

```
python复制编辑    optimizer = AdamW(model.parameters(), lr=1e-4)
    num_epochs = 8
    num_training_steps = num_epochs * len(train_dataloader)
    lr_scheduler = get_scheduler(
        name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
    )
```

- **优化器**：AdamW（适合 Transformer 训练）
- **学习率调度器**：线性下降（`get_scheduler("linear")`）

------

**6. 模型训练**

```
python复制编辑    device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)
```

- 检测是否有可用的GPU，如果有则使用，否则用CPU。

```
python复制编辑    for i, epoch in enumerate(range(num_epochs)):
        total_loss = 0
        model.train()
        for step, batch in enumerate(train_dataloader):
            if step % 10 == 0 and not step == 0:
                print("step: ",step, "  loss:",total_loss/(step*batch_size))
```

- 进入训练循环，每 `10` 步打印一次 `loss`。

```
python复制编辑            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)

            model.zero_grad()        
            outputs = model(b_input_ids, attention_mask=b_input_mask, labels=b_labels)
            loss = outputs.loss   
            loss.mean().backward()
            total_loss += loss.mean().item()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
```

- **前向传播**：
  - `model(b_input_ids, attention_mask=b_input_mask, labels=b_labels)`
- **计算损失**：
  - `loss.mean().backward()`
- **梯度裁剪**：
  - 避免梯度爆炸 `torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)`
- **参数更新**：
  - `optimizer.step()`
  - `lr_scheduler.step()`
  - `optimizer.zero_grad()`

------

 **7. 保存模型**

```
python复制编辑        avg_train_loss = total_loss / len(train_dataloader)      
        print("avg_loss:", avg_train_loss)

        model.save_pretrained(args.save_path + "/ep{}".format(i))
        tokenizer.save_pretrained(args.save_path + "/ep{}".format(i))
```

- 每个 `epoch` 结束后，保存**模型和分词器**。

------

**总结**

这段代码是一个完整的**文本回归训练脚本**，核心功能：

1. 读取 `train_file` 训练数据
2. 使用 `T5Tokenizer` 进行文本编码
3. 使用 `T5ForSequenceClassification` 进行模型训练
4. 使用 `AdamW` 优化器 + `linear` 学习率调度器
5. 训练过程中打印 `loss`
6. 每个 `epoch` 结束后，保存模型和分词器



### 3.计算余弦

### 3. **归一化张量**

Python复制

```python
normalized_tensor_1 = tensor_1 / tensor_1.norm(dim=-1, keepdim=True)
normalized_tensor_2 = tensor_2 / tensor_2.norm(dim=-1, keepdim=True)
```

- 这里对输入的两个张量分别进行 **L2 归一化**。
- `tensor.norm(dim=-1, keepdim=True)`：
  - `dim=-1` 表示沿着张量的最后一个维度计算 L2 范数（即每个向量的模长）。
  - `keepdim=True` 保留了维度信息，使得归一化后的张量形状与原始张量一致。
- 将每个张量除以它的 L2 范数，使得每个向量的长度变为 1（单位向量）。





### 4.jsonlines

1. **处理大数据集**：适合处理非常大的数据集，因为可以逐行读取，而不需要一次性加载整个文件。
2. **流式处理**：可以用于流式数据处理，例如从网络流中逐行读取 JSON 数据。

















# 深度学习相关库

## 1.pandas

### 与时间相关

**示例代码解析：**

```
train = pd.read_csv(DATA_PATH + 'train.csv', parse_dates=['date'])
```

- **`parse_dates=['date']`**：将名为 `'date'` 的列转换为 datetime 类型。
- 转换后，`train['date']` 的数据类型会变为 `datetime64[ns]`，而非字符串。



1. **后续处理更高效**
   转换为 datetime 类型后，你可以直接使用时间序列操作，例如：
   - 按日期筛选数据：`df[df['date'] > '2023-01-01']`
   - 提取年、月、日：`df['date'].dt.year`
   - 计算时间差：`df['date'].diff()`
   - 重采样时间序列：`df.resample('D', on='date').sum()`

### pandas拼接用法

**1. 合并油价数据**

```
oil = oil.rename(columns={'dcoilwtico': 'oil_price'})
full_data = pd.concat([train, test], ignore_index=True)
full_data = pd.merge(full_data, oil, on='date', how='left')
```

- **`oil.rename`**：将油价数据中的列名 `dcoilwtico`（可能是一个缩写）重命名为更易理解的 `oil_price`。
- **`pd.concat([train, test])`**：将训练集 `train` 和测试集 `test` 纵向拼接为一个 DataFrame `full_data`。`ignore_index=True` 表示重置索引，避免索引重复。
- **`pd.merge(full_data, oil)`**：将合并后的 `full_data` 与油价数据 `oil` 按日期列 `date` 进行左连接（`how='left'`）。这一步会为每条数据添加当天的油价信息。

------

**2. 合并全国性假日信息**

```
national_holidays = holidays[holidays['locale'] == 'National']
national_holidays = national_holidays[['date', 'type']].rename(columns={'type': 'holiday_type'})
full_data = pd.merge(full_data, national_holidays, on='date', how='left')
```

- **筛选全国性假日**：`holidays[holidays['locale'] == 'National']` 从原始假日数据中过滤出全国性假日（排除地区性假日）。
- **提取必要列并重命名**：`national_holidays[['date', 'type']]` 只保留日期和假日类型列，并将 `type` 重命名为 `holiday_type`，使列名更明确。
- **左连接合并**：将全国性假日信息按日期合并到 `full_data` 中，非节假日的日期对应的 `holiday_type` 为 `NaN`。

### pandas进行滞后操作

```
def create_lag_features(df, lags=[1, 7, 14, 28]):
    for lag in lags:
        df[f'sales_lag_{lag}'] = df.groupby(['store_nbr', 'family'])['sales'].shift(lag)
    return df
```

1. **输入参数**
   - `df`：包含时间序列数据的 DataFrame，必须包含列 `date`（日期）、`store_nbr`（商店编号）、`family`（商品类别）、`sales`（销售额）。
   - `lags`：指定滞后步长的列表，默认为 `[1, 7, 14, 28]`，表示生成过去 1 天、1 周、2 周、4 周的销售额作为特征。
2. **核心逻辑**
   - **按分组生成滞后值**：
     `groupby(['store_nbr', 'family'])` 表示按商店和商品类别分组，确保每个组内独立计算滞后值。
     *例如：商店A的饮料类商品与商店B的零食类商品的滞后值互不影响。*
   - **`shift(lag)`**：
     对每个组内的 `sales` 列进行滞后操作，将数据向下移动 `lag` 行。
     *例如：`lag=1` 时，当前行的 `sales_lag_1` 值为上一行的 `sales`。*
3. **输出结果**
   - 为每个 `lag` 生成新列，列名格式为 `sales_lag_{lag}`（如 `sales_lag_7`）。
   - 返回更新后的 DataFrame。

## 2. ChromaDB

下面把 Chroma 常用且“必须会”的东西按主题、并配上短代码示例、常见坑与最佳实践列出来。内容基于官方文档 + 社区实践，关键事实我在每部分给出来源链接（便于查阅）。如果你想要我把下面的示例打包成一个可运行的 starter script，我可以直接给你完整脚本。

------

### 核心概念速览（先记住这些）

- **Collection**：相当于一张表，保存向量（embedding）、document（通常是文本 chunk）和 metadata。[Chroma Docs](https://docs.trychroma.com/docs/querying-collections/query-and-get?utm_source=chatgpt.com)
- **Client 类型**：可选内存（Ephemeral/Client）、本地持久（PersistentClient）或通过 HTTP/Cloud（HttpClient / CloudClient）连接远端/Chroma Cloud。持久化目录通常是 `./chroma` 或你指定的 `path`。[Chroma Docs+1](https://docs.trychroma.com/docs/run-chroma/persistent-client?utm_source=chatgpt.com)
- **索引（Index）**：Chroma 内部使用 HNSW（近似最近邻图）来做向量检索，索引通常需要被加载到内存中以获得高性能。索引参数可在 collection metadata 中配置（如距离空间 `l2`/`cosine`、M、ef_construction 等）。[Chroma Docs](https://docs.trychroma.com/guides/deploy/performance?utm_source=chatgpt.com)[cookbook.chromadb.dev](https://cookbook.chromadb.dev/core/configuration/?utm_source=chatgpt.com)

------

### 1) 安装 & 初始化（Python）

```
pip install chromadb
```

Python 快速示例（持久化 client）：

```
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./chroma_db")  # 持久化到磁盘
collection = client.get_or_create_collection(
    name="kb",
    # 可选：传入 embedding function（见后）
)
```

（或 `client = chromadb.Client()`/`EphemeralClient()` 做临时内存测试，或用 `HttpClient`/`CloudClient` 连接远端/Cloud。）[Chroma Docs+1](https://docs.trychroma.com/docs/run-chroma/persistent-client?utm_source=chatgpt.com)

------

### 2) Embedding（嵌入）的常见用法（两条原则非常重要）

1. **维度一致**：一个 collection 的 embedding 维度一旦第一次写入就被“锁定”，后续写入或查询必须使用相同维度的向量（否则会报错/行为异常）。这是最常见的坑之一。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/faq/?utm_source=chatgpt.com)
2. **归一化**：默认距离度量是 `l2`（欧氏），如果你用的 embedding 未归一化，距离会非常大，影响结果。对 `L2` 或 `IP`（内积）敏感的场景，**建议先对向量做 normalize（unit vector）** 或显式设定 `hnsw:space` 为 `cosine`。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/faq/?utm_source=chatgpt.com)[realpython.com](https://realpython.com/chromadb-vector-database/?utm_source=chatgpt.com)

**如何设置 embedding function**（可让 Chroma 自动在 add/query 时调用）：

```
from chromadb.utils import embedding_functions
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="kb", embedding_function=ef)
```

你也可以**自己计算 embeddings**（比如用 OpenAI、HuggingFace、本地模型）再把 embeddings 传给 `collection.add(..., embeddings=...)`。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/embeddings/bring-your-own-embeddings/?utm_source=chatgpt.com)[realpython.com](https://realpython.com/chromadb-vector-database/?utm_source=chatgpt.com)

------

### 3) 写入（add / upsert / update / delete）

- `collection.add(...)`：用于新增（可能会触发 DuplicateIDError，如果 ids 重复需处理）。
- `collection.upsert(...)`：**推荐用于可重复执行的写入流程**，会更新已存在 id，若不存在则创建（id 存在则更新）。这是实现幂等写入的常用方法。[Chroma Docs+1](https://docs.trychroma.com/docs/collections/update-data?utm_source=chatgpt.com)

示例（带 precomputed embeddings）：

```
collection.add(
    ids=["doc1", "doc2"],
    documents=["文本A", "文本B"],
    metadatas=[{"source":"pdf"}, {"source":"web"}],
    embeddings=[[0.1,0.2,...], [0.2,0.3,...]]  # 事先计算好的向量
)
# 幂等更新：
collection.upsert(
    ids=["doc1"],
    documents=["文本A（更新）"],
    metadatas=[{"source":"pdf","version":2}],
    embeddings=[[...]]
)
```

**避免重复 id 的策略**：在写入前用 metadata（如 file-hash）做判断，或使用 upsert 直接覆盖，或捕获 `IDAlreadyExistsError`。社区实践很多（也见 LangChain 的差异注意）。[Reddit](https://www.reddit.com/r/LangChain/comments/1abkaif/avoid_duplicates_inside_a_chroma_db/?utm_source=chatgpt.com)[Stack Overflow](https://stackoverflow.com/questions/76414862/how-do-you-catch-the-duplicate-id-error-when-using-langchain-vectorstores-chroma?utm_source=chatgpt.com)

------

### 4) 查询（query / get / peek）与过滤

- `collection.query(...)`：相似度检索（可传 `query_texts` 或 `query_embeddings`），支持 `n_results`、`where`（metadata 过滤）等参数。
- `collection.get(ids=[...])`：按 id 精确获取记录（非相似检索）。
- `collection.peek(n)`：预览 collection 中前 n 条（调试时非常有用）。[Chroma Docs](https://docs.trychroma.com/docs/querying-collections/query-and-get?utm_source=chatgpt.com)

示例：

```
# 文本查询（Chroma 会使用 collection 的 embedding_function）
res = collection.query(query_texts=["如何部署模型？"], n_results=3)

# 或基于 embedding 查询
res = collection.query(query_embeddings=[[0.12,0.3,...]], n_results=5)

# 带元数据过滤
res = collection.query(query_texts=["xxx"], n_results=5, where={"source":"pdf"})
```

**metadata 过滤支持的操作符**（常用）：`$eq`, `$in`, `$and`, `$or`, `$gt` 等（请参考 docs 的 where 文档）。[Chroma Docs](https://docs.trychroma.com/docs/querying-collections/metadata-filtering?utm_source=chatgpt.com)

------

### 5) 高级搜索：MMR / hybrid / re-ranking（与 LangChain 的常见组合）

- 如果你用 LangChain 的 `Chroma` 包装器，可以把 vectorstore 当作 retriever，支持 `search_type="mmr"`（最大边际相关性）以及 `fetch_k`、`lambda_mult` 等参数来平衡相关性与多样性（MMR）。这在 RAG 场景很常见。[LangChain+1](https://python.langchain.com/docs/integrations/vectorstores/chroma/?utm_source=chatgpt.com)

示例（LangChain retriever）：

```
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 20, "lambda_mult": 0.5},
)
docs = retriever.get_relevant_documents("问题文本")
```

------

### 6) 索引与性能调优（HNSW 参数 & 内存）

- Chroma 使用 HNSW（fork）做索引。HNSW 的索引需要驻留在内存中以获得高性能，因此即便使用磁盘持久化，查询时仍有内存要求（索引大小与向量数量、参数有关）。如果你要处理非常大规模（百万级以上）向量，需要评估内存和分片策略，或考虑更面向分布式/大规模的向量库（如 Milvus 等）。[Chroma Docs](https://docs.trychroma.com/guides/deploy/performance?utm_source=chatgpt.com)[Zilliz](https://zilliz.com/blog/milvus-vs-chroma?utm_source=chatgpt.com)
- 可以在创建 collection 时通过 metadata 设置 HNSW 参数，例如 `{"hnsw:space":"cosine", "hnsw:m":16, "hnsw:ef_construction":200}`（不同版本 API 可能细节略有不同，修改后通常需重建索引或 clone collection）。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/core/configuration/?utm_source=chatgpt.com)

------

### 7) 持久化、备份与迁移

- **PersistentClient(path=...)** 会把数据写到你指定目录（默认 `./chroma`），重启时会自动加载。适合单机持久化。[Chroma Docs](https://docs.trychroma.com/docs/run-chroma/persistent-client?utm_source=chatgpt.com)
- 在 notebook 中写入时，有些版本需要调用 `client.persist()` 来强制把内存写到磁盘（不同版本 API 有差异；在某些版本中 persist 方法被调整/移除，注意你的 chroma 版本）。一般脚本里，client 被销毁时会自动 flush。建议：写完后检查 count / peek，并根据你版本是否支持显式 persist 决定是否调用。[Stack Overflow](https://stackoverflow.com/questions/77231763/cannot-load-persisted-db-using-chroma-langchain?utm_source=chatgpt.com)[GitHub](https://github.com/langchain-ai/langchain/issues/20851?utm_source=chatgpt.com)
- **复制/导出 collection**：cookbook 提供数据导出/导入（local <-> remote）和迁移工具（也可用 cdp export/import）。生产环境常做定期备份（复制持久目录或使用 cdp）。[cookbook.chromadb.dev+1](https://cookbook.chromadb.dev/core/collections/?utm_source=chatgpt.com)

------

### 8) 常见坑、调试建议与最佳实践（必须记住）

1. **embedding 维度不一致** → 直接报错或查询结果异常。上传 embeddings 前统一模型/维度。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/faq/?utm_source=chatgpt.com)
2. **未归一化 embedding 导致大距离** → 归一化或设 `hnsw:space="cosine"`。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/faq/?utm_source=chatgpt.com)
3. **id 重复/去重**：`add` 可能产生 DuplicateIDError，`upsert` 更适合幂等写入，或自己在写入前用 metadata 查重。[Chroma Docs](https://docs.trychroma.com/reference/python/collection?utm_source=chatgpt.com)[Reddit](https://www.reddit.com/r/LangChain/comments/1abkaif/avoid_duplicates_inside_a_chroma_db/?utm_source=chatgpt.com)
4. **内存不足**：HNSW 索引需驻留内存；向量数量大时评估内存/分片/换库。[Chroma Docs](https://docs.trychroma.com/guides/deploy/performance?utm_source=chatgpt.com)
5. **版本差异**：Chroma 的 API 会更新（例如 persist 的行为），在升级前看 changelog 并做数据迁移测试。[Chroma](https://www.trychroma.com/changelog?utm_source=chatgpt.com)[Chroma Docs](https://docs.trychroma.com/docs/overview/migration?utm_source=chatgpt.com)

------

### 9) 常用 API 速查（一行说明 + 示例）

- 创建 client：`client = chromadb.Client()` / `PersistentClient(path="./chroma")`。[Chroma Docs](https://docs.trychroma.com/docs/run-chroma/persistent-client?utm_source=chatgpt.com)
- 创建/获取 collection：`collection = client.get_or_create_collection(name="kb", embedding_function=ef)`。[Chroma Docs](https://docs.trychroma.com/docs/collections/manage-collections?utm_source=chatgpt.com)
- add（带 embeddings）：`collection.add(ids=[...], documents=[...], metadatas=[...], embeddings=[...])`。[realpython.com](https://realpython.com/chromadb-vector-database/?utm_source=chatgpt.com)
- upsert（更新或插入）：`collection.upsert(...)`。[Chroma Docs](https://docs.trychroma.com/docs/collections/update-data?utm_source=chatgpt.com)
- query：`collection.query(query_texts=["..."], n_results=5, where={...})` 或 `query_embeddings=[...]`。[Chroma Docs](https://docs.trychroma.com/docs/querying-collections/query-and-get?utm_source=chatgpt.com)
- get / peek：`collection.get(ids=[...])` / `collection.peek(5)`。[ML EXPLAINED](https://mlexplained.blog/2024/04/09/ultimate-guide-to-chroma-vector-database-everything-you-need-to-know-part-2/?utm_source=chatgpt.com)
- delete：`collection.delete(ids=[...])` 或用 where 条件删除。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/core/collections/?utm_source=chatgpt.com)

------

### 10) 与其他工具/框架整合（很常用）

- **LangChain**：官方有 Chroma 的整合（能直接把 Chroma 当成 vectorstore / retriever 用），并支持 MMR 等策略。对 RAG + QA 很便利。[LangChain+1](https://python.langchain.com/docs/integrations/vectorstores/chroma/?utm_source=chatgpt.com)
- **LlamaIndex / Haystack / other**：都有 Chroma adapter，可以把 Chroma 作为底层向量存储。[LlamaIndex 文档](https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/?utm_source=chatgpt.com)[Haystack Documentation](https://docs.haystack.deepset.ai/docs/chromadocumentstore?utm_source=chatgpt.com)

------

### 11) 推荐的简单工程化流程（POC → 生产）

1. POC：在本地 `Client()` 或 `PersistentClient(path="./tmp")` 做小规模测试，使用现成 embedding（sentence-transformers 或 OpenAI）。[realpython.com](https://realpython.com/chromadb-vector-database/?utm_source=chatgpt.com)
2. 设计 chunk strategy：把长文按合理长度切片并带上来源 metadata（file_hash、page_no 等）。[Medium](https://blog.amikos.tech/chroma-basics-document-primitive-d5a0c97cc813?utm_source=chatgpt.com)
3. 写入时用 `upsert` 保证可重跑；写完用 `peek/count` 验证。[Chroma Docs](https://docs.trychroma.com/docs/collections/update-data?utm_source=chatgpt.com)
4. 性能评估：测索引在内存的占用、查询延迟，根据需要调整 HNSW 参数或考虑分片/更换数据库。[Chroma Docs](https://docs.trychroma.com/guides/deploy/performance?utm_source=chatgpt.com)
5. 备份 & 监控：定期备份 persist dir，并在升级前做 migration 测试。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/core/storage-layout/?utm_source=chatgpt.com)

------

### 参考（节选——我在正文中引用的权威资源）

- Chroma 官方入门 / Query 与 Collection 文档（query/get/metadata filtering）。[Chroma Docs+1](https://docs.trychroma.com/docs/querying-collections/query-and-get?utm_source=chatgpt.com)
- Chroma 性能说明（HNSW 索引需在内存）。[Chroma Docs](https://docs.trychroma.com/guides/deploy/performance?utm_source=chatgpt.com)
- PersistentClient / client 类型与持久化说明。[Chroma Docs](https://docs.trychroma.com/docs/run-chroma/persistent-client?utm_source=chatgpt.com)
- FAQ（维度锁定、向量归一化等常见问题）。[cookbook.chromadb.dev](https://cookbook.chromadb.dev/faq/?utm_source=chatgpt.com)
- upsert/add 行为与 collection API 参考。[Chroma Docs+1](https://docs.trychroma.com/docs/collections/update-data?utm_source=chatgpt.com)

------

### 额外：给你的一份最小化 Python 模板（可直接复制运行）

（如果你愿意，我可以把下面模板完整展开成 `.py` 文件并包含虚拟 embedding 的 demo 数据）

```
import chromadb
from chromadb.utils import embedding_functions

# 1. client（持久化）
client = chromadb.PersistentClient(path="./chroma_db_demo")

# 2. embedding function（可替换为你自己的）
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. collection（设置 HNSW 空间为 cosine）
collection = client.get_or_create_collection(
    name="demo_kb",
    embedding_function=ef,
    metadata={"hnsw:space": "cosine"}
)

# 4. 加入文档（示例）
collection.upsert(
    ids=["d1", "d2"],
    documents=["第一段文本内容", "第二段文本内容"],
    metadatas=[{"source":"pdf","page":1}, {"source":"web","url":"https://..." }]
)

# 5. 查询
res = collection.query(query_texts=["查询示例"], n_results=3, where={"source":"pdf"})
print(res)

# 6. 预览与计数
print("count", collection.count())
print(collection.peek(3))
```

### 1. ChromaDB 与 LangChain 的结合方式

LangChain 已经内置了对 **Chroma** 的支持，可以直接把它当作 `VectorStore` 使用。
 这意味着你可以：

- 用 LangChain 提供的 **文档加载/切分 → embedding → 存入 Chroma** 流程；
- 把 Chroma 封装成 **Retriever**，直接作为 RAG 的知识库查询组件。

典型流程：

```
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. 定义 embedding
embedding = OpenAIEmbeddings()

# 2. 连接 Chroma（持久化到本地目录）
vectorstore = Chroma(
    collection_name="my_kb",
    embedding_function=embedding,
    persist_directory="./chroma_store"
)

# 3. 添加文档
vectorstore.add_texts(
    texts=["你好，这是第一条文本", "这是第二条文本"],
    metadatas=[{"source": "file1"}, {"source": "file2"}],
    ids=["id1", "id2"]
)

# 4. 检索（相似度搜索）
docs = vectorstore.similarity_search("你好", k=2)

# 5. 转 Retriever（用于链）
retriever = vectorstore.as_retriever(
    search_type="mmr",   # 或 similarity
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
)
```

**总结：**

- `Chroma` 在 LangChain 中扮演 **存储 + 检索** 的角色。
- `Retriever` 是 LangChain 的统一接口，支持和各种 LLM 组合，直接做问答/对话。

------

### 2. 参数的含义

#### Chroma 核心参数

- **collection_name**
  - 向量库的集合名（相当于一张表），同一个集合内维度必须一致。
- **embedding_function**
  - 向量生成函数，可以用 OpenAI/HuggingFace/SentenceTransformers 等。
- **persist_directory**
  - 数据持久化路径，如果不写就是内存模式。
- **ids**
  - 每个向量的唯一标识（字符串），避免重复冲突。
- **documents / texts**
  - 原始文本，可以是大块的文档切片。
- **metadatas**
  - 每个向量的元数据（字典），方便后续过滤。

------

#### Query / Search 参数

- **query_texts** / **query_embeddings**

  - 你要查询的文本或 embedding。

- **n_results / k**

  - 返回的 top-k 相似结果。

- **where**

  - metadata 条件过滤，例如：

    ```
    where={"source": "pdf"}  
    where={"page": {"$gt": 10}}
    ```

------

#### Retriever 参数（LangChain 封装）

- **search_type**
  - `"similarity"`：按相似度返回 top-k
  - `"mmr"`：最大边际相关性（减少重复，保证多样性）
- **search_kwargs**（根据 search_type 不同而不同）：
  - `k`：最终返回的文档数量
  - `fetch_k`：初始取多少个候选（MMR 常用）
  - `lambda_mult`：MMR 中的多样性权重（0 偏向相关性，1 偏向多样性）

------

### 3. metadata 是什么？

`metadata` 就是每个向量绑定的 **额外信息（键值对字典）**。
 它不会进入 embedding，但能帮助你做 **过滤 / 溯源 / 上下文追踪**。

举例：
 你把一本书分成很多段落，存进 Chroma：

```
collection.add(
    ids=["para1", "para2"],
    documents=["第一段内容...", "第二段内容..."],
    metadatas=[
        {"source": "book1.pdf", "page": 1},
        {"source": "book1.pdf", "page": 2}
    ]
)
```

之后查询时，可以加条件：

```
res = collection.query(
    query_texts=["某个问题"],
    n_results=3,
    where={"source": "book1.pdf", "page": {"$gte": 2}}
)
```

**常见 metadata 用法：**

- `source`：来源文件名（pdf, docx, url …）
- `page`：所在页数
- `chunk_id`：分块编号
- `timestamp`：数据插入时间
- `version`：数据版本

作用：

- 可以做条件检索（where）
- 可以在最终回答时告诉用户“这段话来自哪一页哪个文件”
- 方便做数据更新/去重/追踪

------

✅ 总结一句话：

- **Chroma 负责存储 + 检索**，LangChain 把它包装成 **Retriever**，方便在 RAG 里直接调用。
- **参数**主要控制存储时（collection, ids, embeddings, metadata）、查询时（n_results, where）、retriever 策略（similarity vs mmr）。
- **metadata** 是“上下文标签”，不影响向量计算，但能做过滤和结果解释，是 RAG 系统中非常重要的“溯源信息”。





## 3. **jieba**

`jieba` 是一个中文分词库，常用于中文文本的切分和处理。它通过将中文句子切分成一个个有意义的词语，帮助计算机理解中文文本的结构。在自然语言处理（NLP）中，分词是中文处理中的基础步骤。

- **安装**：

  ```
  bash
  
  
  复制编辑
  pip install jieba
  ```

- **常用功能**：

  - **精确模式**：默认模式，最适合文本分析。
  - **全模式**：把句子中所有可能的词语都扫描出来，速度非常快，但不能解决歧义。
  - **搜索引擎模式**：适用于搜索引擎构建，粒度比精确模式更细。

### 2. **cut_for_search**

`cut_for_search` 是 `jieba` 中的一个分词方法，适用于将文本切分为搜索引擎友好的细粒度词汇。它会将句子分割成比精确模式更细的粒度，以适应搜索引擎中关键词匹配的需求。

- **用法**：

  ```
  python复制编辑import jieba
  text = "我来到北京清华大学"
  result = jieba.cut_for_search(text)
  print(" ".join(result))
  ```

  输出：

  ```
  复制编辑
  我 来到 北京 清华 大学
  ```

  - 这种方式切分出来的词汇比较细，例如“清华大学”被拆成了“清华”和“大学”，这是因为搜索引擎会用到这些细粒度的关键词来提高匹配的准确性。

## 4. Embedding模型选择

![image-20250731185516271](../AppData/Roaming/Typora/typora-user-images/image-20250731185516271.png)













# 医学

## RAG

### 一些文献

![image-20250508172717363](../AppData/Roaming/Typora/typora-user-images/image-20250508172717363.png)

### 知识图谱

![image-20250603163838384](../AppData/Roaming/Typora/typora-user-images/image-20250603163838384.png)

数据集来源

![image-20250525001846113](../AppData/Roaming/Typora/typora-user-images/image-20250525001846113.png)

节点关系

![image-20250525001941639](../AppData/Roaming/Typora/typora-user-images/image-20250525001941639.png)

别人的想法

![image-20250525002102219](../AppData/Roaming/Typora/typora-user-images/image-20250525002102219.png)

### 论文

![image-20250525205105062](../AppData/Roaming/Typora/typora-user-images/image-20250525205105062.png)









# 算法

## 多模态

### clip

#### 简介

##### 1. 预训练后：“文本-图像配对”思维的形成

在预训练阶段，模型看了**4亿个（图像，文本描述）对**。
*   **它学到的东西**：并不是简单地认识“狗”或“汽车”这个类别标签，而是学习到了 **“某一段文字描述（如‘一只在草坪上奔跑的狗’）在视觉上应该对应什么样的图像特征”** ，反之亦然。
*   **形成的机制**：模型内部建立了一个**共享的语义空间**。在这个空间里，“狗的图片”的特征向量和“描述狗的文本”的特征向量非常接近，但和“描述汽车的文本”的特征向量则很远。

---

##### 2. “自然语言被用来引用学习到的视觉概念”

这是指在**做下游任务时（比如图像分类）**，我们如何“唤醒”模型在预训练中学到的知识。

**传统模型的做法**：给你一张图，模型从1000个固定的类别（如“贵宾犬”、“吉娃娃”）中选一个输出。这些类别是训练时定死的硬编码数字。

**CLIP的做法**：
1.  **把分类任务变成图文匹配任务**：我们不用数字标签，而是用**自然语言描述**来定义类别。
2.  **引用概念**：比如，我们要分类“狗”、“猫”、“汽车”。我们不告诉模型类别编号0，1，2，而是给它**一串文字提示（Prompts）**，例如：
    *   `“一张狗的照片”`
    *   `“一张猫的照片”`
    *   `“一辆汽车的照片”`
3.  **模型如何工作**：
    *   CLIP的**文本编码器**会把这些文本提示转换成特征向量（`T_dog`, `T_cat`, `T_car`）。
    *   CLIP的**图像编码器**会把待分类的图片转换成特征向量（`I`）。
    *   模型计算图片向量`I`与每一个文本向量（`T_dog`等）的相似度。
    *   选择相似度最高的那个文本标签作为预测结果。
    *   **关键**：在这个过程中，文本提示 `“一张狗的照片”` **就像一把钥匙，激活（引用）了模型在预训练时学到的所有关于“狗”的视觉概念**。

---

##### 3. “或描述新的概念”——零样本能力的核心

这才是CLIP最强大的地方。**下游任务中的类别，完全可以不在预训练数据中明确出现过！**

**举个例子**：
假设CLIP在预训练时从未明确见过“新冠检测试剂盒”的图片和文字，但它见过“试纸”、“两条线”、“塑料外壳”、“医学检测”等无数相关概念。

现在，我们想做一个“识别新冠检测结果”的任务。传统模型需要收集大量试剂盒图片重新训练。而CLIP可以直接用自然语言**描述这个新概念**：
*   Prompt 1: `“一张显示新冠阳性结果的检测试剂盒照片”`
*   Prompt 2: `“一张显示新冠阴性结果的检测试剂盒照片”`
*   Prompt 3: `“一张无效的新冠检测试剂盒照片”`

**模型如何工作**：
模型虽然没有直接背下“试剂盒”这个类别，但它理解：
*   `“阳性”`可能关联`“两条线”`、`“红色标记”`等视觉特征。
*   `“检测”`关联`“塑料装置”`、`“试纸”`。
*   `“无效”`可能关联`“模糊”`、`“只有一条控制线”`。

通过**组合这些已有的视觉-语言概念**，模型就能在共享语义空间中，将新的图片与这些新的文本描述进行比较，做出合理判断。**这就是“描述新概念”**。

---

##### 用一个完整比喻来总结

想象CLIP在预训练阶段是一个**博览群书（4亿对图文）的通才**，它不背死答案，而是建立了强大的“图文联想”能力。

当遇到一个新问题（下游任务）时：
1.  **传统专家模型**：需要你给它上专门的培训课（微调），教它认识这个新领域的专用术语（固定类别标签）。
2.  **CLIP这个通才**：你不需要重新培训它。你只需要用**它已经掌握的人类语言**，向它**描述**这个新任务是什么。
    *   **“引用”**：就像你问它：“还记得书里提到的‘柯基犬’吗？”（用已知概念）。
    *   **“描述新的”**：就像你问它：“如果一个物体是透明的、有四个轮子、靠电力驱动，它可能是什么？”（组合已知概念，定义新事物）。

这个通才就能基于它庞大的知识库和强大的联想能力，给出答案。**这就是零样本迁移**——模型迁移的不是某个具体任务的参数，而是迁移了**用语言理解和连接视觉世界的基础能力**。



#### **训练流程详解**

##### **第1步：准备海量“图文对”数据**

- **数据来源**：从互联网上爬取4亿个（图像，文本描述）对。文本就是图片的原始说明、标题或ALT文本。
- **特点**：数据是“噪声”的——描述不一定精确，但足够丰富和多样。这迫使模型去理解语义，而不是死记硬背。

##### **第2步：构建“批次”并进行编码**

1. 随机抽取一个批次的N个图文对，例如 N=1024。
2. **图像编码**：将N张图片输入**图像编码器**（可以是Vision Transformer或ResNet），得到N个图像特征向量 `[I1, I2, ..., IN]`。
3. **文本编码**：将对应的N条文本输入**文本编码器**（一个Transformer），得到N个文本特征向量 `[T1, T2, ..., TN]`。

##### **第3步：计算相似度矩阵**

- 计算**所有图像特征**和**所有文本特征**之间的余弦相似度，得到一个 `N x N` 的矩阵。
- **矩阵对角线**上的元素 `(I1, T1), (I2, T2)...` 是**正样本对**（它们本来就是配对的）。
- **矩阵非对角线**上的元素都是**负样本对**（比如 `I1` 和 `T2`，图片和文字不匹配）。

##### **第4步：通过对比损失函数进行优化**

这是训练的关键。目标很直观：

- **拉近正样本**：让对角线上的相似度尽可能高。
- **推开负样本**：让非对角线上的相似度尽可能低。

这通过一个叫**对称交叉熵损失** 来实现：

- **图像→文本分类**：对于每一张图片 `I_i`，把N条文本当作N个“类别”，计算一个Softmax分类损失。唯一的正确“类别”就是其配对的文本 `T_i`。
- **文本→图像分类**：同理，对于每一条文本 `T_i`，把N张图片当作N个“类别”，唯一的正确“类别”是其配对的图片 `I_i`。
- **总损失**是这两个方向损失的平均。这就是“对称”的含义，确保图文理解是双向对齐的。

##### **第5步：反向传播与迭代**

- 计算出的总损失通过反向传播，同时更新**图像编码器**和**文本编码器**的参数。
- 用新的批次重复这个过程，在数亿的数据上迭代数轮。

















## 大语言模型

### 1. Transformer基础

#### 1.0 深层理解

我们从头梳理一下大模型利用注意力机制生成文本的完整流程。这个过程可以分为三个层次：注意力机制的计算、注意力输出的含义、以及基于该输出的自回归生成。

---

一、注意力机制的核心公式

注意力机制是Transformer模型的基石，其数学形式如下：

\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\mathsf{T}}{\sqrt{d_k}}\right) V

公式中的三个矩阵由输入序列通过线性变换得到：

· Q（Query，查询）：代表当前关注点，可以理解为“我正在寻找什么信息”。
· K（Key，键）：代表序列中每个位置提供的“信息标签”，可以理解为“我这里有什么信息”。
· V（Value，值）：代表序列中每个位置的实际“信息内容”。

计算过程分为三步：

1. 计算相关性：通过 QK^\mathsf{T} 计算查询与所有键的点积，得到注意力分数矩阵，其形状为 [序列长度, 序列长度]。该矩阵的每个元素表示一个位置对另一个位置的关注程度。
2. 缩放与归一化：除以 \sqrt{d_k}（d_k 是键向量的维度）防止分数过大导致梯度消失；然后应用 softmax 函数，将每一行的分数转换为概率分布，得到注意力权重矩阵，每一行的和为1。
3. 加权求和：用注意力权重矩阵对值矩阵 V 进行加权求和，得到最终的输出矩阵。

---

二、公式计算的结果是什么？

公式的输出是一个矩阵，其形状与输入序列相同：[序列长度, 特征维度]。

这个矩阵的每一行对应输入序列中一个位置的新表示向量。该向量不再只代表该位置本身的词，而是融合了整个序列中所有相关位置的信息，相关程度由注意力权重决定。换句话说，经过注意力层后，每个词都“看”了一遍整个上下文，并把重要信息吸收进自己的表示中。

因此，这个矩阵是上下文感知的语义表示，后续的神经网络层（如前馈网络）会基于这些表示继续处理。

---

三、大模型如何利用这个矩阵生成一句话？

大模型（如GPT系列）采用自回归方式生成文本，即每次只生成一个词，然后把新词加入输入序列，再次输入模型预测下一个词，如此循环直到结束。具体步骤如下：

1. 从矩阵到下一个词的概率分布

· 当模型处理当前序列（例如已生成的前 t 个词）时，经过多层Transformer计算，最后一层输出的矩阵中，最后一个位置的向量（记为 h_t）包含了当前已生成序列的全部信息，用于预测下一个词。
· 这个向量通过一个语言模型头（通常是一个线性层 + softmax）映射到词表大小的向量：
  P(\text{下一个词}) = \text{softmax}(h_t W + b)
  其中 W 和 b 是可训练参数。输出向量的每个维度对应词表中的一个词，数值表示该词作为下一个词的概率。

2. 选择下一个词

根据概率分布，模型选择一个词作为输出。常见的策略包括：

· 贪婪搜索：直接选择概率最高的词。
· 随机采样：按照概率分布随机抽样，增加多样性。
· 束搜索：保留多个候选序列，综合评估后选择最优。

3. 循环生成完整句子

· 将选出的新词拼接到输入序列末尾，形成新的输入序列。
· 将新序列再次输入模型，重复上述步骤，得到再下一个词的概率分布。
· 不断重复，直到模型预测出特殊的结束符（EOS，End-of-Sequence token），或达到最大长度限制。

---

四、关键理解要点

· 注意力矩阵 的作用是让每个位置的表示都融入上下文，这是模型“理解”语言的基础。
· 生成过程 是逐词迭代的，每一步都基于当前整个已生成序列重新计算注意力矩阵，从而让模型能够利用最新的上下文进行下一步预测。
· 从矩阵到词 的转换由一个分类层完成，它将最终的语义向量映射到词表空间，输出概率分布。
· 整个流程没有“一次性”生成一句话，而是一步一步地“猜”出下一个最合适的词。

通过这种方式，大模型能够生成连贯、符合上下文的自然语言文本。







#### 1.1 原向量要乘以一个矩阵才能得到查询(query)

这样才能得到包含一定（注意是一定）上下文信息的向量，实质是将嵌入向量映射到相应的低维空间



下面这张图才是都整合了前面的信息（图的左边V是乘以词嵌入的value）

![image-20250209154740877](../AppData/Roaming/Typora/typora-user-images/image-20250209154740877.png)







#### 1.2 每种不同的上下文更新方式，键矩阵和查询矩阵参数都会变，

值矩阵也会因嵌入值更新值而改变



![image-20250209162531504](../AppData/Roaming/Typora/typora-user-images/image-20250209162531504.png)



#### 1.3 n个注意头意味着n个q,k,v矩阵

#### 1.4 多头训练

多加几个头更精确（就多加几个delta）

![image-20250209162936158](../AppData/Roaming/Typora/typora-user-images/image-20250209162936158.png)



#### 1.5 深层理解

![image-20250209163459471](../AppData/Roaming/Typora/typora-user-images/image-20250209163459471.png)





















































# 大模型应用

## 1. 基础

### 1.1 自回归模型

#### 解释

在训练时，模型在预测某个位置的词时，**只能看到这个词之前的所有信息（上文）**，而不能“偷看”未来的词。这个特性就叫 **“自回归”**。

#### 操作

GPT是：

1. 接受提示词
2. 预测并添加第一个新token
3. **把提示词+第一个token一起输入**，预测第二个新token
4. **把提示词+前两个token一起输入**，预测第三个新token
5. 如此循环，直到生成结束

##### **关键技术细节**

​      1.**KV缓存（Key-Value Cache）**：实际实现中，为提升效率，不会每次都重新计算整个序列。

- 第一次计算时，会为`["中国", "的", "首都", "是"]`生成Key和Value向量并缓存。

- 生成`"北京"`时，只需计算`"北京"`的Key/Value，并与缓存的结合。

- 生成`"。"`时，只需计算`"。"`的Key/Value。

- **逻辑上**是每次都输入完整序列，**物理上**只计算新token。

  

  2.**为什么需要整个历史上下文？**

- 因为语言有**长距离依赖**。比如生成第20个词时，可能依赖于第2个词。
- Transformer的自注意力机制理论上可以看到序列中的所有位置。
- 如果没有整个历史，模型就像失忆一样，无法保持一致性。



#### GPT是自监督模型

#### 大数据集起作用原理

这个看似简单的任务，当数据量（整个互联网）和模型规模（千亿级参数）达到临界点后，会产生质变，即 **“涌现能力”**。







### 1.2 传统机器学习模型

#### 1. RNN

##### **RNN的基本原理：通过“记忆”间接传递信息**

RNN（循环神经网络）的核心思想是：**每个时间步只能看到当前输入和上一个时间步的“记忆”（隐藏状态），通过这个“记忆”链式传递信息。**

###### **可视化对比**

**Transformer（自注意力）：**

text

```
输入: [词1, 词2, 词3, 词4, 词5]
处理词5时: 可以直接看到[词1, 词2, 词3, 词4, 词5]的全部
→ 建立任意两个词的直接连接
```



**RNN（单向）：**

text

```
时间线: t1      t2      t3      t4      t5
输入:   词1  →  词2  →  词3  →  词4  →  词5
记忆:   h1  →   h2  →   h3  →   h4  →   h5
            ↗      ↗      ↗      ↗
依赖:    只依赖h1  只依赖h2  只依赖h3  只依赖h4
```



**关键**：在t5时刻，RNN只能直接看到**词5**和**h4**。h4是包含了词1-词4信息的“摘要”，但不是原始信息本身。



























### 1.3 **大模型学习的是组合规律**

有限样本中包含了大量可重用的“模块”，模型学会这些模块后可以组合出新的内容。

比如：

- A 学会了“做饭的步骤”
- B 学会了“鸡蛋怎么处理”
- C 学会了“番茄的特性”

那么模型可以：

→ 组合 A+B+C 生成新菜谱

哪怕训练集中没有出现过这个完整菜谱。

这叫**组合泛化（compositional generalization）**。







## 2. RAG

### 2.1 如何提高

#### 1. 检索前

![image-20260206212003053](../AppData/Roaming/Typora/typora-user-images/image-20260206212003053.png)

#### 2. 创建时技巧

![image-20260206212130963](../AppData/Roaming/Typora/typora-user-images/image-20260206212130963.png)

![image-20260206212743093](../AppData/Roaming/Typora/typora-user-images/image-20260206212743093.png)

![image-20260206213016322](../AppData/Roaming/Typora/typora-user-images/image-20260206213016322.png)

![image-20260206213122967](../AppData/Roaming/Typora/typora-user-images/image-20260206213122967.png)

![image-20260206213739360](../AppData/Roaming/Typora/typora-user-images/image-20260206213739360.png)

![image-20260206213845116](../AppData/Roaming/Typora/typora-user-images/image-20260206213845116.png)

#### 2.2 如何利用有效信息

![image-20260206220921196](../AppData/Roaming/Typora/typora-user-images/image-20260206220921196.png)

##### 解决方法

![image-20260206221631285](../AppData/Roaming/Typora/typora-user-images/image-20260206221631285.png)

![image-20260206221725015](../AppData/Roaming/Typora/typora-user-images/image-20260206221725015.png)

### 2.2 完整系统

![image-20260206221823134](../AppData/Roaming/Typora/typora-user-images/image-20260206221823134.png)

![image-20260206222014011](../AppData/Roaming/Typora/typora-user-images/image-20260206222014011.png)























# 科研感悟

## 1. 科研是循序渐进的

**这是clip模型之前的工作**

20 多年前，Mori 等人 (1999) 探索了通过训练一个模型来预测与图像配对的文本文档中的名词和形容词，从而改进基于内容的图像检索。Quattoni 等人 (2007) 证明了通过在学习用于预测与图像相关的标题中单词的分类器权重空间中进行流形学习，可以学习到数据效率更高的图像表示。











