import os
import whisper
import subprocess

vo_dir = r"e:\Promptwars2026\Hackathon_falkordb\User_VoiceOver"
print("Loading Whisper model...")
model = whisper.load_model("base")

for i in range(1, 7):
    f = f"Part {i}.m4a"
    path = os.path.join(vo_dir, f)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    # Get total duration
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    tot_dur = float(subprocess.check_output(cmd).decode().strip())
    
    res = model.transcribe(path, language="en")
    print(f"\n{'='*60}")
    print(f"FILE: {f} (Total duration: {tot_dur:.2f}s)")
    print(f"{'='*60}")
    print(f"TRANSCRIPTION:\n{res['text'].strip()}\n")
    
    segments = res.get("segments", [])
    if segments:
        first_seg = segments[0]
        last_seg = segments[-1]
        print(f"First speech detected: {first_seg['start']:.2f}s -> {first_seg['text'].strip()}")
        print(f"Last speech detected:  {last_seg['end']:.2f}s -> {last_seg['text'].strip()}")
        print(f"Leading silence: {first_seg['start']:.2f}s | Trailing silence: {tot_dur - last_seg['end']:.2f}s")
        print(f"Active speech duration: {last_seg['end'] - first_seg['start']:.2f}s")
        print("\nSegments breakdown:")
        for seg in segments:
            print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s]: {seg['text'].strip()}")
