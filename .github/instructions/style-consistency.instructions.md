---
description: "Use when writing, editing, or extending chapters in 'Algorithm for Future Leaders'. Enforces bilingual (Chinese/English) structure, heading hierarchy, formatting conventions, callout patterns, and mathematical notation standards for both Volume I and Volume II."
applyTo: "**/*.md"
---

# Style Consistency: Algorithm for Future Leaders

## Language & Bilingualism

- Every substantive paragraph must appear in **both Chinese and English**, with Chinese first.
- Every section heading must appear in both languages, either on the same line `## 公理一：约束是真实的 (Axiom 1: Constraints are Real)` or as a Chinese/English paired title pair.
- Technical algorithm names, complexity notations, and well-known English terms (e.g., `Greedy`, `DP`, `NP-Hard`, `Brute Force`) are kept in English even in Chinese text.
- New terms are introduced as: **中文名（English Name）** in bold on first use, then referenced consistently afterward.

## Header Hierarchy

| Level | Usage |
|-------|-------|
| `#` | Chapter title only — format: `# 第N章：[Chinese] (English)` |
| `##` | Major sections |
| `###` | Subsections |
| `####` | Minor breakdowns (use sparingly) |

Never skip a heading level. Never use `#` for anything other than a chapter title.

## Chapter Structure

Each chapter must follow this order:
1. **H1 chapter title** (bilingual)
2. **Epigraph / blockquote** — original-language quote, then Chinese translation, then `—— Author`
3. **Opening context** — relatable or philosophical framing with questions like "为什么...？ / Why do...?"
4. **Intuitive explanation** — concept explained before any formalism
5. **Technical deep-dive** — formal definitions, algorithm logic, invariants
6. **Examples and case studies** — concrete problems with code
7. **Summary** — one-line or short summary, bilingual

## Epigraphs & Blockquotes

```markdown
> "Original quote in English or source language."
> "中文翻译。"
> —— Author Name
```

Always use two trailing spaces after each `>` line for line breaks inside the blockquote.

## Emphasis & Inline Formatting

- **Bold**: Key concepts, definitions, algorithm names on first introduction, critical invariants and principles.
- *Italic*: Minor emphasis, attributions, rarely used.
- `` `backticks` ``: Code identifiers, variable names, complexity like `O(log n)`, short expressions like `while (left <= right)`.
- Do NOT bold entire paragraphs. Bold is for phrases and terms, not sentences.

## Code Blocks

- Always specify the language: ` ```python `, ` ```cpp `, etc.
- Include comments in English (bilingual optional for key lines).
- Use clear, descriptive variable names.
- Explain invariants and pre/postconditions in comments.

## Math Notation

- Inline math: `$O(N)$`, `$[L, R]$`, `$\text{Target} \in \text{nums}[left..right]$`
- Display math for core formulas:
  ```
  $$\text{Efficient Algorithm} = \text{Invariant (Correctness)} + \text{Monotonicity (Efficiency)}$$
  ```
- Use `\text{}` for words inside math environments.

## Lists

- **Bullet lists** (`-`): Concept elaborations, feature comparisons, related points. Each bullet should include a Chinese statement followed by its English equivalent.
- **Numbered lists**: Step-by-step procedures, algorithm phases (Initialization → Maintenance → Termination), sequential decisions.
- Nesting is allowed up to 4 levels; alternate `-` and `*` for visual distinction.
- Do not mix numbered and bullet lists at the same nesting level.

## Tables

- Use left-aligned columns (`:---`) by default.
- For bilingual tables, include both languages in the header: `| 类别 (Category) |`
- Bold important header cells.
- Example structure:
  ```markdown
  | 算法范式 | 进程变量 | 状态语义 |
  | :--- | :--- | :--- |
  | DP | 子问题规模 单调增 | dp[i] 表示规模 i 的最优解 |
  ```

## Key Term Introduction Pattern

1. Bold the Chinese name with English in parentheses: `**贪心算法（Greedy Algorithm）**`
2. Immediately provide a one-sentence definition in both languages.
3. Use the abbreviation or English form consistently thereafter.

## Summary / One-Line Summary Pattern

Use a blockquote callout at the end of sections for key takeaways:

```markdown
> **一句话总结（One-Line Summary）**：
> [Chinese summary.]
> [English summary.]
```

## Tone & Voice

- Begin chapters with philosophical or intuitive questions before introducing formalism.
- Write for a reader who understands algorithms but benefits from conceptual grounding.
- Avoid overly academic or dry phrasing — bridge abstract concepts to real decision-making.
- Use first-person plural ("we") sparingly; prefer direct exposition.
