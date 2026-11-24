# 第5章：等价状态与计算复用 (Equivalent States and Reuse)

> "Do not repeat the calculation whose consequences are already known."  
> “不要重复计算已经知道结果的事情。”  
> —— Volume II Editorial Note

为什么两条不同决策路径可能汇入同一个子问题？当所有可影响未来的因素只剩相同摘要时，重复路径就不必重复计算。

Why can two different decision paths converge on the same subproblem? When the same summary contains all factors that can affect the future, repeated paths need not repeat computation.

## DP 的核心不是二维表 (The Core of DP Is Not a Table)

**状态等价（State Equivalence）**意味着两个完整历史对所有未来转移和目标产生相同答案，因此可由同一充分状态表示。

**状态等价（State Equivalence）** means that two complete histories yield the same answers for all future transitions and objectives, so one sufficient state can represent them both.

DP 通常需要：

DP usually requires:

1. 一个足够描述未来的状态定义。A state definition sufficient for the future.
2. 覆盖最后一步或所有选择的转移。A transition covering every relevant final step or choice.
3. 基础情形与无效状态。Base cases and invalid states.
4. 不产生环的计算顺序或记忆化递归。An acyclic computation order or memoized recursion.

DP 不是只在 DAG 上求最短或最长路。DAG 是许多 bottom-up DP 的执行视图，但 DP 也可以计数、求概率、判定可行性、枚举组合值，或通过非路径型递推复用结果。

DP is not only shortest or longest path on a DAG. A DAG is an execution view of many bottom-up DPs, but DP may count, compute probabilities, test feasibility, aggregate combinations, or reuse non-path recurrences.

## Coin Change：金额作为充分状态 (Coin Change: Amount as a Sufficient State)

若硬币可重复使用，剩余金额足以决定未来；过去如何得到该金额对之后无影响。

If coins are reusable, the remaining amount determines the future; how that amount was reached no longer matters.

$$
dp[x]=1+\min_{c\in C,\ c\le x,\ dp[x-c]<\infty}dp[x-c].
$$

```python
def coin_change(coins: list[int], amount: int) -> int:
    infinity = amount + 1
    dp = [infinity] * (amount + 1)
    dp[0] = 0
    for value in range(1, amount + 1):
        for coin in coins:
            if 0 < coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)
    return -1 if dp[amount] == infinity else dp[amount]
```

**正确性**：按金额递增时，每个候选最后一步都来自已计算的较小金额，且全部可用硬币被检查。  
**Correctness**: increasing amounts ensure that every candidate last step uses a previously computed smaller amount and every allowed coin is checked.

**复杂度**：$O(A\cdot |C|)$ 时间，$O(A)$ 空间。  
**Complexity**: $O(A\cdot |C|)$ time and $O(A)$ space.

## Memoization 与 Bottom-Up (Memoization and Bottom-Up)

Memoization 按需求访问子问题；Bottom-Up 按拓扑顺序预先求值。两者共享状态复用的机制，只是调度策略不同。

Memoization visits demanded subproblems; Bottom-Up evaluates a topological order. Both reuse states but use different scheduling strategies.

若某些状态永不需要，Memoization 可能更省；若全部状态都需要且顺序已知，Bottom-Up 通常更少递归开销。

If some states are never needed, Memoization may save work; if all states are needed and the order is known, Bottom-Up often avoids recursion overhead.

## 0/1 背包与依赖顺序 (0/1 Knapsack and Dependency Order)

状态 `dp[i][w]` 保留前 `i` 个物品和容量 `w` 的最优价值。压缩为一维时，容量倒序保证读取的是上一层状态，不会重复使用当前物品。

State `dp[i][w]` retains optimal value for the first `i` items and capacity `w`. In a one-dimensional compression, descending capacity reads the previous layer and cannot reuse the current item.

```python
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for remaining in range(capacity, weight - 1, -1):
            dp[remaining] = max(dp[remaining], dp[remaining - weight] + value)
    return dp[capacity]
```

## Rolling Array 不是 Pair Cancellation (A Rolling Array Is Not Pair Cancellation)

Rolling array 删除的是未来依赖集合之外的历史表示，而不是让两个值相互抵消。

A rolling array discards historical representations outside the future dependency set; it does not cancel two values against each other.

只有当未来转移只依赖有限层次时，才可把 `O(n)` 或 `O(nm)` 降到常数层空间；若查询需回溯路径，仍应保留父指针或其他恢复信息。

Space can fall to a constant number of layers only when transitions depend on bounded layers; reconstructing paths still requires parent pointers or other recovery information.

## 边界与反例 (Boundary and Counterexample)

- 若下标相同但手中优惠券、买卖状态或温度不同，索引不是充分状态。  
  If coupon, trade state, or temperature differs despite equal indices, the index alone is not sufficient.
- 有环的 Memoization 需要识别访问状态或特殊求值规则，否则递归不会终止。  
  Memoization over cycles needs visiting-state detection or another evaluation rule, otherwise recursion may not terminate.
- “旧历史无影响”必须相对于查询证明；不能只因当前状态看似相同便丢弃。  
  “Old history has no effect” must be proved relative to the query; apparent current similarity alone is insufficient.

> **一句话总结（One-Line Summary）**：  
> DP 通过充分状态合并等价历史，复用而不必重复探索相同未来。  
> DP merges equivalent histories through sufficient states and reuses, rather than repeatedly explores, the same future.

## 章节导航 (Navigation)

👈 **上一章：[第4章：支配关系与候选淘汰](Volume2_04_Chapter04_Dominance_Monotonic_Structures.md)**  
👉 **下一章：[第6章：递归、分解与归纳](Volume2_06_Chapter06_Recursion_Decomposition.md)**
