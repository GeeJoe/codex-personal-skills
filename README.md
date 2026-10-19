# Codex Personal Skills

This repository packages personal Codex skills as a local Codex plugin.

## Contents

- `.agents/plugins/marketplace.json`: repo-local marketplace definition.
- `plugins/personal-skills/.codex-plugin/plugin.json`: plugin manifest.
- `plugins/personal-skills/skills/`: synced skill directories.
- `plugins/personal-skills/scripts/`: optional helper scripts for future skills.
- `plugins/personal-skills/assets/`: optional assets for future skills.

## Install On Another Machine

Clone this repository, then install the marketplace and plugin:

```bash
git clone <repo-url> ~/Code/codex-personal-skills
codex plugin marketplace add ~/Code/codex-personal-skills
codex plugin add personal-skills@codex-personal
```

Start a new Codex thread after installing so the plugin skills are loaded.

Skills do not bundle machine-level executables. For Hypit CLI, local rendering,
browser capture and video-download dependencies, see [Hypit setup](docs/hypit-setup.md).

## Update Flow

After editing or adding skills:

```bash
git diff --check
git add .
git commit -m "Update personal skills"
git push
```

On another machine:

```bash
git pull
codex plugin add personal-skills@codex-personal
```

Start a new Codex thread after reinstalling.

## Included Skills

The initial import copies non-system skills from `~/.codex/skills` only. It intentionally does not copy `~/.agents/skills`.

Current imported skills:

- android-interview-feedback
- android-interview-outline
- dreamina-android-env-setup
- game-designer
- generate2dmap
- generate2dsprite
- godogen
- godot-api
- grill-me
- handoff
- hypit
- last30days
- last30days-cn
- level-designer
- text-to-lottie
- yue2-music
- zhongjie

Additional upstream sources: [Hypit](https://github.com/hypit-ai/hypit/tree/main/skills/hypit),
[last30days-cn](https://github.com/Jesseovo/last30days-skill-cn/tree/main/skills/last30days),
[YuE2 Music](https://github.com/multimodal-art-projection/YuE/tree/1647252d68b70cbead046ffd3f7caf036dde47ee/skills/yue2-music),
and [zhongjie](https://github.com/MorvanZhou/zhongjie/tree/main/skills/zhongjie).
Their upstream terms apply; Hypit and YuE2 Music retain their bundled licenses.

YuE2 Music is imported from upstream commit `1647252d68b70cbead046ffd3f7caf036dde47ee`,
including its instrumental workflow. Model weights and inference environments are
installed separately; see [YuE2 setup](plugins/personal-skills/skills/yue2-music/references/models-and-setup.md).

## Before Publishing

Review the imported skill content before pushing to a public repository. Several skills may contain company-specific workflow knowledge, so a private repository is the safer default.
