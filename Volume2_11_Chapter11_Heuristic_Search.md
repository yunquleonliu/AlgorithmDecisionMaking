# 第11章：启发式与最优性边界 (Heuristics and Optimality Boundaries)

> "A heuristic decides where to look first; a proof decides what result can be claimed."  
> “启发式决定先看哪里；证明决定可以声称什么结果。”  
> —— Original epigraph

为什么看起来更靠近终点的状态应先搜索？因为启发式排序可能减少探索，但最短路仍需与真实已付成本和启发函数的性质一起证明。

Why should a state that looks closer to the goal be explored first? Heuristic ordering may reduce exploration, but shortest-path claims still require paid cost and properties of the heuristic.

## A* 的评价函数 (The A* Evaluation Function)

状态 `n` 的优先级是：

The priority of state `n` is:

$$
f(n)=g(n)+h(n),
$$

其中 `g(n)` 是当前已知最短起点成本，`h(n)` 是对剩余成本的估计。

where `g(n)` is the best known start cost and `h(n)` estimates remaining cost.

若 $h=0$，A* 退化为 Dijkstra。仅按 `h` 排序的是 Greedy Best-First Search，不能一般保证最短路。

If $h=0$, A* reduces to Dijkstra. Ordering only by `h` is Greedy Best-First Search and does not generally guarantee a shortest path.

## 可采纳性与一致性 (Admissibility and Consistency)

**可采纳启发式（Admissible Heuristic）**从不高估真实剩余最优成本：$h(n)\le h^*(n)$。

**可采纳启发式（Admissible Heuristic）** never overestimates the true remaining optimal cost: $h(n)\le h^*(n)$.

**一致启发式（Consistent Heuristic）**满足三角不等式：

**一致启发式（Consistent Heuristic）** satisfies the triangle inequality:

$$
h(n)\le c(n,n')+h(n'),\qquad h(\text{goal})=0.
$$

在非负边权与可采纳启发式下，目标首次从开放集合弹出时可通过图搜索最优性论证得到最短路；允许重新开节点时通常需要谨慎处理已关闭状态。使用一致启发式可简化这一保证。

With nonnegative edge costs and an admissible heuristic, a goal's first extraction from the open set can support an optimality argument; reopening closed nodes needs care. Consistency simplifies the guarantee.

```python
import heapq
from collections.abc import Callable

def a_star(
    start: tuple[int, int],
    goal: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[tuple[int, int], float]]],
    heuristic: Callable[[tuple[int, int]], float],
) -> tuple[float, list[tuple[int, int]]] | None:
    best = {start: 0.0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    frontier = [(heuristic(start), 0.0, start)]
    while frontier:
        _, cost, node = heapq.heappop(frontier)
        if cost != best[node]:
            continue
        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return cost, list(reversed(path))
        for neighbor, edge_cost in neighbors(node):
            if edge_cost < 0:
                raise ValueError("A* requires nonnegative edge costs")
            candidate = cost + edge_cost
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                parent[neighbor] = node
                heapq.heappush(frontier, (candidate + heuristic(neighbor), candidate, neighbor))
    return None
```

## 可用启发函数的几何例子 (Geometric Heuristics)

在只允许四方向、每步成本 1 的网格中，Manhattan Distance 通常可采纳；只允许八方向且对角线成本 1 时，Chebyshev Distance 通常可采纳。

On a four-neighbor unit-cost grid, Manhattan Distance is usually admissible; on an eight-neighbor unit-diagonal grid, Chebyshev Distance is usually admissible.

当墙、地形成本或动作集合改变，简单几何距离仍必须重新验证。

When walls, terrain costs, or legal actions change, a geometric distance must be revalidated.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> A* 可类比为“已有事实加未来估计”，但它不是离散 SGD。A* 是对状态图使用优先队列的最短路搜索；SGD 依赖连续梯度和采样更新。A* 的最优性来自启发函数条件，不来自 SGD 收敛理论。  
> A* may be compared to combining past facts with future estimates, but it is not discrete SGD. A* is priority-ordered graph search; SGD uses continuous gradients and sampled updates. A* optimality follows from heuristic conditions, not SGD convergence.

## 边界与反例 (Boundary and Counterexample)

- 不可采纳启发式可能让目标过早弹出，产生非最短路。An inadmissible heuristic may make a goal pop early and yield a non-shortest path.
- 稀有解但启发式差时，额外排序仍不能避免近乎穷举。A poor heuristic does not prevent near-exhaustive exploration.
- 加大 `h` 权重可加速找到某条路径，但会改变普通 A* 的最优保证；Weighted A* 需按其另一个界声明结果。  
  Increasing heuristic weight may speed finding a path but changes ordinary A* optimality; Weighted A* must state its different bound.

> **一句话总结（One-Line Summary）**：  
> 启发式影响探索顺序；可采纳性与一致性等条件决定能否把排序变成最优性证明。  
> A heuristic changes exploration order; admissibility and consistency determine whether ordering becomes an optimality proof.

## 章节导航 (Navigation)

👈 **上一章：[第10章：不确定性下的权衡](Volume2_10_Chapter10_Uncertainty_Tradeoffs.md)**  
👉 **下一章：[第12章：有限资源与反馈控制](Volume2_12_Chapter12_Feedback_Control.md)**
