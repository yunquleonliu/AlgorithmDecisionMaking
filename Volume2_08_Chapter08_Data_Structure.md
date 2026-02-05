# 第八章：数据结构设计 (Data Structure Design) —— 不变性的容器
# Chapter 08: Data Structure Design — The Container of Invariance

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."  
> —— Linus Torvalds

在前几章中，我们讨论的算法（Algorithm）通常是瞬态的：输入 -> 处理 -> 输出 -> 结束。
而 **数据结构 (Data Structure)** 是持久态的。它像一个有机体，必须在整个生命周期内维持某种秩序。

In previous chapters, the Algorithms we discussed were usually transient: Input -> Process -> Output -> End.
But **Data Structure** is persistent. Like an organism, it must maintain a certain order throughout its lifecycle.

这种秩序，就是 **Class Invariant (类级不变性)**。

This order is the **Class Invariant**.

## 一、什么是 Class Invariant？
## I. What is a Class Invariant?

当你设计一个类（Class）时，你向使用者承诺了一组 Public API。
在内部，你必须向自己承诺一组 Invariants。

When you design a Class, you promise a set of Public APIs to the user.
Internally, you must promise a set of Invariants to yourself.

**契约 (Contract)**：
1.  **构造函数**：必须建立 Invariant。
    *   **Constructor**: Must establish the Invariant.
2.  **Public 方法**：
    *   **Public Methods**:
    *   调用前 (Pre-condition)：假设 Invariant 成立。
        *   **Pre-condition**: Assume the Invariant holds.
    *   执行中：可能会暂时破坏 Invariant。
        *   **Execution**: May temporarily violate the Invariant.
    *   返回前 (Post-condition)：必须**修复** Invariant。
        *   **Post-condition**: Must **restore** the Invariant.

## 二、案例：堆 (Binary Heap)
## II. Case Study: Binary Heap

**二叉最小堆 (Min-Heap)** 看起来只是一个数组，但它严格维护着一个**结构不变量**。

**Binary Min-Heap** looks like just an array, but it strictly maintains a **structural invariant**.

**Heap Invariant**:
对于任意节点 `i`，`arr[i] <= arr[left_child(i)]` 且 `arr[i] <= arr[right_child(i)]`。
（通俗说：父亲永远比儿子小）。

**Heap Invariant**:
For any node `i`, `arr[i] <= arr[left_child(i)]` and `arr[i] <= arr[right_child(i)]`.
(In simple terms: The father is always smaller than the son).

让我们看看 `push` 和 `pop` 是如何围绕这个不变量设计的：
Let's see how `push` and `pop` are designed around this invariant:

### 1. Push (插入)
*   **动作**：把新元素放在数组末尾。
    *   **Action**: Place the new element at the end of the array.
*   **破坏**：这可能打破了“父小于子”的规则。
    *   **Violation**: This might break the "father < son" rule.
*   **修复 (Sift Up)**：如果不变量被破坏（子 < 父），就交换它们。持续向上追溯，直到不变量恢复。
    *   **Restore (Sift Up)**: If the invariant is violated (son < father), swap them. Trace up continuously until the invariant is restored.

### 2. Pop (弹出最小值)
*   **动作**：移除根节点（`arr[0]`）。把末尾元素放到根部。
    *   **Action**: Remove the root node (`arr[0]`). Move the last element to the root.
*   **破坏**：新的根可能非常大，严重破坏不变量。
    *   **Violation**: The new root might be very large, severely violating the invariant.
*   **修复 (Sift Down)**：把这个大的根往下沉，和较小的儿子交换。持续向下，直到不变量恢复。
    *   **Restore (Sift Down)**: Sink this large root down, swapping with the smaller child. Continue downwards until the invariant is restored.

所有的代码逻辑，本质上都是 **Invariant Restorer (不变量修复器)**。
All code logic is essentially an **Invariant Restorer**.

## 三、案例：LRU 缓存 (LRU Cache)
## III. Case Study: LRU Cache

设计一个 LRU (Least Recently Used) 缓存，要求 `get` 和 `put` 都是 $O(1)$。

Design an LRU (Least Recently Used) cache, requiring both `get` and `put` to be $O(1)$.

这是一个典型的**复合数据结构设计**。我们需要维护两个互锁的不变性：
This is a typical **Composite Data Structure Design**. We need to maintain two interlocking invariants:

1.  **查找快**：必须有 HashMap。
    *   **Fast Lookup**: Must have a HashMap.
2.  **顺序维护**：必须有顺序，且能 $O(1)$ 移动元素 -> Doubly Linked List。
    *   **Order Maintenance**: Must have order, and be able to move elements in $O(1)$ -> Doubly Linked List.

**Invariant**:
*   HashMap 中的 Key 指向链表中的 Node。
    *   Key in HashMap points to Node in Linked List.
*   链表头 (Head) 是“最近使用”，链表尾 (Tail) 是“最久未用”。
    *   Linked List Head is "Most Recently Used", Tail is "Least Recently Used".
*   HashMap.size() == LinkedList.size() <= Capacity。
    *   HashMap.size() == LinkedList.size() <= Capacity.

```python
class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {} # Map<Key, Node>
        # Dummy Head/Tail simplify boundary checks
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        # 纯粹的链表手术：断开节点
        # Pure linked list surgery: detach node
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        # 纯粹的链表手术：插入头部
        # Pure linked list surgery: insert at head
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            # 维护 Invariant: 使用了就要去头部
            # Maintain Invariant: Used means move to head
            self._remove(node)
            self._add_to_head(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        
        # 维护 Invariant: 容量超标
        # Maintain Invariant: Capacity exceeded
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

## 四、总结
## IV. Summary

设计数据结构时，不要只是堆砌 `list` 和 `dict`。
先写下注释：**"Class Invariant 是什么？"**

When designing data structures, don't just pile up `list` and `dict`.
Write down the comment first: **"What is the Class Invariant?"**

*   "栈的 Invariant 是 FIFO 还是 LIFO？"
    *   "Is the Stack Invariant FIFO or LIFO?"
*   "红黑树的 Invariant 是什么？"（路径黑色节点数相同）。
    *   "What is the Red-Black Tree Invariant?" (Same number of black nodes on path).

代码中的每一个 Helper Function（如 `_remove`, `_sift_up`），都是为了局部地执行手术，以服务于全局的不变性。
Every Helper Function in the code (like `_remove`, `_sift_up`) is there to perform local surgery to serve the global invariant.
