# 第4章：支配关系与候选淘汰 (Dominance and Candidate Removal)

> "The useful survives because no remaining future can make the discarded alternative better."  
> “有用者留下，因为任何剩余未来都不会让被淘汰者变得更优。”  
> —— Original epigraph

窗口滑动时，是否每个历史元素都值得保留？Daily Temperatures 和 Sliding Window Maximum 的共同答案是：只保留对某个未来查询仍可能胜出的候选。

As a window moves, is every historical element worth retaining? Daily Temperatures and Sliding Window Maximum give the same answer: keep only candidates that can still win for some future query.

## 定义支配 (Defining Dominance)

若候选 `A` 在所有相关未来情形下都不优于候选 `B`，且 `B` 至少活得与 `A` 一样久，就可以安全丢弃 `A`。

If candidate `A` is no better than `B` in every relevant future scenario and `B` lives at least as long, `A` can be discarded safely.

这不是一般的“值更大就更好”；只有明确过期顺序、查询目标和比较方向后，支配证明才完整。

This is not a generic claim that a larger value is better. Dominance is complete only after expiry order, query target, and comparison direction are specified.

## Daily Temperatures：从语义到单调栈 (Daily Temperatures: From Semantics to a Monotonic Stack)

目标是每个 `i` 的第一个严格更高温度：

The target is the first strictly higher temperature for each `i`:

$$
j(i)=\min\{j>i:T[j]>T[i]\}.
$$

### 暴力基线 (Brute-Force Baseline)

每个 `i` 向右搜索，正确但重复，最坏 $O(n^2)$。

Each `i` searches rightward, correctly but repetitively, at worst $O(n^2)$.

### 只保留未解决状态 (Retain Only Unresolved States)

从左向右扫描时，`T[j]` 可以一次解决多个历史下标 `i`；只要它们满足 `T[i]<T[j]`。

While scanning left to right, `T[j]` can resolve several prior indices `i` whenever `T[i]<T[j]`.

`pending` 只保存尚未找到答案的下标。这个充分表示本身不是单调栈；用普通列表维护它仍可能为 $O(n^2)$。

`pending` retains only unresolved indices. This sufficient representation is not yet a monotonic stack; maintaining it in a plain list may still cost $O(n^2)$.

```python
def pending_scan(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    pending: list[int] = []
    for right, current in enumerate(temperatures):
        still_pending = []
        for left in pending:
            if temperatures[left] < current:
                answer[left] = right - left
            else:
                still_pending.append(left)
        pending = still_pending
        pending.append(right)
    return answer
```

用有序 `map` 按温度提取所有小于当前值的集合，可得到 $O(n\log n)$；但未解决集合还有更强性质。

An ordered map extracts all values below the current temperature for $O(n\log n)$, but the unresolved set has a stronger property.

### 推导出的单调性 (Derived Monotonicity)

设两个未解决位置 `a<b`。若 `T[a]<T[b]`，则在 `b` 出现时 `a` 已应被解决，矛盾。因此：

Let two unresolved positions be `a<b`. If `T[a]<T[b]`, then `a` should already have been resolved when `b` appeared, a contradiction. Hence:

$$
a<b,\quad a,b\ \text{unresolved}
\implies T[a]\ge T[b].
$$

这不是输入数组的单调性，而是由“未解决状态”派生的不变量。

This is not monotonicity of the input array; it is an invariant derived from the unresolved-state definition.

所有可被当前温度解决的元素位于序列尾部的连续段，因此只需 `back`、`pop_back` 和 `push_back`：Stack 是操作需求的结果。

All elements resolvable by the current temperature form a contiguous suffix, so only `back`, `pop_back`, and `push_back` are needed: the Stack follows from the required operations.

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for right, current in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < current:
            left = stack.pop()
            answer[left] = right - left
        stack.append(right)
    return answer
```

**摊还复杂度**：每个下标入栈一次、最多出栈一次，时间 $O(n)$；某轮仍可能弹出多个元素。  
**Amortized complexity**: each index enters once and exits at most once, so time is $O(n)$; one iteration can still pop several elements.

## Sliding Window Maximum：时间与值域的双重顺序 (Sliding Window Maximum: Time and Value Order)

需要查询窗口最大值，而非保留窗口全部元素。若后来的 `B` 不小于较早的 `A`，在 `B` 过期前 `A` 绝不可能成为最大值。

The query needs the window maximum, not every window element. If later `B` is no smaller than earlier `A`, then `A` cannot be maximal before `B` expires.

```python
from collections import deque

def max_sliding_window(values: list[int], k: int) -> list[int]:
    candidates: deque[int] = deque()
    answer: list[int] = []
    for i, value in enumerate(values):
        while candidates and values[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(i)
        while candidates[0] <= i - k:
            candidates.popleft()
        if i >= k - 1:
            answer.append(values[candidates[0]])
    return answer
```

队列下标递增、值单调递减；前端是最大值，后端支持支配淘汰。时间 $O(n)$，空间 $O(k)$。

Indices increase and values decrease monotonically; the front is the maximum and the back supports dominance removal. Time is $O(n)$ and space is $O(k)$.

## 选择结构而非记模板 (Choose a Structure, Not a Template)

`multiset` 保留完整窗口，给出 $O(n\log k)$；懒删除 Heap 也可能正确，但总空间可能达 $O(n)$；单调队列只保留未被支配候选。

A `multiset` retains the complete window for $O(n\log k)$; a lazily cleaned heap can also be correct but may use $O(n)$ space; a monotonic deque retains only undominated candidates.

## 边界与反例 (Boundary and Counterexample)

- Daily Temperatures 要求“严格更高”，因此使用 `<`，不是 `<=`；相等温度不能互相解决。  
  Daily Temperatures requires “strictly higher,” so use `<`, not `<=`; equal temperatures cannot resolve one another.
- Sliding Window Maximum 淘汰等值较早元素通常安全，因为它先过期；若查询还要求原始重复出现位置，不能丢弃。  
  Removing an equal earlier window element is usually safe because it expires first; if duplicate positions must also be reported, it cannot be discarded.
- 支配必须覆盖全部相关未来；只比较当前最好值并不自动安全。  
  Dominance must cover all relevant futures; comparing only the present best value is not automatically safe.

> **一句话总结（One-Line Summary）**：  
> 先证明候选何时永久失去价值，再让数据结构只维护仍可能成为答案的表示。  
> First prove when a candidate permanently loses value, then let a data structure maintain only the representation that may still become the answer.

## 章节导航 (Navigation)

👈 **上一章：[第3章：单调性与批量排除](Volume2_03_Chapter03_Monotonicity_Bulk_Elimination.md)**  
👉 **下一章：[第5章：等价状态与计算复用](Volume2_05_Chapter05_Equivalent_States_DP.md)**
