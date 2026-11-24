# 第2章：不变量与正确性 (Invariants and Correctness)

> "A program is a proof that can be executed."  
> “程序是可以执行的证明。”  
> —— Donald Knuth

如果程序正在改变数据，怎样判断每次改变都没有偏离答案？不变量把局部操作连接成全局正确性。

If a program keeps changing its data, how can each change be shown not to depart from the answer? Invariants connect local operations into a global correctness argument.

## 不变量证明三部曲 (The Three-Part Invariant Proof)

**循环不变量（Loop Invariant）**是在循环每次检查时都成立的陈述。它通常用 Initialization、Maintenance 和 Termination 证明。

**循环不变量（Loop Invariant）** is a statement true at each specified loop checkpoint. It is normally proved with Initialization, Maintenance, and Termination.

1. **Initialization**：第一次迭代前成立。It holds before the first iteration.
2. **Maintenance**：当前轮成立则下一轮仍成立。If it holds in one round, it holds in the next.
3. **Termination**：终止时不变量推出目标结论。At termination, the invariant implies the required result.

不变量回答“为什么正确”，它不回答“为什么快”。

An invariant answers why a result is correct, not why it is fast.

## 案例一：Sort Colors 的已知区间 (Case 1: Known Regions in Sort Colors)

输入只包含 `0`、`1`、`2`。原问题要求全部位置排列，不允许依赖排序函数。

The input contains only `0`, `1`, and `2`. The task is to place every element without relying on a sorting routine.

三个指针把数组分成四段：

Three pointers divide the array into four regions:

$$
[0,\text{low})=0,\quad
[\text{low},\text{mid})=1,\quad
[\text{mid},\text{high}]=\text{unknown},\quad
(\text{high},n)=2
$$

每轮处理 `nums[mid]`。交换至低端时 `low` 与 `mid` 前进；交换至高端时只移动 `high`，因为交换回来的元素仍未知。

Each round processes `nums[mid]`. Swapping toward the low side advances `low` and `mid`; swapping toward the high side advances only `high`, because the exchanged-in value is still unknown.

```python
def sort_colors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

**正确性**：未知区间每次至少减少一个位置，三个已知区间满足约束，因此终止时整个数组有序。  
**Correctness**: the unknown interval shrinks by at least one position each round, and the three known regions preserve their constraints, so the array is sorted at termination.

**复杂度**：时间 $O(n)$，额外空间 $O(1)$。  
**Complexity**: $O(n)$ time and $O(1)$ extra space.

## 案例二：二分查找的候选约束 (Case 2: Candidate Constraint in Binary Search)

查找一个值时，Brute Force 逐个检查。二分查找可成立，是因为谓词 $P(i)=a[i]\ge t$ 从假变真，并且允许高效读取中点。

For a search task, Brute Force checks each position. Binary Search is valid because the predicate $P(i)=a[i]\ge t$ changes from false to true and midpoint access is efficient.

选定半开区间 $[L,R)$，其不变量是“边界答案若存在，位置仍在 $[L,R]$ 中”。

Choose the half-open interval $[L,R)$; its invariant is that the boundary answer, if present, remains at a position in $[L,R]$.

```python
def lower_bound(a: list[int], target: int) -> int:
    left, right = 0, len(a)
    while left < right:
        mid = left + (right - left) // 2
        if a[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

Initialization 覆盖整个可能边界；Maintenance 只丢弃不可能包含边界的一半；Termination 时 `left == right` 是第一个满足位置，或 `n`。

Initialization covers the full boundary range; Maintenance discards only a half that cannot contain it; at Termination, `left == right` is the first satisfying position, or `n`.

**复杂度**：$O(\log n)$ 时间，$O(1)$ 额外空间。  
**Complexity**: $O(\log n)$ time and $O(1)$ extra space.

## 选择而非排序：两个有序数组的中位数 (Selection Rather Than Sorting)

两个有序数组若被划分为 `A[0:i]`、`B[0:j]` 的左半与各自余下的右半，且左半元素总数固定，则只需寻找一条交叉有序分割线。

If two sorted arrays are split into left parts `A[0:i]` and `B[0:j]` with a fixed total left size, only a cross-ordered cut needs to be found.

正确切分满足：

A correct cut satisfies:

$$
\max A[i-1]\le\min B[j],\qquad
\max B[j-1]\le\min A[i].
$$

在较短数组上二分 `i`，若 `A[i-1]>B[j]` 就向左缩 `i`，若 `B[j-1]>A[i]` 就向右扩 `i`。边界位置用 $-\infty$ 和 $+\infty$ 解释空侧。

Binary-search `i` in the shorter array; move left if `A[i-1]>B[j]`, and right if `B[j-1]>A[i]`. Interpret empty boundary sides as $-\infty$ and $+\infty$.

算法不需要合并并排序全部元素，因为信息需求只包括一个顺序统计量。时间 $O(\log\min(m,n))$，额外空间 $O(1)$。

The arrays need not be merged and sorted because the information requirement is one order statistic. Time is $O(\log\min(m,n))$ and extra space is $O(1)$.

## 排序、选择与信息需求 (Sorting, Selection, and Information Requirement)

Sort Colors 要求确定全部元素的最终区域；lower bound 只要求确定一个边界。二者需要的最终信息不同，因此维护的最强结构也不同。

Sort Colors requires final regions for all elements; lower bound requires only one boundary. Their information requirements differ, so the strongest structure maintained differs as well.

## 失效边界 (Boundary and Counterexample)

- 对排序无序数组执行二分，单点比较不能推出应删除哪半边。Binary Search on an unsorted array cannot infer which half to delete from one comparison.
- 谓词 `a[i]` 可上下波动时，真值不是单调边界，二分可能丢掉答案。When the predicate fluctuates, binary search can discard the answer.
- Sort Colors 的三色语义改为任意整数时，三个区间不再构成充分信息。For arbitrary integer values, three fixed color regions no longer constitute a sufficient representation.

> **一句话总结（One-Line Summary）**：  
> 不变量把局部变化约束到正确语义；效率仍需要独立的结构与成本证明。  
> An invariant constrains local changes to correct semantics; efficiency still requires a separate structural and cost proof.

## 章节导航 (Navigation)

👈 **上一章：[第1章：优化从何而来](Volume2_01_Chapter01_Design_Intro.md)**  
👉 **下一章：[第3章：单调性与批量排除](Volume2_03_Chapter03_Monotonicity_Bulk_Elimination.md)**
