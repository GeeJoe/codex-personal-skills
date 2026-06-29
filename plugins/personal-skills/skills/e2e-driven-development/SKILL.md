---
name: e2e-driven-development
description: "Use when a change should be driven by end-to-end acceptance cases: align E2E criteria before development, run unit tests when practical, execute real E2E validation, and produce an evidence-backed report."
---

# E2E Driven Development

Drive implementation through user-aligned E2E acceptance cases and finish with real execution evidence. Success means the change is developed, locally verified with the fastest relevant tests, validated through an actual end-to-end flow, and documented in a report that proves what ran.

Announce at start: "I'm using the `e2e-driven-development` skill to drive this change through E2E acceptance and evidence-backed validation."

## Core Rules

- Align E2E acceptance cases before implementation. Do not start development until the cases have been presented and the user explicitly confirms they are aligned.
- After E2E acceptance cases are aligned and before implementation, set the delivery Goal when the environment provides a goal mechanism. The Goal defines completion for the whole delivery, while the task plan or checklist tracks the individual steps.
- If the requirement is unclear, use the `idea-to-design` skill first, then return to this skill after requirements and examples are aligned.
- Prefer existing project test standards over inventing a new harness. For Python, TypeScript, backend, CLI, or library work, run practical unit tests before E2E because they are faster and easier to diagnose.
- Skip unit tests only when the project has no practical unit-test path for the change, such as many device-only Android or iOS flows. Record the reason in the report.
- E2E must be real execution. Static code review, mocked-only checks, screenshots without interaction, or unit tests alone do not count as E2E validation.
- The final report must include enough evidence for another engineer to see what ran, where it ran, what passed or failed, and which artifacts prove it.
- Write user-facing generated artifacts such as `e2e/cases.md`, `e2e/report.md`, and review summaries in Chinese by default, unless the user or project explicitly requires another language. Keep commands, paths, code identifiers, logs, and exact evidence filenames unchanged.

## Output Directory

Keep this skill's files in the same task directory as the matching `idea-to-design` design note.

Default shape:

```text
docs/idea-to-deliverable/YYYY-MM-DD-<topic>/
|-- design.md
`-- e2e/
    |-- cases.md
    |-- report.md
    `-- evidence/
```

Rules:

- If `design.md` already exists for the task, reuse its parent directory.
- If no task directory exists, create `docs/idea-to-deliverable/YYYY-MM-DD-<topic>/` unless the user or project has a stronger convention.
- Use `e2e/cases.md` for the pre-development acceptance cases.
- Use `e2e/report.md` for the final E2E execution report.
- Use `e2e/evidence/` as the evidence root. Organize files inside it however the task needs, such as by timestamp, platform, case id, screenshots, logs, traces, UI dumps, recordings, or raw command output.
- Large artifacts do not have to be copied into `e2e/evidence/`, but `report.md` must include an absolute path or accessible artifact link.
- Do not commit generated notes or evidence unless the user explicitly asks.

## Workflow

Use this checklist when a task tool is available. Track only the active path, and mark conditional work clearly.

```text
Task Progress:
- [ ] Step 1. Establish the task directory — reuse the matching `idea-to-design` task directory when available
- [ ] Step 2. Write and align E2E cases — define accepted executable case IDs, expected behavior, required evidence, and get user confirmation before implementation
- [ ] Delivery Goal Gate — after Step 2 and before Step 3, set the delivery Goal from the accepted Spec and E2E cases, or use task tracking when a goal mechanism is unavailable
- [ ] Step 3. Implement the change — keep edits scoped to the accepted behavior and follow existing project patterns
- [ ] Step 4. Run fast verification, or record why it is skipped — run practical unit tests, type checks, linters, or narrow integration tests when meaningful
- [ ] Step 5. Execute real E2E — run the accepted user flow or system workflow and capture evidence
- [ ] Step 6. Write the E2E report — map every accepted executable case ID to status, result, evidence, or blocker
- [ ] Step 7. Summarize the result for the user — report the outcome, case coverage, evidence paths, and remaining risk or next action
```

### Step 1. Establish The Task Directory

Inspect the current project context and identify the task directory. If an `idea-to-design` design note exists, use the same directory. If multiple candidate directories exist, choose the one clearly tied to the current task or ask one focused question.

### Step 2. Write And Align E2E Cases

Write `e2e/cases.md` before implementation. Keep it concise but concrete enough to be testable.

Include:

- Scope and non-goals.
- Environment or platform assumptions.
- Happy-path cases.
- Edge, error, or counterexample cases.
- For each executable case: stable case ID, setup, user-visible behavior or actions, expected result, required evidence, and pass criteria.

#### Case Design Principles

`e2e/cases.md` is an acceptance map, not a rigid template. Choose the structure that makes the real behavior easiest to review and execute.

- Give every executable leaf case a stable case ID, such as `E2E-001`, `UI-E2E-001`, or a domain-specific prefix when that improves traceability.
- Use case IDs consistently across `e2e/cases.md`, evidence directories or filenames, and `e2e/report.md`.
- After cases are aligned, do not renumber existing case IDs. Add new IDs for new cases so older evidence and reports remain traceable.
- Keep a compact case index near the top when there is more than one case. The index should let the report map each case ID to scenario, type, summary, and required evidence.
- Use the body structure that fits the task: flat tables for simple independent cases, scenario trees for branching user flows, validation matrices for product/build variants, and nested sections when shared setup or branches would otherwise be repeated.
- Parent scenarios, trees, and matrices are organization aids. The coverage unit is the executable leaf case ID.
- Tie behavior, expected result, and evidence together. A case is weak if it names an action but not what proves the expected result.

After writing or summarizing the cases, ask the user to confirm they are aligned. If the user changes the requirement, update the cases before implementation.

### Delivery Goal Gate

Run this gate only after the user confirms `e2e/cases.md` or an equivalent accepted E2E case summary. Do not set a delivery Goal before the acceptance cases are aligned, because the Goal should describe the confirmed delivery boundary rather than a still-moving requirement.

<HARD-GATE>
Do NOT start Step 3, write implementation code, create scripts, or invoke code-writing tools until the accepted E2E cases are aligned and this gate is complete: either set a delivery Goal from the accepted Spec and E2E cases, or record why a goal mechanism is unavailable and use task-plan or checklist tracking for the same delivery boundary.
</HARD-GATE>

If the environment provides a goal mechanism, set the delivery Goal before Step 3. The Goal covers Step 3 through Step 7: implementation, fast verification, real E2E execution, report writing, and final user summary. Use the task plan or checklist to track those steps; use the Goal to define what counts as complete.

Use this template and fill every placeholder that is available:

```text
Complete end-to-end delivery for <task-name> according to the accepted Spec and E2E acceptance cases.

Context:
- Spec/design source: <design.md path, or concise aligned requirement summary>
- E2E cases: <e2e/cases.md path, or accepted case summary>
- Accepted executable case IDs: <case IDs>

Done when:
- Implementation is complete and scoped to the accepted behavior.
- Fast verification has run when practical, or the skip reason is recorded in `e2e/report.md`.
- Each accepted executable E2E case has been executed in the real workflow, or a concrete blocker is recorded.
- `e2e/report.md` maps every accepted case ID to status, result, evidence path, or blocker.
- The final user summary reports the overall result, case coverage, report path, key evidence, and remaining risk or next action.
```

If a goal mechanism is unavailable, not permitted, or already occupied by a different active objective, use the task plan or checklist to track the same delivery boundary. Keep `e2e/cases.md`, `e2e/report.md`, and evidence files current enough that the work can resume after context compression.

### Step 3. Implement The Change

Implement only after the E2E acceptance cases are aligned. Keep edits scoped to the accepted behavior and follow existing project patterns.

Follow any plan the user already aligned before implementation, including requirements, design decisions, accepted E2E cases, constraints, or saved design notes from earlier workflow stages. Do not quietly change the agreed direction during implementation.

### Step 4. Run Fast Verification First

Run the relevant unit tests, type checks, linters, or narrow integration tests when the project has a practical path. Prefer the smallest command that covers the changed behavior.

If tests are unavailable, too expensive, or not meaningful for the project type, record the reason and move to E2E.

### Step 5. Execute Real E2E

Run the actual user flow or system workflow described in `e2e/cases.md`.

Examples of real E2E validation:

- Web: open the app in a browser and interact with the UI.
- Android or iOS: build, install or launch the app, and operate the target flow on a real device, simulator, or emulator.
- CLI, backend, scripts, or agents: run the real command or multi-step workflow with realistic inputs and observe the real output or side effects.

Capture evidence while executing. Useful evidence includes screenshots, logs, traces, UI trees, recordings, command output, generated files, device identifiers, build/install output, request/response samples, or artifact links.

If cases run in parallel, report each case independently. Do not merge results into a single pass/fail claim without per-case evidence.

### Step 6. Write The E2E Report

Write `e2e/report.md` after execution.

Include:

- Summary: pass, fail, partial, or blocked.
- Change under test and commit/worktree context when relevant.
- Unit or fast-test commands and results, or the reason they were skipped.
- E2E environment: platform, device/browser/runtime, build, URL, app id, command, or other meaningful context.
- Case-by-case results mapped back to `e2e/cases.md`.
- Coverage matrix: every accepted case ID, status, result summary, and evidence path or blocker.
- Evidence paths or links for every important claim.
- Failures, blockers, observed-vs-expected differences, and recommended next action.
- Only when applicable: significant deviations from the accepted Spec, implementation approach, accepted cases, pass criteria, or evidence requirements caused by bug or blocker fixes, including the reason and impact.

#### Success Criteria

Mark the overall E2E result as `pass` only when:

- Every accepted executable case ID is covered in the report.
- Every accepted executable case ID has a passing result.
- Every passing claim is backed by sufficient, trustworthy evidence.
- Evidence is mapped to the exact case ID and execution environment.

Never write a passing report for a failed or unexecuted case. If any accepted case is missing, unexecuted, blocked, failed, or supported only by weak evidence, mark the summary as `partial`, `blocked`, or `fail` as appropriate. If execution was blocked, say exactly where and preserve the evidence collected before the block.

### Step 7. Summary

After `e2e/report.md` is written, summarize the result for the user in Chinese by default.

Keep the summary concise and evidence-backed. Include:

- Overall result: pass, fail, partial, or blocked.
- Case coverage: whether every accepted executable case ID was covered.
- Evidence: the report path and the most important evidence paths or artifact links.
- Fast verification: commands that ran, or the documented skip reason.
- Remaining risk, blocker, or recommended next action when relevant.

## Failure Handling During Delivery

Apply this cross-step policy when Step 3 through Step 5 exposes bugs, blockers, repeated failures, or surprising behavior.

**Thinking Mode**

- `Avoid overfitting` - Do not optimize for the latest failing symptom only. Check whether the same rule, boundary, state transition, data contract, environment assumption, or test setup affects multiple cases.
- `Review from a higher level` - Step back from the failing line, action, or assertion. Reason from the system structure, data flow, state model, integration boundary, environment, accepted assumptions, and evidence path before choosing a fix.

**Analysis Flow**

1. State the observed failure, blocker, or surprising behavior and the evidence that proves it.
2. Group related failures, cases, logs, requests, states, or screenshots instead of treating each one as unrelated.
3. Identify the most likely root cause, or clearly mark it as a hypothesis when it is not proven.
4. Decide whether the fix is a local correction, a broader implementation approach adjustment, or a change to the accepted cases or pass criteria.
5. Use the `systematic-debugging` skill when the root cause is unclear, failures repeat, evidence conflicts, or fixes start to oscillate.

**Action Rules**

- Avoid patch ping-pong where fixing A breaks B and fixing B breaks A again.
- If the fix stays within accepted scope, E2E cases, pass criteria, and evidence requirements, continue and verify the affected cases.
- If the fix significantly changes the original Spec, implementation approach, accepted cases, pass criteria, or evidence requirements, treat it as a significant adjustment and record the reason and impact in `e2e/report.md`.
- Ordinary reports do not need root-cause writeups for every issue.

## Execution Skill Routing

Use project-specific skills when they fit the actual E2E surface. Choose the route by the system under test and the evidence needed, not only by repository type.

**Web**

- Use the `browser:browser` skill for local web, localhost, file URL, and in-app browser validation.
- Use the `chrome:Chrome` skill when validation depends on the user's Chrome profile, cookies, extensions, or logged-in session.

**Android**

- Use the `android-test-device-manager` skill before Android emulator validation that needs a managed device lease.
- Use the `test-android-apps:android-emulator-qa` skill for Android emulator QA.
- Use the `rax-cli` skill when Android validation can be accelerated through a RAX-connected device: device selection, app launch or schema entry, screenshots, UI describe/tap/swipe/input, network capture/search/mock/weak network, AB mock, MMKV, SharedPreferences, Settings, router logs, event logs, bridge logs, or other execution evidence.

Use RAX as an acceleration and evidence layer when it fits the accepted case. Continue to use emulator QA, adb-driven checks, platform automation, or project-specific test commands when the case requires build/install control, deeper UI automation, raw logcat, performance traces, or behavior RAX cannot prove.

**General**

- Use the `systematic-debugging` skill when tests fail, E2E behavior is unexpected, or the root cause is unclear.

Do not try to enumerate every language or platform. Choose the execution path that proves the accepted case in the real system the user cares about.

## Completion Checklist

Before ending:

- `e2e/cases.md` exists and matches the final accepted scope.
- Every executable case in `e2e/cases.md` has a stable case ID.
- The delivery Goal was set after E2E case alignment, or task tracking records that a goal mechanism was unavailable or not permitted.
- Implementation is complete or the report clearly states what remains blocked.
- Unit or fast verification ran when practical, or the skip reason is documented.
- Real E2E execution ran for every claimed passing case.
- `e2e/report.md` maps every accepted executable case ID to status, result, and evidence or blocker.
- The final user summary reports the E2E result, case coverage, evidence/report paths, and remaining risk or next action when relevant.
- Evidence paths or artifact links are valid and specific.
