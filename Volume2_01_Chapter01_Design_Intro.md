# 第1章：优化从何而来 (Where Optimization Comes From)

> "The formulation of the problem is often more essential than its solution."  
> “提出问题往往比解决问题更重要。”  
> —— Albert Einstein

为什么有些算法从 $O(n^2)$ 下降到 $O(n)$，而另一些问题似乎只能艰难搜索？答案不在代码长度，而在问题允许我们保留、丢弃、合并和重新组织什么。

Why do some algorithms fall from $O(n^2)$ to $O(n)$ while other problems seem to require difficult search? The answer lies not in code length, but in what the problem permits us to retain, discard, merge, and reorganize.

## 设计链：从语义到证明 (The Design Chain: From Semantics to Proof)

Volume II 使用一条统一设计链；它是检查表，而不是声称每一步都必须显式编码。

Volume II uses one unified design chain; it is a checklist, not a claim that every step must be implemented explicitly.

$$
\text{Problem Semantics}
\to \text{Information Requirement}
\to \text{State Space}
\to \text{Mathematical Structure}
\to \text{Sufficient Representation}
\to \text{Optimization Mechanism}
\to \text{Algorithm / Data Structure}
\to \text{Proof}
\to \text{Boundary}
$$

### 问题语义 (Problem Semantics)

语义说明输入、输出、合法操作、成本和约束。仅知道“输入是数组”还不够；必须知道数组上的哪些操作和问题目标是被允许的。

Semantics specify the input, output, legal operations, costs, and constraints. Knowing only that the input is an array is insufficient; the permitted operations on it and the target query must also be known.

### 信息需求 (Information Requirement)

先问真正需要什么结果：完整路径、一个可行路径、最优值，还是一组统计量？只需要最短跳数而不需要具体路线时，可压缩的信息就可能更多。

First ask what result is actually required: a full path, one feasible path, an optimum, or a summary. If only the minimum jump count is needed and not the route, more information may be compressible.

### 状态空间 (State Space)

**状态空间（State Space）**包含所有可能状态及合法转移。它可以显式为图，也可以隐式存在于数组、区间或函数调用中。

**状态空间（State Space）** contains all possible states and legal transitions. It may be an explicit graph or remain implicit in arrays, intervals, or function calls.

Brute Force 通常有清楚状态空间，也可能完全正确；它慢是因为它重复访问、合并或组织不当，而不是缺少正确性。

Brute Force often has a clear state space and may be completely correct; it is slow because it visits redundantly or merges and organizes poorly, not because it lacks correctness.

### 数学结构与充分表示 (Mathematical Structure and Sufficient Representation)

**数学结构（Mathematical Structure）**包括顺序、单调性、支配、等价、结合律、守恒、可分解性和区间连续性。结构不是装饰；它决定哪些推理可成立。

**数学结构（Mathematical Structure）** includes order, monotonicity, dominance, equivalence, associativity, conservation, decomposability, and interval continuity. Structure is not decoration; it determines which deductions are valid.

**充分表示（Sufficient Representation）**是在给定查询和操作集合下保留了足够信息的表示。例如，只回答静态连通性时，Union-Find 的分量代表元足够；回答最短路时则不够。

**充分表示（Sufficient Representation）** preserves enough information for a specified set of queries and operations. Union-Find component representatives suffice for connectivity queries, but not for shortest paths.

$$
\text{Optimization Opportunity}
=
\text{Problem Structure}
+
\text{Sufficient Representation}
+
\text{Optimization Mechanism}
$$

## 五类优化机制 (Five Optimization Mechanisms)

| 机制 (Mechanism) | 问题 (Question) | 例子 (Examples) |
| :--- | :--- | :--- |
| **Eliminate / Prune** | 哪些候选可永久排除？What candidates can be removed permanently? | Binary Search、Two Pointers、Greedy |
| **Merge / Reuse** | 哪些等价计算只做一次？Which equivalent computations can be done once? | Memoization、DP、Prefix Sum |
| **Decompose / Combine** | 如何拆分并组合？How can work be split and combined? | Recursion、Merge Sort、Divide & Conquer |
| **Compress / Transform** | 哪个较小表示仍充分？Which smaller representation remains sufficient? | Reachability boundary、Rolling array |
| **Organize / Maintain** | 如何降低访问、更新和聚合成本？How can access, update, and aggregation costs fall? | Hash、Heap、BST、LRU、Segment Tree |

这五类并不互斥。二分需要单调谓词，也需要可随机访问；单调队列同时使用支配、数据组织和摊还分析。

These five categories are not mutually exclusive. Binary Search needs a monotone predicate and random access; a monotonic queue combines dominance, data organization, and amortized analysis.

## 正确性不是效率 (Correctness Is Not Efficiency)

**不变量（Invariant）**支持正确性证明，但不自动带来速度。一个 $O(n^2)$ 算法也可以拥有完美的不变量。

**不变量（Invariant）** supports a correctness proof but does not automatically create speed. An $O(n^2)$ algorithm can have a perfect invariant.

效率来自额外理由：每次排除多少候选、每个状态计算几次、哪些工作被摊还，或访问某个信息需要多少成本。

Efficiency comes from additional reasons: how many candidates each step excludes, how often each state is computed, what work is amortized, or what it costs to access information.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> “剪枝像修剪花园”只是类比；真正的机制是候选空间的包含关系和安全排除证明。  
> “Pruning resembles trimming a garden” is only an analogy; the actual mechanism is containment in the candidate space plus a proof of safe exclusion.

## 算法与数据结构的职责 (Responsibilities of Algorithms and Data Structures)

算法规定计算与决策顺序；数据结构规定充分信息如何被表示、索引、更新和访问。

Algorithms specify computation and decision order; data structures specify how sufficient information is represented, indexed, updated, and accessed.

例如，Daily Temperatures 首先通过“未解决状态”识别可删除信息，再证明这些状态温度非递增，最后才选择 Stack。Stack 不是结论的来源，而是这些数学性质的实现载体。

For Daily Temperatures, one first identifies disposable resolved states, then proves the remaining temperatures are non-increasing, and only then selects a Stack. The Stack is not the source of correctness; it implements the established properties.

## 从 Brute Force 开始 (Start from Brute Force)

Brute Force 不应被羞辱；它先建立正确的语义基线。

Brute Force should not be shamed; it first establishes a correct semantic baseline.

1. **列出所有状态和转移**。List every state and transition.
2. **验证完整而可终止**。Verify completeness and termination.
3. **寻找重复、被支配状态和共享查询**。Find repetition, dominated states, and shared queries.
4. **证明压缩仍相对于目标充分**。Prove that compression remains sufficient for the target.
5. **分析实现的最坏或期望成本**。Analyze worst-case or expected implementation costs.

## 边界与反例 (Boundary and Counterexample)

- Binary Search 的边界不是“数组排好序就永远有效”；还需要单调谓词与中点访问。Binary Search requires a monotone predicate and usable midpoint access.
- Rolling array 有效仅当未来只依赖有限邻近状态。A rolling array works only when the future depends on a bounded state neighborhood.
- 随机化可以改变期望性能，却不自动消除对抗性最坏情况。Randomization can change expected performance without necessarily eliminating adversarial worst cases.

> **一句话总结（One-Line Summary）**：  
> 先确定问题真正需要什么信息，再利用数学结构找到充分表示，并证明哪些工作可被消除、复用、分解、压缩或组织。  
> First determine what information the problem truly requires, then use mathematical structure to find a sufficient representation and prove which work can be eliminated, reused, decomposed, compressed, or organized.

## 章节导航 (Navigation)

👉 **下一章：[第2章：不变量与正确性](Volume2_02_Chapter02_Invariants_Correctness.md)**
