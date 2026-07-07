---
name: dreamina-android-env-setup
description: Set up, diagnose, repair, or continue the Dreamina Android local run environment on company macOS machines. Use when a non-Android developer, product manager, designer, or newcomer needs to clone git@code.byted.org:faceu-android/Dreamina.git, request Codebase permissions, install or configure Android Studio, Android SDK, NDK, CMake, adb, emulator/AVD, local.properties, RemoteX, and run the Dreamina app on an Android emulator.
---

# Dreamina Android Env Setup

## Purpose

Use this skill to get Dreamina Android running from zero on a company Mac. The target user may not know Android development, so drive the process with checks, precise repair actions, and one next step when human authorization is required.

This skill is macOS-only. If the host is Windows or Linux, stop and explain that v1 only supports macOS.

## Default Contract

Default product target is domestic `dreamina`. Support `dreaminaoversea` only when the user explicitly asks or passes `--target dreaminaoversea`.

Use the repo path rules:

- If the user provides a path and it is the Dreamina repo, reuse it.
- If the user provides a path and it is not the Dreamina repo, stop; do not overwrite it.
- If no path is provided, use `~/DreaminaProjects/Dreamina`, creating `~/DreaminaProjects` when needed.
- New clones use `git@code.byted.org:faceu-android/Dreamina.git -b dreamina/develop`.
- Reused repos are never reset, deleted, overwritten, or force-switched. Report the current branch if it differs from `dreamina/develop`.

Default Codebase permission request level is `developer`, because non-RD users may need to submit code. Always show the target repo list and reason before requesting permission.

## Quick Start

Run checks first:

```bash
python3 <skill-dir>/scripts/dreamina_android_env.py doctor
```

Continue setup after user approval:

```bash
python3 <skill-dir>/scripts/dreamina_android_env.py goal-run --apply
```

Use a caller-provided repo path:

```bash
python3 <skill-dir>/scripts/dreamina_android_env.py goal-run --apply --repo-dir /path/to/Dreamina
```

Accept SDK licenses only after explicit user approval:

```bash
python3 <skill-dir>/scripts/dreamina_android_env.py goal-run --apply --accept-licenses
```

## Workflow

1. Run `doctor` to inspect without changing the machine.
2. Explain planned writes before `--apply`: `/Applications`, `~/Library/Android/sdk`, `~/.zshrc`, `~/.ssh`, `~/DreaminaProjects`, and the selected repo's local files.
3. Run `goal-run --apply` to continue from current state. If it blocks on SSO, SSH, Codebase approval, Android Studio GUI, SDK licenses, or RemoteX auth, give the user the exact action and rerun the same command afterward.
4. Finish only with `Ready`, `Partially ready`, or `Blocked`.

## Success Criteria

Ready means:

- Dreamina repo exists and has the expected origin.
- `local.properties` exists with `build.target=dreamina` or the requested target and `sdk.dir` pointing to a real SDK.
- Android Studio is installed; expected version is Koala Feature Drop `2024.1.2 Patch 1` / package `2024.1.2.13`.
- JDK 11 is available and project Gradle JDK config is initialized by `local_dev/env/init_project.sh`.
- SDK platform 35 and 33, platform-tools/adb, emulator, build-tools, NDK `21.3.6528147`, and CMake `3.10.2` are present.
- An AVD named `Dreamina_API_35` exists and boots.
- RemoteX build produces a debug APK.
- APK installs to the emulator and the app process starts.

## Required References

Read `references/android-studio.md` before installing or explaining Android Studio, SDK, NDK, CMake, JDK, adb, or emulator requirements.

Read `references/troubleshooting.md` when `doctor` or `goal-run` reports `Blocked`, `Partially ready`, or an external command failure.

## Safety Rules

- Do not store, print, upload, or copy SSH private keys, tokens, cookies, or app secrets.
- Generate SSH keys only after user approval. Display only the public key path and public key content when needed.
- Do not overwrite an existing Android Studio app with a mismatched version.
- Do not delete or recreate an existing AVD automatically.
- Do not accept SDK licenses unless the user explicitly approved it or passed `--accept-licenses`.
- Do not run destructive git commands.
- Do not switch branches in a reused repo without explicit user approval.

## Output Style

Use Chinese for user-facing guidance. Keep command names, paths, package names, activity names, versions, error keys, and UI labels in English.
