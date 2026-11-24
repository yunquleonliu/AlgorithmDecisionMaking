# 第10章：不确定性下的权衡 (Trade-offs Under Uncertainty)

> "A guarantee must name the uncertainty it permits."  
> “保证必须说明它允许哪一种不确定性。”  
> —— Volume II Editorial Note

当内存不足、输入流未知或搜索输入可由对手控制时，确定性保证、随机保证、概率误差和空间成本需要分开说明。

When memory is insufficient, stream length is unknown, or an adversary controls search input, deterministic guarantees, randomized guarantees, probabilistic error, and space costs must be stated separately.

## Reservoir Sampling：有限内存中的均匀样本 (Reservoir Sampling: Uniform Samples with Bounded Memory)

未知长度流中保存固定 `k` 个样本。处理第 `t` 个元素时，选择 $j\in[0,t)$；若 `j<k`，替换第 `j` 个样本。

In an unknown-length stream, retain a fixed `k` samples. On item `t`, choose $j\in[0,t)$; if `j<k`, replace reservoir slot `j`.

```python
import random
from collections.abc import Iterable

def reservoir_sample(stream: Iterable[int], capacity: int) -> list[int]:
    if capacity < 0:
        raise ValueError("capacity must be nonnegative")
    reservoir: list[int] = []
    for count, item in enumerate(stream, start=1):
        if count <= capacity:
            reservoir.append(item)
        else:
            choice = random.randrange(count)
            if choice < capacity:
                reservoir[choice] = item
    return reservoir
```

归纳可得，处理完 $t\ge k$ 个元素后任意前缀元素留在池中的概率都是 $k/t$。

Induction shows that after $t\ge k$ items, every prior item remains with probability $k/t$.

空间 $O(k)$，处理每项为 $O(1)$，但随机性来源必须足够好。该算法保证边缘均匀性与任意 $k$ 元子集的均匀选择，而不是每项都能同时独立入选。

Space is $O(k)$ and each item costs $O(1)$, assuming adequate randomness. It gives uniform $k$-subsets rather than independent inclusion of every item.

## Bloom Filter：单向错误 (Bloom Filter: One-Sided Error)

Bloom Filter 用位数组和 `k` 个哈希位置回答成员测试。若任何测试位为 0，可确定元素未被添加；若全部为 1，只能回答“可能存在”。

A Bloom Filter answers membership with a bit array and `k` hash positions. Any zero bit proves the element was not inserted; all ones mean only “possibly present.”

```python
class BloomFilter:
    def __init__(self, size: int):
        self.bits = 0
        self.size = size

    def _positions(self, item: str) -> tuple[int, int, int]:
        encoded = item.encode("utf-8")
        import hashlib
        return tuple(
            int.from_bytes(hashlib.sha256(seed + encoded).digest(), "big") % self.size
            for seed in (b"a", b"b", b"c")
        )

    def add(self, item: str) -> None:
        for position in self._positions(item):
            self.bits |= 1 << position

    def might_contain(self, item: str) -> bool:
        return all(self.bits & (1 << position) for position in self._positions(item))
```

### 假阳性模型 (False-Positive Model)

理想独立哈希下，插入 `n` 项后，近似假阳性率为：

With ideal independent hashes, after `n` insertions the approximate false-positive rate is:

$$
p_{\mathrm{fp}}\approx \left(1-e^{-kn/m}\right)^k.
$$

达到目标错误率需要根据预计 `n`、位数 `m` 和哈希数 `k` 一起设计；只增加哈希次数并不一定降低误报。

Meeting a target error rate requires choosing `n`, `m`, and `k` together; simply adding hashes does not always reduce false positives.

### 不是语义分布特征 (Not Semantic Distributed Features)

Bloom Filter 的同一个位可能被许多无关元素共享；该共享来自哈希碰撞与覆盖，不自动代表“水果”“危险”等语义特征。

A Bloom bit can be shared by unrelated elements; that sharing comes from hash collisions and coverage, not automatically from semantic features such as “fruit” or “danger.”

> **机制 vs 类比（Mechanism vs Analogy）**：  
> Bloom bits 可类比为分布式表示，但这只是类比。它们没有训练得到的可解释或可迁移语义。  
> Bloom bits can be compared with distributed representations, but this is only an analogy. They have no learned, interpretable, or transferable semantics.

## Randomized Quicksort：期望不等于消除最坏情况 (Randomized Quicksort: Expectation Is Not Elimination)

随机 Pivot 使固定的恶意排列不再天然指定不良 Pivot，通常给出 $O(n\log n)$ 期望时间。

A random Pivot prevents a fixed adversarial permutation from naturally specifying bad pivots and normally gives expected $O(n\log n)$ time.

但随机过程仍可能每次选到极端元素；因此最坏时间仍为 $O(n^2)$，只是概率与对抗关系改变。

The random process can still select extreme elements repeatedly; worst-case time remains $O(n^2)$, though probability and adversarial control change.

## 错误、保证与边界 (Errors, Guarantees, and Boundaries)

| 方法 (Method) | 保证 (Guarantee) | 代价 (Trade-off) |
| :--- | :--- | :--- |
| Reservoir Sampling | 均匀抽样；与随机源有关 (uniform sampling; depends on randomness) | 不能恢复未采样项 (discarded items cannot be recovered) |
| Bloom Filter | 无假阴性；假阳性随参数变化 (no false negatives; tunable false positives) | 不支持删除标准位；不可枚举成员 (no standard deletion; no enumeration) |
| Random Pivot | 期望复杂度改善 (expected complexity improves) | 最坏 $O(n^2)$ 仍存在 (worst $O(n^2)$ remains) |

> **一句话总结（One-Line Summary）**：  
> 不确定性算法以明确的错误类型或期望保证换取资源，不能用“随机”替代对最坏边界的声明。  
> Algorithms under uncertainty trade explicit error types or expected guarantees for resources; “random” cannot replace a worst-case boundary.

## 章节导航 (Navigation)

👈 **上一章：[第9章：等价类与代数结构](Volume2_09_Chapter09_Equivalence_Algebra.md)**  
👉 **下一章：[第11章：启发式与最优性边界](Volume2_11_Chapter11_Heuristic_Search.md)**
