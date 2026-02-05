# 第五章：滑动窗口 (Sliding Window) —— 伸缩的视野
# Chapter 05: Sliding Window — The Expanding and Contracting Vision

> "The only way to find specific information in a sea of data is to filter it through a moving frame of reference."

很多数组/字符串题目要求我们寻找一个**连续子数组 (Subarray)** 满足特定条件。暴力做法是枚举所有起点 $i$ 和终点 $j$，复杂度 $O(N^2)$。

Many array/string problems ask us to find a **Subarray** that satisfies a specific condition. The brute force approach is to enumerate all start points $i$ and end points $j$, with a complexity of $O(N^2)$.

**滑动窗口 (Sliding Window)** 将其优化为 $O(N)$。它的核心在于利用**单调性**：当右边界 `right` 向右扩张时，左边界 `left` 通常只需要向右追赶，而不需要回头。

**Sliding Window** optimizes this to $O(N)$. Its core lies in utilizing **Monotonicity**: When the right boundary `right` expands to the right, the left boundary `left` usually only needs to chase to the right, without ever turning back.

## 一、双指针的不变性
## I. The Invariant of Two Pointers

滑动窗口本质上是**双指针 (Two Pointers)** 的变体。我们需要维护一个窗口 `[left, right]`，并定义一个关于该窗口的**不变性**。

Sliding Window is essentially a variant of **Two Pointers**. We need to maintain a window `[left, right]` and define an **Invariant** regarding that window.

**模版范式**：
**Template Paradigm**:
1.  **进窗**：`right` 每一步主动向右移动，将元素加入窗口。
    *   **Expand**: `right` moves right actively at each step, adding elements to the window.
2.  **出窗**：当窗口**不再满足条件**（或满足条件需要收缩）时，`left` 被动向右移动，踢出元素。
    *   **Shrink**: When the window **no longer satisfies the condition** (or meets the condition but needs to shrink), `left` moves right passively, kicking elements out.
3.  **计算**：在每次窗口状态合法时，更新答案。
    *   **Calculate**: Update the answer whenever the window state is valid.

## 二、案例：无重复字符的最长子串
## II. Case Study: Longest Substring Without Repeating Characters

**问题**：给定字符串，找出不含重复字符的最长子串长度。
**Problem**: Given a string, find the length of the longest substring without repeating characters.

我们不需要回溯。
We don't need backtracking.

**不变性 定义**：`window` (即 `s[left...right]`) 内部永远**没有重复字符**。
**Invariant Definition**: Inside the `window` (i.e., `s[left...right]`), there are effectively **no repeating characters**.

1.  **Init**: `left = 0`, `right` 遍历，`window = set()`。
    *   **Init**: `left = 0`, iterate with `right`, `window = set()`.
2.  **Right Move**: 尝试将 `s[right]` 加入窗口。
    *   **Right Move**: Try to add `s[right]` to the window.
3.  **Violation & Restore Invariant**:
    如果 `s[right]` 已经在 window 里了，说明不变性即将被破坏。
    怎么办？保持 `right` 不动，**移动 `left` 并不断移除元素**，直到 `s[right]` 不再重复为止。
    *   这个过程就是“收缩拆除”，直到环境再次适合“建设”。
    *   **Violation & Restore Invariant**:
    *   If `s[right]` is already in the window, the invariant is about to be violated.
    *   What to do? Keep `right` still, **move `left` and continuously remove elements**, until `s[right]` is no longer repeating.
    *   This process is "shrinking and demolition" until the environment is suitable for "construction" again.
4.  **Update**: 此时窗口恢复合法，更新 `max_len`。
    *   **Update**: Now the window is valid again, update `max_len`.

```python
def lengthOfLongestSubstring(s):
    seen = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # 破坏不变性了吗？如果是，修补它
        # Did we violate the invariant? If so, fix it.
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
            
        # 此时不变性成立：s[left...right] 无重复
        # Invariant holds: s[left...right] has no duplicates
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
        
    return max_len
```

## 三、什么时候能用滑动窗口？
## III. When Can We Use Sliding Window?

不是所有子数组问题都能滑。核心在于 **单调性 (Monotonicity)**。
Not all subarray problems can be solved by sliding. The core lies in **Monotonicity**.

**判据**：
**Criterion**:
*   当窗口变宽（`right++`）时，条件是否**单调地**变得更满足或更不满足？
    *   When the window widens (`right++`), does the condition become **monotonically** more satisfied or less satisfied?
*   例如“子数组和 >= K”：加元素和变大（更满足），减元素和变小（更不满足）。这就能滑。
    *   Example "Subarray Sum >= K": Adding elements increases sum (more satisfied), removing elements decreases sum (less satisfied). This can be slid.
*   如果是“子数组异或和等于 K”：加一个数，异或值可能变大也可能变小。**没有单调性，不能用滑动窗口**（通常要用前缀和 + HashMap）。
    *   Example "Subarray XOR Sum == K": Adding a number might increase or decrease the XOR value. **No monotonicity, cannot use sliding window** (usually use Prefix Sum + HashMap).

## 四、总结
## IV. Summary

滑动窗口是**解空间手术**中的“蠕动式扫描”。它不再遍历所有可能的 `[i, j]`，而是只遍历那些“有潜力”的边界。

Sliding Window is a "Peristaltic Scan" in **Solution Space Surgery**. It no longer traverses all possible `[i, j]`, but only those "potential" boundaries.

**Variables as Boundaries**:
*   `right`：探索未知的先锋。
    *   `right`: The pioneer exploring the unknown.
*   `left`：维持合法性的底线。
    *   `left`: The baseline maintaining validity.
*   Invariant：区间 `[left, right]` 始终是一个“候选解”（或者“合法解”）。
    *   Invariant: The interval `[left, right]` is always a "Candidate Solution" (or "Valid Solution").
