# 第三章：动态规划 (DP) —— 什么时候应该忘记历史
# Chapter 03: Dynamic Programming (DP) — When to Forget History

> "The past is a foreign country; they do things differently there."  
> —— L.P. Hartley

在人类社会中，“坚持”通常被视为一种绝对的美德。我们被反复教导：不要轻言放弃，要对得起过去的付出，再坚持一下也许就是黎明。
In human society, "perseverance" is generally considered an absolute virtue. We are repeatedly taught: do not give up easily, be worthy of past efforts, and perhaps dawn is just one more moment of persistence away.

但在算法的冷峻视角下，这种盲目的“坚持”往往是灾难的根源。企业为了维护面子继续投入已经被市场证伪的产品，投资者为了“回本”持续向亏损的仓位补钱，人们为了“不甘心”而维持一段注定破裂的关系。
However, from the cold perspective of algorithms, this blind "persistence" is often the root of disaster. Companies throw money at products already falsified by the market to save face; investors pour cash into losing positions to "break even"; people maintain doomed relationships out of "unwillingness to let go."

这些悲剧的根源在于：我们分不清什么时候该坚持，什么时候该止损。
The root of these tragedies lies in: our inability to distinguish when to persist and when to cut losses.

动态规划（Dynamic Programming, DP）作为计算机科学中最优雅的方法论之一，对此给出了一个数学级的回答。通过其中的 **Kadane 算法**，它向我们展示了一个反直觉的真理：**什么情况下应该忘记历史。**
Dynamic Programming (DP), one of the most elegant methodologies in computer science, provides a mathematical answer to this. Through **Kadane's Algorithm**, it reveals a counter-intuitive truth: **Under what circumstances should we forget history.**

### 动态规划的本质：记忆与遗忘
### The Essence of Dynamic Programming: Memory and Oblivion

动态规划的核心哲学只有两句话：
The core philosophy of Dynamic Programming consists of only two sentences:
1.  **记住那些有用的**（Reuse Sub-solutions）。
    *   **Remember what is useful** (Reuse Sub-solutions).
2.  **忘掉那些没用的**（Forgetfulness）。
    *   **Forget what is useless** (Forgetfulness).

大多数教科书侧重于第一点（如何通过存储解来避免重复计算），但在人生决策中，第二点——**如何优雅地遗忘**——往往不仅更难，而且更关键。一个高效的系统，必须具备“遗忘”的能力，否则它会被无限增长的历史数据拖垮。
Most textbooks focus on the first point (how to avoid redundant calculations by storing solutions), but in life decisions, the second point—**how to forget gracefully**—is often not only harder but more critical. An efficient system must possess the ability to "forget"; otherwise, it will be dragged down by infinitely growing historical data.

### 核心案例：Kadane 定律
### Core Case: Kadane's Law

让我们看一个经典问题：**最大子数组和问题**。
Let's look at a classic problem: **The Maximum Subarray Sum Problem**.
给定一个包含正数和负数的人生（数组），如何找到一段连续的区间，使得其中的收益总和最大？
Given a life (array) containing positive and negative numbers, how do you find a continuous interval where the total gain is maximized?
比如：`[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
For example: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

1984年，Joseph Kadane 提出了一个震惊学界的 O(N) 算法。这个算法的核心逻辑极其简单，我们可以将其抽象为一条决策定律：
In 1984, Joseph Kadane proposed an O(N) algorithm that shocked the academic world. The core logic of this algorithm is extremely simple, and we can abstract it into a decision law:

> **Kadane 定律**：
> 在遍历过程中，一旦当前的“累积收益”变成了负数，无论它之前多么辉煌，或者你投入了多少，每一刻的理性选择都应该是：**立刻归零，重新开始**。
>
> **Kadane's Law**:
> During the traversal, once the current "cumulative gain" becomes negative, no matter how glorious it was before, or how much you have invested, the rational choice at every moment should be: **Reset to zero immediately and start over.**

不是“暂时搁置”，不是“再观察一下”，而是**立刻清零**。
Not "put aside temporarily," not "observe a bit longer," but **clear to zero immediately**.

### 为什么必须切断？
### Why Must We Cut It Off?

这背后有着严格的数学证明。
There is a rigorous mathematical proof behind this.

Kadane 算法发现了一个深刻的结构性事实：
Kadane's algorithm discovered a profound structural fact:
**如果一段历史（前缀和）的结果是负的，那么任何包含这段历史的未来规划，都绝对不如“抛弃这段历史、从头开始”来得好。**
**If the result of a history (prefix sum) is negative, then any future plan containing this history is absolutely inferior to "discarding this history and starting from scratch."**

想象你背着一个包袱在走人生路。
Imagine you are walking the path of life carrying a bundle.
*   如果包袱里是（正收益），带着它走进未来，你的起点会更高。
    *   If the bundle contains (positive gain), carrying it into the future gives you a higher starting point.
*   如果包袱里是（负收益），带着它走进未来，你只会比空手出发的人更累，你的每一个未来时刻的收益都会被这块石头拉低。
    *   If the bundle contains (negative gain), carrying it into the future only makes you more tired than someone starting empty-handed; your gain at every future moment will be dragged down by this stone.

在这种情况下，切断历史，不是因为情绪上的“绝望”，而是基于逻辑上的“最优性”。**清零，是为了让未来更有竞争力。**
In this case, cutting off history is not out of emotional "despair," but based on logical "optimality." **Resetting is to make the future more competitive.**

### 沉没成本的数学终结
### The Mathematical End of Sunk Costs

经济学告诉我们要忽略“沉没成本（Sunk Cost）”，但它往往通过心理疏导来讲道理。Kadane 算法则直接从数学上判处了沉没成本死刑。
Economics tells us to ignore "Sunk Costs," but it often reasons through psychological counseling. Kadane's algorithm, however, directly sentences sunk costs to death mathematically.

当你试图用“我已经投入了这多”来说服自己继续时，你在算法上正在做一个极其愚蠢的操作：**你试图强行保留一个负的 `Current_Sum`**。
When you try to convince yourself to continue by saying "I have invested so much," you are performing an extremely stupid operation algorithmically: **You are trying to forcibly retain a negative `Current_Sum`.**

算法告诉你：历史的价值，不取决于你投入了多少（Cost），只取决于它对未来是正资产还是负资产（State Value）。一旦它变为负资产，它的最佳归宿就是被遗忘。
Algorithms tell you: The value of history depends not on how much you invested (Cost), but only on whether it is a positive or negative asset for the future (State Value). Once it becomes a negative asset, its best destiny is to be forgotten.

### 边界：何时不能忘？
### Boundary: When Can We Not Forget?

当然，DP 和 Kadane 只有在满足 **无后效性（Markov Property）** 的系统中才成立。
Of course, DP and Kadane only hold true in systems that satisfy the **Markov Property**.

这意味着：现在的状态必须能完全概括历史。
This means: The current state must fully summarize history.
*   **适用场景**：赌博输掉的钱、纯粹消耗情绪的坏关系、技术债累累的旧代码。在这些场景中，亏了就是亏了，没有任何隐藏的“经验值”。
    *   **Applicable Scenarios**: Money lost in gambling, bad relationships that purely consume emotions, legacy code riddled with technical debt. In these scenarios, a loss is a loss; there are no hidden "experience points."
*   **不适用场景**：创业虽然亏了钱但积累了人脉、学习虽然痛苦但重塑了大脑。这里，“亏损”并不是单纯的负数，它转化为了另一种形式的“隐形资产”。
    *   **Non-applicable Scenarios**: A startup lost money but accumulated connections; studying was painful but reshaped the brain. Here, "loss" is not a simple negative number; it transformed into another form of "invisible asset."

但在那些可以量化的单一维度赛道上，Kadane 是绝对真理。
But on those quantifiable single-dimension tracks, Kadane is absolute truth.

### 小结
### Summary

Kadane 算法不是教你如何更努力地计算，而是教你如何**更理性地放弃**。
Kadane's algorithm does not teach you how to calculate harder, but how to **give up more rationally**.

在一个充满不确定性的世界里，最大的风险往往不是开始得太晚，而是结束得太晚。
In a world full of uncertainty, the biggest risk is often not starting too late, but ending too late.

**如果历史不能照亮未来，那就哪怕在深夜，也要熄灭身后的灯。**
**If history cannot illuminate the future, then even in the dead of night, extinguish the lamp behind you.**
