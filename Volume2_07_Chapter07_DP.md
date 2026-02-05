# 第七章：动态规划 (Dynamic Programming) —— 状态的流变
# Chapter 07: Dynamic Programming — The Flux of State

> "Those who cannot remember the past are condemned to repeat it."  
> —— Dynamic Programming Motto

很多初学者觉得 DP 是玄学：突然画个表，填几个数，答案就出来了。
在 Volume II 中，我们要去魅：**DP 本质上就是有向无环图 (DAG) 上的最短/最长路径问题。**

Many beginners find DP mystical: suddenly draw a table, fill in a few numbers, and the answer appears.
In Volume II, we want to demystify it: **DP is essentially a Shortest/Longest Path problem on a Directed Acyclic Graph (DAG).**

## 一、DP 的解剖学
## I. Anatomy of DP

任何 DP 算法都由三个核心组件构成，缺一不可：
Any DP algorithm is composed of three core components, none of which can be dispensed with:

1.  **State Definition (状态定义)**：即 DAG 中的**节点**。
    *   **State Definition**: The **Node** in the DAG.
    *   `dp[i]` 到底代表什么物理意义？是“前 i 个物品的最大价值”，还是“以第 i 个字符结尾的最长长度”？
    *   What exactly does `dp[i]` represent physically? Is it "the max value of the first i items" or "the longest length ending at the i-th character"?
    *   这是不变性 (Invariant) 的载体。
    *   This is the carrier of the Invariant.
2.  **Transition Equation (状态转移方程)**：即 DAG 中的**边**。
    *   **Transition Equation**: The **Edge** in the DAG.
    *   节点之间如何推导？`dp[i] = max(dp[i-1], dp[i-2] + val)`。
    *   How to derive between nodes? `dp[i] = max(dp[i-1], dp[i-2] + val)`.
3.  **Base Case (边界)**：即 DAG 的**起点**。
    *   **Base Case**: The **Start Point** of the DAG.

## 二、从递归到 DP
## II. From Recursion to DP

回想第四章的递归。
递归是**自顶向下 (Top-Down)**：我想解决 `f(10)`，所以我先问 `f(9)`。
DP 是**自底向上 (Bottom-Up)**：我先算 `f(1)`，再算 `f(2)` ... 最后算出 `f(10)`。

Recall Recursion from Chapter 4.
Recursion is **Top-Down**: I want to solve `f(10)`, so I first ask `f(9)`.
DP is **Bottom-Up**: I verify `f(1)` first, then calculate `f(2)` ... and finally calculate `f(10)`.

它们计算的**拓扑顺序 (Topological Order)** 是一模一样的，只是方向不同。
Their **Topological Order** of computation is exactly the same, only the direction differs.

### 案例：爬楼梯 (Climbing Stairs)
### Case Study: Climbing Stairs

*   **状态**：`dp[i]` 表示到达第 $i$ 阶的方法总数。
    *   **State**: `dp[i]` represents the total number of ways to reach the $i$-th step.
*   **不变量**：要到达 $i$，最后一步要么是跨 1 步（来自 $i-1$），要么跨 2 步（来自 $i-2$）。没有第三种路。
    *   **Invariant**: To reach $i$, the last step was either 1 step (from $i-1$) or 2 steps (from $i-2$). There is no third way.
*   **方程**：`dp[i] = dp[i-1] + dp[i-2]`。
    *   **Equation**: `dp[i] = dp[i-1] + dp[i-2]`.

这看起来像斐波那契数列？是的。但请注意**空间优化**。
既然 `dp[i]` 只依赖 `i-1` 和 `i-2`，我们不需要保留整个数组。
这又是 **Pair Cancellation** 思想的变体：旧的历史如果对未来无影响，就该被遗忘。

Does this look like the Fibonacci sequence? Yes. But please note the **Space Optimization**.
Since `dp[i]` only depends on `i-1` and `i-2`, we don't need to keep the entire array.
This is again a variant of the **Pair Cancellation** idea: If old history has no effect on the future, it should be forgotten.

```python
def climbStairs(n):
    if n <= 2: return n
    
    # Init (Base Case)
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        # State Transition
        curr = prev1 + prev2
        
        # Forget History (Space Optimization)
        prev2 = prev1
        prev1 = curr
        
    return prev1
```

## 三、背包问题的视角
## III. Perspective of the Knapsack Problem

**0/1 背包问题**是 DP 的试金石。
`dp[i][w]`：前 `i` 个物品，放入容量 `w` 的背包，最大价值。

**0/1 Knapsack Problem** is the touchstone of DP.
`dp[i][w]`: Max value of putting the first `i` items into a backpack of capacity `w`.

这里有个关键的**二元决策 (Binary Decision)**：
对于第 `i` 个物品：
Here represents a key **Binary Decision**:
For the `i`-th item:

1.  **不选**：价值继承自 `dp[i-1][w]`。
    *   **Not Pick**: Value inherited from `dp[i-1][w]`.
2.  **选**：价值变大 `val[i]`，但容量要预留 `weight[i]`，所以找 `dp[i-1][w - weight[i]]`。
    *   **Pick**: Value increases by `val[i]`, but capacity must reserve `weight[i]`, so we look for `dp[i-1][w - weight[i]]`.

方程就是在这两条“边”中选最大值。
The equation simply selects the maximum value between these two "edges".

**空间压缩 (Space Optimization)**：
你可以把二维表压成一维 `dp[w]`。
但必须**倒着遍历**容量。为什么？
**不变性维护**！

**Space Optimization**:
You can compress the 2D table into 1D `dp[w]`.
But you must iterate capacity **backwards**. Why?
**Invariant Maintenance**!

当我们计算 `dp[w]` 时，我们需要的是“上一轮（未放入物品 i）”的 `dp[w-weight]`。
When we calculate `dp[w]`, we need the `dp[w-weight]` from the "previous round (without item i)".

*   正序遍历：`dp[w-weight]` 已经被这一轮更新过了（意味着物品 i 可能被放了两次 -> 变成了完全背包）。
    *   Forward traversal: `dp[w-weight]` has already been updated in this round (meaning item i might be placed twice -> becomes Unbounded Knapsack).
*   倒序遍历：`dp[w-weight]` 还是上一轮的值（确保物品 i 只被用一次）。
    *   Backward traversal: `dp[w-weight]` is still the value from the previous round (ensuring item i is used only once).

你看，连遍历顺序都是由**不变性**严格推导出来的，而不是试出来的。
You see, even the traversal order is strictly derived from the **Invariant**, not found by trial and error.

## 四、总结
## IV. Summary

做 DP 题，不要上来就画表格。
先画**状态转移图**。

When doing DP problems, don't start by drawing a table.
Draw the **State Transition Diagram** first.

1.  我的**状态**够不够描述当前局面？（如果不够，就是由**推导性不足 (Lack of Markov Property)**，需要加维度）。
    *   Does my **State** adequately describe the current situation? (If not, it's due to **Lack of Markov Property**, and dimensions need to be added).
2.  我的**转移**是否覆盖了所有可能性 (MECE 原则)?
    *   Does my **Transition** cover all possibilities (MECE principle)?
