# Repair Checklist

Use this when a user says the generated Seedance 2.0 output is wrong.

## Common Failures

- **Weak hook**: Rewrite the first 3 seconds with one visible event, surprise, or direct viewer address.
- **Motion is chaotic**: Reduce to one main action per shot; specify body parts, speed, force, and transition.
- **Identity drift**: Add face close-up reference; define `图片1` as face, `图片2` as full-body styling; put identity early.
- **Style drift**: Repeat the target style near the top and in constraints; convert references to target style before video generation when possible.
- **Unwanted subtitles**: Add “不要生成未指定字幕 / keep subtitles off”; remove text from reference assets if possible.
- **Watermark/logo**: Add explicit no watermark/no logo constraints and avoid web-sourced reference frames with watermarks.
- **Duplicate people/twins**: Define each person and reference image separately; add “同一画面中每个角色只出现一次，不生成同款分身或双胞胎”.
- **Audio ending noise**: Regenerate or add fade-out instruction; in post, fade final audio frames.
- **Chinese pronunciation issue**: Replace rare or polyphonic characters with common homophones if exact pronunciation matters.
- **Extension jump cut**: Use post-edit keyframe alignment; for multiple extensions, avoid repeatedly extending compressed generated video.

## Iteration Rule

Change one variable at a time:

1. Opening hook.
2. Camera movement.
3. Subject action.
4. Lighting/style.
5. Reference order or reference count.
6. Constraints.

Do not rewrite the entire prompt unless the concept itself is unclear.

