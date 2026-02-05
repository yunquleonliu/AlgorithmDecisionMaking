# 第五章：概率 (Probability) —— 人可以抛骰子计算
# Chapter 05: Probability — Calculating by Rolling Dice

> "It is a scientific fact that the future is unpredictable. ... So, the only way to prepare for the future is to create a future that is robust."  
> —— A Consensus in Modern Complexity Theory (or inspired by Stanislaw Ulam)

> "The probable is what usually happens."  
> —— Aristotle

人类的大脑天生厌恶不确定性。我们喜欢因果律，喜欢“如果...就...”，喜欢如同精密钟表一样的牛顿式宇宙。然而，现实世界更像是混沌的。当我们试图用“确定性思维”去规划一个充满变数的人生项目（比如创业、投资、或者抚养孩子）时，我们不仅会陷入焦虑，还经常会犯下大错。
The human brain is naturally averse to uncertainty. We like causality, we like "if... then...", and we like the Newtonian universe that operates like a precision clock. However, the real world is more like chaos. When we try to plan a life project full of variables (such as entrepreneurship, investing, or raising children) using "deterministic thinking," we not only fall into anxiety but often make grave mistakes.

计算机科学家在处理最棘手的计算问题时，往往会放弃“精确解”，转而求助于一种看似狂野的方法：**随机性**。
When computer scientists deal with the most intractable computational problems, they often abandon "exact solutions" and turn to a seemingly wild method: **Randomness**.

这一章的主角，是现代算法中最具颠覆性的思想工具：**蒙特卡洛方法（Monte Carlo Method）**。
The protagonist of this chapter is the most disruptive intellectual tool in modern algorithms: **The Monte Carlo Method**.

### 乌拉姆的纸牌：别算，去试
### Ulam's Solitaire: Don't Calculate, Just Try

二战期间，数学家斯塔尼斯拉夫·乌拉姆（Stanislaw Ulam）在养病时玩纸牌接龙。他想计算出“一副乱序的牌能成功解开的概率是多少”。作为顶级数学家，他的第一反应是拿起笔，试图用组合数学公式进行精确推导。但他很快发现，计算量大到了连他都无法驾驭的程度。
During World War II, mathematician Stanislaw Ulam was playing solitaire while recovering from an illness. He wanted to calculate "what is the probability that a shuffled deck can be successfully solved." As a top mathematician, his first reaction was to pick up a pen and try to derive it precisely using combinatorial mathematics formulas. But he soon realized that the computational volume was so vast that even he could not master it.

于是他换了一个思路：“如果我不去‘算’它，而是直接‘玩’它呢？如果我快速地玩 100 把，其中赢了 35 把，我是不是就可以说，成功的概率大概是 35%？”
So he changed his approach: "What if I don't 'calculate' it, but just 'play' it? If I play 100 games quickly and win 35 of them, can I say that the probability of success is approximately 35%?"

这个极其朴素的思想，后来成为了制造原子弹、预测天气和训练 AlphaGo 的核心算法。
This extremely simple idea later became the core algorithm for building atomic bombs, predicting weather, and training AlphaGo.

### 蒙特卡洛智慧：采样胜过推导
### Monte Carlo Wisdom: Sampling Beats Deduction

在算法世界观里，这告诉我们一个深刻的道理：**当面对一个过于复杂的系统时，逻辑推导（Prediction）往往是脆弱的，而随机模拟（Simulation）才是鲁棒的。**
In the algorithmic worldview, this teaches us a profound truth: **When facing a system that is too complex, logical deduction (Prediction) is often fragile, while random simulation (Simulation) is robust.**

我们经常陷入“分析瘫痪”：
We often fall into "Analysis Paralysis":
*   这个产品推出后市场反应会怎样？（试图推导所有变量）
    *   How will the market react after this product is launched? (Trying to deduce all variables)
*   选这个专业将来会不会失业？（试图预测宏观原本）
    *   Will choosing this major lead to unemployment in the future? (Trying to predict the macro script)

算法建议：**不要试图推导。去采样（Sampling）。**
The algorithm recommends: **Do not try to deduce. Go Sample.**
*   与其闭门造车写几百页的商业计划书，不如先做一个最小可行性产品（MVP）扔到市场上去跑两周。
    *   Instead of writing a business plan of hundreds of pages behind closed doors, it is better to build a Minimum Viable Product (MVP) and let it run in the market for two weeks.
*   与其纠结哪个职业更好，不如利用假期去那个行业实习（采样）一个月。
    *   Instead of agonizing over which career is better, use your vacation to intern (sample) in that industry for a month.

你不需要喝光整桶汤才知道它咸不咸，只需要喝一勺（采样）。只要样本是随机且具有代表性的，**模糊的正确永远胜过精确的错误**。
You don’t need to drink the whole pot of soup to know if it’s salty; you just need to taste a spoonful (sample). As long as the sample is random and representative, **vague correctness is always better than precise error.**

### 两座赌城：蒙特卡洛 (Monte Carlo) vs 拉斯维加斯
### Two Gambling Cities: Monte Carlo vs. Las Vegas

在引入随机性时，计算机科学家给出了两种截然不同的策略，并用两座著名的赌城来命名它们。理解这两者的区别，对生活决策至关重要。
When introducing randomness, computer scientists offered two distinctly different strategies and named them after two famous gambling cities. Understanding the difference between these two is crucial for life decisions.

1.  **蒙特卡洛算法 (Monte Carlo)**：
    *   **Monte Carlo Algorithm**:
    *   **哲学**：**“我一定要在 10 分钟内给出一个结果，哪怕它可能是错的（或者有误差）。”**
        *   **Philosophy**: **"I must give a result within 10 minutes, even if it might be wrong (or have errors)."**
    *   **交换**：用**精确性**换取**时间确定性**。
        *   **Exchange**: Trading **accuracy** for **time certainty**.
    *   **应用**：上述的乌拉姆纸牌、大选预测。当我们没有足够的时间去穷尽真相时，我们用概率换取速度。
        *   **Application**: The aforementioned Ulam's Solitaire, election predictions. When we don't have enough time to exhaust the truth, we trade accuracy for speed using probability.

2.  **拉斯维加斯算法 (Las Vegas)**：
    *   **Las Vegas Algorithm**:
    *   **哲学**：**“我一定要给出一个绝对正确的结果，哪怕它可能要花上无限长的时间。”**
        *   **Philosophy**: **"I must give an absolutely correct result, even if it might take an infinite amount of time."**
    *   **交换**：用**时间确定性**换取**精确性**。
        *   **Exchange**: Trading **time certainty** for **accuracy**.
    *   **应用**：寻找一把丢失的钥匙。你随机在各个口袋和抽屉里找，你不知道要找多久（时间不确定），但只要找到了，它一定是那把钥匙（结果绝对正确）。
        *   **Application**: Looking for a lost key. You check random pockets and drawers; you don't know how long it will take (time uncertainty), but once you find it, it is definitely that key (result absolute correctness).

### 随机化快排：用混乱对抗恶意
### Randomized Quicksort: Fighting Malice with Chaos

经典的 **快速排序（Quicksort）** 的随机化版本，本质上就是一种拉斯维加斯策略。
The randomized version of the classic **Quicksort** is essentially a Las Vegas strategy.

它通常很快，但在遇到特定的“恶意数据”（比如已经排好序的数据）时，它会慢得像蜗牛。为了避免这种最坏情况，聪明的工程师引入了**随机化**：在排序前，先随机打乱数据，或者随机选取基准点。
It is usually fast, but when it encounters specific "malicious data" (such as data that is already sorted), it slows down to a snail's pace. To avoid this worst-case scenario, smart engineers introduced **randomization**: randomly shuffling the data before sorting, or randomly selecting a pivot thinking point.

这听起来很不讲理——为什么要故意把数据搞乱？
因为：**随机是唯一没有模式（Pattern）的东西。** 只要你足够随机，现实世界中那些恶意的、死板的、针对性的陷阱就很难击中你。
This sounds unreasonable—why deliberately mess up the data?
Because: **Randomness is the only thing without a Pattern.** As long as you are random enough, those malicious, rigid, and targeted traps in the real world will find it hard to hit you.

**决策智慧**：
**Decision Wisdom**:

*   **何时使用蒙特卡洛？** 当你面临**截止日期（Deadlines）**时。比如考试还剩 5 分钟，与其空着，不如像蒙特卡洛一样快速填满答题卡。在人生的大部分“此时此刻”的决策中，我们需要的是蒙特卡洛——给出一个过得去的解，然后继续前进。
    *   **When to use Monte Carlo?** When you face **Deadlines**. For instance, with 5 minutes left in an exam, instead of leaving it blank, fill the answer sheet quickly like Monte Carlo. In most "here and now" decisions in life, what we need is Monte Carlo—give a passable solution and keep moving.
*   **何时使用拉斯维加斯？** 当你需要**创新（Breakthroughs）**时。创新就是找钥匙，你不知道在哪，也不能接受“假钥匙”。这时候，你需要允许自己进行大量低成本的随机尝试（Random Trials）。不要按部就班，去读一本毫不相关的书，去一个从未去过的城市。这是一次“拉斯维加斯式”的随机游走，虽然效率不确定，但只有这样才能跳出局部最优，找到那个确定的“新大陆”。
    *   **When to use Las Vegas?** When you need **Breakthroughs**. Innovation is searching for a key; you don't know where it is, and you can't accept a "fake key." At this time, you need to allow yourself to conduct a large number of low-cost Random Trials. Don't follow the routine; read an irrelevant book, go to a city you've never been to. This is a "Las Vegas style" random walk; although the efficiency is uncertain, only in this way can you jump out of the local optimum and find that certain "New World."

### 小结
### Summary

拥抱概率，意味着放弃对“全知全能”的幻想。
Embracing probability means giving up the fantasy of "omniscience and omnipotence."

*   **从 Predicton（预测）转向 Simulation（模拟）**：别问“未来一定会怎样”，问“由于概率分布，我该如何配置仓位”。
    *   **Shift from Prediction to Simulation**: Don't ask "what will definitely happen in the future," ask "given the probability distribution, how should I allocate my positions."
*   **从 Certainty（确定性）转向 Robustness（鲁棒性）**：别追求一个这一刻完美的计划，追求一个在大多数随机未来里都不算太差的计划。
    *   **Shift from Certainty to Robustness**: Don't pursue a plan that is perfect for this moment; pursue a plan that is not too bad in most random futures.

上帝也许掷骰子，但在这个复杂的世界里，拿着骰子的人，才算得最准。
God may play dice, but in this complex world, the person holding the dice calculates most accurately.
