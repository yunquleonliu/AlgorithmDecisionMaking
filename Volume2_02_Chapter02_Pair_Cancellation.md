# 第二章：配对消除 (Pair Cancellation) —— 抵消的艺术
# Chapter 02: Pair Cancellation — The Art of Offsetting

> "Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."  
> —— Antoine de Saint-Exupéry

有些问题看似需要大量储存空间，但如果你仔细观察 **不变性 (Invariant)**，会发现很多元素是可以“相互抵消”的。一旦它们“同归于尽”，我们要处理的问题规模就缩小了。

Some problems seem to require a lot of storage space, but if you carefully observe the **Invariant**, you will discover that many elements can "offset each other." Once they "mutually annihilate," the scale of the problem we need to deal with shrinks.

**Pair Cancellation (配对消除)** 的核心思想：找到一种机制，让一对元素相互湮灭，同时**不改变问题的答案**。

The core idea of **Pair Cancellation**: Find a mechanism that allows a pair of elements to annihilate each other **without changing the answer to the problem**.

## 一、多数投票问题 (Majority Vote)
## I. Majority Vote

**问题**：给定一个长度为 $n$ 的数组，找出出现次数超过 $n/2$ 的元素（假设必定存在）。

**Problem**: Given an array of length $n$, find the element that appears more than $n/2$ times (assuming it must exist).

*   **直觉 (HashMap)**：统计每个元素频率。空间 $O(N)$。
    *   **Intuition (HashMap)**: Count the frequency of each element. Space $O(N)$.
*   **排序 (Sorting)**：排序后取中间元素。时间 $O(N \log N)$。
    *   **Sorting**: Sort and take the middle element. Time $O(N \log N)$.
*   **抵消思维**：如果一个“众数”和一个“非众数”一起同归于尽会发生什么？
    *   **Cancellation Thinking**: What happens if a "majority element" and a "non-majority element" perish together?
    *   剩下的元素中，众数**依然是**众数（因为众数超过半数，它比其他所有加起来还多）。
    *   Among the remaining elements, the majority element **is still** the majority (because the majority is more than half, it is more than all the others combined).
    *   如果两个“非众数”同归于尽呢？众数的比例占比更高了，依然是众数。
    *   What if two "non-majority elements" perish together? The proportion of the majority becomes even higher, so it remains the majority.

**Boyer-Moore Voting Algorithm** 就是利用了这个**不变性**。

The **Boyer-Moore Voting Algorithm** exploits this **invariant**.

### Invariant & Algorithm
我们维护一个 `candidate` 和一个 `count`。
We maintain a `candidate` and a `count`.

*   **不变性**：如果我们将当前遍历过的部分中，每两个**不同**的元素进行抵消，那么剩下的那个元素就是 `candidate`，且它的“净剩个数”是 `count`。
*   **Invariant**: If we offset every two **different** elements in the part traversed so far, then the remaining element is the `candidate`, and its "net remaining count" is `count`.

```python
def majority_element(nums):
    candidate = None
    count = 0
    
    for x in nums:
        # Invariant: candidate represents the survivor of previous cancellations
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            # Pair Cancellation: Current x cancels out one existing candidate
            count -= 1
            
    return candidate
```

**手术刀分析**：
我们将 $O(N)$ 的空间（HashMap）压缩到了 $O(1)$ 的寄存器。这是因为我们识别出了“抵消不改变结果”这一不变性。

**Scalpel Analysis**:
We compressed $O(N)$ space (HashMap) into $O(1)$ registers. This is because we identified the invariant that "cancellation does not change the result."

## 二、栈与括号 (Stack as Cancellation)
## II. Stack and Parentheses (Stack as Cancellation)

栈（Stack）通常被视为一种数据结构，但在算法设计中，它更像是一个**消除场**。

A Stack is often viewed as a data structure, but in algorithm design, it is more like a **Cancellation Field**.

**问题**：Valid Parentheses (`(()[])`).

This is essentially a **Nearest Match Cancellation** problem.
*   `(` 是一个“待消除”的请求。
    *   `(` is a request "waiting to be cancelled."
*   `)` 是一个“消除者”。
    *   `)` is a "canceller."
*   当 `)` 遇到栈顶的 `(` 时，两者同时湮灭。
    *   When `)` meets the `(` at the top of the stack, both mutually annihilate.

**不变性 (The Stack Invariant)**：
栈中永远只存储**目前还未被抵消的左括号**。
一旦栈顶元素遇到了它的配对者，它们就离开了解空间。

**The Stack Invariant**:
The stack always stores only **the left parentheses that have not yet been offset**.
Once the top element meets its pair, they leave the solution space.

```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in pairs:
            # Inspection: Can we cancel the top?
            if stack and stack[-1] == pairs[char]:
                stack.pop() # Cancellation!
            else:
                return False
        else:
            stack.append(char)
            
    return len(stack) == 0 # Invariant: Everything should be canceled
```

## 三、异或的唯一 (XOR Cancellation)
## III. The Uniqueness of XOR (XOR Cancellation)

最纯粹的消除，莫过于计算机底层的异或运算（XOR）。
The purest form of cancellation is the computer's low-level XOR operation.

*   性质：`a ^ a = 0` (Self-Cancellation)
*   性质：`a ^ 0 = a` (Identity)
*   性质：`a ^ b ^ c = a ^ c ^ b` (Commutativity)

**问题**：数组中除了一个数字出现一次，其他所有数字都出现两次。找出那个数字。

**Problem**: In an array, except for one number that appears once, all other numbers appear twice. Find that number.

在这里，解空间中的每一个数字 `x` 都有一个通过 `^` 运算连接的“影子”。
我们的手术刀是 `XOR`。
**不变关系**：无论运算顺序如何，成对的数字最终都会通过 `x ^ x = 0` 消失，只有孤独的那个数字会留下来。

Here, every number `x` in the solution space has a "shadow" connected via the `^` operation.
Our scalpel is `XOR`.
**Invariant Relation**: Regardless of the order of operations, paired numbers will eventually disappear via `x ^ x = 0`, and only the lonely number will remain.

```python
def single_number(nums):
    survivor = 0
    for x in nums:
        survivor ^= x # Introduction and Cancellation happen simultaneously
    return survivor
```

## 四、总结

**Pair Cancellation** 是一种极强的**降维打击**手段。
当我们看到题目涉及“计数”、“匹配”、“成对出现”或者“超过阈值”时，先问自己：
1.  **什么东西可以和什么东西抵消？**（不同的元素？左右括号？二进制位？）
2.  **抵消之后，我们要找的答案（Invariant）是否保持不变？**

如果答案是肯定的，你就可以抛弃复杂的数据结构，用简单的计数器或指针来解决战斗。
