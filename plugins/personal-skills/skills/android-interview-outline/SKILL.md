---
name: android-interview-outline
description: Use when the user provides an Android candidate resume, asks to analyze the resume and produce an interview plan, wants questions selected from the prior Android interview question bank, or asks for a professional senior Android interviewer workflow with self-introduction, project discussion, detailed project follow-ups, computer fundamentals, and one algorithm problem.
---

# Android Interview Outline

## Workflow

1. Read the candidate resume screenshot or resume text first.
2. Extract only evidence visible in the resume:
   - current/previous companies and roles
   - years of experience if inferable
   - Android stack keywords
   - project domains
   - claimed responsibilities and measurable results
   - suspicious gaps, vague claims, or over-broad keywords
3. Build a candidate profile before writing questions:
   - seniority estimate: junior, mid-level, senior, staff-like, or unclear
   - strongest resume signals
   - risk points to verify
   - likely project depth
4. Select questions from `references/android-interview-question-bank.md`.
   - Load the reference only when choosing concrete questions.
   - Prefer questions matching the resume evidence.
   - Use broader fundamentals only to calibrate baseline ability.
   - Avoid asking unrelated niche topics just because they exist in the bank.
5. Draft a 60-minute interview outline in Chinese unless the user asks otherwise.
6. Publish the final outline to a Feishu/Lark document unless the user explicitly says not to create a document.
   - Use the `lark-doc` skill before creating or updating the document; it contains the required `lark-cli docs +create` workflow.
   - Read and follow the `lark-shared` skill if authentication, identity, or permission handling is needed.
   - Prefer creating the document as the current user so the candidate outline is immediately visible in the user's own cloud space.
   - If the user provides a folder, wiki node, or wiki space, create the document there. Otherwise create it in the default personal cloud space.
   - Use a clear title: `面试大纲：<候选人姓名或“候选人”> - Android 客户端`.
   - After creation succeeds, return the Feishu/Lark document URL and a brief summary. Do not paste the full outline in chat unless the user asks for it.
   - If document creation is blocked by missing CLI, login, scope, or permission, do not claim success. Explain the exact blocker and keep the generated outline ready to publish after the user completes the unblock step.

## Time Allocation

Use this default schedule unless the user specifies a different duration:

- 0-5 min: 自我介绍
- 5-20 min: 项目介绍与项目真实性校验
- 20-40 min: 项目深挖与 Android 专项问题
- 40-52 min: 计算机基础与工程基础
- 52-60 min: 算法题与总结

Adjust difficulty by resume level:

- Intern/new grad: mostly L1-L2, one L3 stretch question.
- 1-3 years: L2 core, several L3 mechanism questions.
- 3-6 years: L3 project depth, selected L4 architecture/stability questions.
- 6+ years or staff-like: L4 architecture, tradeoff, system design, team-level engineering governance.

## Output Format

Use this structure. When creating the Feishu/Lark document, put the title in the document title field and start the Markdown body at `## 1. 简历判断` to avoid duplicating the document title.

```markdown
## 1. 简历判断
- 年限/级别判断：
- 技术栈关键词：
- 项目关键词：
- 亮点：
- 风险点：

## 2. 60 分钟节奏
| 时间 | 模块 | 目标 |
|---|---|---|

## 3. 自我介绍（0-5 min）
- 观察点：
- 建议追问：

## 4. 项目介绍与深挖（5-40 min）
### 项目 A：<项目名>
- 让候选人先讲：
- 主问题：
- 深挖追问：
- 识别信号：
- 不合格信号：

## 5. Android 专项问题
### Q1 ...
- 来源题库：
- 难度：
- 提问：
- 期望回答：
- 追问：
- 评分点：

## 6. 计算机基础（40-52 min）

## 7. 算法题（52-60 min）
- 题目：
- 为什么选这题：
- 期望思路：
- 追问：
- 评分点：

## 8. 评价建议
- 强通过信号：
- 弱通过/待定信号：
- 拒绝信号：
```

## Question Selection Rules

Map resume signals to the bank:

- Kotlin/coroutines/Flow: use Kotlin inline/delegate, suspend, lifecycleScope/viewModelScope, Flow/SharedFlow/StateFlow.
- UI/custom View/rendering/list: use View drawing, Choreographer, event dispatch, RecyclerView cache, layout optimization, animation.
- framework/system/IPC/startup: use application startup, Binder, Handler/Looper, Service/Broadcast/Provider, startup initialization.
- performance/stability: use ANR, OOM, FPS, StrictMode, LeakCanary, crash handling, stability governance.
- architecture/refactor/platform: use MVC/MVP/MVVM/MVI, ArchUnit, decoupling, layering, APT, initialization dependency chains.
- dynamic delivery/hotfix/plugin: use ClassLoader, plugin Activity, resource loading, hotfix categories.
- network/security: use TCP/UDP, HTTP versions, HTTPS, encryption, cookie/session/token.
- data structure/algorithm: use HashMap, ConcurrentHashMap, LruCache, SparseArray, Top K, linked list, tree traversal.

Pick around:

- 4-6 project-specific deep questions.
- 3-5 Android mechanism questions.
- 2-3 computer fundamentals questions.
- 1 algorithm problem.

For each selected question, include why it matches the resume. If the resume is too thin, say so and use baseline questions.

## Interviewer Behavior

- Ask open-ended project questions first, then narrow to mechanisms.
- Verify ownership by asking for concrete decisions, alternatives, bugs, metrics, and tradeoffs.
- Prefer “你当时怎么判断/怎么验证/失败过什么” over pure definition questions for senior candidates.
- For vague claims such as “负责架构优化” or “性能提升明显”, ask for before/after metrics, tooling, bottleneck, rollout, and regression prevention.
- For algorithm questions, require the candidate to explain complexity and edge cases before code.

## Reference

- Full question bank: `references/android-interview-question-bank.md`
