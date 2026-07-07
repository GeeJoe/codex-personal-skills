#!/usr/bin/env python3
"""Dreamina Android local environment setup helper.

The script is intentionally conservative:
- commands that modify the machine require --apply;
- SDK license acceptance requires --accept-licenses;
- existing user repos, Android Studio installs, and AVDs are not overwritten.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import plistlib
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_URL = "git@code.byted.org:faceu-android/Dreamina.git"
REPO_ID = "faceu-android/Dreamina"
DEFAULT_BRANCH = "dreamina/develop"
DEFAULT_PARENT = Path.home() / "DreaminaProjects"
DEFAULT_REPO_DIR = DEFAULT_PARENT / "Dreamina"

ANDROID_STUDIO_APP = Path("/Applications/Android Studio.app")
ANDROID_STUDIO_PACKAGE = "2024.1.2.13"
ANDROID_STUDIO_VERSION_HINTS = ("2024.1.2", "241.19072")
AS_DMG_ARM64 = "https://edgedl.me.gvt1.com/edgedl/android/studio/install/2024.1.2.13/android-studio-2024.1.2.13-mac_arm.dmg"
AS_DMG_X64 = "https://edgedl.me.gvt1.com/edgedl/android/studio/install/2024.1.2.13/android-studio-2024.1.2.13-mac.dmg"

DEFAULT_TARGET = "dreamina"
TARGETS = {
    "dreamina": {
        "package": "com.bytedance.dreamina",
        "activity": "com.bytedance.dreamina.main.MainActivity",
        "apk_globs": [
            "apps/dreamina/build/outputs/apk/prod/debug/*.apk",
            "apps/dreamina/build/outputs/apk/debug/*.apk",
        ],
    },
    "dreaminaoversea": {
        "package": "com.lemon.dreamina",
        "activity": "com.bytedance.dreamina.host.launch.MainActivity",
        "apk_globs": [
            "apps/dreamina/build/outputs/apk/oversea/debug/*.apk",
            "apps/dreamina/build/outputs/apk/debug/*.apk",
        ],
    },
}

SDK_PACKAGES = [
    "platform-tools",
    "emulator",
    "platforms;android-35",
    "platforms;android-33",
    "build-tools;35.0.0",
    "ndk;21.3.6528147",
    "cmake;3.10.2.4988404",
]
AVD_NAME = "Dreamina_API_35"


@dataclass
class Step:
    name: str
    status: str
    detail: str = ""
    next_action: str = ""


@dataclass
class Context:
    args: argparse.Namespace
    repo_dir: Path
    target: str
    steps: list[Step] = field(default_factory=list)

    @property
    def apply(self) -> bool:
        return bool(self.args.apply)

    def add(self, name: str, status: str, detail: str = "", next_action: str = "") -> None:
        self.steps.append(Step(name, status, detail, next_action))
        label = {"ok": "OK", "warn": "WARN", "blocked": "BLOCKED", "skip": "SKIP"}.get(status, status.upper())
        print(f"[{label}] {name}: {detail}")
        if next_action:
            print(f"       下一步: {next_action}")


def run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    capture: bool = True,
    check: bool = False,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        text=True,
        input=input_text,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=check,
    )


def run_login_shell(command: str, *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return run(["/bin/zsh", "-lic", command], cwd=cwd)


def quote(path: Path | str) -> str:
    return subprocess.list2cmdline([str(path)])


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_arm64() -> bool:
    return platform.machine().lower() in {"arm64", "aarch64"}


def cpu_label() -> str:
    return "Apple Silicon" if is_arm64() else "Intel"


def ensure_dir(path: Path, ctx: Context) -> bool:
    if path.is_dir():
        return True
    if not ctx.apply:
        return False
    path.mkdir(parents=True, exist_ok=True)
    return True


def repo_origin(repo_dir: Path) -> str | None:
    if not (repo_dir / ".git").exists():
        return None
    cp = run(["git", "remote", "get-url", "origin"], cwd=repo_dir)
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def is_dreamina_repo(repo_dir: Path) -> bool:
    origin = repo_origin(repo_dir)
    if not origin:
        return False
    return "faceu-android/Dreamina" in origin or "faceu-android/Dreamina.git" in origin


def current_branch(repo_dir: Path) -> str | None:
    cp = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir)
    if cp.returncode == 0:
        return cp.stdout.strip()
    return None


def clone_repo(ctx: Context) -> None:
    repo_dir = ctx.repo_dir
    explicit = bool(ctx.args.repo_dir)

    if repo_dir.exists():
        if is_dreamina_repo(repo_dir):
            branch = current_branch(repo_dir) or "unknown"
            detail = f"复用 {repo_dir}, branch={branch}"
            if branch != DEFAULT_BRANCH:
                ctx.add("repo", "warn", detail, f"推荐分支是 {DEFAULT_BRANCH}; 如需切换请先确认无本地改动")
            else:
                ctx.add("repo", "ok", detail)
            return
        status = "blocked" if explicit else "blocked"
        ctx.add("repo", status, f"{repo_dir} 已存在但不是 Dreamina 仓库", "请指定 --repo-dir 到正确仓库，或移动/改名该目录")
        return

    if explicit:
        ctx.add("repo", "blocked", f"用户指定路径不存在: {repo_dir}", "请创建该路径或改用默认路径")
        return

    if not ensure_dir(repo_dir.parent, ctx):
        ctx.add("repo", "blocked", f"默认父目录不存在: {repo_dir.parent}", "重新运行时添加 --apply 以创建并 clone")
        return

    if not ctx.apply:
        ctx.add("repo", "blocked", f"将 clone 到 {repo_dir}", "重新运行 goal-run --apply")
        return

    cp = run(["git", "clone", REPO_URL, "-b", DEFAULT_BRANCH, str(repo_dir)], capture=True)
    if cp.returncode == 0:
        ctx.add("repo", "ok", f"已 clone {REPO_URL} -> {repo_dir}")
        return

    detail = (cp.stderr or cp.stdout).strip()
    ctx.add(
        "repo",
        "blocked",
        "git clone 失败",
        "检查 bytedcli auth、Codebase 权限、SSH key 和 VPN；失败信息: " + detail[:500],
    )


def bytedcli_status(ctx: Context) -> None:
    cp = run_login_shell("bytedcli --json auth status")
    if cp.returncode != 0:
        ctx.add("bytedcli auth", "warn", "无法读取 bytedcli auth status", "确认 bytedcli 已安装并运行 bytedcli auth login")
        return
    try:
        data = json.loads(cp.stdout)
    except json.JSONDecodeError:
        ctx.add("bytedcli auth", "warn", "bytedcli auth status 非 JSON 输出", "运行 bytedcli auth login")
        return
    auth = data.get("data", {}).get("authenticated")
    if auth:
        ctx.add("bytedcli auth", "ok", "已登录")
    else:
        next_cmd = data.get("data", {}).get("bytecloud_auth", {}).get("nextCommand", "bytedcli auth login")
        ctx.add("bytedcli auth", "blocked", "未登录", next_cmd)


def check_codebase_permissions(ctx: Context) -> None:
    command = f"bytedcli --json codebase permission check -R {REPO_ID!r} --revision {DEFAULT_BRANCH!r}"
    cp = run_login_shell(command)
    if cp.returncode != 0:
        message = (cp.stderr or cp.stdout).strip()
        ctx.add("codebase permissions", "warn", "无法检查依赖仓库权限", f"登录后运行: {command}; 错误: {message[:400]}")
        return
    try:
        data = json.loads(cp.stdout)
    except json.JSONDecodeError:
        ctx.add("codebase permissions", "warn", "permission check 输出无法解析", f"手动运行: {command}")
        return

    repos = sorted(extract_repo_paths(data))
    repos = [repo for repo in repos if repo != REPO_ID]
    if not repos:
        ctx.add("codebase permissions", "ok", "未解析到缺失依赖仓库权限")
        return

    ctx.add("codebase permissions", "blocked", f"需要申请 {len(repos)} 个依赖仓库 developer 权限", ", ".join(repos[:10]))
    if ctx.apply:
        reason = ctx.args.permission_reason or "Setup Dreamina Android local environment and run/debug the app"
        apply_cmd = (
            f"bytedcli --json codebase permission apply -R {REPO_ID!r} "
            f"--action developer --reason {reason!r} --repos {','.join(repos)!r}"
        )
        apply_cp = run_login_shell(apply_cmd)
        if apply_cp.returncode == 0:
            ctx.add("codebase permission apply", "ok", "已提交 developer 权限申请")
        else:
            ctx.add("codebase permission apply", "blocked", "提交权限申请失败", (apply_cp.stderr or apply_cp.stdout).strip()[:500])


def extract_repo_paths(obj: object) -> set[str]:
    found: set[str] = set()
    pattern = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?$")

    def visit(value: object) -> None:
        if isinstance(value, str):
            if pattern.match(value) and " " not in value:
                found.add(value)
        elif isinstance(value, dict):
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(obj)
    return found


def read_local_properties(repo_dir: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    path = repo_dir / "local.properties"
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def write_local_property(repo_dir: Path, key: str, value: str) -> None:
    path = repo_dir / "local.properties"
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines() if path.exists() else []
    output: list[str] = []
    replaced = False
    for line in lines:
        if line.strip().startswith("#") or "=" not in line:
            output.append(line)
            continue
        current_key = line.split("=", 1)[0].strip()
        if current_key == key:
            output.append(f"{key}={value}")
            replaced = True
        else:
            output.append(line)
    if not replaced:
        output.append(f"{key}={value}")
    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def android_studio_info() -> dict[str, str] | None:
    info = ANDROID_STUDIO_APP / "Contents" / "Info.plist"
    if not info.exists():
        return None
    try:
        with info.open("rb") as file:
            plist = plistlib.load(file)
    except Exception:
        return {"path": str(ANDROID_STUDIO_APP)}
    return {key: str(value) for key, value in plist.items() if key.startswith("CFBundle") or key in {"JVMVersion"}}


def check_android_studio(ctx: Context) -> None:
    info = android_studio_info()
    if info:
        text = " ".join(info.values())
        if any(hint in text for hint in ANDROID_STUDIO_VERSION_HINTS):
            ctx.add("Android Studio", "ok", f"已安装，版本信息匹配 {ANDROID_STUDIO_PACKAGE}")
        else:
            ctx.add("Android Studio", "warn", "已安装，但版本无法确认或不匹配", "Dreamina wiki 期望 Koala 2024.1.2 Patch 1 / 2024.1.2.13；不要自动覆盖")
        return

    if not ctx.apply:
        ctx.add("Android Studio", "blocked", "未发现 /Applications/Android Studio.app", "重新运行 goal-run --apply 下载安装，或手动安装 2024.1.2.13")
        return
    install_android_studio(ctx)


def install_android_studio(ctx: Context) -> None:
    url = AS_DMG_ARM64 if is_arm64() else AS_DMG_X64
    cache_dir = Path.home() / ".codex" / "dreamina_android_env" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    dmg = cache_dir / Path(url).name
    if not dmg.exists():
        cp = run(["curl", "-L", url, "-o", str(dmg)], capture=False)
        if cp.returncode != 0:
            ctx.add("Android Studio install", "blocked", "下载 DMG 失败", url)
            return

    mount_root = cache_dir / "mnt"
    mount_root.mkdir(parents=True, exist_ok=True)
    attach = run(["hdiutil", "attach", str(dmg), "-mountpoint", str(mount_root), "-nobrowse"])
    if attach.returncode != 0:
        ctx.add("Android Studio install", "blocked", "挂载 DMG 失败", (attach.stderr or attach.stdout).strip()[:500])
        return
    try:
        app_candidates = list(mount_root.glob("*.app"))
        if not app_candidates:
            ctx.add("Android Studio install", "blocked", "DMG 中未找到 .app", "请手动安装 Android Studio")
            return
        if ANDROID_STUDIO_APP.exists():
            ctx.add("Android Studio install", "warn", "Android Studio 已存在，未覆盖", str(ANDROID_STUDIO_APP))
            return
        cp = run(["cp", "-R", str(app_candidates[0]), str(ANDROID_STUDIO_APP)], capture=True)
        if cp.returncode == 0:
            ctx.add("Android Studio install", "ok", f"已安装 {ANDROID_STUDIO_APP}")
        else:
            ctx.add("Android Studio install", "blocked", "复制到 /Applications 失败", (cp.stderr or cp.stdout).strip()[:500])
    finally:
        run(["hdiutil", "detach", str(mount_root)], capture=True)


def detect_sdk_dir(repo_dir: Path | None = None) -> Path | None:
    candidates: list[str] = []
    if repo_dir:
        props = read_local_properties(repo_dir)
        if props.get("sdk.dir"):
            candidates.append(props["sdk.dir"])
    for key in ("ANDROID_SDK_ROOT", "ANDROID_HOME"):
        if os.environ.get(key):
            candidates.append(os.environ[key])
    candidates.append(str(Path.home() / "Library" / "Android" / "sdk"))
    for item in candidates:
        path = Path(item).expanduser()
        if path.exists():
            return path
    return None


def find_sdk_tool(sdk_dir: Path | None, name: str) -> Path | None:
    if not sdk_dir:
        return None
    candidates = [
        sdk_dir / "cmdline-tools" / "latest" / "bin" / name,
        sdk_dir / "cmdline-tools" / "bin" / name,
        sdk_dir / "tools" / "bin" / name,
        sdk_dir / "platform-tools" / name,
        sdk_dir / "emulator" / name,
    ]
    for path in candidates:
        if path.exists() and os.access(path, os.X_OK):
            return path
    return None


def check_sdk(ctx: Context) -> Path | None:
    sdk_dir = detect_sdk_dir(ctx.repo_dir)
    if not sdk_dir:
        default_sdk = Path.home() / "Library" / "Android" / "sdk"
        if ctx.apply:
            default_sdk.mkdir(parents=True, exist_ok=True)
            sdk_dir = default_sdk
            ctx.add("Android SDK", "warn", f"创建默认 SDK 目录 {sdk_dir}", "仍需 Android Studio 或 Command-line Tools 提供 sdkmanager")
        else:
            ctx.add("Android SDK", "blocked", "未找到 SDK 目录", "安装 Android Studio 后打开 SDK Manager，或重新运行 goal-run --apply 创建默认目录")
            return None
    else:
        ctx.add("Android SDK", "ok", str(sdk_dir))

    sdkmanager = find_sdk_tool(sdk_dir, "sdkmanager")
    if not sdkmanager:
        ctx.add("sdkmanager", "blocked", "未找到 sdkmanager", "在 Android Studio SDK Manager 安装 Android SDK Command-line Tools")
        return sdk_dir

    installed = list_installed_sdk_packages(sdkmanager)
    if installed is None:
        ctx.add(
            "sdkmanager",
            "blocked",
            f"{sdkmanager} 无法正常列出 SDK 包",
            "在 Android Studio SDK Manager 安装新版 Android SDK Command-line Tools",
        )
        return sdk_dir
    missing = [pkg for pkg in SDK_PACKAGES if pkg not in installed]
    if not missing:
        ctx.add("SDK packages", "ok", "必需 SDK/NDK/CMake 组件已安装")
    elif not ctx.apply:
        ctx.add("SDK packages", "blocked", "缺少组件: " + ", ".join(missing), "重新运行 goal-run --apply 安装")
    else:
        if ctx.args.accept_licenses:
            run([str(sdkmanager), "--licenses"], input_text="y\n" * 80, capture=True)
        cp = run([str(sdkmanager), *missing], capture=False)
        if cp.returncode == 0:
            ctx.add("SDK packages", "ok", "已安装缺失组件: " + ", ".join(missing))
        else:
            ctx.add("SDK packages", "blocked", "sdkmanager 安装失败", "如为 licenses 问题，确认后添加 --accept-licenses")

    if ctx.apply and sdk_dir:
        sync_sdk_to_shell_and_local_properties(ctx, sdk_dir)
    return sdk_dir


def list_installed_sdk_packages(sdkmanager: Path) -> set[str] | None:
    cp = run([str(sdkmanager), "--list_installed"])
    installed: set[str] = set()
    if cp.returncode != 0:
        cp = run([str(sdkmanager), "--list"])
        if cp.returncode != 0:
            return None
    for line in cp.stdout.splitlines():
        value = line.split("|", 1)[0].strip()
        if value and not value.startswith("[") and value != "Path":
            installed.add(value)
    return installed


def sync_sdk_to_shell_and_local_properties(ctx: Context, sdk_dir: Path) -> None:
    if (ctx.repo_dir / ".git").exists():
        write_local_property(ctx.repo_dir, "sdk.dir", str(sdk_dir))
        write_local_property(ctx.repo_dir, "build.target", ctx.target)

    zshrc = Path.home() / ".zshrc"
    marker_start = "# >>> dreamina android env >>>"
    marker_end = "# <<< dreamina android env <<<"
    block = "\n".join(
        [
            marker_start,
            f"export ANDROID_HOME={sdk_dir}",
            f"export ANDROID_SDK_ROOT={sdk_dir}",
            'export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/tools/bin:$PATH"',
            marker_end,
        ]
    )
    text = zshrc.read_text(encoding="utf-8", errors="ignore") if zshrc.exists() else ""
    if marker_start in text and marker_end in text:
        text = re.sub(re.escape(marker_start) + r".*?" + re.escape(marker_end), block, text, flags=re.S)
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        text += block + "\n"
    zshrc.write_text(text, encoding="utf-8")
    ctx.add("shell PATH", "ok", f"已更新 {zshrc}")


def check_jdk11(ctx: Context) -> None:
    candidates = []
    if os.environ.get("JAVA_11_HOME"):
        candidates.append(Path(os.environ["JAVA_11_HOME"]))
    java_home = Path("/usr/libexec/java_home")
    if java_home.exists():
        cp = run([str(java_home), "-v", "11"])
        if cp.returncode == 0 and cp.stdout.strip():
            candidates.append(Path(cp.stdout.strip()))
    if os.environ.get("JAVA_HOME"):
        candidates.append(Path(os.environ["JAVA_HOME"]))
    for home in candidates:
        java = home / "bin" / "java"
        if java.exists():
            version = run([str(java), "-version"])
            output = (version.stderr or version.stdout)
            if 'version "11' in output or "version \"11" in output:
                ctx.add("JDK 11", "ok", str(home))
                return
    ctx.add("JDK 11", "blocked", "未找到 JDK 11", "在 Android Studio Gradle JDK 里 Download JDK 11，或设置 JAVA_11_HOME")


def run_project_init(ctx: Context) -> None:
    script = ctx.repo_dir / "local_dev" / "env" / "init_project.sh"
    if not script.exists():
        ctx.add("project init", "blocked", f"未找到 {script}", "确认 repo 路径正确")
        return
    if not ctx.apply:
        ctx.add("project init", "blocked", "尚未运行 init_project.sh", "重新运行 goal-run --apply")
        return
    cp = run(["bash", str(script)], cwd=ctx.repo_dir, capture=False)
    if cp.returncode == 0:
        ctx.add("project init", "ok", "已运行 local_dev/env/init_project.sh")
    else:
        ctx.add("project init", "blocked", "init_project.sh 失败", "检查 JDK 11 和 Android Studio 配置")


def check_avd(ctx: Context, sdk_dir: Path | None) -> None:
    if not sdk_dir:
        ctx.add("AVD", "blocked", "无法检查 AVD，因为 SDK 不存在")
        return
    avdmanager = find_sdk_tool(sdk_dir, "avdmanager")
    emulator = find_sdk_tool(sdk_dir, "emulator")
    if not avdmanager or not emulator:
        ctx.add("AVD", "blocked", "缺少 avdmanager 或 emulator", "安装 Android SDK Command-line Tools 和 Android Emulator")
        return

    avds = run([str(emulator), "-list-avds"])
    if AVD_NAME in avds.stdout.splitlines():
        ctx.add("AVD", "ok", AVD_NAME)
        return
    if not ctx.apply:
        ctx.add("AVD", "blocked", f"未找到 {AVD_NAME}", "重新运行 goal-run --apply 创建默认模拟器")
        return

    sdkmanager = find_sdk_tool(sdk_dir, "sdkmanager")
    if not sdkmanager:
        ctx.add("AVD", "blocked", "缺少 sdkmanager，无法安装 system image")
        return
    image = "system-images;android-35;google_apis;arm64-v8a" if is_arm64() else "system-images;android-35;google_apis;x86_64"
    cp = run([str(sdkmanager), image], capture=False)
    if cp.returncode != 0:
        ctx.add("AVD", "blocked", f"安装 system image 失败: {image}", "检查网络或手动通过 Device Manager 安装")
        return

    device = choose_avd_device(avdmanager)
    create_cmd = [str(avdmanager), "create", "avd", "-n", AVD_NAME, "-k", image]
    if device:
        create_cmd += ["-d", device]
    cp = run(create_cmd, input_text="no\n")
    if cp.returncode == 0:
        ctx.add("AVD", "ok", f"已创建 {AVD_NAME}")
    else:
        ctx.add("AVD", "blocked", "创建 AVD 失败", (cp.stderr or cp.stdout).strip()[:500])


def choose_avd_device(avdmanager: Path) -> str | None:
    cp = run([str(avdmanager), "list", "device"])
    text = cp.stdout
    for preferred in ("pixel_8", "pixel_7", "medium_phone"):
        if preferred in text:
            return preferred
    return None


def boot_emulator(ctx: Context, sdk_dir: Path | None) -> bool:
    if not sdk_dir:
        ctx.add("emulator boot", "blocked", "SDK 不存在")
        return False
    emulator = find_sdk_tool(sdk_dir, "emulator")
    adb = find_sdk_tool(sdk_dir, "adb")
    if not emulator or not adb:
        ctx.add("emulator boot", "blocked", "缺少 emulator 或 adb")
        return False

    devices = run([str(adb), "devices"])
    if "\tdevice" in devices.stdout and is_boot_completed(adb):
        ctx.add("emulator boot", "ok", "已有可用设备")
        return True

    if not ctx.apply:
        ctx.add("emulator boot", "blocked", "没有已启动模拟器", "重新运行 run --apply 或手动启动 Dreamina_API_35")
        return False

    subprocess.Popen(
        [str(emulator), "-avd", AVD_NAME, "-no-snapshot-load"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 180
    while time.time() < deadline:
        run([str(adb), "wait-for-device"], capture=True)
        if is_boot_completed(adb):
            ctx.add("emulator boot", "ok", AVD_NAME)
            return True
        time.sleep(5)
    ctx.add("emulator boot", "blocked", "模拟器 180 秒内未完成启动", "打开 Android Studio Device Manager 查看错误")
    return False


def is_boot_completed(adb: Path) -> bool:
    cp = run([str(adb), "shell", "getprop", "sys.boot_completed"])
    return cp.returncode == 0 and cp.stdout.strip() == "1"


def run_remotex_build(ctx: Context) -> Path | None:
    remotex = ctx.repo_dir / "remotex"
    if not remotex.exists():
        ctx.add("RemoteX build", "blocked", "未找到 ./remotex", "确认 repo 完整")
        return locate_apk(ctx)
    if not ctx.apply:
        apk = locate_apk(ctx)
        if apk:
            ctx.add("RemoteX build", "ok", f"找到已有 APK: {apk}")
            return apk
        ctx.add("RemoteX build", "blocked", "尚未构建 APK", "重新运行 run --apply 或 goal-run --apply")
        return None
    cp = run(["bash", str(remotex), "build"], cwd=ctx.repo_dir, capture=False)
    if cp.returncode != 0:
        ctx.add("RemoteX build", "blocked", "./remotex build 失败", "检查 SSO、权限、VPN、RemoteX 日志")
        return locate_apk(ctx)
    apk = locate_apk(ctx)
    if apk:
        ctx.add("RemoteX build", "ok", str(apk))
        return apk
    ctx.add("RemoteX build", "blocked", "构建结束但未定位到 APK", "检查 apps/dreamina/build/outputs/apk")
    return None


def locate_apk(ctx: Context) -> Path | None:
    candidates: list[Path] = []
    for pattern in TARGETS[ctx.target]["apk_globs"]:
        candidates.extend(Path(p) for p in glob.glob(str(ctx.repo_dir / pattern)))
    candidates = [path for path in candidates if path.exists()]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def install_and_launch(ctx: Context, sdk_dir: Path | None, apk: Path | None) -> None:
    if not apk:
        ctx.add("install app", "blocked", "没有 APK 可安装")
        return
    if not sdk_dir:
        ctx.add("install app", "blocked", "SDK 不存在")
        return
    adb = find_sdk_tool(sdk_dir, "adb")
    if not adb:
        ctx.add("install app", "blocked", "缺少 adb")
        return
    target = TARGETS[ctx.target]
    if not ctx.apply:
        ctx.add("install app", "blocked", f"将安装 {apk}", "重新运行 run --apply")
        return
    cp = run([str(adb), "install", "-r", str(apk)], capture=True)
    if cp.returncode != 0:
        ctx.add("install app", "blocked", "adb install 失败", (cp.stderr or cp.stdout).strip()[:500])
        return
    launch = f"{target['package']}/{target['activity']}"
    cp = run([str(adb), "shell", "am", "start", "-n", launch])
    if cp.returncode != 0:
        ctx.add("launch app", "blocked", "启动 App 失败", (cp.stderr or cp.stdout).strip()[:500])
        return
    time.sleep(2)
    pid = run([str(adb), "shell", "pidof", target["package"]])
    if pid.returncode == 0 and pid.stdout.strip():
        ctx.add("launch app", "ok", f"{target['package']} pid={pid.stdout.strip()}")
    else:
        ctx.add("launch app", "warn", "已发送启动命令，但未确认进程", f"手动检查: adb shell pidof {target['package']}")


def command_doctor(ctx: Context) -> None:
    if not is_macos():
        ctx.add("platform", "blocked", f"当前系统: {platform.system()}", "v1 仅支持 macOS")
        return
    ctx.add("platform", "ok", f"macOS / {cpu_label()}")
    clone_repo(ctx)
    bytedcli_status(ctx)
    check_codebase_permissions(ctx)
    check_android_studio(ctx)
    sdk_dir = check_sdk(ctx)
    check_jdk11(ctx)
    check_avd(ctx, sdk_dir)
    if ctx.repo_dir.exists() and is_dreamina_repo(ctx.repo_dir):
        props = read_local_properties(ctx.repo_dir)
        if props.get("build.target") == ctx.target:
            ctx.add("local.properties", "ok", f"build.target={ctx.target}")
        else:
            ctx.add("local.properties", "blocked", f"build.target={props.get('build.target')}", f"运行 project-init --apply --target {ctx.target}")


def command_setup(ctx: Context) -> None:
    if not is_macos():
        ctx.add("platform", "blocked", "v1 仅支持 macOS")
        return
    check_android_studio(ctx)
    sdk_dir = check_sdk(ctx)
    check_jdk11(ctx)
    check_avd(ctx, sdk_dir)


def command_project_init(ctx: Context) -> None:
    clone_repo(ctx)
    if ctx.repo_dir.exists() and is_dreamina_repo(ctx.repo_dir):
        run_project_init(ctx)


def command_run(ctx: Context) -> None:
    sdk_dir = check_sdk(ctx)
    if sdk_dir:
        check_avd(ctx, sdk_dir)
    if not boot_emulator(ctx, sdk_dir):
        return
    apk = run_remotex_build(ctx)
    install_and_launch(ctx, sdk_dir, apk)


def command_goal_run(ctx: Context) -> None:
    command_doctor(ctx)
    if any(step.status == "blocked" for step in ctx.steps) and not ctx.apply:
        return
    if ctx.repo_dir.exists() and is_dreamina_repo(ctx.repo_dir):
        run_project_init(ctx)
    sdk_dir = detect_sdk_dir(ctx.repo_dir)
    if sdk_dir:
        boot_emulator(ctx, sdk_dir)
        apk = run_remotex_build(ctx)
        install_and_launch(ctx, sdk_dir, apk)


def summarize(ctx: Context) -> int:
    blocked = [step for step in ctx.steps if step.status == "blocked"]
    warn = [step for step in ctx.steps if step.status == "warn"]
    print("\n== Summary ==")
    if blocked:
        print("Status: Blocked")
        print("Next actions:")
        for step in blocked[:8]:
            print(f"- {step.name}: {step.next_action or step.detail}")
        return 2
    if warn:
        print("Status: Partially ready")
        for step in warn[:8]:
            print(f"- {step.name}: {step.detail}")
        return 1
    print("Status: Ready")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up Dreamina Android local run environment")
    parser.add_argument("command", choices=["doctor", "goal-run", "setup", "clone", "project-init", "run"])
    parser.add_argument("--repo-dir", type=Path, default=None)
    parser.add_argument("--target", choices=sorted(TARGETS), default=DEFAULT_TARGET)
    parser.add_argument("--apply", action="store_true", help="allow machine changes")
    parser.add_argument("--accept-licenses", action="store_true", help="accept Android SDK licenses after explicit user approval")
    parser.add_argument("--permission-reason", default=None)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo_dir = (args.repo_dir.expanduser().resolve() if args.repo_dir else DEFAULT_REPO_DIR)
    ctx = Context(args=args, repo_dir=repo_dir, target=args.target)

    if args.accept_licenses and not args.apply:
        print("--accept-licenses requires --apply", file=sys.stderr)
        return 2

    if args.command == "doctor":
        command_doctor(ctx)
    elif args.command == "setup":
        command_setup(ctx)
    elif args.command == "clone":
        clone_repo(ctx)
        bytedcli_status(ctx)
        check_codebase_permissions(ctx)
    elif args.command == "project-init":
        command_project_init(ctx)
    elif args.command == "run":
        command_run(ctx)
    elif args.command == "goal-run":
        command_goal_run(ctx)
    return summarize(ctx)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
