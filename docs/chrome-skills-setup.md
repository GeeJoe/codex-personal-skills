# Chrome Skills Setup

This plugin bundles the two skills recommended by the Chrome team's
[extension development guide](https://developer.chrome.com/docs/extensions/ai/build-with-ai#modern_web_guidance):

- `chrome-extensions`: Manifest V3 implementation, extension API references, and
  Chrome Web Store preparation through `CHROMEWEBSTORE.md`.
- `modern-web-guidance`: modern web patterns, browser compatibility, and guidance
  for CSS, accessibility, performance, security, and browser APIs.

## Source and license

Both directories are copied from [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance/tree/4f2b13e25c5815b3f080ca0d983e828d96561a0f/skills),
release `v0.0.196`, commit `4f2b13e25c5815b3f080ca0d983e828d96561a0f`.
The upstream skill files are unchanged. Each directory also includes a copy of
the upstream Apache 2.0 `LICENSE` so the license accompanies standalone copies.

## Install and use

Follow the repository README to register the marketplace. After pulling updates,
refresh the installed plugin:

```bash
codex plugin add personal-skills@codex-personal
```

The skills are available on the next turn; start a new chat if an existing chat
still shows the old skill catalog. Example requests:

- "Use chrome-extensions to build a Manifest V3 extension with a side panel."
- "Use modern-web-guidance to check the best pattern for a light-dismiss dialog."

Modern Web Guidance invokes its upstream CLI through `npx`. Install Node.js and
npm on each machine and allow network access when fetching the package or guides.
A basic CLI check is:

```bash
npx -y modern-web-guidance@latest search "light dismiss dialog"
npx -y modern-web-guidance@latest retrieve "light-dismiss-a-dialog"
```

Chrome DevTools MCP is a separate optional debugging integration. This skill import
does not configure it or change browser remote-debugging settings.

## Update the imported skills

The skill files in this repository are pinned snapshots. They do not automatically
update when the upstream CLI changes. To refresh them, import both skill directories
from a reviewed upstream commit, retain the license in each directory, and update
the source revision in this document and the repository README. Bump the personal
plugin version, validate the skills and their references, then reinstall the plugin.
