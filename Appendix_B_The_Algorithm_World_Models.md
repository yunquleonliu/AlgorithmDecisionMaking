# 附录 B：算法世界观模型 (Appendix B: The Algorithm World Models)

> 目的：给出一套**长期可复用的算法认知框架**，统一理解 Greedy / 分治 / DP / 随机化 等算法思想，以及它们在不同“世界模型”中的位置。
> Purpose: To provide a **long-term reusable cognitive framework for algorithms**, unifying the understanding of algorithmic ideas such as Greedy / Divide and Conquer / DP / Randomization, and their positions in different "World Models".

---

## 一、算法的五个“世界模型”（World Models）
## I. The Five "World Models" of Algorithms

这五个世界不是算法本身，而是**问题与计算的自然形态**。
These five worlds are not the algorithms themselves, but **the natural forms of problems and computation**.

### 1. 图世界（Graph / Dependency World）
- 核心：**依赖、先后顺序、可达性**
    - Core: **Dependency, Order, Reachability**
- 抽象：节点 = 状态，边 = 转移/依赖
    - Abstraction: Node = State, Edge = Transition/Dependency
- 典型问题：
    - Typical Problems:
  - DP
  - 搜索 / 回溯 (Search / Backtracking)
  - BFS / DFS / A*
  - 调度、路径、可达性 (Scheduling, Path, Reachability)

> 核心问题：**谁依赖谁？必须先算什么？**
> Core Question: **Who depends on whom? What must be calculated first?**

---

### 2. 代数世界（Algebraic / Transform World）
- 核心：**运算结构、合并、重排、并行**
    - Core: **Operation Structure, Merge, Reorder, Parallelism**
- 抽象：运算 + 运算律（结合律、分配律等）
    - Abstraction: Operation + Laws of Operation (Associativity, Distributivity, etc.)
- 典型问题：
    - Typical Problems:
  - 前缀和、差分 (Prefix Sum, Difference Array)
  - FFT / 卷积 (FFT / Convolution)
  - 矩阵算法 (Matrix Algorithms)
  - 快速幂 (Fast Power)

> 核心问题：**这些计算能不能换个顺序更快算？**
> Core Question: **Can these calculations be done faster by changing the order?**

---

### 3. 几何 / 连续世界（Geometric / Continuous World）
- 核心：**距离、方向、局部信息**
    - Core: **Distance, Direction, Local Information**
- 抽象：点在空间中移动
    - Abstraction: Moving points in space
- 典型问题：
    - Typical Problems:
  - 数值优化 (Numerical Optimization)
  - 凸优化 (Convex Optimization)
  - 梯度下降 (Gradient Descent)
  - 最近邻搜索 (Nearest Neighbor Search)

> 核心问题：**往哪个方向走更接近目标？**
> Core Question: **Which direction gets us closer to the target?**

---

### 4. 概率 / 统计世界（Probabilistic World）
- 核心：**不确定性、分布、期望**
    - Core: **Uncertainty, Distribution, Expectation**
- 抽象：随机变量 + 分布
    - Abstraction: Random Variable + Distribution
- 典型问题：
    - Typical Problems:
  - Monte Carlo
  - 随机算法 (Randomized Algorithms)
  - MCMC
  - 贝叶斯推断 (Bayesian Inference)

> 核心问题：**如何在不确定条件下获得高概率好结果？**
> Core Question: **How to obtain a high-probability good result under uncertain conditions?**

---

### 5. 逻辑 / 约束世界（Logical / Constraint World）
- 核心：**可满足性、规则、约束**
    - Core: **Satisfiability, Rules, Constraints**
- 抽象：约束系统
    - Abstraction: Constraint System
- 典型问题：
    - Typical Problems:
  - SAT / SMT
  - 约束规划 (Constraint Programming)
  - 规则引擎 (Rule Engine)

> 核心问题：**是否存在一个解满足所有约束？**
> Core Question: **Does there exist a solution ensuring all constraints?**

---

## 二、算法思想（Paradigms）与五个世界的映射
## II. Mapping Algorithm Paradigms to the Five Worlds

### 1. Greedy（贪心）

**本质**：
**Essence**:
- 假设问题结构具有**单调性 / 交换性**
    - Assumes problem structure has **Monotonicity / Commutativity**
- 每一步做局部最优选择，不回头
    - Makes locally optimal choice at each step, no backtracking

**主要世界**：
**Primary World**:
- 图世界（特殊 DAG / 调度）
    - Graph World (Special DAG / Scheduling)
- 代数世界（可交换结构）
    - Algebraic World (Commutative Structure)

**成功条件**：
**Success Condition**:
- Matroid
- 区间调度 (Interval Scheduling)
- 连续可拆（Fractional Knapsack）

---

### 2. Divide & Conquer（分治）

**本质**：
**Essence**:
- 把问题拆成**相互独立的子问题**
    - Split problem into **mutually independent subproblems**
- 子问题解可直接合并
    - Subproblem solutions can be directly merged

**主要世界**：
**Primary World**:
- 代数世界（FFT、矩阵）
    - Algebraic World (FFT, Matrix)
- 图世界（树型递归）
    - Graph World (Tree Recursion)

**失败信号**：
**Failure Signal**:
- 子问题共享状态/资源（如标准 Knapsack）
    - Subproblems share state/resources (e.g., standard Knapsack)

---

### 3. Dynamic Programming（动态规划）

**本质**：
**Essence**:
- 合并**等价的中间状态**
    - Merge **equivalent intermediate states**
- 用状态空间代替解空间
    - Replace solution space with state space

**唯一归属世界**：
**Sole Belonging World**:
- **图世界（DAG）**
    - **Graph World (DAG)**

**图解释**：
**Graph Interpretation**:
- 状态 = 节点
    - State = Node
- 转移 = 边
    - Transition = Edge
- DP = DAG 上的最短/最长路径
    - DP = Shortest/Longest Path on DAG

---

### 4. Randomized / Approximation（随机化 / 近似）

**本质**：
**Essence**:
- 放弃确定性或最优性
    - Give up determinism or optimality
- 换取规模与速度
    - Exchange for scale and speed

**主要世界**：
**Primary World**:
- 概率世界
    - Probabilistic World
- 几何世界（扰动 / 邻域）
    - Geometric World (Perturbation / Neighborhood)

**典型方法**：
**Typical Methods**:
- 模拟退火 (Simulated Annealing)
- 遗传算法 (Genetic Algorithm)
- Monte Carlo
- FPTAS

---

## 三、为什么 DP 天然是“图算法”而不是代数算法？
## III. Why is DP naturally a "Graph Algorithm" rather than an "Algebraic Algorithm"?

- DP 的正确性来自：
    - The correctness of DP comes from:
  - 状态依赖 (State Dependency)
  - 先后顺序 (Sequence Order)
- 不能随意重排计算顺序
    - Cannot arbitrarily reorder the calculation sequence

> **DP = 在状态依赖图上按拓扑顺序计算节点值**
> **DP = Calculating node values in topological order on a state dependency graph**

而代数算法：
While algebraic algorithms:
- 正确性来自运算律
    - Correctness comes from operation laws
- 顺序可重排
    - Sequence can be reordered

---

## 四、三种“空间”的严格区分
## IV. Strict Distinction of Three "Spaces"

### 1. 解空间（Solution Space）
- 所有完整合法解的集合
    - The set of all complete legal solutions
- 通常指数级
    - Usually exponential
- 很少直接操作
    - Rarely operated on directly

### 2. 状态空间（State Space）
- 构造解过程中的中间状态
    - Intermediate states working towards solution
- 算法真正运行的空间
    - The space where the algorithm actually runs
- 可建模为图
    - Can be modeled as a graph

### 3. 参数空间（Parameter Space）
- 连续参数集合
    - Set of continuous parameters
- 优化/学习使用
    - Used in optimization/learning
- 几何/连续世界
    - Geometric/Continuous World

---

## 五、统一认知：算法 = 世界模型 × 思想策略
## V. Unified Cognition: Algorithm = World Model × Thought Strategy

| 层级 | 问题 |
|---|---|
| Level | Issue |
| 世界模型 | 问题的自然结构 |
| World Model | Natural structure of the problem |
| 算法思想 | 人的设计策略 |
| Algorithm Paradigm | Human design strategy |
| 执行模型 | 图 / 代数 |
| Execution Model | Graph / Algebra |

> **几乎所有算法，最终都会被编译成：依赖图 或 运算结构**
> **Almost all algorithms are essentially compiled into: Dependency Graphs or Operation Structures**

---

## 六、10 条算法世界观定律
## VI. 10 Laws of Algorithm Worldview

1. 所有算法都在管理解空间
    1. All algorithms are managing the Solution Space.
2. 算法真正运行在状态空间，而不是解空间
    2. Algorithms actually run in the State Space, not the Solution Space.
3. DP 是状态图上的路径问题
    3. DP is a path problem on the state graph.
4. Greedy 成功依赖结构，不依赖聪明
    4. Greedy success depends on structure, not cleverness.
5. 分治要求子问题独立
    5. Divide & Conquer requires independent subproblems.
6. 代数算法允许任意重排
    6. Algebraic algorithms allow arbitrary reordering.
7. 图算法严格受依赖约束
    7. Graph algorithms are strictly constrained by dependencies.
8. 随机化是对规模的妥协
9. 近似是对精度的妥协
10. 工程中，稳定性高于理论最优

---

## 七、终极总结

> **算法思想很多，但计算机只理解两种执行模型：**
> - **依赖图**
> - **运算结构**

> 其他一切，都是人类的抽象层。

