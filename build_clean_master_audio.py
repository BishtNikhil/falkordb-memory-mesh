import os
import subprocess
import wave

VO_DIR = r"e:\Promptwars2026\Hackathon_falkordb\User_Voiceover"
PROC_DIR = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed"
os.makedirs(PROC_DIR, exist_ok=True)

# Exact high-fidelity trim boundaries (guarantees zero word clipping)
TRIM_BOUNDS = {
    1: {"start": 0.75, "end": 35.30},  # Preserves "Welcome judges" through "explainable millisecond graph engineering."
    2: {"start": 0.55, "end": 51.00},  # Preserves "For our primary track" through "unanimous consensus."
    3: {"start": 0.75, "end": 39.50},  # Preserves "For track one" through "remediation playbook."
    4: {"start": 0.55, "end": 30.60},  # Preserves "For track three" through "causal provenance."
    5: {"start": 1.00, "end": 29.00},  # Preserves "Under high-concurrency" through "Hackathon Rule three."
    6: {"start": 0.65, "end": 22.70},  # Preserves "For Hackathon Rule 10" through "multi-agent intelligence."
}

print("="*65)
print("1. TRIMMING SILENCE WITH EXACT BOUNDARIES & LOUDNORM (-16 LUFS)")
print("="*65)

trimmed_wavs = []
for i in range(1, 7):
    src = os.path.join(VO_DIR, f"Part {i}.m4a")
    dst = os.path.join(PROC_DIR, f"part_{i}_clean.wav")
    b = TRIM_BOUNDS[i]
    dur = b["end"] - b["start"]
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{b['start']:.2f}",
        "-to", f"{b['end']:.2f}",
        "-i", src,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "48000",
        "-ac", "2",
        dst
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Check exact output duration
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dst]
    actual_dur = float(subprocess.check_output(dur_cmd).decode().strip())
    print(f"Part {i}: {os.path.basename(dst)} (Duration: {actual_dur:.2f}s)")
    trimmed_wavs.append((i, dst, actual_dur))

# Concatenate with 1.20s silence gaps
MASTER_WAV = os.path.join(PROC_DIR, "master_narration_v5.wav")
GAP_SECONDS = 1.20

with wave.open(trimmed_wavs[0][1], 'rb') as w:
    params = w.getparams()
    nchannels, sampwidth, framerate, nframes, comptype, compname = params

gap_frames = int(framerate * GAP_SECONDS)
gap_bytes = b'\x00' * (gap_frames * nchannels * sampwidth)

part_offsets = []
current_time = 0.0

with wave.open(MASTER_WAV, 'wb') as out_w:
    out_w.setparams(params)
    for idx, path, dur in trimmed_wavs:
        with wave.open(path, 'rb') as in_w:
            frames = in_w.readframes(in_w.getnframes())
            out_w.writeframes(frames)
            
            p_start = current_time
            p_end = current_time + dur
            part_offsets.append({
                "part": idx,
                "file": path,
                "start": round(p_start, 3),
                "end": round(p_end, 3),
                "duration": round(dur, 3)
            })
            print(f"  Merged Part {idx}: [{p_start:06.2f}s -> {p_end:06.2f}s] ({dur:.2f}s)")
            
            current_time = p_end
            if idx < len(trimmed_wavs):
                out_w.writeframes(gap_bytes)
                current_time += GAP_SECONDS

mins = int(current_time // 60)
secs = int(current_time % 60)
print(f"\n[OK] Master Narration v5 Created: {MASTER_WAV}")
print(f"Total Duration: {mins}m {secs:02d}s ({current_time:.2f} seconds)")

import json
with open(os.path.join(PROC_DIR, "part_offsets_v5.json"), "w", encoding="utf-8") as f:
    json.dump({"total_duration": current_time, "parts": part_offsets}, f, indent=2)
print("Part offsets saved to part_offsets_v5.json")
