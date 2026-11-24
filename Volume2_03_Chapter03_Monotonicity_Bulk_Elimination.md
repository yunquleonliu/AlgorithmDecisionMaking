# 第3章：单调性与批量排除 (Monotonicity and Bulk Elimination)

> "Order is the shape upon which possibility can be cut."  
> “次序是裁切可能性的轮廓。”  
> —— Original epigraph

为什么指针只需向一个方向移动？因为当前比较能一次排除一整组候选，未排除空间仍保持足够表示。

Why can a pointer move in only one direction? Because the current comparison can eliminate a whole group of candidates while the remaining space stays sufficient.

## 原始候选空间 (The Original Candidate Space)

Two Sum II 的输入升序，候选是所有下标对：

For the sorted Two Sum II input, candidates are all index pairs:

$$
S=\{(i,j):0\le i<j<n\},\qquad |S|=O(n^2).
$$

Brute Force 逐点检查候选；Two Pointers 证明整行或整列不可能含解。

Brute Force checks candidates individually; Two Pointers proves that an entire row or column cannot contain the answer.

## 有序输入的双向单调性 (Bidirectional Monotonicity of Sorted Input)

若 `a` 非递减，则：

If `a` is nondecreasing, then:

$$
a[i+1]+a[j]\ge a[i]+a[j],\qquad
a[i]+a[j+1]\ge a[i]+a[j].
$$

- 和小于目标时，固定 `i` 的所有剩余配对更小，可安全前移 `i`。  
  If the sum is below target, all remaining pairs with fixed `i` are also small, so `i` may advance.
- 和大于目标时，固定 `j` 的所有剩余配对更大，可安全后移 `j`。  
  If the sum is above target, all remaining pairs with fixed `j` are also large, so `j` may retreat.

```python
def two_sum_sorted(a: list[int], target: int) -> bool:
    left, right = 0, len(a) - 1
    while left < right:
        value = a[left] + a[right]
        if value == target:
            return True
        if value < target:
            left += 1
        else:
            right -= 1
    return False
```

指针总移动不到 $n$ 次，故时间 $O(n)$、额外空间 $O(1)$。

The pointers move fewer than $n$ times total, giving $O(n)$ time and $O(1)$ extra space.

## Sliding Window：边界追赶 (Sliding Window: Boundary Catch-Up)

滑动窗口面对的是连续区间，而不是二维下标对。当扩张窗口只会让违规更严重，左边界一旦失效便不必回退。

A sliding window considers contiguous intervals rather than index pairs. If expansion can only worsen a violation, a left boundary that fails need not retreat.

最长无重复字符子串中，右端进入字符会增加重复风险；若重复，可移动左端直到窗口恢复合法。

For the longest substring without repetition, entering a character can increase duplication; when it does, the left endpoint advances until validity returns.

```python
def longest_unique(s: str) -> int:
    left, best = 0, 0
    counts: dict[str, int] = {}
    for right, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        while counts[char] > 1:
            left_char = s[left]
            counts[left_char] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**不变量**：`s[left:right+1]` 当前合法；`right` 单调向前；对每个 `right`，已检查到最短合法左边界。  
**Invariant**: `s[left:right+1]` is valid; `right` moves forward; for each `right`, the earliest valid required left boundary has been considered.

每个字符至多进入并离开一次，所以时间 $O(n)$，额外空间最多 $O(|\Sigma|)$。

Each character enters and leaves at most once, giving $O(n)$ time and at most $O(|\Sigma|)$ extra space.

## 二分答案：把优化改写为判定 (Binary Search on Answer: Optimization as Decision)

若谓词 `feasible(x)` 随答案上界 `x` 单调，可把“最小可行值”转成一系列可回答的是非问题。

If `feasible(x)` is monotone in an answer bound `x`, “minimum feasible value” becomes a sequence of yes/no decisions.

总复杂度是 $O(\log R\cdot C)$，其中 `C` 是一次判定成本；二分并不把判定本身免费化。

Total complexity is $O(\log R\cdot C)$, where `C` is the cost of one feasibility check; Binary Search does not make that check free.

## 机制不是单一模板 (The Mechanism Is Not One Template)

Two Pointers 是实现模式，其证明可以来自排序产生的支配、快慢指针的周期结构、或窗口约束的单调性。

Two Pointers is an implementation pattern whose proof may come from sorted dominance, the cycle structure of fast/slow pointers, or the monotonicity of window constraints.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> 把指针想象成扫描仪可帮助直觉；真正支持它的是“移动后被删除的候选不含答案”的证明。  
> Imagining pointers as scanners helps intuition; the actual support is a proof that the candidates deleted after a move cannot contain an answer.

## 边界与反例 (Boundary and Counterexample)

- 子数组 XOR 等于目标时，扩大窗口可能增加也可能减少匹配数量，不适用简单窗口。With XOR targets, widening a window can add or remove matches non-monotonically, so a simple sliding window does not work.
- “子数组和大于等于目标”对任意含负数输入不单调。For inputs with arbitrary negative values, “subarray sum at least target” is not monotone.
- Two Sum 的排序假设缺失后，不能安全删除当前较小端的整行；Hash Map 是另一种组织机制。Without sorting, an entire Two Sum row cannot be safely removed; a Hash Map provides a different organization mechanism.

> **一句话总结（One-Line Summary）**：  
> 单调性让一次比较批量排除候选，指针只是该证明形成的高效执行顺序。  
> Monotonicity lets one comparison exclude many candidates; pointers are the efficient execution order created by that proof.

## 章节导航 (Navigation)

👈 **上一章：[第2章：不变量与正确性](Volume2_02_Chapter02_Invariants_Correctness.md)**  
👉 **下一章：[第4章：支配关系与候选淘汰](Volume2_04_Chapter04_Dominance_Monotonic_Structures.md)**
