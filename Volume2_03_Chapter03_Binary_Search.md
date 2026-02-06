# 第三章：二分查找 (Binary Search) —— 剪枝的极致
# Chapter 03: Binary Search — The Ultimate Pruning

> "Search for the truth is the noblest occupation of man; its publication is a duty."  
> "探寻真理是人类最高贵的职业；而公布真理则是一种责任。"  
> —— Madame de Stael

如果说算法是对解空间的手术，那么**二分查找 (Binary Search)** 就是其中最精准的“截肢手术”。
它不仅用于在一个有序数组里找数字，更是一种通用的**解空间剪枝 (Pruning)** 策略。

If algorithms are surgery on the solution space, then **Binary Search** is the most precise "amputation" among them.
It is not just for finding numbers in a sorted array, but a universal strategy for **Solution Space Pruning**.

## 一、猜数字游戏的本质
## I. The Essence of the Number Guessing Game

在这个游戏中，我心里想一个 [1, 100] 的数字，你来猜。
In this game, I think of a number between [1, 100], and you guess.

*   你猜 50。
    *   You guess 50.
*   我说“太大了”。
    *   I say "Too high."
*   **发生什么了？** 你不仅知道 50 错了，你还确定 **[50, 100] 里的这 51 个数字全错了**。
    *   **What happened?** You didn't just learn that 50 is wrong; you became certain that **all 51 numbers in [50, 100] are wrong**.
*   **Prune (剪枝)**：你一次性砍掉了一半的解空间。
    *   **Prune**: You chopped off half the solution space in one go.

二分查找的本质，不是“折半”，而是**利用单调性 (Monotonicity) 进行大规模剪枝**。
The essence of Binary Search is not "halving," but **using Monotonicity for massive pruning**.

## 二、永远写不对的二分？
## II. The Binary Search You Can Never Write Correctly?

二分查找是出了名的“思路简单，细节魔鬼”。
Binary Search is notoriously "simple in concept, devilish in details."

*   `while (left < right)` 还是 `while (left <= right)`?
    *   `while (left < right)` or `while (left <= right)`?
*   `mid = (left + right) / 2` 还是 `+ 1`?
    *   `mid = (left + right) / 2` or `+ 1`?
*   `right = mid` 还是 `mid - 1`?
    *   `right = mid` or `mid - 1`?

如果你试图通过“试几个例子”来决定这些细节，你永远会遇到死循环或边界错误。
**解药：明确定义不变性 (Invariant)。**

If you try to decide these details by "trying a few examples," you will forever run into infinite loops or boundary errors.
**The Antidote: Clearly Define the Invariant.**

### The Concept of "Search Interval"

我们需要定义一个区间，使得**目标值 (Target) 如果存在，必然在这个区间内**。
We need to define an interval such that **if the Target exists, it must be within this interval**.

*   **左闭右闭 `[left, right]`**: 常规写法。
    *   **Left-closed, Right-closed `[left, right]`**: Conventional approach.
*   **左闭右开 `[left, right)`**: C++ STL 写法。
    *   **Left-closed, Right-open `[left, right)`**: C++ STL approach.

我们采用**左闭右闭 `[left, right]`** 为例。
We take **Left-closed, Right-closed `[left, right]`** as an example.

### The Invariant
**不变性**：`Target` (如果存在) $\in$ `nums[left...right]`。

**Invariant**: `Target` (if it exists) $\in$ `nums[left...right]`.

1.  **初始化**：`left = 0`, `right = N - 1`。区间覆盖全集，不变性成立。
    *   **Initialization**: `left = 0`, `right = N - 1`. The interval limits cover the full set, invariant holds.
2.  **终止条件**：`while (left <= right)`。
    *   **Termination Condition**: `while (left <= right)`.
    *   只要 `left <= right`，区间非空，我们就还没找完。
    *   As long as `left <= right`, the interval is non-empty, and we are not done searching.
    *   当 `left > right` 时，区间为空。根据不变性，Target 不在空集里，所以 Target 不存在。
    *   When `left > right`, the interval is empty. According to the invariant, the Target is not in the empty set, so the Target does not exist.
3.  **区间缩减 (Maintenance)**：
    *   **Interval Reduction (Maintenance)**:
    *   计算 `mid`。
        *   Calculate `mid`.
    *   如果 `nums[mid] < target`：
        *   If `nums[mid] < target`:
        *   说明 `nums[left...mid]` 都太小了（因为有序）。
        *   It implies `nums[left...mid]` are all too small (because it's sorted).
        *   Target 只能在 `[mid+1...right]`。
        *   Target can only be in `[mid+1...right]`.
        *   新区间必须是 `[mid+1, right]`。所以 `left = mid + 1`。
        *   The new interval must be `[mid+1, right]`. So `left = mid + 1`.
    *   如果 `nums[mid] > target`：
        *   If `nums[mid] > target`:
        *   说明 `nums[mid...right]` 都太大了。
        *   It implies `nums[mid...right]` are all too large.
        *   Target 只能在 `[left...mid-1]`。
        *   Target can only be in `[left...mid-1]`.
        *   新区间必须是 `[left, mid-1]`。所以 `right = mid - 1`。
        *   The new interval must be `[left, mid-1]`. So `right = mid - 1`.

只要你严格遵守 `[left, right]` 的定义，`mid+1` 和 `mid-1` 就是必然的推导，而不是一种选择。

As long as you strictly adhere to the definition of `[left, right]`, `mid+1` and `mid-1` are inevitable deductions, not choices.

```python
def binary_search(nums, target):
    # Definition: search space is [left, right] (inclusive)
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            # Prune [left...mid]
            left = mid + 1
        else:
            # Prune [mid...right]
            right = mid - 1
            
    return -1
```

## 三、二分答案
## III. Binary Search on Answer

二分的威力在于，**只要解空间具有单调性，我们就可以通过二分来锁定答案**，哪怕这个“答案”并不是在一个数组里。

The power of binary search lies in the fact that **as long as the solution space has monotonicity, we can use binary search to lock onto the answer**, even if this "answer" is not in an array.

**场景**：
*   “求满足条件 $P(x)$ 的最小 $x$”。
    *   "Find the minimal $x$ that satisfies condition $P(x)$."
*   如果 $x$ 满足，$x+1$ 肯定也满足（单调性）。
    *   If $x$ satisfies it, $x+1$ definitely satisfies it (monotonicity).

**通用模板 (寻找左边界)**：
我们定义解空间为 `[left, right]`。
*   我们试图找**第一个 `Satisfy(mid) == True` 的点**。

**Universal Template (Finding Left Boundary)**:
We define solution space as `[left, right]`.
*   We try to find the **first point where `Satisfy(mid) == True`**.

```python
def solve():
    # Definition: Answer is in [left, right]
    left, right = MIN_POSSIBLE_ANS, MAX_POSSIBLE_ANS
    ans = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if check(mid):
            # mid 满足条件，记录它是潜在答案
            # mid satisfies condition, record it as a potential answer
            ans = mid

            # 尝试找更小的？往左缩
            # Try to find a smaller one? Shrink to the left
            right = mid - 1
        else:
            # mid 不满足，说明太小了，往右找
            # mid does not satisfy, it's too small, search right
            left = mid + 1
            
    return ans
```

在这里，`check(mid)` 函数是核心。
我们将一个**最优化问题**（求最小的 $x$），转化为了一个**判定问题**（$x$ 可行吗？）。
通常判定这一步不仅仅是 $O(1)$，可能是 $O(N)$ 的贪心检查。

Here, the `check(mid)` function is the core.
We transform an **Optimization Problem** (find the minimum $x$) into a **Decision Problem** (is $x$ feasible?).
Often, this decision step is not just $O(1)$ but might be an $O(N)$ greedy check.

## 四、总结
## IV. Summary

二分查找是**剪枝**思维的极致体现。
当你的算法需要由 $O(N)$ 优化到 $O(\log N)$ 时，立刻寻找**单调性**。

Binary Search is the ultimate embodiment of **Pruning** thinking.
When your algorithm needs to be optimized from $O(N)$ to $O(\log N)$, look for **Monotonicity** immediately.

*   数组是有序的吗？ -> 二分下标。
    *   Is the array sorted? -> Binary Search on Index.
*   答案越大越容易满足条件吗？ -> 二分答案。
    *   Does a larger answer make it easier to satisfy the condition? -> Binary Search on Answer.

记住：**定义好你的区间开闭性（不变性），代码会自动写出来。**
Remember: **Define your interval closure (Invariant) clearly, and the code will write itself.**
