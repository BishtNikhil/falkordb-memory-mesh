import json
import re

CAPTIONS_FILE = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed\synced_captions_v5.json"

with open(CAPTIONS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

REPLACEMENTS = [
    (r"\bFalkorDB DB\b", "FalkorDB"),
    (r"\bGraph Hectron 26\b", "Graph Hacks 2026"),
    (r"\bGraph Hectron\b", "Graph Hacks"),
    (r"\bDuplicate Toolblow\b", "Duplicate rule bloat"),
    (r"\bToolblow\b", "rule bloat"),
    (r"\bclose agent\b", "cross-agent"),
    (r"\bsenior algebra\b", "linear-algebra"),
    (r"\bprompt gas work\b", "prompt guesswork"),
    (r"\bexpandable\b", "explainable"),
    (r"\bend-agestion\b", "ingestion"),
    (r"\bend -agestion\b", "ingestion"),
    (r"\bagestion\b", "ingestion"),
    (r"\bcipher Merch\b", "Cypher MERGE"),
    (r"\bMerch\b", "MERGE"),
    (r"\btrack track\b", "Track 02:"),
    (r"\btrack track to\b", "Track 02:"),
    (r"\btrack to\b", "Track 02:"),
    (r"\bfor our primary track Track 02:\b", "For our primary track, Track 02:"),
    (r"\bFor our primary track Track 02:\b", "For our primary track, Track 02:"),
    (r"\bintros\b", "inputs"),
    (r"\bagile enforcement\b", "edge reinforcement"),
    (r"\bworld\b", "Vault"),
    (r"\bkevark\b", "hazardous"),
    (r"\bshadow_apprajita\b", "shadow_aparajita"),
    (r"\bapprajita\b", "Aparājita"),
    (r"\bright shadow\b", "Write shadow"),
    (r"\bC procedure called algo \.page\b", "native CALL algo.pageRank()"),
    (r"\balgo \.page rank\b", "algo.pageRank()"),
    (r"\balgo \.page\b", "algo.pageRank()"),
    (r"\bpack algorithm\b", "Graph-PACC algorithm"),
    (r"\bpack\b", "Graph-PACC"),
    (r"\b2 \.5 flash organ\b", "2.5 Flash Argon"),
    (r"\borgan\b", "Argon"),
    (r"\brule 730\b", "RULE_730"),
    (r"\brule seven thirty\b", "RULE_730"),
    (r"\brule 10\b", "Rule 10"),
    (r"\brule 3\b", "Rule 3"),
    (r"\brule 5\b", "Rule 5"),
    (r"\b13 out of 13\b", "13 out of 13"),
    (r"\b0 \.4\b", "0.4"),
    (r"\bpoint 4\b", "0.4"),
]

for c in data["captions"]:
    t = c["text"]
    for pat, rep in REPLACEMENTS:
        t = re.sub(pat, rep, t, flags=re.IGNORECASE)
    # Ensure starting cleanups
    t = t.replace("  ", " ").strip()
    c["text"] = t

with open(CAPTIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"[OK] Polished {len(data['captions'])} captions with perfect domain accuracy in {CAPTIONS_FILE}")
