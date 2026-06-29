# Source Insights

## Data-Backed Viral Patterns

The initial analysis used Dreamina App content stats snapshot `20260524`, rolling 7-day metrics, top 2000 original video works by `like_cnt_7d`, filtered to online video-like works and original creation mode.

Key findings:

- Top 2000 like range: 195-12918; median 372.
- Within those top works, 1067 were created from `2026-05-18` to `2026-05-24`; their 7-day like median was 355. The recent-created subset showed the same pattern: 81% quality/style constraints, 61% timeline/storyboard, 57% dialogue/voice/subtitle, 54% dance/beat/transition, 44% handheld/one-take/live-action language.
- Prompt median length: about 593 Chinese characters.
- 80% contain explicit quality/style constraints such as 8K, cinematic, high definition, lighting, depth of field, no blur.
- 58% use timeline/storyboard structure.
- 53% include dialogue, subtitles, voiceover, or speaking tone.
- 56% involve beauty/fashion/atmosphere; 51% involve dance, beat sync, transition, or performance.
- 43% use first-person, handheld, real-shot, one-take, or documentary language.
- Strong reversal comedy is only 16% by count but over-indexes in likes.
- Cute anthropomorphic/cartoon characters are 14% by count but also over-index in likes.

Use these findings as priors, not hard rules. The highest-performing prompts are not just adjective piles; they are short-video scripts with hooks, character action, camera plans, sound, and constraints.

## Seedance 2.0 Principles

Public and internal docs converge on these principles:

- Seedance 2.0 supports text, image, audio, and video input, and can use references for composition, motion, camera movement, visual effects, and sound.
- It can output high-quality 15-second multi-shot audio-video clips.
- Treat it as a multimodal AI director: write what is in the frame and how it changes over time.
- Use structured, executable prompts: subject + action + scene + camera + style + audio + constraints.
- For complex videos, use shot order or timeline storyboards.
- Specify body parts, speed, force, and transitions for actions.
- Prefer slow, continuous, readable action unless the concept needs fast impact.
- Use standard camera terminology directly.
- Define reference materials by type and number: `图片1`, `视频1`, `音频1`.
- Place the most important identity/style reference early.
- Avoid complete raw scripts that include irrelevant exposition; keep instructions clear and focused.

## Viral Topic Playbook

- **Strong reversal comedy**: serious setup, fast embarrassment or unexpected logic, final punchline.
- **Blessing/fortune口播**: direct viewer address, warm voice, “正在看视频的你”, simple wish, shareable emotion.
- **Dance/transition/beauty**: one clear identity fantasy, beat-synced camera, clothing/hair movement, scene spectacle.
- **National style / wuxia / Dunhuang**: visual iconography, fabric/ribbon motion, dramatic lighting, music cue.
- **Cute character / anthropomorphic**: short dialogue, expressive faces, clear joke, soft material details.
- **Product/ad**: object stable, one camera move, one reveal, clean surface/light, no text artifacts unless deliberately specified.
