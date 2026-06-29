---
name: seedance2-viral-video
description: "Create high-quality Seedance 2.0 and Seedance 2.0 Fast video prompts for viral short videos, Dreamina/即梦/豆包/方舟 video generation, multimodal reference-to-video, image/video/audio reference workflows, storyboard scripts, camera moves, audio/dialogue control, prompt repair, and 爆款短视频 prompt optimization."
---

# Seedance 2.0 Viral Video

Use this skill when the user asks for Seedance 2.0 prompts, 即梦/豆包/方舟视频生成提示词, 爆款短视频脚本, 文生视频, 图生视频, 多模态参考生视频, prompt 改写, or viral short-video ideation.

## Workflow

1. Classify the task:
   - **T2V**: text-only video prompt.
   - **I2V**: image-to-video; preserve source image identity/composition and describe motion.
   - **R2V / multimodal reference**: reference images, videos, and/or audio for subject, scene, camera, motion, style, or sound.
   - **Edit / extend**: modify or continue an existing video.
2. Identify the viral intent: strong reversal comedy, blessing/fortune口播, creator/UGC demo, dance/transition, beauty/fashion atmosphere, national-style/wuxia/Dunhuang, cute character, product ad, or cinematic B-roll.
3. Produce a prompt using this order:
   `output spec -> 3-second hook -> subject/reference definitions -> scene/emotion -> storyboard timeline -> action/expression details -> camera/movement -> audio/dialogue/subtitle plan -> style/quality -> constraints`.
4. If the user provides references, define them explicitly with numbered pointers: `图片1`, `视频1`, `音频1`. Do not refer to asset IDs unless the target product explicitly supports them.
5. Return:
   - the final copy-paste prompt;
   - a short rationale for the structure;
   - 2-3 iteration knobs such as camera move, opening hook, or audio tone.

## Prompt Rules

- Start with a concrete shot and visible action. Avoid opening with only style words.
- Make the first 3 seconds understandable without context.
- For complex clips, use `0-3s / 3-7s / 7-12s` or `镜头1/镜头2/镜头3`.
- Describe emotions through body details: gaze, mouth corners, hand motion, posture, breathing, pause, reaction.
- Use standard camera language: close-up, medium shot, wide shot, handheld, slow push-in, pan, tracking, POV, fixed camera, rack focus.
- Keep the main action count low. Seedance 2.0 can do complex motion, but high-quality viral clips usually need one clear action per shot.
- Add audio deliberately: BGM mood, ambient sound, foley, dialogue voice, dialect, and audio-visual timing.
- Add constraints at the end: no watermark, no logo, no unintended subtitles, stable face/identity, no duplicate people, no warped hands, no extra characters, keep reference identity consistent.
- For real-person likeness, IP characters, celebrity-like outputs, or branded assets, require authorization or transform the concept into an original character/style.

## Multimodal Reference

Use references as functional roles:

- Character anchor: 1-2 images, ideally face close-up plus full-body styling.
- Scene tone: 1 image for environment, lighting, palette, or art direction.
- Camera/motion reference: 1 video for movement, rhythm, action, special effect, or camera language.
- Audio atmosphere: 1 audio clip for music mood, voice tone, or sound design.

Recommended phrasing:

```text
<角色1> 的面部特征参考图片1，服装与体态参考图片2；场景氛围参考图片3；镜头节奏参考视频1；BGM 情绪参考音频1。
```

For editing tasks, say `严格编辑视频1，将...改为...，未提及部分保持不变`. For extension tasks, say `向后延长视频1，延续主体、场景、音频风格和叙事...`.

## References

- Read `references/source-insights.md` when you need the data-backed viral patterns and Seedance 2.0 prompt principles.
- Read `references/prompt-templates.md` when the user asks for finished prompts or prompt variants.
- Read `references/repair-checklist.md` when improving a failed prompt or diagnosing bad generations.

