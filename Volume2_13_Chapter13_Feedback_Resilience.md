# 第十三章：系统的呼吸 (Feedback & Resilience) —— 限流即也是一种保护
# Chapter 13: The Breath of Systems (Feedback & Resilience) — Limiting is Protecting

> "Stability is not the absence of change, but the ability to cope with it."  
> "稳定不是没有变化，而是应对变化的能力。"  

在 Volume 1 的 **"Feedback"** 章节，我们讨论了正反馈（爆炸）和负反馈（稳定）。
In Volume 1's chapter on **"Feedback"**, we discussed Positive Feedback (Explosion) and Negative Feedback (Stability).

在工程世界里，**负反馈 (Negative Feedback)** 是系统生存的根基。
In the engineering world, **Negative Feedback** is the foundation of system survival.
这就是 **Control Theory (控制论)** 的核心：当 Error（误差/压力）变大时，施加一个反向的力，让系统回归稳态。

今天，我们要实现互联网基础设施中最不起眼但最重要的组件——**限流器 (Rate Limiter)**。
Today, we will implement the most humble yet most critical component of internet infrastructure—**The Rate Limiter**.

**如果你不能控制它，那就限制它。** 没有任何系统能承载无限的压力。与其在过载中崩溃，不如优雅地拒绝。
**If you can't control it, limit it.** No system can bear infinite pressure. Better to reject elegantly than to crash in overload.
 
## 一、当潮水涌来
## I. When the Tide Comes

假设你的服务器每秒只能处理 100 个请求 (QPS)。
Suppose your server can only handle 100 requests per second (QPS).

突然，黑客攻击（DDoS）或者突发热点（Celebrity News）导致流量飙升到 10,000 QPS。
Suddenly, a hacker attack (DDoS) or a sudden hotspot (Celebrity News) causes traffic to spike to 10,000 QPS.

### 1. 无保护状态
CPU 飙升到 100%，内存耗尽，数据库连接池卡死。
CPU spikes to 100%, memory is exhausted, DB connection pool hangs.
**结果**：宕机。那 100 个正常用户也无法访问了。
**Result**: Downtime. Even the 100 normal users cannot access it.

### 2. 也是一种拒绝 (Load Shedding)
限流器说：**“对不起，现在太挤了，请稍后再来。”**
It says: **"Sorry, too crowded, please come back later."**
它丢弃了 9,900 个请求，但保住了那 100 个请求的成功执行。
It drops 9,900 requests but ensures the successful execution of the 100 requests.

**活着，比服务所有人更重要。**
**Being alive is more important than serving everyone.**

## 二、令牌桶算法 (Token Bucket)
## II. Token Bucket Algorithm

如何实现限流？最优雅的物理模型是 **令牌桶 (Token Bucket)**。

*   **Bucket Strategy**：有一个桶，容量是 $C$。
*   **Refill Rate**：以恒定的速率 $R$ 往桶里扔“令牌 (Token)”。如果桶满了，多余的令牌就溢出丢掉。
*   **Consumption**：每来一个请求，必须从桶里拿走一个令牌。
    *   拿到了 $\rightarrow$ 处理请求。
    *   桶空了 $\rightarrow$ 拒绝请求 (HTTP 429 Too Many Requests)。

这个模型的精妙之处在于它允许**突发流量 (Burst)**。
The beauty of this model is that it allows **Bursts**.
只要桶里有存货，你可以瞬间处理一批请求，然后再慢慢回血。

## 三、代码实现 (Code Implementation)
## III. Code Implementation

这是一个生产级限流器的极简核心版。

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity      # 桶的容量 (比如 100)
        self.refill_rate = refill_rate # 充能速度 (比如 10 tokens/sec)
        self.tokens = capacity        # 当前令牌数 (初始满)
        self.last_refill_timestamp = time.time()
        
    def allow_request(self, tokens_needed=1):
        self._refill() # 先尝试充能
        
        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True # 通过
        else:
            return False # 拒绝 (429)
            
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_timestamp
        
        # 计算这段时间通过了，应该生成多少新令牌
        new_tokens = elapsed * self.refill_rate
        
        if new_tokens > 0:
            # 令牌不能超过容量
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill_timestamp = now

# Engineering Case:
# API 限流：容量 10，每秒恢复 1 个
limiter = TokenBucket(capacity=10, refill_rate=1)

# 模拟突发流量
for i in range(15):
    allowed = limiter.allow_request()
    print(f"Request {i}: {'Allowed' if allowed else 'Rejected'}")
    
# output: 
# 前 10 个瞬间通过 (消耗库存)
# 第 11-14 个被拒绝 (库存空了，且恢复速度没跟上)
```

### 关键点解析 (Key Insights)

1.  **时间的积分**：
    *   `elapsed * refill_rate` 本质上是对时间的积分。
    *   我们不需要开一个后台线程每秒钟去 `+1`（那样太重了）。我们利用**惰性计算 (Lazy Calculation)**，只在请求来的时候计算一下“上次到现在积累了多少钱”。

2.  **Backoff (退避)**：
    *   当 Client 收到 `False` (429) 时，他不应该立刻重试（那会让拥堵更严重）。
    *   他应该 `sleep(exponential_backoff)`。**退一步，海阔天空。**

## 四、系统的呼吸
## IV. The Breathing of Systems

一个健康的系统，必须像生物一样会**呼吸**。
A healthy system must **breathe** like a living organism.

*   **吸 (Refill)**：积累资源，恢复能量。
*   **呼 (Consume)**：处理请求，释放能量。

如果你只呼不吸（无限接客），你会窒息。
如果你只吸不呼（囤积资源），你会便秘（资源浪费）。

**决策智慧**：
在职场和生活中，**Token Bucket** 也是你的精力管理模型。
*   你的精力是有限的 `capacity`。
*   睡眠和休息是 `refill_rate`。
*   如果任务（Process Request）来得太快，超过了你的恢复速度，你要学会返回 **HTTP 429 (Say "No")**。
*   这不是无能，这是为了防止系统崩溃 (Burnout)，为了明天还能继续工作。

**懂得拒绝系统的输入，才能保证系统的输出稳定。**
**Knowing how to reject system input is the only way to guarantee stable system output.**
