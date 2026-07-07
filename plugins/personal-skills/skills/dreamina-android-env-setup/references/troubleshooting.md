# Troubleshooting

## Codebase Or Git Access

Symptoms:

- `git clone` fails with permission denied.
- `Permission denied (publickey)`.
- `bytedcli --json auth status` says `need_login`.

Actions:

1. Run `bytedcli auth login`.
2. Verify SSH access to Codebase.
3. If no SSH key exists, generate one only after user approval and add the public key to Codebase.
4. Request `developer` permission for `faceu-android/Dreamina` and required dependency repositories.

Never print or upload private keys.

## Android Studio Version Mismatch

If `/Applications/Android Studio.app` exists but is newer or unknown, do not overwrite it. Tell the user the Dreamina wiki expects Koala Feature Drop `2024.1.2 Patch 1` / package `2024.1.2.13`, and ask whether they want to install that version side-by-side or manually replace the app.

## Missing sdkmanager

Install `Android SDK Command-line Tools` from Android Studio SDK Manager. The automation can install SDK packages only after `sdkmanager` exists.

## SDK Licenses

If Gradle or `sdkmanager` reports license errors, ask the user for explicit approval, then rerun with:

```bash
python3 <skill-dir>/scripts/dreamina_android_env.py goal-run --apply --accept-licenses
```

## JDK 11 Missing

Open Android Studio `Settings > Build, Execution, Deployment > Build Tools > Gradle`, then use `Gradle JDK > Download JDK` and choose version 11. Rerun `./local_dev/env/init_project.sh` afterward.

## Emulator Boot Problems

Check:

- `adb devices`
- `adb shell getprop sys.boot_completed`
- Android Studio Device Manager can launch `Dreamina_API_35`

On Apple Silicon, use `arm64-v8a` images. On Intel, use `x86_64` images.

## RemoteX Build Fails

Run from the repo root:

```bash
./remotex build
```

Common blockers are SSO/session, Codebase permissions, VPN/network, or stale RemoteX workspace cache. If the target changed between `dreamina` and `dreaminaoversea`, clean before rebuilding.

## APK Installed But App Does Not Start

Domestic launch:

```bash
adb shell am start -n com.bytedance.dreamina/com.bytedance.dreamina.main.MainActivity
```

Overseas launch:

```bash
adb shell am start -n com.lemon.dreamina/com.bytedance.dreamina.host.launch.MainActivity
```

Then check:

```bash
adb shell pidof com.bytedance.dreamina
adb shell pidof com.lemon.dreamina
```
