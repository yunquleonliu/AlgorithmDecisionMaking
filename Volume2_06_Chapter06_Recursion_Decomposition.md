# 第6章：递归、分解与归纳 (Recursion, Decomposition, and Induction)

> "To understand a whole, define how smaller answers become the whole."  
> “理解整体，先定义较小答案如何组成整体。”  
> —— Original epigraph

递归不是函数调用自己的语法技巧，而是把问题契约分解为更小同类契约。

Recursion is not the syntactic trick of a function calling itself; it decomposes a problem contract into smaller contracts of the same kind.

## 递归契约 (The Recursive Contract)

函数签名应先说明输入、输出、前置条件和副作用，再讨论栈帧。

A function signature should state input, output, preconditions, and side effects before stack frames are considered.

递归证明与归纳法对应：

A recursive proof mirrors induction:

1. **Base Case**：最小合法输入直接正确。The smallest valid input is directly correct.
2. **Induction Hypothesis**：相信所有严格更小的调用遵守契约。Every strictly smaller call is trusted to obey the contract.
3. **Inductive Step**：利用这些结果与有限局部工作完成当前输入。These results plus finite local work complete the current input.

## 反转链表 (Reverse a Linked List)

`reverse(head)` 返回反转后新头节点；只需假设 `reverse(head.next)` 已经正确。

`reverse(head)` returns the new head after reversal; only trust `reverse(head.next)` to work correctly.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def reverse(head: Node | None) -> Node | None:
    if head is None or head.next is None:
        return head
    new_head = reverse(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

子调用保住后缀反转；两条指针修改把当前节点接回链尾，归纳完成。时间 $O(n)$，递归栈 $O(n)$。

The recursive call reverses the suffix; two pointer updates attach the current node to its tail. Time is $O(n)$ and stack space is $O(n)$.

## 分治与合并排序 (Divide and Conquer with Merge Sort)

分治并不要求子问题完全不重叠，但要求拆分后可独立求解并用已知代价组合。

Divide and Conquer need not require non-overlapping inputs in every setting, but it does require independently solvable subproblems and a known combine cost.

```python
def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

递推式为 $T(n)=2T(n/2)+O(n)$，所以时间 $O(n\log n)$，稳定实现的额外空间为 $O(n)$。

The recurrence is $T(n)=2T(n/2)+O(n)$, giving $O(n\log n)$ time and $O(n)$ extra space for a stable implementation.

## 递归与 DP 的区别 (Recursion and DP Are Different Dimensions)

递归描述控制方式；DP 描述对重叠充分状态的复用。递归加 Memoization 可以成为 DP，没有重叠时仍只是递归或分治。

Recursion describes control; DP describes reuse of overlapping sufficient states. Recursion plus memoization can implement DP, while recursion without overlap remains recursion or Divide and Conquer.

## 边界与反例 (Boundary and Counterexample)

- 如果递归参数不严格减小，归纳没有基础顺序，可能无限递归。  
  Without a strictly smaller recursive argument, induction has no order and recursion may never terminate.
- Merge Sort 的合并若不稳定，正确排序仍可能成立，但稳定性承诺被破坏。  
  If merge is unstable, sortedness may still hold, but the stability guarantee is lost.
- 两个重叠子问题必须通过同一可证明状态合并；可复用数据不等于可以忽略参数。  
  Overlapping subproblems may merge only through the same proven state; shared data does not imply parameters can be ignored.

> **一句话总结（One-Line Summary）**：  
> 递归由更小契约组成当前答案，归纳证明为什么每层连接都能沿规模推进到终点。  
> Recursion composes the current answer from smaller contracts; induction proves that each level advances the contract to termination.

## 章节导航 (Navigation)

👈 **上一章：[第5章：等价状态与计算复用](Volume2_05_Chapter05_Equivalent_States_DP.md)**  
👉 **下一章：[第7章：图、前沿与可达性](Volume2_07_Chapter07_Graph_Frontier_Reachability.md)**
