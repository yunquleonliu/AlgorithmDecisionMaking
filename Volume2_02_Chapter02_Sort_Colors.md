# 第二章：排序 vs 选择 —— 消解未知的艺术
# Chapter 02: Sort vs Selection — The Art of Reducing the Unknown

> "Sorting is about structure; Selection is about rank."  
> "排序是为了结构；选择是为了排名。"

在第一章中，我们将算法设计定义为 **"Reducing the Unknown" (消解未知)** 的过程。
本章将通过两个经典问题，展示两种截然不同的消解策略：
1.  **Sort Colors (Dutch National Flag)**: 必须确定每个元素的最终位置 -> **Linear Reduction ($O(N)$)**.
2.  **Median of Two Sorted Arrays**: 只需确定“分割线”的位置 -> **Logarithmic Reduction ($O(\log N)$)**.

---

## Part 1: 全量消除 —— 荷兰国旗问题 (Linear Reduction)
## Part 1: Linear Reduction — The Dutch National Flag Problem

### 问题定义 (Problem Definition)
给定一个包含红、白、蓝三种颜色的数组（`0, 1, 2`），**原地排序** 使得所有相同颜色的球聚集在一起。
**Input**: `[2, 0, 2, 1, 1, 0]` -> **Output**: `[0, 0, 1, 1, 2, 2]`

### Invariant-Based Design 推导

#### Step 1: Boundaries / Variables (Define Unknown)
我们需要三个指针来切分数组，从而定义出 **Unknown Region**。
*   `low`: 红色区间的下一个位置。
*   `high`: 蓝色区间的前一个位置。
*   `mid`: 当前探测的未处理位置。

**Unknown Region (未知区域)**: `[mid, high]`
*   在此区域之外的元素，都是 **Known (已归位)** 的。
*   在此区域之内的元素，是 **Unknown (待处理)** 的。

#### Step 2: Semantic Invariant (Define Correctness)
我们承诺在算法执行的 **每一刻**（循环开始前、中、后），以下性质恒等成立：

$$
\underbrace{[0, 0, \dots]}_{\text{Red} [0, low-1]} \quad
\underbrace{[1, 1, \dots]}_{\text{White} [low, mid-1]} \quad
\underbrace{[?, ?, \dots]}_{\text{Unknown} [mid, high]} \quad
\underbrace{[2, 2, \dots]}_{\text{Blue} [high+1, N-1]}
$$

#### Step 3: Reduce Unknown (Define Monotonicity)
目标：通过移动 `mid` 或 `high`，使得 `Unknown Region` 的长度严格减小。
我们查看 `Unknown` 区域的第一个元素 `nums[mid]`：

*   **Case A: 遇见红球 (0)**
    *   **Action**: 将其丢给左边的红色区间 -> `swap(nums[low], nums[mid])`。
    *   **Effect**: 红色区间扩张 (`low++`)，白色区间平移，未知区域左边界收缩 (`mid++`)。
    *   **Monotonicity**: Unknown Length $\downarrow 1$.
*   **Case B: 遇见白球 (1)**
    *   **Action**: 它已经在正确的位置（白色区间尾部）。
    *   **Effect**: 只是确认了它，未知区域左边界收缩 (`mid++`)。
    *   **Monotonicity**: Unknown Length $\downarrow 1$.
*   **Case C: 遇见蓝球 (2)**
    *   **Action**: 将其丢给右边的蓝色区间 -> `swap(nums[mid], nums[high])`。
    *   **Effect**: 蓝色区间扩张 (`high--`)。注意此时 `mid` 不能动，因为交换过来的 `nums[high]` 是未知的，下轮需重新检查。
    *   **Monotonicity**: Unknown Length $\downarrow 1$.

#### Step 4: Code Implementation
一旦上述逻辑确立，代码只是翻译：

```cpp
void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    // Termination: When Unknown Region is empty (mid > high)
    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums[low++], nums[mid++]);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            swap(nums[mid], nums[high--]);
        }
    }
}
```

---

## Part 2: 二分消除 —— 寻找两个有序数组的中位数 (Logarithmic Reduction)
## Part 2: Logarithmic Reduction — Median of Two Sorted Arrays

### 问题定义 (Problem Definition)
给定两个大小分别为 $m$ 和 $n$ 的有序数组 `A` 和 `B`，找出它们合并后的**中位数**。
**Constraint**: 时间复杂度需为 $O(\log (m+n))$。
这也是 LeetCode 004 (Hard).

### 核心思想：不要排序！(Selection != Sorting)
如果说 Sort Colors 是“我全都要”（排好每一个元素），那么 Selection 问题就是“我只要那一个”（Find K-th Element）。
我们不需要消除所有元素的未知性（排序），我们只需要消除 **“它一定不是第 K 个”** 的那些元素的未知性。

**Unknown Region (未知区域)**:
我们不需要知道 A 和 B 的所有元素谁大谁小，我们只需要确定 **Cut (分割线)** 在 A 中的位置 `i`。
变量 `i` 的搜索区间 `[L, R]` 就是我们的 Unknown Region。

### Invariant-Based Design 推导

#### Step 1: Boundaries / Variables (Define Unknown)
我们定义切分点：
*   $i$：在数组 A 中的切分位置 (0 到 m)。
*   $j$：在数组 B 中的切分位置 (0 到 n)。
*   目标：左半边总元素个数 $TotalLeft = (m + n + 1) / 2$。
*   约束：$j = TotalLeft - i$。

因此，**Unknown** 仅仅是变量 $i$ 的正确值。我们用二分查找维护 $i$ 的范围 $[L, R]$。

#### Step 2: Semantic Invariant (Define Correctness)
如果 $(i, j)$ 是正确的切分，必须满足 **"Cross-Order Invariant"**：
1.  **左 $\le$ 右**: $A$ 的左半最大值 $\le$ $B$ 的右半最小值 ($A[i-1] \le B[j]$)
2.  **左 $\le$ 右**: $B$ 的左半最大值 $\le$ $A$ 的右半最小值 ($B[j-1] \le A[i]$)

#### Step 3: Reduce Unknown (Define Monotonicity)
我们在 `A` 的区间 $[L, R]$ 上二分。
令 $i = (L + R) / 2$，计算对应的 $j$。检查 Invariant：

*   **Case A: $A[i-1] > B[j]$**
    *   **Analysis**: A 的左边太大了，挤占了 B 的名额。正确的 cut 一定在 $i$ 的左边。
    *   **Action**: $R = i - 1$。
    *   **Monotonicity**: Unknown Range $\downarrow 50\%$.
*   **Case B: $B[j-1] > A[i]$**
    *   **Analysis**: B 的左边太大了，A 给的名额太少。正确的 cut 一定在 $i$ 的右边。
    *   **Action**: $L = i + 1$。
    *   **Monotonicity**: Unknown Range $\downarrow 50\%$.
*   **Case C: Invariant Holds**
    *   **Action**: Found it! 计算中位数并返回。

#### Step 4: Code Implementation

```python
class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        # Ensure binary search on the shorter array for efficiency
        if len(nums1) > len(nums2):
            return self.findMedianSortedArrays(nums2, nums1)
        
        m, n = len(nums1), len(nums2)
        total_left = (m + n + 1) // 2
        
        L, R = 0, m
        
        while L <= R:
            i = (L + R) // 2
            j = total_left - i
            
            # Boundary checks using infinity
            max_left_A = float('-inf') if i == 0 else nums1[i-1]
            min_right_A = float('inf') if i == m else nums1[i]
            max_left_B = float('-inf') if j == 0 else nums2[j-1]
            min_right_B = float('inf') if j == n else nums2[j]
            
            # Check Invariant violations
            if max_left_A > min_right_B:
                R = i - 1  # Reduce Unknown to left half
            elif max_left_B > min_right_A:
                L = i + 1  # Reduce Unknown to right half
            else:
                # Invariant Met
                if (m + n) % 2 == 1:
                    return max(max_left_A, max_left_B)
                else:
                    return (max(max_left_A, max_left_B) + 
                            min(min_right_A, min_right_B)) / 2.0
```

---

## 总结：Contrast & Decision

| Feature | Sort Colors (Linear) | Median Selection (Logarithmic) |
| :--- | :--- | :--- |
| **Goal** | Determine **all** positions | Determine **rank-k** value |
| **Invariant** | Global Order: $[0,0,1,1,2,2]$ | Local Partition Constraint |
| **Unknown Region** | 物理上的数组段 `[mid, high]` | 逻辑上的参数范围 `[L, R]` |
| **Reduction** | $N \to N-1$ (Process 1 element) | $N \to N/2$ (Discard half range) |
| **Complexity** | $O(N)$ | $O(\log N)$ |

**设计启示 (Engineering Wisdom)**：
1.  **定义最弱的 Invariant**：如果只需要 Top K，就不要排序整个数组。Invariant 越强（如全序），维护成本越高（O(N log N) 或 O(N)）。Invariant 越弱（如 Partition），Reduction 越快。
2.  **变量即 Unknown**：写代码前，先问自己“我的 unknown 区域在哪里”。代码的每一行都应该是在“消除”这个 unknown。
