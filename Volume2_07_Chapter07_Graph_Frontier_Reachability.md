# 第7章：图、前沿与可达性 (Graphs, Frontiers, and Reachability)

> "A path exists in the state space before it exists in the code."  
> “路径先存在于状态空间，然后才存在于代码。”  
> —— Original epigraph

很多题目没有画出图，却已经由状态和合法操作构成图。先建模，再决定遍历、复用或压缩。

Many problems draw no graph, yet their states and legal operations already form one. Model first, then choose traversal, reuse, or compression.

## 状态图与前沿 (State Graphs and Frontiers)

图节点是状态，边是一次合法转移，边权是本问题定义的成本。**前沿（Frontier）**是已发现、尚未完全处理的状态。

Graph vertices are states, edges are legal transitions, and edge costs are problem-defined costs. **前沿（Frontier）** is the set of discovered states not yet fully processed.

- Queue 产生 BFS 层次顺序，适合无权最短路。A Queue creates BFS level order for unweighted shortest paths.
- Stack 或递归产生 DFS 顺序，适合完备探索与结构检测。A Stack or recursion creates DFS order for complete exploration and structural detection.
- Priority Queue 按已知总代价或估计排序前沿。A Priority Queue orders the frontier by known or estimated total cost.

## BFS、DFS 与 Dijkstra (BFS, DFS, and Dijkstra)

BFS 将边数作为层数；其 Invariant 是队列按起点距离非递减，第一次发现目标即最短。

BFS uses edge count as depth; its invariant is nondecreasing source distance in the queue, so first discovery of the target is shortest.

Dijkstra 适用于非负边权：从所有未确定节点中取 `dist` 最小者，才能断言其最短路已确定。负边会破坏该论证。

Dijkstra supports nonnegative weights: extracting the smallest `dist` among unsettled states supports finalizing it. Negative edges break that argument.

```python
import heapq

def dijkstra(graph: list[list[tuple[int, int]]], source: int) -> list[float]:
    distance = [float("inf")] * len(graph)
    distance[source] = 0
    frontier = [(0, source)]
    while frontier:
        cost, node = heapq.heappop(frontier)
        if cost != distance[node]:
            continue
        for neighbor, weight in graph[node]:
            if weight < 0:
                raise ValueError("Dijkstra requires nonnegative weights")
            candidate = cost + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(frontier, (candidate, neighbor))
    return distance
```

## Jump Game II：可达前缀与前沿压缩 (Jump Game II: Reachable Prefix and Frontier Compression)

在位置 `i`，合法转移是 $i<j\le i+\text{nums}[i]$。所以输入直接定义一个无权 DAG，终点最少跳数是最短路径。

At position `i`, legal transitions satisfy $i<j\le i+\text{nums}[i]$. The input therefore defines an unweighted DAG, and the minimum number of jumps is a shortest path.

DFS 与 DP 都可求解，但可能枚举 $O(n^2)$ 条边；BFS 看似也会枚举全部边。

DFS and DP can solve it but may examine $O(n^2)$ edges; BFS also appears to examine every edge.

### 可达集合是前缀 (Reachable Sets Are Prefixes)

令 $R_k$ 为最多 `k` 跳可达位置。归纳可得：

Let $R_k$ be positions reachable in at most `k` jumps. Induction gives:

$$
R_k=[0,r_k].
$$

基础层是 `R_0={0}`。若 `R_k` 是前缀，每个点的一次跳跃区间都向右延伸并连接原前缀，所以 `R_{k+1}` 仍无空洞。

The base is `R_0={0}`. If `R_k` is a prefix, each one-jump interval from it extends right and joins the existing prefix, so `R_{k+1}` remains hole-free.

因此整个集合只需记录最远边界，建立充分表示：

Thus the complete set needs only its farthest boundary as a sufficient representation:

$$
r_{k+1}
=\min\left(n-1,\max_{0\le i\le r_k}(i+\text{nums}[i])\right).
$$

### 从 BFS 层到一次扫描 (From BFS Layers to One Pass)

`end` 是当前跳数层的边界，`farthest` 是下一层边界。扫描到 `end` 后才增加跳数，这模拟一次完整 BFS 层。

`end` bounds the current jump-count layer and `farthest` bounds the next. Only after scanning `end` is the jump count increased, simulating one complete BFS layer.

```python
def jump(nums: list[int]) -> int:
    if len(nums) <= 1:
        return 0
    jumps = current_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            if farthest == current_end:
                return -1
            jumps += 1
            current_end = farthest
            if current_end >= len(nums) - 1:
                break
    return jumps
```

时间 $O(n)$，额外空间 $O(1)$。它压缩的是当前 BFS frontier，而不是直接押注某个落点。

Time is $O(n)$ and extra space is $O(1)$. It compresses the current BFS frontier, not a wager on one landing point.

> **机制 vs 反例（Mechanism vs Counterexample）**：  
> “每次跳到当前可达的最远点”是错的：`[3,7,1,0,0,0,0,0,0]` 中从 `0` 跳到 `3` 会卡住，跳到 `1` 才可到终点。正确算法贪的是整个当前层能覆盖的下一边界。  
> “Jump to the current farthest point” is false: in `[3,7,1,0,0,0,0,0,0]`, jumping from `0` to `3` gets stuck, while `1` can reach the goal. The correct algorithm maximizes the next boundary covered by the whole current layer.

## 边界与反例 (Boundary and Counterexample)

- 负权图不能直接使用 Dijkstra。Dijkstra does not directly support negative weights.
- 可达前缀依赖每次跳跃可覆盖连续区间；若转移只到离散集合，边界压缩不再自动充分。  
  Prefix compression relies on contiguous jump intervals; it is not sufficient for arbitrary discrete transitions.
- 终点不可达时，最小跳数需返回失败或无穷大，不能沿用“必可达”的循环假设。  
  If the target is unreachable, report failure or infinity rather than assuming reachability.

> **一句话总结（One-Line Summary）**：  
> 图搜索管理前沿；Jump Game II 因可达前缀可把整个前沿压缩为一个边界。  
> Graph search manages a frontier; Jump Game II compresses that frontier to one boundary because reachable states form a prefix.

## 章节导航 (Navigation)

👈 **上一章：[第6章：递归、分解与归纳](Volume2_06_Chapter06_Recursion_Decomposition.md)**  
👉 **下一章：[第8章：数据表示与组织成本](Volume2_08_Chapter08_Data_Representation.md)**
