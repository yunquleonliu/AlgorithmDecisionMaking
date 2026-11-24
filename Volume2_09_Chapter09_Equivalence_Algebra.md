# 第9章：等价类与代数结构 (Equivalence Classes and Algebraic Structure)

> "A compact representation earns its place by preserving the operation that matters."  
> “紧凑表示以保留真正重要的操作为代价赢得位置。”  
> —— Original epigraph

为什么并查集能只保留代表元，前缀和能从两个端点恢复区间？因为查询由等价关系、结合律或逆元允许的操作决定。

Why can Union-Find retain only representatives, and Prefix Sum recover an interval from two endpoints? Because the query is permitted by equivalence, associativity, or an inverse operation.

## 等价类与 Union-Find (Equivalence Classes and Union-Find)

连通性是自反、对称、传递的等价关系。对于“是否连通”查询，组件代表元是充分表示。

Connectivity is a reflexive, symmetric, transitive equivalence relation. For connectivity queries, component representatives are sufficient.

```python
class DisjointSet:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, left: int, right: int) -> None:
        left, right = self.find(left), self.find(right)
        if left == right:
            return
        if self.rank[left] < self.rank[right]:
            left, right = right, left
        self.parent[right] = left
        if self.rank[left] == self.rank[right]:
            self.rank[left] += 1
```

不变量是：`find(u)==find(v)` 当且仅当已加入边使 `u` 与 `v` 连通。路径压缩与按秩合并使操作接近 $O(\alpha(n))$ 均摊。

The invariant is that `find(u)==find(v)` exactly when prior union edges connect `u` and `v`. Path compression and union by rank yield nearly $O(\alpha(n))$ amortized operations.

Union-Find 不回答最短路，也通常不支持任意删边；那超出了其充分表示。

Union-Find does not answer shortest paths and normally does not support arbitrary edge deletion; those exceed its sufficient representation.

## Prefix Sum：结合律与逆元 (Prefix Sum: Associativity and Inverses)

对于静态区间和：

For static range sums:

$$
\sum_{k=l}^{r}a[k]=P[r+1]-P[l].
$$

预计算 $O(n)$，查询 $O(1)$。加法的结合律允许预聚合；加法逆元允许从前缀中减去左部。

Preprocessing takes $O(n)$ and a query $O(1)$. Associativity permits pre-aggregation; additive inverses allow the left part to be removed.

若操作只有结合律没有逆元，如 `min`，不能用 `P[r]-P[l]` 恢复区间；Segment Tree 等保留分层聚合的表示更合适。

If an operation is associative but lacks an inverse, such as `min`, `P[r]-P[l]` cannot recover a range; a Segment Tree or another hierarchical aggregate is better.

## Pair Cancellation：有限度摘要 (Pair Cancellation: A Finite-Order Summary)

Pair Cancellation 仅在抵消后问题查询不变时成立。

Pair Cancellation applies only when the query remains unchanged after cancellation.

### Boyer-Moore Voting (多数投票)

当多数值出现次数超过 $n/2$，一个多数值与一个不同值抵消后，多数性质仍保留；两个非多数值抵消也不会使真正多数消失。

When a value occurs more than $n/2$ times, canceling it with a different value preserves the majority property; canceling two non-majority values cannot remove the true majority.

```python
def majority_candidate(values: list[int]) -> int:
    if not values:
        raise ValueError("values must be nonempty")
    candidate, count = values[0], 1
    for value in values[1:]:
        if count == 0:
            candidate = value
            count = 1
        elif value == candidate:
            count += 1
        else:
            count -= 1
    return candidate
```

若题目只保证“最多出现的元素”而不保证严格过半，返回候选还必须第二遍计数验证。

If the input guarantees only “most frequent,” not strict majority, the candidate must be recounted and verified in a second pass.

### XOR (异或)

XOR 利用 $x\oplus x=0$ 和单位元 $0$，可提取恰有一个出现奇数次的值，前提是其他元素出现偶数次。

XOR uses $x\oplus x=0$ and identity $0$ to extract the sole odd-occurrence value, provided every other value occurs an even number of times.

相同性质并不适用于按任意配对做普通加法，因为 `+` 下不同数不能自动抵消。

The same property does not hold for ordinary addition under arbitrary pairing because different numbers do not automatically cancel under `+`.

### 括号匹配 (Parenthesis Matching)

Valid Parentheses 中，右括号只与最近未匹配的同类型左括号抵消。Stack 因此维护一个充分的未解决前缀；遇到类型不符时立即证明全串无效。

In Valid Parentheses, a closing bracket cancels only the nearest unmatched left bracket of the same type. A Stack therefore maintains a sufficient unresolved prefix; a type mismatch immediately proves the string invalid.

这里 Stack 组织 LIFO 匹配，而不是泛化“所有数据都能配对消除”。

Here the Stack organizes LIFO matching; it does not generalize to arbitrary pairwise cancellation.

## 数据组织与代数 (Data Organization and Algebra)

Segment Tree 利用结合律分层保存区间摘要；Fenwick Tree 利用可加分解保存树状前缀；Hash Key 将规范化对象映射为等价类查询键。

A Segment Tree uses associativity to store hierarchical range summaries; a Fenwick Tree stores additive prefix decompositions; a hash key maps a canonicalized object to an equivalence-class lookup key.

## 边界与反例 (Boundary and Counterexample)

- 连接相同物体的关系不必是等价关系；有方向或成本时，代表元不足。  
  A relation between objects is not always equivalence; with direction or cost, a representative is insufficient.
- Prefix Sum 对浮点误差的精度与整数不同，答案需要考虑数值稳定性。  
  Prefix Sum has different floating-point accuracy concerns than integer arithmetic.
- Rolling array 的空间压缩不是 Pair Cancellation；它依赖依赖图的局部性，不依赖代数逆元。  
  Rolling-array compression is not Pair Cancellation; it relies on dependency locality, not an algebraic inverse.

> **一句话总结（One-Line Summary）**：  
> 等价关系与代数定律决定哪些状态可由代表元或聚合摘要替代。  
> Equivalence relations and algebraic laws determine which states can be replaced by representatives or aggregate summaries.

## 章节导航 (Navigation)

👈 **上一章：[第8章：数据表示与组织成本](Volume2_08_Chapter08_Data_Representation.md)**  
👉 **下一章：[第10章：不确定性下的权衡](Volume2_10_Chapter10_Uncertainty_Tradeoffs.md)**
