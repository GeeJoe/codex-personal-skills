# Android Studio And SDK Reference

Source: Dreamina Android developer wiki section "二、环境配置", cross-checked with the current repository.

## Version Facts

- Android Studio: Koala Feature Drop `2024.1.2 Patch 1`, installer package `2024.1.2.13`.
- Apple Silicon DMG: `https://edgedl.me.gvt1.com/edgedl/android/studio/install/2024.1.2.13/android-studio-2024.1.2.13-mac_arm.dmg`
- Intel DMG: `https://edgedl.me.gvt1.com/edgedl/android/studio/install/2024.1.2.13/android-studio-2024.1.2.13-mac.dmg`
- SDK platforms: Android API `35` and `33`.
- SDK Build-Tools: install `35.0.0` if no compatible build-tools exist.
- NDK: use repository source of truth, `gradle/infra.gradle`: `21.3.6528147`. The wiki text contains a likely typo around this version.
- CMake: `3.10.2` package id is normally `cmake;3.10.2.4988404`.
- Gradle JDK: JDK 11.
- Kotlin compiler settings in Android Studio: Kotlin compiler `2.0.20`, language/API `2.0`, K2 enabled. The repository Gradle scripts also configure Kotlin language/API version.

## Manual Android Studio Install Fallback

If automatic DMG install fails:

1. Open `https://developer.android.com/studio/archive` in English.
2. Download Android Studio `2024.1.2.13` for the user's CPU:
   - Apple Silicon: `android-studio-2024.1.2.13-mac_arm.dmg`
   - Intel: `android-studio-2024.1.2.13-mac.dmg`
3. Mount the DMG and drag `Android Studio.app` to `/Applications`.
4. Do not upgrade to a newer Android Studio unless the Dreamina Android team confirms support.

## Manual SDK Manager Fallback

In Android Studio, open `Settings > Languages & Frameworks > Android SDK`.

Install:

- `Android SDK Platform 35`
- `Android SDK Platform 33`
- `Android SDK Build-Tools`
- `Android SDK Platform-Tools`
- `Android Emulator`
- `Android SDK Command-line Tools`
- `NDK (Side by side)` version `21.3.6528147`
- `CMake` version `3.10.2`

If `sdkmanager` is available, equivalent packages are:

```text
platform-tools
emulator
platforms;android-35
platforms;android-33
build-tools;35.0.0
ndk;21.3.6528147
cmake;3.10.2.4988404
```

For the default AVD:

- Apple Silicon system image: `system-images;android-35;google_apis;arm64-v8a`
- Intel system image: `system-images;android-35;google_apis;x86_64`
- AVD name: `Dreamina_API_35`

## Project Initialization

After clone and SDK setup, run:

```bash
./local_dev/env/init_project.sh
```

This script creates or updates `local.properties`, configures Gradle JDK 11 in `.gradle/config.properties` and `.idea/gradle.xml`, and refreshes Android Studio run configurations from `.run/`.

The active product is selected by `local.properties`:

```properties
build.target=dreamina
```

Use `dreaminaoversea` only when explicitly requested.
