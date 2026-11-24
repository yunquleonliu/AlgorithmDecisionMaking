# 第8章：数据表示与组织成本 (Data Representation and Organization Cost)

> "Choose the representation whose maintained invariant makes the required operation cheap."  
> “选择一个被维护的不变量能让所需操作变便宜的表示。”  
> —— Original epigraph

数据结构不只是“强制单调性”。它还改变定位、聚合、更新、顺序、淘汰与访问成本。

A data structure does more than enforce monotonicity. It changes the costs of lookup, aggregation, update, ordering, eviction, and access.

## 数据结构契约 (The Data-Structure Contract)

设计数据结构要回答四个问题：

Designing a data structure answers four questions:

1. **Supported Operations**：必须支持哪些 API？Which APIs must be supported?
2. **Invariant**：内部表示始终承诺什么？What does the internal representation always promise?
3. **Maintenance Cost**：每次操作修复不变量的成本？What does each operation cost to restore its invariant?
4. **Guarantee Type**：是最坏、摊还还是期望复杂度？Is the complexity worst-case, amortized, or expected?

## Heap：只组织必要偏序 (Heap: Maintaining Only the Needed Partial Order)

二叉 Heap 不维护全序；其父节点优先级不低于或不高于子节点，且移除、插入可通过 sift 恢复。

A binary Heap does not maintain total order; a parent has priority over its children, and insertions and removals restore this with sift operations.

- `peek` 为 $O(1)$。`peek` is $O(1)$.
- `push` 与 `pop` 为 $O(\log n)$ 最坏时间。`push` and `pop` take $O(\log n)$ worst-case time.
- 任意删除通常为 $O(n)$，除非另有索引。Arbitrary deletion is usually $O(n)$ unless indexed.

## Hash：定位而非排序 (Hash: Lookup Rather Than Order)

Hash Table 以分桶或开放寻址将键映射到位置。常见操作期望 $O(1)$，但哈希碰撞、扩容和对抗输入会影响保证。

A Hash Table maps keys to locations through buckets or open addressing. Common operations are expected $O(1)$, but collisions, resizing, and adversarial inputs affect guarantees.

Hash 适合精确键查找，却不天然支持前驱、后继或范围聚合；有序树或平衡索引更适合那些查询。

Hash supports exact-key lookup but not natural predecessor, successor, or range aggregation; ordered trees or balanced indexes suit those queries better.

## LRU：复合表示与访问成本 (LRU: Composite Representation and Access Cost)

LRU 需要同时做到常量时间查找和任意节点常量时间移动，因此组合 Hash Map 与 Doubly Linked List。

LRU needs both constant-time lookup and constant-time relocation of an arbitrary node, so it combines a Hash Map with a Doubly Linked List.

不变量是：

The invariants are:

- 字典中的每个键恰好指向链表一个节点。Every dictionary key points to exactly one list node.
- 链表头到尾按最近使用到最久未用排序。The list runs from most to least recently used.
- 节点数不超过 `capacity`。The node count does not exceed `capacity`.

`get` 也是写操作，因为访问后必须移动节点。

`get` is also a write operation because it relocates the accessed node.

```python
class Node:
    def __init__(self, key: int, value: int):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes: dict[int, Node] = {}
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev, self.head.next = node, node

    def get(self, key: int) -> int:
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.nodes:
            self._remove(self.nodes[key])
            del self.nodes[key]
        node = Node(key, value)
        self.nodes[key] = node
        self._add_front(node)
        if len(self.nodes) > self.capacity:
            victim = self.tail.prev
            self._remove(victim)
            del self.nodes[victim.key]
```

在正常 Hash Map 假设下，`get` 与 `put` 期望 $O(1)$，最坏情况还需看具体哈希实现。

Under the ordinary Hash Map assumptions, `get` and `put` are expected $O(1)$; worst-case behavior depends on hashing.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> LRU 像有限注意力，但它不是 Attention Mechanism：LRU 按确定性访问时间淘汰整个键值；Attention 对内容计算连续权重。  
> LRU resembles limited attention, but it is not Attention Mechanism: LRU deterministically evicts whole key-value entries by access time, while Attention computes continuous weights from content.

## 预处理、更新与查询 (Preprocessing, Updates, and Queries)

Prefix Sum 用 $O(n)$ 预处理换静态 $O(1)$ 区间和；修改频繁时该维护成本可能不划算，Segment Tree 或 Fenwick Tree 更合适。

Prefix Sum trades $O(n)$ preprocessing for static $O(1)$ range sums; with frequent updates, a Segment Tree or Fenwick Tree may be better.

## 边界与反例 (Boundary and Counterexample)

- `capacity=0` 的 LRU 不能直接插入后再按同一逻辑读取；必须拒绝或立即淘汰。  
  LRU with `capacity=0` must reject insertion or evict immediately.
- Hash 的期望复杂度不能被写成无条件最坏 $O(1)$。Expected Hash complexity is not unconditional worst-case $O(1)$.
- Heap 顶端不代表任意范围的聚合信息；组织越强，维护通常越贵。A Heap top is not an arbitrary range aggregate; stronger organization generally costs more to maintain.

> **一句话总结（One-Line Summary）**：  
> 数据结构选择的是表示和操作成本；不变量保证含义，复杂度声明还必须指明保证类型。  
> A data structure chooses representation and operation costs; invariants preserve meaning, and complexity claims must state the type of guarantee.

## 章节导航 (Navigation)

👈 **上一章：[第7章：图、前沿与可达性](Volume2_07_Chapter07_Graph_Frontier_Reachability.md)**  
👉 **下一章：[第9章：等价类与代数结构](Volume2_09_Chapter09_Equivalence_Algebra.md)**
