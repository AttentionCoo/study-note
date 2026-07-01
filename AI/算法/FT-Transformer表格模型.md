# Titanic-FT-Transformer 知识总结

本文档对使用 FT-Transformer (Feature Tokenizer Transformer) 在 Kaggle Titanic 数据集上进行二分类任务的全过程进行了系统梳理，涵盖了模型原理、数据预处理、架构设计、正则化策略、训练技巧以及工程化部署等核心知识点。

---

## 1. 项目背景

**任务**：Kaggle Titanic 生存预测（二分类）。  
**数据规模**：训练集 891 行，特征包括乘客等级、性别、年龄、亲属数量、票价、登船港口等。  
**核心挑战**：数据集极小（891 条），深度模型极易过拟合。  
**解决思路**：采用 FT-Transformer 架构，并通过多种正则化手段和特征工程组合，稳定提升模型泛化能力。

---

## 2. FT-Transformer 模型原理

### 2.1 Feature Tokenizer（特征分词器）

将表格数据中的每一个特征（连续或离散）转换为一个固定维度的向量（Token）。

- **数值特征**：  
  使用可学习的权重矩阵 \( W_i \) 和偏置 \( b_i \)，计算 Token：  
  \[
  \text{Token}_i = x_i \cdot W_i + b_i
  \]  
  其中 \( W_i \in \mathbb{R}^{d_{\text{token}}} \)，通常用正态分布初始化（\(\mu=0, \sigma=0.01\)），\( b_i \) 初始化为 0。  
  生成后通过 LayerNorm 统一量纲。

- **类别特征**：  
  使用 `nn.Embedding` 将每个类别映射为 \( d_{\text{token}} \) 维向量。

- **所有 Token 堆叠**：  
  得到形状为 `(batch_size, n_features, d_token)` 的序列。

### 2.2 `[CLS]` Token

借鉴 BERT 的架构，在特征 Token 序列前拼接一个可学习的 `[CLS]` Token。经过 Transformer 编码器后，该 Token 的输出被用来进行最终分类。

### 2.3 Transformer 编码器

堆叠多个 Transformer Block，每个 Block 包含：

- **Multi-Head Self-Attention**：捕捉特征间的交互关系。
- **Position-wise Feed-Forward Network**：两层线性变换，中间使用 ReLU 激活。
- **残差连接 + LayerNorm**：稳定训练。
- **Dropout**：在 Attention 权重和 FFN 中间施加高比例 Dropout（如 0.45）。

### 2.4 预测头 (MLP Head)

取 `[CLS]` Token 的最终输出，可选地拼接特征 Token 的统计量（如平均值），再通过一个小型 MLP 产生 logits。二分类使用 `BCEWithLogitsLoss`。

---

## 3. 面对小数据的正则化“全家桶”

本项目为应对 891 条样本的过拟合问题，设计了一套多维正则化方案：

| 技术                           | 具体实现与参数                                               |
| ------------------------------ | ------------------------------------------------------------ |
| **高 Dropout**                 | Attention、FFN、MLP Head 均采用 p=0.45 的 Dropout            |
| **权重衰减**                   | 使用 AdamW 优化器，weight_decay = 1e-2                       |
| **随机深度 (DropPath)**        | 在残差路径上随机丢弃整个 Transformer Block，概率 0.2         |
| **标签平滑 (Label Smoothing)** | 将真实标签从 {0,1} 调整为 {0.05, 0.95}，防止模型过分自信     |
| **学习率调度**                 | ReduceLROnPlateau，监控验证准确率，耐心值 5，衰减因子 0.5    |
| **早停 (Early Stopping)**      | 若连续 20 个 epoch 验证指标不提升则停止训练                  |
| **小模型容量**                 | Token 维度降至 32（原论文常用 64~256），MLP 隐藏层 64        |
| **5 折交叉验证**               | StratifiedKFold 划分，保证类别比例一致，评估结果取均值±标准差 |

---

## 4. 特征工程扩展

原始特征信息量有限，通过特征工程引入更多先验知识，显著提升模型上限。

- **Title（头衔）**：从 `Name` 字段提取（Mr, Mrs, Miss, Master 等），罕见头衔归为 “Rare”，作为类别特征 Embedding。
- **FamilySize**：`SibSp + Parch + 1`，直观反映家庭规模。
- **IsAlone**：`FamilySize == 1` 的二值特征，标记独自乘船的乘客。
- **Deck（甲板）**：从 `Cabin` 首字母提取，缺失填充为 “Unknown”，也作为类别特征。
- **缺失值处理**：`Age` 按 Title + Pclass 分组的中位数填充，`Fare` 按 Pclass 中位数填充，`Embarked` 用众数填充。
- **标准化**：所有连续特征经 `StandardScaler` 处理。

---

## 5. 架构改进细节

为防止 Transformer 的深层 Attention 冲刷掉原始线性信号，模型在 MLP Head 处加入了特征残差连接：

- 取所有特征 Token 的**均值**向量（代表原始特征的整体信息）。
- 通过一个线性投影 `proj_residual` 映射到与 `[CLS]` 输出相同的维度。
- 将 `[CLS]` 输出与投影后的特征均值拼接，送入最终分类器。

这种设计使得模型既保留了全局交互信息，又直接利用了原始特征的线性组合，在小样本上非常有效。

---

## 6. 训练流程与工程实现

- **数据加载**：自定义 `TitanicDataset`，返回连续特征、类别特征列表和标签。
- **训练函数**：每个 batch 计算标签平滑后的损失，反向传播。
- **评估函数**：不启用 Dropout/DropPath，计算准确率。
- **交叉验证循环**：  
  1. 按 `StratifiedKFold` 划分训练/验证集。  
  2. 每折重新初始化模型，独立训练。  
  3. 记录每折最佳验证准确率。  
  4. 最终输出平均准确率和标准差。
- **硬件**：支持 CPU/GPU 切换。

---

## 7. 实验建议与提升方向

为进一步挖掘模型潜力，可尝试：

- **与树模型融合**：将本模型的 OOF 预测与 LightGBM / CatBoost 加权平均，两种不同归纳偏置的模型往往带来显著提升。
- **更多特征**：票号（Ticket）重复信息、年龄分箱与 Title 交叉、Cabin 数量等。
- **超参数搜索**：对 `d_token`、`dropout`、`weight_decay` 等使用网格搜索或贝叶斯优化。
- **集成多个 Transformer**：用不同随机种子训练多个模型，进行预测平均。

---

## 8. 关键代码结构

```
├── main.py                # 主程序：预处理、模型定义、训练、CV
├── train.csv              # Kaggle 训练集
├── test.csv               # Kaggle 测试集
└── README.md              # 项目说明
```

核心模块概览：

- `load_and_preprocess()`：读取数据 → 特征工程 → 编码 → 标准化 → 划分训练/测试。
- `FeatureTokenizer`：数值 tokenization + 类别 embedding + LayerNorm。
- `TransformerBlock`：Self-Attention + FFN + DropPath 集成。
- `FTTransformer`：完整模型，含残差连接。
- `train_epoch()` / `evaluate()`：带标签平滑的训练与准确率评估。
- 主程序：5 折 CV 循环，打印平均准确率。

---

## 9. 总结

本项目展示了如何在极端小样本表格数据上成功应用 Transformer 模型。核心思想可归纳为三点：

1. **强特征工程** 提升信息量。
2. **极小容量 + 多重正则化** 限制过拟合。
3. **架构微调**（特征残差） 保留线性信号。

该实践可作为其他小规模结构化数据深度学习任务的参考模板，同时也为 Kaggle 新手提供了从特征处理到模型融合的完整思路。
