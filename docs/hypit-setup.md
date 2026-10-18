# Hypit local setup

The plugin supplies the Hypit skill, not the CLI, browser binaries, Python
environments or model credentials. Install those on each machine separately.
Upstream: <https://github.com/hypit-ai/hypit>.

## Install the CLI and host tools

Hypit 0.3.1 requires Node.js >= 22.15.0. With a compatible Node selected:

```bash
npm install --global @hypit/hypit@0.3.1
brew install ffmpeg uv
hypit version
ffmpeg -version
ffprobe -version
uv --version
```

Reuse compatible existing host tools. If Volta manages your commands, use
`volta install @hypit/hypit@0.3.1` with a compatible default Node instead of the
npm command. This pins the CLI's Node without changing another project's Node
selection. Resolve commands through your login shell if an agent's PATH differs
from your terminal.

## Prepare credential-free local rendering

Copy the following complete Profile to `hypit.runtime.json` in a video project
(or keep it outside the project and pass its path with `--runtime`):

```json
{
  "format": "hypit.runtime-local@1",
  "dataRoot": ".hypit/execution",
  "credentials": {},
  "endpoints": {
    "media.local": { "use": "@hypit/media-local" },
    "html.local": {
      "use": "@hypit/provider-html-local",
      "config": { "maxWorkers": 2, "browserCapacity": 2 }
    }
  },
  "bindings": {}
}
```

Both FFmpeg and FFprobe must be on the invoking process's PATH. Alternatively,
set `ffmpegPath` and `ffprobePath` in **both** endpoints' `config` using that
machine's actual paths. Do not replace an existing production Profile blindly.

```bash
hypit programs prepare --runtime ./hypit.runtime.json --project . --endpoint media.local --endpoint html.local
hypit doctor --runtime ./hypit.runtime.json --project . --endpoint media.local --endpoint html.local
hypit capture install-browser
hypit download prepare
```

Rendering and website capture have separate release-selected browsers. Keep the
defaults unless deliberately selecting another supported browser; installing
Playwright or a system Chrome alone does not prepare these defaults. The download
command prepares the packaged, locked yt-dlp Python environment through uv.

Select an existing Profile for a video project and inspect its locations:

```bash
hypit runtime use /absolute/path/to/hypit.runtime.json --project /absolute/path/to/video-project
hypit paths --project /absolute/path/to/video-project
```

## Local installation verified on 2026-10-18

- CLI: Hypit 0.3.1, managed by Volta with Node 22.21.1.
- Host tools: FFmpeg/FFprobe 8.1.1 and uv 0.11.7 (existing installations reused).
- HTML renderer: managed Chrome Headless Shell 152.0.7928.2.
- Website capture: managed Chrome for Testing 153.0.8010.12.
- Video downloads: managed yt-dlp 2026.8.19 with its locked Python dependencies.
- Shared local-only Profile: `~/.config/hypit/local.runtime.json`; it uses explicit
  local FFmpeg/FFprobe paths and needs no credentials.
- Validation: `hypit doctor` passed for both local endpoints. A direct local
  renderer smoke test produced a 1-second, 320×180 H.264 MP4 with 24 frames;
  FFprobe confirmed the output and FFmpeg decoded it without errors. This tests
  the browser/renderer/encoder pipeline, not a full authored video Build.

These versions record this machine's verification, not requirements to copy all
browser versions into future Profiles. The provider release selects its browser.
Machine caches, credentials, environments and rendered test outputs are not
committed to this repository.

Hosted generation still requires the user's chosen provider/account and credits.
Local WhisperX is optional: select a model, device and alignment languages before
preparing it; this setup does not download unspecified large model weights or
claim to validate hosted generation or transcription.
