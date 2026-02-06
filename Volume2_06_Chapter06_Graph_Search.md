# 第六章：图搜索 (Graph Search) —— 探索的边界
# Chapter 06: Graph Search — The Boundaries of Exploration

> "Not all those who wander are lost."  
> "流浪者未必迷路。"  
> —— J.R.R. Tolkien

图论算法看起来很难，但如果你把所有图算法剥去外壳，它们都共享同一个内核：**前沿 (Frontier) 的管理**。

Graph theory algorithms look difficult, but if you strip away the shell of all graph algorithms, they all share the same kernel: **Management of the Frontier**.

## 一、隐式图
## I. Implicit Graph

在算法面试中，很少有人直接给你画一幅图。图通常是隐式的：
In algorithm interviews, rarely does anyone draw a graph for you directly. Graphs are usually implicit:

*   **矩阵 (Matrix)**：格子是点，相邻格子有边。
    *   **Matrix**: Cells are nodes, adjacent cells involve edges.
*   **状态机 (State Machine)**：密码锁的状态是点，拨动一下是边。
    *   **State Machine**: The state of a combination lock is a node, toggling it is an edge.
*   **社交网络**：人是点，关注是边。
    *   **Social Network**: People are nodes, following/friending is an edge.

只要涉及“从 A 到 B 的路径”或“联通性”，这就是图论。
As long as it involves "path from A to B" or "connectivity," this is graph theory.

## 二、探索的三种颜色
## II. Three Colors of Exploration

我们可以用三种颜色标记解空间中的节点（这也是经典算法导论 CLRS 的标记法）：
We can mark nodes in the solution space with three colors (this is also the marking method in the classic algorithm textbook CLRS):

1.  **White (未知)**：还没见过的点。
    *   **White (Unknown)**: Points not seen yet.
2.  **Gray (前沿/活跃)**：见到了，但还没检查完它的邻居（在 Queue/Stack 中）。
    *   **Gray (Frontier/Active)**: Seen, but neighbors not yet fully inspected (currently in Queue/Stack).
3.  **Black (已完成)**：彻底探索完的点（Visited）。
    *   **Black (Completed)**: Points fully explored (Visited).

**算法本质**：不断从 **Gray** 集合中拿出一个点，把它的 **White** 邻居变成 **Gray**，然后把自己涂成 **Black**。

**Algorithm Essence**: Constantly take a point from the **Gray** set, turn its **White** neighbors into **Gray**, and then paint itself **Black**.

*   如果 Gray 集合是 **Queue (队列)** -> **BFS (广度优先)** -> 像水波纹一样层层推进。
    *   If the Gray set is a **Queue** -> **BFS (Breadth-First Search)** -> Rippling out layer by layer like water waves.
*   如果 Gray 集合是 **Stack (栈)** -> **DFS (深度优先)** -> 像一条贪吃蛇钻到底。
    *   If the Gray set is a **Stack** -> **DFS (Depth-First Search)** -> Drilling down to the bottom like a snake.

## 三、BFS 与 最短路不变量
## III. BFS and the Shortest Path Invariant

为什么 BFS 能求**无权图**的最短路径？
因为它维护了一个极其严格的 **单调不变量**。

Why can BFS find the shortest path in an **Unweighted Graph**?
Because it maintains an strictly **Monotonic Invariant**.

**BFS Invariant**:
队列中的所有节点，按距离起点的层数（dist）排序。队列中至多只有两层：`k` 层和 `k+1` 层。且 `k` 层都在 `k+1` 层前面。

**BFS Invariant**:
All nodes in the queue are sorted by their layer distance from the start (`dist`). There are at most two layers in the queue: layer `k` and layer `k+1`. And layer `k` is always before layer `k+1`.

因为我们总是先处理完距离为 `k` 的所有点，才可能碰到距离为 `k+1` 的点。所以第一次遇到目标节点时，一定是最短路径。

Because we always process all points at distance `k` before encountering points at distance `k+1`. Therefore, when we encounter the target node for the first time, it must be via the shortest path.

```python
def bfs(start, target):
    queue = deque([start])
    visited = {start}
    step = 0
    
    while queue:
        # Invariant: All nodes in current extraction are at distance 'step'
        size = len(queue)
        for _ in range(size):
            curr = queue.popleft()
            if curr == target: return step
            
            for neighbor in get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        step += 1
    return -1
```

## 四、Dijkstra —— 带权图的贪心不变量
## IV. Dijkstra — The Greedy Invariant of Weighted Graphs

如果有权重怎么办？波纹就不是均匀扩散了。
Dijkstra 算法引入了一个**优先队列 (Priority Queue)**。

What if there are weights? The ripples don't spread uniformly anymore.
Dijkstra's algorithm introduces a **Priority Queue**.

**Dijkstra Invariant**:
我们将节点分为两组：
We divide nodes into two groups:

1.  **S (Settled)**: 已经确定了最短路径的点。
    *   **S (Settled)**: Points for which the shortest path is already determined.
2.  **Q (Queue)**: 还没确定的点。
    *   **Q (Queue)**: Points not yet determined.

**核心性质**：每次从 Q 中选出距离起点最近的点 $u$，那么 $u$ 的最短路径就已经确定了（不可能绕一圈更远的路回来比它还短，假设无负权边）。
所以，一旦节点从 Q 弹出加入 S，它就“结案”了。

**Core Property**: Every time we pick the node $u$ closest to the start from Q, the shortest path to $u$ is determined (it's impossible to take a longer detour and come back shorter than it, assuming no negative weight edges).
So, once a node is popped from Q and added to S, it is "case closed."

## 五、总结
## V. Summary

图搜索算法是在解空间中建立秩序的过程。
**Visited 集合**（或 dist 数组）就是我们的防线，防止我们在解空间中原地打转（死循环）。

Graph search algorithms are the process of establishing order in the solution space.
The **Visited Set** (or dist array) is our line of defense, preventing us from spinning in circles (infinite loops) in the solution space.

设计图算法时，问自己：
When designing graph algorithms, ask yourself:

1.  我的**状态 (Node)** 是什么？
    *   What is my **Node (State)**?
2.  我的**边 (Edge)** 意味着什么操作？
    *   What operation does my **Edge** represent?
3.  我要维护什么样的**前沿 (Frontier)**？
    *   What kind of **Frontier** do I want to maintain?
