import os
import subprocess
import whisper

VO_DIR = r"e:\Promptwars2026\Hackathon_falkordb\User_VoiceOver"
PROC_DIR = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed"
os.makedirs(PROC_DIR, exist_ok=True)

print("="*60)
print("1. TRIMMING SILENCE & NORMALIZING LOUDNESS (-16 LUFS)")
print("="*60)

processed_files = []

for i in range(1, 7):
    src = os.path.join(VO_DIR, f"Part {i}.m4a")
    dst = os.path.join(PROC_DIR, f"part_{i}_norm.wav")
    
    # 1. First pass: trim leading/trailing silence + loudnorm
    # start_periods=1:start_duration=0.08:start_threshold=-38dB
    # areverse silenceremove areverse for trailing silence
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-af", (
            "silenceremove=start_periods=1:start_duration=0.08:start_threshold=-40dB,"
            "areverse,silenceremove=start_periods=1:start_duration=0.15:start_threshold=-40dB,areverse,"
            "loudnorm=I=-16:TP=-1.5:LRA=11"
        ),
        "-ar", "48000", "-ac", "2",
        dst
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Check duration & volume
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dst]
    dur = float(subprocess.check_output(dur_cmd).decode().strip())
    print(f"Part {i}: Processed -> {os.path.basename(dst)} (Duration: {dur:.2f}s)")
    processed_files.append((i, dst, dur))

print("\n" + "="*60)
print("2. EXTRACTING PRECISE CAPTION SEGMENTS WITH WHISPER")
print("="*60)

model = whisper.load_model("base")

all_captions = {}

for i, path, dur in processed_files:
    res = model.transcribe(path, language="en")
    print(f"\nPart {i} Transcribed ({dur:.2f}s):")
    segments = []
    for s in res.get("segments", []):
        t_start = round(s["start"], 2)
        t_end = round(s["end"], 2)
        txt = s["text"].strip()
        segments.append({
            "start": t_start,
            "end": t_end,
            "text": txt
        })
        print(f"  [{t_start:05.2f}s - {t_end:05.2f}s]: {txt}")
    all_captions[f"part_{i}"] = {
        "duration": dur,
        "segments": segments,
        "full_text": res["text"].strip()
    }

import json
with open(os.path.join(PROC_DIR, "captions.json"), "w", encoding="utf-8") as f:
    json.dump(all_captions, f, indent=2)

print("\nCaptions saved to:", os.path.join(PROC_DIR, "captions.json"))
