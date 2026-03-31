#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
NARRATION_JSON="$SCRIPT_DIR/narration.json"
TIMESTAMPS_JSON="$OUTPUT_DIR/demo-timestamps.json"

mkdir -p "$OUTPUT_DIR"

echo "========================================="
echo "  Smart Campaign Designer - Demo Builder"
echo "========================================="

# ─── Phase 1: Install Dependencies ───
echo ""
echo "[Phase 1] Checking dependencies..."

if ! command -v ffmpeg &>/dev/null; then
  echo "  Installing ffmpeg..."
  brew install ffmpeg
else
  echo "  ffmpeg: OK"
fi

if ! command -v aws &>/dev/null; then
  echo "  ERROR: AWS CLI not found. Install it first."
  exit 1
else
  echo "  aws cli: OK"
fi

echo "  Installing Playwright chromium..."
npx playwright install chromium

# ─── Phase 2: Playwright Screen Recording ───
echo ""
echo "[Phase 2] Recording browser demo..."
npx tsx "$SCRIPT_DIR/record-app.ts"

# Convert webm to mp4 if needed
if [ -f "$OUTPUT_DIR/demo-video.webm" ] && [ ! -f "$OUTPUT_DIR/demo-video.mp4" ]; then
  echo "  Converting webm to mp4..."
  ffmpeg -y -i "$OUTPUT_DIR/demo-video.webm" \
    -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
    "$OUTPUT_DIR/demo-video.mp4"
fi

# Verify timestamps file
if [ ! -f "$TIMESTAMPS_JSON" ]; then
  echo "  ERROR: demo-timestamps.json not found"
  exit 1
fi
echo "  Recording complete."

# ─── Phase 3: AWS Polly TTS ───
echo ""
echo "[Phase 3] Generating narration audio with AWS Polly..."

SCENE_IDS=$(python3 -c "
import json
with open('$NARRATION_JSON') as f:
    for s in json.load(f):
        print(s['id'])
")

for scene_id in $SCENE_IDS; do
  TEXT=$(python3 -c "
import json
with open('$NARRATION_JSON') as f:
    for s in json.load(f):
        if s['id'] == '$scene_id':
            print(s['englishText'])
            break
")
  OUT_FILE="$OUTPUT_DIR/narration-${scene_id}.mp3"
  echo "  Generating: $scene_id"
  aws polly synthesize-speech \
    --region us-east-1 \
    --output-format mp3 \
    --voice-id Joanna \
    --engine neural \
    --text "$TEXT" \
    "$OUT_FILE" > /dev/null
done
echo "  TTS generation complete."

# ─── Phase 4: Build Combined Audio Track ───
echo ""
echo "[Phase 4] Building combined audio track..."

python3 -c "
import json, subprocess, os

output_dir = '$OUTPUT_DIR'
with open('$TIMESTAMPS_JSON') as f:
    timestamps = json.load(f)

scenes = ['login', 'upload', 'chat_q1', 'chat_q2', 'chat_q3', 'drag', 'export']
input_args = []
filter_parts = []
mix_inputs = []

for idx, sid in enumerate(scenes):
    mp3 = os.path.join(output_dir, f'narration-{sid}.mp3')
    start_ms = int(timestamps[sid]['start'] * 1000)
    input_args.extend(['-i', mp3])
    filter_parts.append(f'[{idx}]adelay={start_ms}|{start_ms}[a{idx}]')
    mix_inputs.append(f'[a{idx}]')

filt = ';'.join(filter_parts) + ';' + ''.join(mix_inputs) + f'amix=inputs={len(scenes)}:duration=longest[out]'
cmd = ['ffmpeg', '-y'] + input_args + ['-filter_complex', filt, '-map', '[out]', os.path.join(output_dir, 'narration-combined.mp3')]
subprocess.run(cmd, check=True)
"

echo "  Combined audio track ready."

# ─── Phase 5: Generate SRT Subtitles ───
echo ""
echo "[Phase 5] Generating SRT subtitles..."

python3 -c "
import json

with open('$NARRATION_JSON') as f:
    scenes = json.load(f)
with open('$TIMESTAMPS_JSON') as f:
    timestamps = json.load(f)

def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

srt_lines = []
for idx, scene in enumerate(scenes, 1):
    sid = scene['id']
    ts = timestamps[sid]
    start = ts['start']
    end = ts['end']
    srt_lines.append(str(idx))
    srt_lines.append(f'{fmt_time(start)} --> {fmt_time(end)}')
    srt_lines.append(scene['englishText'])
    srt_lines.append('')

with open('$OUTPUT_DIR/subtitles.srt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(srt_lines))
print('  Subtitles written to subtitles.srt')
"

# ─── Phase 6: Final Merge ───
echo ""
echo "[Phase 6] Merging video + audio + subtitles..."

cd "$OUTPUT_DIR" && ffmpeg -y \
  -i demo-video.mp4 \
  -i narration-combined.mp3 \
  -vf "subtitles=subtitles.srt:force_style='FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=1,MarginV=20'" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  -shortest \
  demo-final.mp4 && cd -

echo ""
echo "========================================="
echo "  Done! Output: $OUTPUT_DIR/demo-final.mp4"
echo "========================================="
