import os
import json
import whisper

PROC_DIR = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed"
OFFSETS_JSON = os.path.join(PROC_DIR, "part_offsets_v5.json")

with open(OFFSETS_JSON, "r", encoding="utf-8") as f:
    meta = json.load(f)
    part_offsets = meta["parts"]

print("="*65)
print("EXTRACTING PRECISE WORD-LEVEL CAPTIONS FOR MASTER V5")
print("="*65)

model = whisper.load_model("base")

CORRECTIONS = {
    "falco": "FalkorDB",
    "falko": "FalkorDB",
    "falco db": "FalkorDB",
    "falko db": "FalkorDB",
    "falkordb": "FalkorDB",
    "cipher": "Cypher",
    "merch": "MERGE",
    "merge": "MERGE",
    "apprajita": "Aparājita",
    "aparajita": "Aparājita",
    "shadow_apprajita": "shadow_aparajita",
    "varuna": "Varuna",
    "vishokarma": "Vishwakarma",
    "vishwakarma": "Vishwakarma",
    "sanjay": "Sanjaya",
    "sanjaya": "Sanjaya",
    "kalki": "Kalki",
    "naada": "Naada",
    "graph hectron": "Graph Hacks",
    "graph hacks 2026": "Graph Hacks 2026",
    "cow": "CoW",
    "ast": "AST",
    "json": "JSON",
    "llm": "LLM",
    "mcp": "MCP",
    "dna": "DNA",
    "end-agestion": "ingestion",
    "agestion": "ingestion",
    "injestion": "ingestion",
    "gas work": "guesswork",
    "casual": "causal",
    "tool bloat": "rule bloat",
    "close agent": "cross-agent",
    "world": "Vault",
    "airgap": "air-gapped",
    "right shadow": "Write shadow",
    "c procedure": "C procedure",
    "algo .page": "algo.pageRank",
    "algo .page rank": "algo.pageRank",
    "algo.pagerank": "algo.pageRank",
    "pack": "PACC",
    "pacc": "PACC",
    "argon": "Argon",
    "gemini": "Gemini",
    "ps5": "PS5",
    "gta 6": "GTA VI",
    "gta vi": "GTA VI"
}

def clean_word(txt):
    cleaned = txt.strip()
    low = cleaned.lower()
    for k, v in CORRECTIONS.items():
        if low == k:
            return v
    return cleaned

all_phrases = []

for p in part_offsets:
    p_num = p["part"]
    p_file = p["file"]
    p_start = p["start"]
    p_end = p["end"]
    print(f"\nTranscribing Part {p_num} (Offset: +{p_start:.2f}s)...")
    
    res = model.transcribe(p_file, word_timestamps=True)
    words = []
    for s in res["segments"]:
        for w in s.get("words", []):
            words.append({
                "word": clean_word(w["word"]),
                "start": round(p_start + w["start"], 3),
                "end": round(p_start + w["end"], 3)
            })
    
    # Group words into 3-5 word rhythmic chunks
    i = 0
    while i < len(words):
        chunk_words = []
        c_start = words[i]["start"]
        
        while i < len(words) and len(chunk_words) < 5:
            w = words[i]
            chunk_words.append(w["word"])
            c_end = w["end"]
            i += 1
            # Break on punctuation
            if w["word"].endswith(('.', ',', '?', '!', ';', ':')) and len(chunk_words) >= 3:
                break
        
        chunk_text = " ".join(chunk_words).strip()
        all_phrases.append({
            "part": p_num,
            "start": c_start,
            "end": c_end,
            "text": chunk_text
        })

# Smoothing pass: set end time to next start time (up to +0.6s) to eliminate flickering,
# but respect part boundaries!
for idx in range(len(all_phrases)):
    cur = all_phrases[idx]
    if idx + 1 < len(all_phrases):
        nxt = all_phrases[idx + 1]
        if nxt["part"] == cur["part"]:
            # Same part: extend smoothly to next start, max +0.6s
            cur["end"] = min(nxt["start"] - 0.05, cur["end"] + 0.6)
        else:
            # End of part: leave pause clean!
            cur["end"] = min(part_offsets[cur["part"] - 1]["end"], cur["end"] + 0.3)
    else:
        cur["end"] = cur["end"] + 0.3

print(f"\n[OK] Generated {len(all_phrases)} smoothly paced caption phrases!")

out_file = os.path.join(PROC_DIR, "synced_captions_v5.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"total_duration": meta["total_duration"], "captions": all_phrases, "parts": part_offsets}, f, indent=2)

print(f"Saved captions to: {out_file}")
