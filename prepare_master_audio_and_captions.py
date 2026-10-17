import os
import sys
import wave
import json
import numpy as np
import whisper

PROC_DIR = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed"
MASTER_WAV = os.path.join(PROC_DIR, "master_narration.wav")
GAP_SECONDS = 0.45

# 1. Seamless Audio Concatenation with Pure PCM
print("="*65)
print("1. BUILDING ZERO-OVERLAP MASTER NARRATION WAV (48kHz Stereo)")
print("="*65)

wav_inputs = [os.path.join(PROC_DIR, f"part_{i}_norm.wav") for i in range(1, 7)]

# Read first wave to get params
with wave.open(wav_inputs[0], 'rb') as w:
    params = w.getparams()
    nchannels, sampwidth, framerate, nframes, comptype, compname = params

gap_frames = int(framerate * GAP_SECONDS)
gap_bytes = b'\x00' * (gap_frames * nchannels * sampwidth)

part_ranges = []
current_time = 0.0

with wave.open(MASTER_WAV, 'wb') as out_w:
    out_w.setparams(params)
    for idx, path in enumerate(wav_inputs, 1):
        with wave.open(path, 'rb') as in_w:
            frames = in_w.readframes(in_w.getnframes())
            dur = in_w.getnframes() / framerate
            out_w.writeframes(frames)
            
            p_start = current_time
            p_end = current_time + dur
            part_ranges.append({
                "part": idx,
                "start": round(p_start, 2),
                "end": round(p_end, 2),
                "duration": round(dur, 2)
            })
            print(f"  Part {idx}: [{p_start:.2f}s -> {p_end:.2f}s] ({dur:.2f}s)")
            
            current_time = p_end
            if idx < len(wav_inputs):
                out_w.writeframes(gap_bytes)
                current_time += GAP_SECONDS

print(f"\n[OK] Master WAV created: {MASTER_WAV}")
print(f"Total Master Duration: {current_time:.2f}s (~{int(current_time // 60)}m {int(current_time % 60):02d}s)")

# 2. Extract Word-Level Timestamps with Whisper
print("\n" + "="*65)
print("2. EXTRACTING WORD-BY-WORD TIMESTAMPS WITH WHISPER")
print("="*65)

model = whisper.load_model("base")
result = model.transcribe(MASTER_WAV, language="en", word_timestamps=True)

# 3. Clean and Chunk into Fast-Paced Rhythmic Captions (3 to 6 words each)
# Replacements for domain vocabulary
REPLACEMENTS = {
    "falco db": "FalkorDB",
    "falco": "Falkor",
    "falkordb": "FalkorDB",
    "falkor": "FalkorDB",
    "cipher": "Cypher",
    "cipher merge": "Cypher MERGE",
    "apprajita": "Aparājita",
    "aparajita": "Aparājita",
    "varuna": "Varuna",
    "vishokarma": "Vishwakarma",
    "vishwakarma": "Vishwakarma",
    "sanjay": "Sanjaya",
    "sanjaya": "Sanjaya",
    "kalki": "Kalki",
    "naada": "Naada",
    "graph hectron": "Graph Hacks",
    "graph hack": "Graph Hacks",
    "cow": "CoW",
    "ast": "AST",
    "json": "JSON",
    "llm": "LLM",
    "mcp": "MCP",
    "dna": "DNA"
}

def clean_word(w):
    w_clean = w.strip()
    w_lower = w_clean.lower()
    for k, v in REPLACEMENTS.items():
        if w_lower == k:
            return v
    return w_clean

all_words = []
for segment in result.get("segments", []):
    for w_obj in segment.get("words", []):
        all_words.append({
            "word": clean_word(w_obj["word"]),
            "start": float(w_obj["start"]),
            "end": float(w_obj["end"])
        })

print(f"Total words transcribed: {len(all_words)}")

# Group words into 3-5 word chunks with max duration ~1.8s
chunks = []
curr_chunk = []
curr_start = None
curr_end = None

for w in all_words:
    if not curr_chunk:
        curr_chunk = [w["word"]]
        curr_start = w["start"]
        curr_end = w["end"]
    else:
        # Check condition to split
        # Split if: 4 words or duration > 1.6s or natural pause > 0.4s
        time_since_last = w["start"] - curr_end
        if len(curr_chunk) >= 5 or (curr_end - curr_start) >= 1.6 or time_since_last > 0.35:
            chunks.append({
                "start": round(curr_start, 2),
                "end": round(curr_end, 2),
                "text": " ".join(curr_chunk)
            })
            curr_chunk = [w["word"]]
            curr_start = w["start"]
            curr_end = w["end"]
        else:
            curr_chunk.append(w["word"])
            curr_end = w["end"]

if curr_chunk:
    chunks.append({
        "start": round(curr_start, 2),
        "end": round(curr_end, 2),
        "text": " ".join(curr_chunk)
    })

print(f"Generated {len(chunks)} dynamic, fast-paced caption chunks!")
for c in chunks[:12]:
    print(f"  [{c['start']:05.2f}s -> {c['end']:05.2f}s]: {c['text']}")

# Save
output_data = {
    "master_duration": round(current_time, 2),
    "part_ranges": part_ranges,
    "captions": chunks
}

with open(os.path.join(PROC_DIR, "master_captions_word_sync.json"), "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print(f"\n[OK] Saved synchronized word-level captions to master_captions_word_sync.json")
