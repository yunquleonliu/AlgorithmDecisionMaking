# Volume 2, Chapter 1: Invariant-Based Design Guidance
## Sliding Window Maximum —— 从暴力到极致的演进笔记

> "An algorithm is not something you memorize. It's something you **discover** from the problem's structure."

---

### 零、问题陈述与朴素理解

**问题**：给定数组 `nums` 和窗口大小 `k`，对于每个长度为 `k` 的滑动窗口，输出该窗口中的最大值。

```
Input:  nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]

窗口:
[1,3,-1]      -> 3
  [3,-1,-3]   -> 3
    [-1,-3,5] -> 5
      [-3,5,3]-> 5
        [5,3,6]-> 6
          [3,6,7]-> 7
```

### 一、定义 Invariant：什么是"有效的窗口"？

在这个问题中，我们需要首先定义什么不变：
*   **区间 Invariant**：在任何时刻，我们维护的数据结构都应该清晰地表示当前窗口 `[L, R]` 内的信息。
*   **正确性 Invariant**：无论我们采用什么数据结构，取出的最大值必须是窗口内实际的最大值。

这两个 Invariant 是所有方案的共同基础。区别在于如何维护它们的**效率**。

---

### 二、方案 1：Multiset（最直观的"平衡树"）

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        multiset<int> window;
        vector<int> ans;

        // Process first window
        for(int i = 0; i < k; ++i) {
            window.insert(nums[i]);
        }
        ans.push_back(*window.rbegin());  // 最大值

        // Slide the window
        for(int i = k; i < nums.size(); ++i) {
            window.insert(nums[i]);
            window.erase(window.find(nums[i-k]));
            ans.push_back(*window.rbegin());
        }
        return ans;
    }
};
```

#### 核心分析

**Invariant**：`multiset` 始终包含当前窗口的所有元素。

**数据结构的选择**：
*   `multiset` 是一个**自平衡二叉搜索树**，维持元素有序。
*   查询最大值：O(1)（直接访问最后一个元素）。
*   插入/删除：O(log k)。

**复杂度**：
*   时间：$O(n \log k)$。对于每个元素，我们做一次插入和删除，各需 O(log k)。
*   空间：$O(k)$。窗口大小。

**问题**：这个方案依赖于树的**自平衡特性**。如果我们没有 STL 的 `multiset`，或者题目要求用数组实现怎么办？

**洞察**：我们是否真的需要维护**整个窗口的完全有序集合**？或者我们只需要知道**最大值**？

这个问题引出了第二个方案的核心思想。

---

### 三、方案 2：Deque（单调性的显式体现）

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;  // 存索引，不存值
        vector<int> ans;

        // Process first window
        for(int i = 0; i < k; i++) {
            while(!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }
            dq.push_back(i);
        }
        ans.push_back(nums[dq.front()]);

        // Slide the window
        for(int i = k; i < nums.size(); i++) {
            while(!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }
            dq.push_back(i);

            if(dq.front() <= i - k) {
                dq.pop_front();
            }

            ans.push_back(nums[dq.front()]);
        }
        return ans;
    }
};
```

#### 核心分析

**Invariant**：
1.  **队内元素的索引单调递增**（因为我们只从队尾添加）。
2.  **队内元素的值单调递减**（这是关键）。

**Monotonicity 在这里的含义**：
*   一旦元素进入队列，它要么被后来的"更大元素"挤出，要么随时间流逝而越界。
*   **永不回头**：曾经被弹出的元素，永远不会再被考虑。

**为什么这样设计？**

想象窗口中有元素 `[3, 5, 2, 7, 1]`。
*   我们关心的是：最大值是什么？
*   数学上，5 和 2 作为"最大值候选者"，一旦 7 进来，它们都永远不可能再成为最大值（因为 7 > 5 > 2，且 7 在所有剩余情况下都会被后续窗口包含）。
*   **所以可以安全地弹出它们**。

**复杂度**：
*   时间：$O(n)$。每个元素最多被压入和弹出一次。
*   空间：$O(k)$。但实际队列大小往往远小于 k。

**相比方案 1 的优势**：
*   不依赖树的自平衡，逻辑上更简洁。
*   时间复杂度更优（O(n) vs O(n log k)）。

**关键教学点**：这里的单调栈（单调队列）不是为了"排序"，而是为了**识别"永不会成为答案的元素"并及时剔除它们**。

---

### 四、方案 3：Priority Queue（堆的"被动"特性）

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        priority_queue<pair<int, int>> pq;  // {值, 索引}
        vector<int> ans;

        // Process first window
        for(int i = 0; i < k; i++) {
            pq.push({nums[i], i});
        }
        ans.push_back(pq.top().first);

        // Slide the window
        for(int i = k; i < nums.size(); i++) {
            while(!pq.empty() && pq.top().second <= i - k) {
                pq.pop();
            }
            pq.push({nums[i], i});
            ans.push_back(pq.top().first);
        }
        return ans;
    }
};
```

#### 核心分析

**堆的特性**：
*   堆不像队列那样"主动"弹出不需要的元素。
*   堆是**懒惰的** (Lazy)：它只在你读取最大值时保证那个值是当前最大的；对于过期的元素，它们可能还在堆中，但会在需要时被跳过。

**Invariant**：
*   堆顶始终是所有未过期元素中的最大值。
*   过期元素可能还在堆中，但不影响答案的正确性。

**为什么这也能工作？**

当我们查询 `pq.top()` 时：
1.  我们先清理一下堆顶，把所有过期元素弹出。
2.  新的堆顶必然是未过期元素中最大的。

**复杂度**：
*   时间：最坏情况 $O(n \log n)$（如果所有元素都被压入堆）。
*   比方案 2 弱，因为堆内可能积累了大量过期元素。
*   但如果元素单调递减（如降序数组），堆可能很小，接近 O(n)。

**什么时候选择这个？**
*   当你信赖 STL 的 `priority_queue` 但不想写 `multiset`。
*   当不知道 k 的大小，只想要一个"足够好"的解。

---

### 五、三个方案的对比与选择

| 方案 | 数据结构 | 时间复杂度 | 空间复杂度 | 算法思想 | 难度 |
|:---|:---|:---|:---|:---|:---|
| 1 | Multiset | O(n log k) | O(k) | 平衡树维护有序集合 | 中 |
| 2 | Deque (单调) | **O(n)** | **O(k)** | **主动识别无效元素** | 中上 |
| 3 | Priority Queue | O(n log n) | O(n) | 懒惰维护，延迟清理 | 中下 |

**推荐顺序**（从"发现"的角度）：
1.  **首先学方案 2 (单调队列)**：这是"理解 sliding window maximum 本质"的方式。
2.  **其次学方案 1 (multiset)**：当你没时间手写单调队列时的折衷。
3.  **方案 3 (heap)**：了解即可，通常不是首选。

---

### 六、算法设计的思维过程（最重要）

**如何从零开始"发现"单调队列解法？**

**第一步：问清楚你要维护什么**
*   暴力想法："我需要维护窗口内所有元素。"
*   问题："为什么？"
*   答案："因为我需要找到最大值。"
*   **更聪明的想法**："我真的需要所有元素吗，还是只需要候选的最大值？"

**第二步：识别"永不会成为答案的元素"**
*   看这个例子：`[1, 3, -1, -3, 5]`（k=3）
*   当我们看到 `3` 时，`1` 还是候选吗？是的（可能是最大值）。
*   当我们看到 `-1` 时，`1` 和 `3` 都还是候选吗？`1` 不再是（因为 3 > 1），但 `3` 是。
*   **关键洞察**：一旦进来了更大的元素，所有更小的元素都永远不会再成为最大值（只要那个大元素在窗口内）。

**第三步：设计"有序的弃一堆"**
*   维护一个**单调递减的队列**。
*   新元素来时，弹出所有 ≤ 它的元素（它们永远不会再有用）。
*   添加新元素。
*   队头就是当前最大值。

**第四步：处理边界**
*   元素过期时，从队头弹出。
*   只有窗口形成后（i >= k-1），才输出答案。

**这正是算法设计的精髓**：不是"记住"单调队列，而是从问题的结构出发，自然地推导出来。

---

### 七、进阶思考：从 Sliding Window Maximum 到通用模板

我们可以将这个思路抽象为一个 **Invariant-Based 框架**：

```
1. 定义要维护的 Invariant（在这里：最大值）
   ↓
2. 选择合适的数据结构（multiset, deque, heap, ...）
   ↓
3. 识别 Monotonicity（哪些元素可以被安全地丢弃）
   ↓
4. 在每一步维持 Invariant 和 Monotonicity
   ↓
5. 从数据结构中快速提取答案
```

这个框架适用于：
*   Sliding Window Maximum/Minimum
*   Largest Rectangle in Histogram
*   Trapping Rain Water
*   Next Greater Element
*   ...以及几乎所有涉及"区间查询"的问题

---

### 总结

不要记住"单调队列是怎么写的"。
而要理解"**为什么** sliding window maximum 需要单调这个性质"。

这个思维方式，才是 Invariant-Based Design 的核心。
