---
name: android-interview-feedback
description: Use when writing or refining Android interview feedback from interview transcripts, especially when the output must be evidence-based, conservatively scored, and avoid exaggerated evaluation language.
---

# Android Interview Feedback

## Use This Skill When

- The user provides Android interview notes, transcripts, or Q&A records and asks for interview feedback.
- The user asks to organize interview answers into dimensions such as technology, experience, basic qualities, or high-potential qualities.
- The user asks to optimize, apply, or enforce a conservative interview-feedback template.

## Core Rules

- Base every conclusion on the interview record only.
- Separate what the candidate said from what the answer can support.
- Do not add, infer, embellish, or repair missing information.
- Remove filler words and repeated connective phrases when summarizing, while preserving meaning and factual details.
- Prefer conservative scoring when evidence is incomplete.
- Mark `未考察` when a dimension was not covered.
- Mark `信息不足` when the record is insufficient for a supported judgment.

## Scoring

Use only these scores:

| Score | Meaning |
| --- | --- |
| `2.5` | 未达到岗位要求；回答有明显错误、明显缺失，或无法支撑能力判断。 |
| `3` | 基本达到要求；回答较浅、结构不完整，或主要停留在经验描述。 |
| `3+` | 达到要求；回答较完整，能覆盖关键点，并有一定实践或思考支撑。 |
| `3.5` | 明显高于要求；回答完整、准确、深入，并体现系统性思考、权衡意识或较强实践沉淀。 |

Scoring constraints:

- Default to the lower score when evidence is ambiguous.
- Do not give `3.5` without clear, repeatable evidence in the record.
- Give `3+` or `3.5` only when the answer contains concrete support, not just claimed ownership.
- If a competency has only indirect evidence, the maximum score is `3` unless the transcript directly supports more.

## Language Discipline

Avoid high-intensity praise unless the score is `3.5` and at least two concrete evidence points are cited.

Avoid words such as:

- `极其`
- `非常`
- `顶尖`
- `卓越`
- `出色`
- `很强`
- `远超`
- `完美`
- `优秀到明显领先`

Prefer restrained evidence-based phrasing:

- `回答覆盖了...`
- `能够说明...`
- `体现出一定的...`
- `有实践经验支撑...`
- `展开不充分...`
- `关键细节缺失...`
- `信息不足以判断...`
- `未体现出...`
- `回答停留在...层面`

## Required Output Format

```text
【综合评价】

总体结论：[岗位匹配度 / 适合方向建议。必须基于下方证据，避免夸张评价。]

Pros：

- [亮点1：必须来自面试记录]
- [亮点2：必须来自面试记录]

Cons：

- [短板1：必须来自面试记录]
- [风险点/疑问点1：如信息不足，请明确说明]

【技术】[分数 / 信息不足 / 未考察]

- 基础知识：[分数 / 信息不足 / 未考察]
- 算法和数据结构：[分数 / 信息不足 / 未考察]
- 编码能力：[分数 / 信息不足 / 未考察]
- 设计能力：[分数 / 信息不足 / 未考察]
- 其他补充：[如有请注明]

详细反馈：

- [问题]：
  [分数]：
  [回答]：
  [评价]：

【经验】[分数 / 信息不足 / 未考察]

- 项目经验：[分数 / 信息不足 / 未考察]
- 业务理解：[分数 / 信息不足 / 未考察]
- 其他补充：[如有请注明]

详细反馈：

- [问题]：
  [分数]：
  [回答]：
  [评价]：

【基本素质】[分数 / 信息不足 / 未考察]

- 团队协作：[分数 / 信息不足 / 未考察]
- 沟通表达：[分数 / 信息不足 / 未考察]
- owner 意识：[分数 / 信息不足 / 未考察]
- 解决问题能力：[分数 / 信息不足 / 未考察]
- 其他补充：[如有请注明]

详细反馈：

- [问题]：
  [分数]：
  [回答]：
  [评价]：

【高潜素质】[分数 / 信息不足 / 未考察]

- 聪明：[分数 / 信息不足 / 未考察]
- 自驱：[分数 / 信息不足 / 未考察]
- 韧性：[分数 / 信息不足 / 未考察]
- 其他补充：[可自定义子项并打分]

详细反馈：

- [问题]：
  [分数]：
  [回答]：
  [评价]：

【字节范】

[选填。如下一轮需要关注，请说明具体原因。没有充分证据时写“信息不足”。]
```

## Feedback Item Format

Each Q&A item must use:

```text
[问题]：面试官问题概括
[分数]：2.5 / 3 / 3+ / 3.5 / 信息不足 / 未考察
[回答]：候选人回答概括，忠于原文
[评价]：基于回答的判断，只写可由原文支撑的结论
```

## Final Check

Before responding, verify:

- Every score has transcript evidence or is marked `信息不足` / `未考察`.
- No unsupported claims were added.
- High-intensity praise was removed unless justified by `3.5` evidence.
- The output preserves the required section order and labels.
