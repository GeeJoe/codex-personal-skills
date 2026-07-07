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

## Update Flow

After editing or adding skills:

```bash
python3 /Users/bytedance/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/personal-skills
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
- level-designer
- text-to-lottie

## Before Publishing

Review the imported skill content before pushing to a public repository. Several skills may contain company-specific workflow knowledge, so a private repository is the safer default.
