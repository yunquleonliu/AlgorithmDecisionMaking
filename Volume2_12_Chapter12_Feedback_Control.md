# 第12章：有限资源与反馈控制 (Limited Resources and Feedback Control)

> "A resilient system spends some requests to preserve its capacity to serve the next."  
> “有韧性的系统会放弃部分请求，以保住服务下一批请求的能力。”  
> —— Original epigraph

任何有限容量系统都要回答：请求超过处理能力时，允许谁、拒绝谁、何时恢复？限流器不是增加容量，而是维持容量约束。

Every finite-capacity system must answer who is allowed, who is rejected, and when service recovers when requests exceed capacity. A limiter does not add capacity; it maintains a capacity constraint.

## Rate Limiter 的信息需求 (Information Requirement of a Rate Limiter)

令牌桶需要容量 `C`、补充速度 `R` 和每个请求成本。状态只需当前令牌与上次更新时间，而不必保留全部历史请求。

A token bucket needs capacity `C`, refill rate `R`, and cost per request. State requires only current tokens and the last update time, not the complete request history.

$$
T_{\text{new}}=\min\left(C,\ T_{\text{old}}+R\Delta t\right).
$$

这种惰性计算在请求到达时结算时间积分；不需要独立线程逐次加令牌。

This lazy computation settles the time integral when a request arrives; it needs no separate token-by-token thread.

```python
import time

class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        if capacity < 0 or refill_rate < 0:
            raise ValueError("capacity and refill_rate must be nonnegative")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.updated_at = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        if cost < 0:
            raise ValueError("cost must be nonnegative")
        now = time.monotonic()
        elapsed = now - self.updated_at
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.updated_at = now
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True
```

## Burst 与长期速率 (Burst and Long-Term Rate)

容量允许短时爆发；补充速度控制长期平均。如果需要严格窗口限额，Token Bucket 的语义可能与 Sliding Log 或 Fixed Window 不同。

Capacity permits short bursts; refill rate controls the long-term average. If a strict window quota is required, a Token Bucket may not match a Sliding Log or Fixed Window.

## 反馈信号与 Backoff (Feedback Signals and Backoff)

`429`、队列长度、超时或饱和指标可作为负反馈。客户端应在重试前等待，并可使用带抖动的 Exponential Backoff 避免同步重试。

`429`, queue length, timeout, or saturation metrics can be negative-feedback signals. Clients should wait before retrying and may use jittered Exponential Backoff to avoid synchronized retries.

Backoff 不是限流器内部的同一个机制；它是消费方对失败信号的响应策略。

Backoff is not the limiter's internal mechanism; it is a consumer response policy to a failure signal.

## 分布式边界 (Distributed Boundaries)

单进程桶容易按调用顺序更新；多实例共享总额时，还需共享原子存储、租约、一致的时钟假设或确定性分配。

A single-process bucket is easy to update serially; shared quotas across instances need atomic shared storage, leases, clock assumptions, or deterministic allocation.

`time.monotonic()` 适合单进程持续时间，不适合作为跨主机共同基准；分布式实现需明确时钟来源。

`time.monotonic()` measures single-process duration, not a common clock across hosts; distributed implementations must state the time source.

> **机制 vs 类比（Mechanism vs Analogy）**：  
> 系统像“呼吸”只是类比。真正机制是资源守恒、时间积分、准入决策与失败反馈。  
> A system resembling “breathing” is only an analogy. The actual mechanism is resource accounting, time integration, admission decisions, and failure feedback.

## 边界与反例 (Boundary and Counterexample)

- 容量大不代表长期允许更高平均速率；补充率才决定稳定上限。A large bucket does not raise the long-term average; refill rate does.
- 拒绝太晚会已消耗 CPU、内存或下游连接，限流应尽量位于受保护资源前。Rejecting too late may already consume CPU, memory, or downstream connections, so admission should happen before protected resources.
- Token 成本为可变值时，必须确认最大请求成本、原子扣费与浮点误差。Variable token costs require maximum request costs, atomic charging, and floating-point considerations.

> **一句话总结（One-Line Summary）**：  
> 限流以小而充分的资源状态实现准入边界，反馈与 Backoff 再调节负载回到可承受区域。  
> Rate limiting uses a small sufficient resource state to enforce admission boundaries, while feedback and Backoff return load to a tolerable region.

## 章节导航 (Navigation)

👈 **上一章：[第11章：启发式与最优性边界](Volume2_11_Chapter11_Heuristic_Search.md)**  
👉 **下一章：[第13章：从问题结构推导算法](Volume2_13_Chapter13_Deriving_Algorithms.md)**
