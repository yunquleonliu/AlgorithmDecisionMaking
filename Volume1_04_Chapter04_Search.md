# 第四章：搜索 (Search) —— 37% 的爱情法则
# Chapter 04: Search — The 37% Rule of Love

> "Maximizing is a difficult cognitive task... Satisficing, finding an alternative that is 'good enough', is much easier and often smarter."
> "追求最大化是一项艰难的认知任务……满意化（Satisficing），即寻找一个‘足够好’的替代方案，要容易得多，往往也更明智。"
> —— Herbert A. Simon (Turing Award Winner & Nobel Laureate)

在所有的人生决策中，最令人焦虑的莫过于“寻找伴侣”。
In all of life's decisions, the most anxiety-inducing is perhaps "finding a partner."

在这个 Tantan 和 Tinder 的时代，我们面临的困境不是选择太少，而是选择太多。手指轻轻一划，下一个可能更好。于是我们陷入了一种永恒的纠结：
In this era of Tantan and Tinder, the dilemma we face is not having too few choices, but too many. With a swipe of a finger, the next one might be better. Thus, we fall into an eternal struggle:
*   如果我现在结婚，万一后面遇到了更好的怎么办？
    *   If I marry now, what if I meet someone better later?
*   如果我继续找下去，万一最后只能剩下一堆烂得多的选项怎么办？
    *   If I keep looking, what if I end up with a pile of much worse options?

这不仅是一个情感问题，这在计算机科学中是一个经典的**最优停止问题（Optimal Stopping Problem）**，又被称为**“秘书问题”**或**“相亲问题”**。
This is not just an emotional issue; in computer science, this is a classic **Optimal Stopping Problem**, also known as the **"Secretary Problem"** or the **"Marriage Problem."**

数学家们发现，面对这种“单向的时间流”和“不可回头的选择”，竟然存在一个精确的黄金分割点。
Mathematicians have discovered that facing this "unidirectional flow of time" and "irreversible choices," there actually exists a precise golden ratio point.

### 困境：在线算法的残酷
### The Dilemma: The Cruelty of Online Algorithms

在这个模型里，我们要面对几个残酷的公理（这也符合 Chapter 1 提到的公理）：
In this model, we have to face several cruel axioms (which also align with the axioms mentioned in Chapter 1):
1.  **序列性**：人是一个个出现的，你不能把他们一次性全列出来对比。
    *   **Sequentiality**: People appear one by one; you cannot list them all at once for comparison.
2.  **不可回头**：一般来说，你错过了一个人，就很难再回头去找他/她。
    *   **No Return**: Generally speaking, once you miss someone, it is hard to go back and find them again.
3.  **盲盒**：你不知道后面还有谁，也不知道一共有多少人适合你。
    *   **Blind Box**: You don't know who is coming next, nor do you know the total number of people suitable for you.

在这种情况下，如果你选择得太早，你可能还没见过世面，错过真正的珍珠；如果你选择得太晚，好的可能都已经被挑走了。
In this scenario, if you choose too early, you might lack experience and miss the real pearl; if you choose too late, the good ones might all be taken.

### 37% 规则：理性的刹车片
### The 37% Rule: The Rational Brake

数学推导出的最优策略出乎意料地简洁，被称为 **37% 规则**。
The optimal strategy derived from mathematics is unexpectedly simple, known as the **37% Rule**.

这一策略把寻找过程分为两个阶段：
This strategy divides the search process into two phases:
1.  **观察期（Explore）**：在前 37% 的时间里（或者前 37% 的人数里），**只看不选**。无论遇到多心动的人，都不要许下承诺。这个阶段的目标不是“拥有”，而是“建立基准（Benchmark）”。你需要知道这个市场大概是什么水平，什么是“好”，什么是“极好”。
    *   **Observation Phase (Explore)**: In the first 37% of the time (or the first 37% of candidates), **look but do not choose**. No matter how tempted you are, do not make a commitment. The goal of this phase is not "possession," but "benchmarking." You need to know the general level of the market, what is "good," and what is "excellent."
2.  **行动期（Exploit）**：过了这个节点后，一旦遇到**任何一个比观察期里最好的人还要好（或者持平）**的人，**立刻拿下**，不再看后面任何一眼。
    *   **Action Phase (Exploit)**: After this point, once you meet **anyone who is better than (or equal to) the best person from the observation phase**, **commit immediately** and never look back.

数学证明，这个策略能让你选中“全局最优解”的概率最大化（约为 37%）。
Mathematical proof shows that this strategy maximizes the probability of selecting the "global optimum" (approximately 37%).

### 探索（Explore） vs 利用（Exploit）
### Explore vs. Exploit

37% 规则的本质，是解决计算机科学中著名的 **Explore/Exploit Trade-off（探索与利用的权衡）**。
The essence of the 37% Rule is resolving the famous **Explore/Exploit Trade-off** in computer science.

*   **Explore（探索）**：指去收集信息，去尝试未知的可能性。
    *   **Explore**: To collect information and try unknown possibilities.
*   **Exploit（利用）**：指根据已知信息，做出当下最好的决定，获取回报。
    *   **Exploit**: To make the best decision based on known information and reap the rewards.

现代人的痛苦，往往在于**过度探索（Over-Exploration）**。在信息爆炸的时代，我们总觉得“再刷一下，也许有更好的内容”，“再划一下，也许有更适合的人”。我们的手指在屏幕上无休止地滑动，一直处于 Explore 模式，却从未进入 Exploit 模式。
The misery of modern people often lies in **Over-Exploration**. In the age of information explosion, we always feel "swipe again, maybe there's better content," "swipe again, maybe there's a more suitable person." Our fingers slide endlessly on the screen, constantly in Explore mode, yet never entering Exploit mode.

算法告诉我们：**无限的探索是零收益的。**一个只探索不利用的系统，就像一只不断闻味却从不张嘴吃肉的狼，最终会饿死在寻找最完美猎物的路上。
Algorithms tell us: **Infinite exploration yields zero return.** A system that only explores without exploiting is like a wolf that constantly sniffs but never opens its mouth to eat, eventually starving to death on the way to finding the perfect prey.

### 完美的敌人
### The Enemy of Perfect

当然，37% 规则应用到恋爱中，并不是让你掐着表去谈恋爱。它传递的是一种深刻的**止损智慧**。
Of course, applying the 37% Rule to love doesn't mean you should date with a stopwatch. It conveys a profound wisdom of **cutting losses**.

它通过数学告诉我们三件事：
It tells us three things through mathematics:
1.  **必须要试错**：年轻时的几段“无果而终”的恋爱不是浪费时间，那是必要的 Sample（采样）。没有这些样本，你根本无法建立正确的 Benchmark。
    *   **Trial and Error is Mandatory**: Relationships that "end fruitlessly" in your youth are not a waste of time; they are necessary Samples. Without these samples, you simply cannot establish a correct Benchmark.
2.  **必须要有停止点**：你不可能遍历全世界。当你建立了足够样本后，遇到那个超越基准的人，就要有勇气按下停止键。
    *   **There Must Be a Stopping Point**: You cannot traverse the whole world. Once you have established enough samples and meet someone who surpasses the benchmark, you must have the courage to press the stop button.
3.  **接受“错过”**：哪怕用了最优策略，你依然有 63% 的概率错过真爱。但这是在不确定性世界里的最优解。
    *   **Accept "Missing Out"**: Even with the optimal strategy, you still have a 63% chance of missing true love. But this is the optimal solution in a world of uncertainty.

### 小结
### Summary

完美的伴侣是不存在的，或者说，寻找完美伴侣的算法复杂度是人类寿命无法承受的。
The perfect partner does not exist, or rather, the algorithmic complexity of finding a perfect partner is unbearable for a human lifespan.

算法思维给出的建议是：给自己划定一个**观察期**（比如 20-28 岁），尽情去探索，去建立标准。一旦过了这个窗口，请收起你的望远镜。当下一个超越你标准的人出现时，不要再想“后面会不会有更好的”。
The suggestion from algorithmic thinking is: define an **Observation Phase** for yourself (e.g., ages 20-28), explore to your heart's content, and establish standards. Once this window passes, please put away your telescope. When the next person who surpasses your standards appears, do not wonder "will there be a better one later?"

**抓住手里的，就是最优解。**
**Holding onto what you have is the optimal solution.**

运气，其实就是在这 37% 的时刻，做好了准备。
Luck, in fact, is being prepared at this 37% moment.
