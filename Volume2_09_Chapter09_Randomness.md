# 第九章：随机的力量 (Randomized Algorithms) —— 随机是对抗偏见的武器
# Chapter 9: The Power of Randomness — Randomness is the Weapon Against Bias

> "God does not play dice with the universe." —— Einstein
> "上帝不和宇宙玩骰子。" —— Einstein
> "But computer scientists do." —— Knuth
> "但是计算机科学家玩。" —— Knuth

在 Volume 1 中，我们要么在追求**确定性**（DP, Greedy），要么在利用**梯度**（SGD）。
In Volume 1, we were either pursuing **Determinism** (DP, Greedy) or utilizing **Gradients** (SGD).
但在工程和统计的世界里，有一种更强大的力量：**概率 (Probability)**。

今天，我们要解决一个在“大数据流”场景下极其经典的问题：**蓄水池抽样 (Reservoir Sampling)**。

**随机不是混乱，而是公平。** 当数据流无限且未知时，只有随机性能对抗“最坏情况” (Worst Case)。
**Randomness is not chaos; it is fairness.** When the data stream is infinite and unknown, only randomness can fight against the "Worst Case".
> 
## 一、无限与未知的挑战
## I. The Challenge of the Infinite and Unknown

假设你是一个 Google 的工程师。
Suppose you are a Google engineer.

*   每天有 10 亿个搜索 Query 流过你的服务器。
*   你需要选出 100 个 Query，拿给人工去审核质量。
*   **约束 1**：你不能把 10 亿个 Query 全存下来再随机选（内存不够）。
*   **约束 2**：Query 是像流水一样过来的，你不知道今天到底会有多少个（$N$ 是未知的）。
*   **约束 3**：必须保证**每个 Query 被选中的概率是完全相等的** ($100/N$)。

### 1. 错误的直觉：掷硬币
“每来一个 Query，我掷一次硬币，正面的话就留下？”
*   错。如果你不知道 $N$，你没法设定硬币的概率。如果概率设大了，刚开始就把 100 个名额填满了；概率设小了，最后可能没凑齐 100 个。

我们需要一种算法，它能**动态适应** $N$ 的增长，始终维持公平。

## 二、蓄水池算法：动态的公平
## II. Reservoir Algorithm: Dynamic Fairness

**蓄水池抽样 (Reservoir Sampling)** 的核心逻辑惊人地简单，却蕴含深奥的数学证明。

我们维护一个容量为 $K$ 的“蓄水池”（也就是我们要选的那 100 个样本）。

1.  **初始化**：前 $K$ 个数据，直接进入蓄水池。
2.  **第 $i$ 个数据 ($i > K$)**：
    *   以 $K/i$ 的概率决定是否**替换**蓄水池中的某一个。
    *   如果决定替换，随机选蓄水池里这一刻存在的一个元素，把它踢走，换成新元素。

就这么简单。

## 三、代码实现 (Code Implementation)
## III. Code Implementation

```python
import random

def reservoir_sampling(stream, k):
    """
    从无限流 stream 中随机选取 k 个元素
    """
    reservoir = []
    
    # 1. 蓄水阶段：前 k 个照单全收
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            # 2. 也是 i+1 个元素 (索引是 i)
            # 只有 k/(i+1) 的概率被选中
            # j 是 [0, i] 之间的随机整数
            j = random.randint(0, i)
            
            if j < k:
                # 只有当 j 落在蓄水池范围内 [0, k-1] 时，才进行替换
                reservoir[j] = item
                
    return reservoir

# Test Case
# 模拟一个 0 到 99 的流，我们要选 10 个
sample = reservoir_sampling(range(100), 10)
print(sample)
```

### 关键点解析 (Key Insights)

**为什么要用 `j < k` 来判断？**
让我们做个数学推导：假设当前已经是第 $N$ 个元素。
*   第 $N$ 个元素想进入池子，概率是 $K/N$。
*   它一旦进入，就要把原来的某人踢走。
*   对于已经在池子里的某个老元素 $X$，它留下的概率是：
    $$ P(\text{survive}) = 1 - P(\text{kicked}) $$
    $$ P(\text{kicked}) = P(\text{new guy enters}) \times P(\text{X is chosen to swap}) = \frac{K}{N} \times \frac{1}{K} = \frac{1}{N} $$
    $$ P(\text{survive}) = 1 - \frac{1}{N} = \frac{N-1}{N} $$

通过归纳法可以证明，无论 $N$ 增长到多少，每个元素最终留在池子里的概率始终是 $K/N$。

## 四、随机性作为一种 Feature
## IV. Randomness as a Feature

这种算法被称为 **Randomized Algorithm**。我们不是**不管**结果，而是利用随机性来**优化**资源。

1.  **Quicksort (快速排序)**：随机选 Pivot，是为了避免 $O(N^2)$ 的最坏情况。
2.  **Reservoir Sampling**：随机替换，是为了在 $O(1)$ 空间下处理无限数据。
3.  **Bitcoin Pow**：随机寻找哈希碰撞，是为了无需中心化机构就能达成共识。

**决策哲学**：
当你面对**无限的不确定性**（不知道未来 $N$ 有多大）时，你也应该维护你的“蓄水池”。
*   你的“朋友圈”容量是有限的（邓巴数字 150）。
*   你不能因为那是你的“老同学”就永远留着即使不再联系。
*   当认识了更优秀的新朋友（第 $i$ 个人），你应该给他们 $K/i$ 的机会进入你的核心圈。
*   **Fairness keeps the water fresh.** 流水不腐，随机性让你的系统保持活力。
