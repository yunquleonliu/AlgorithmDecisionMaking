# 第13章：从问题结构推导算法 (Deriving Algorithms from Structure)

> "Patterns are useful after the premises have been checked."  
> “模式有用，前提是其假设已经被检验。”  
> —— Original epigraph

遇到新问题时，怎样避免先猜模板？把每个设计决定连接到问题语义、必要信息、数学结构、正确性和资源成本。

When facing a new problem, how can template guessing be avoided? Tie every design decision to semantics, required information, mathematical structure, correctness, and resource cost.

## 八步工作流 (An Eight-Step Workflow)

1. **描述语义**：写出输入、输出、合法操作、约束与目标。  
   **State semantics**: write inputs, outputs, legal operations, constraints, and objective.
2. **建立 Brute Force**：定义完整状态空间与转移，证明基线可行。  
   **Build Brute Force**: define the complete state space and transitions, and prove a baseline.
3. **压缩信息需求**：区分完整路径、最优值、判定、统计与恢复要求。  
   **Compress the information requirement**: distinguish path, optimum, decision, aggregate, and reconstruction.
4. **寻找数学结构**：序、单调、支配、等价、结合、守恒、连续、凸性。  
   **Find mathematical structure**: order, monotonicity, dominance, equivalence, associativity, conservation, continuity, convexity.
5. **证明充分表示**：对每个未来查询，当前摘要足够。  
   **Prove a sufficient representation**: the current summary suffices for every future query.
6. **选择优化机制**：消除、复用、分解、压缩、变换、组织或近似。  
   **Choose an optimization mechanism**: eliminate, reuse, decompose, compress, transform, organize, or approximate.
7. **选择算法和数据结构**：满足操作集与保证类型。  
   **Choose algorithm and data structure**: satisfy operations and guarantee types.
8. **证明与设边界**：Correctness、Complexity、Counterexample。  
   **Prove and bound**: Correctness, Complexity, Counterexample.

## 复盘一：Daily Temperatures (Review 1: Daily Temperatures)

| 阶段 (Stage) | 结论 (Conclusion) |
| :--- | :--- |
| Information Requirement | 只需第一个严格更高温度。Only the first strictly higher temperature. |
| Sufficient Representation | 未解决位置集合。The unresolved-index set. |
| Generic Organization | 平衡树可给出 $O(n\log n)$。A balanced tree gives $O(n\log n)$. |
| Derived Structure | 未解决温度非递增。Unresolved temperatures are non-increasing. |
| Specialized Structure | Stack 尾部批量处理。A Stack handles a suffix in batches. |
| Proof | 不变量 + 每元素一次出入栈。Invariant + one push and at most one pop. |

## 复盘二：Jump Game II (Review 2: Jump Game II)

| 阶段 (Stage) | 结论 (Conclusion) |
| :--- | :--- |
| State Space | 位置与合法跳跃形成无权 DAG。Positions and legal jumps form an unweighted DAG. |
| Baseline | DFS / DP / BFS 可得正确答案。DFS / DP / BFS can produce a correct result. |
| Structure | 最多 `k` 跳可达集合是连续前缀。At most `k` jumps reaches a contiguous prefix. |
| Sufficient Representation | 前缀最远边界。The farthest prefix boundary. |
| Mechanism | 按层压缩 BFS frontier。Compress the BFS frontier by level. |
| Proof | 归纳保证边界准确，层数为首次覆盖终点。Induction proves the boundary and first-covering layer. |

## 复盘三：LRU (Review 3: LRU)

LRU 的数学问题不是 Attention，而是维护最近使用顺序。Hash Map 提供键定位，Doubly Linked List 提供任意节点 $O(1)$ 移动；两者共同满足 API。

The mathematical LRU problem is not Attention but maintaining recency order. Hash Map supplies key lookup and a Doubly Linked List supplies $O(1)$ node relocation; together they satisfy the API.

## 设计审查表 (Design Review Checklist)

- 输出下界是否已被考虑？Has the output lower bound been considered?
- 是否把状态等价误当成当前值相等？Was state equivalence confused with equal current values?
- 不变量只证明正确，效率是否有独立理由？The invariant proves correctness; is there a separate efficiency argument?
- 数据结构满足的是精确、期望还是摊还成本？Does the data structure claim exact, expected, or amortized cost?
- 哪个前提消失时算法失败？Which missing premise breaks the algorithm?
- 哪句话是机制，哪句话只是 Analogy？Which statement is mechanism and which is only analogy?

## 为什么模板仍然有用 (Why Patterns Still Matter)

模板压缩经验，并不是压缩证明。识别出 Binary Search、BFS 或 Heap 后，仍应迅速检查本题是否具备单调谓词、无权层、非负边、所需优先级等前提。

Templates compress experience, not proof. After recognizing Binary Search, BFS, or Heap, still check the monotone predicate, unweighted levels, nonnegative edges, or required priority assumptions.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> 现实决策类比可以降低学习门槛，但只能在机制、保证和反例之后使用，不能替代它们。  
> A real-world analogy can lower the learning barrier, but it belongs after mechanism, guarantees, and counterexamples—not in their place.

> **一句话总结（One-Line Summary）**：  
> 算法设计是从语义证明一种充分表示，再为该表示选择可证明正确且成本合适的操作。  
> Algorithm design proves a sufficient representation from semantics, then selects provably correct operations with an appropriate cost for that representation.

## 章节导航 (Navigation)

👈 **上一章：[第12章：有限资源与反馈控制](Volume2_12_Chapter12_Feedback_Control.md)**  
👉 **下一章：[终章：从计算者到设计者](Volume2_14_Epilogue.md)**
