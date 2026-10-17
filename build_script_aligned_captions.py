import os
import json

# Authoritative script phrases with exact timing calibrated to user voiceover
CAPTIONS = [
    # =========================================================================
    # PART 1: The Multi-Agent Crisis & Architecture Intro (0.00s -> 34.55s)
    # =========================================================================
    {"part": 1, "start": 0.00, "end": 2.10, "text": "Hi everyone, and welcome judges"},
    {"part": 1, "start": 2.10, "end": 3.92, "text": "to the FalkorDB Universal Memory Mesh,"},
    {"part": 1, "start": 3.92, "end": 6.10, "text": "architected for Graph Hacks 2026"},
    {"part": 1, "start": 6.10, "end": 8.08, "text": "across all three challenge tracks."},
    {"part": 1, "start": 8.08, "end": 10.30, "text": "When engineering autonomous multi-agent systems,"},
    {"part": 1, "start": 10.30, "end": 12.32, "text": "the biggest bottleneck isn't the LLM—"},
    {"part": 1, "start": 12.32, "end": 13.84, "text": "it's flat JSON memory."},
    {"part": 1, "start": 13.84, "end": 16.20, "text": "Storing agent memory in flat JSON arrays"},
    {"part": 1, "start": 16.20, "end": 18.16, "text": "causes three compounding failures:"},
    {"part": 1, "start": 18.16, "end": 19.80, "text": "duplicate rule bloat,"},
    {"part": 1, "start": 19.80, "end": 21.10, "text": "cross-agent secret leaks,"},
    {"part": 1, "start": 21.10, "end": 22.40, "text": "and zero causal provenance."},
    {"part": 1, "start": 22.40, "end": 24.60, "text": "We solved this by placing"},
    {"part": 1, "start": 24.60, "end": 26.88, "text": "our sovereign agent fleet directly"},
    {"part": 1, "start": 26.88, "end": 29.68, "text": "onto FalkorDB's high-performance linear algebra substrate,"},
    {"part": 1, "start": 29.68, "end": 32.40, "text": "turning untraceable prompt guesswork into"},
    {"part": 1, "start": 32.40, "end": 34.55, "text": "explainable, millisecond graph engineering."},

    # (Silence Gap: 34.55s -> 35.75s)

    # =========================================================================
    # PART 2: Track 02 — Memory Ingestion, Quarantine & CoW Sandbox (35.75s -> 86.20s)
    # =========================================================================
    {"part": 2, "start": 35.75, "end": 38.80, "text": "For our primary track, Track 02: Agent Memory and Coordination,"},
    {"part": 2, "start": 38.80, "end": 41.19, "text": "watch our ingestion pipeline."},
    {"part": 2, "start": 41.19, "end": 43.80, "text": "Instead of appending duplicate JSON strings,"},
    {"part": 2, "start": 43.80, "end": 46.55, "text": "our Cypher MERGE pipeline collapses 300 raw DNA inputs"},
    {"part": 2, "start": 46.55, "end": 49.50, "text": "into 93 canonical rules in just 67 milliseconds,"},
    {"part": 2, "start": 49.50, "end": 52.95, "text": "converting repeats into edge reinforcement weights."},
    {"part": 2, "start": 52.95, "end": 55.80, "text": "Simultaneously, our security sentinel, Agent Varuna,"},
    {"part": 2, "start": 55.80, "end": 58.71, "text": "automatically intercepts 18 synthetic canary leak attempts"},
    {"part": 2, "start": 58.71, "end": 61.20, "text": "and locks them into an isolated QuarantineVault"},
    {"part": 2, "start": 61.20, "end": 63.67, "text": "before they ever touch production memory."},
    {"part": 2, "start": 63.67, "end": 66.50, "text": "When agents need to battle-test risky workflows,"},
    {"part": 2, "start": 66.50, "end": 69.43, "text": "FalkorDB forks an air-gapped Copy-on-Write shadow graph—"},
    {"part": 2, "start": 69.43, "end": 72.50, "text": "shadow_aparajita—in 25 milliseconds."},
    {"part": 2, "start": 72.50, "end": 75.43, "text": "Inside the sandbox, our 4-stage handoff relay"},
    {"part": 2, "start": 75.43, "end": 79.20, "text": "passes cryptographic state hashes across Kalki, Varuna,"},
    {"part": 2, "start": 79.20, "end": 82.71, "text": "Vishwakarma, and Sanjaya in 11 milliseconds,"},
    {"part": 2, "start": 82.71, "end": 86.20, "text": "before clean dispel and merge back into the master brain."},

    # (Silence Gap: 86.20s -> 87.40s)

    # =========================================================================
    # PART 3: Track 01 — Native Graph Algorithms & Graph-PACC (87.40s -> 126.15s)
    # =========================================================================
    {"part": 3, "start": 87.40, "end": 90.60, "text": "For Track 01: Agents Acting on Connected Data,"},
    {"part": 3, "start": 90.60, "end": 93.56, "text": "FalkorDB does real algorithmic work under Rule 3."},
    {"part": 3, "start": 93.56, "end": 96.20, "text": "Clicking 'Native PageRank' executes the in-engine C-procedure"},
    {"part": 3, "start": 96.20, "end": 99.80, "text": "CALL algo.pageRank directly in FalkorDB in 5 milliseconds"},
    {"part": 3, "start": 99.80, "end": 102.68, "text": "to calculate structural rule authority."},
    {"part": 3, "start": 102.68, "end": 105.80, "text": "When an outage occurs, our Blast Radius tool"},
    {"part": 3, "start": 105.80, "end": 108.60, "text": "traverses native directed shortestPath from incident roots"},
    {"part": 3, "start": 108.60, "end": 111.32, "text": "to remediation playbooks in 4 milliseconds."},
    {"part": 3, "start": 111.32, "end": 115.40, "text": "These algorithms power our Graph-PACC context engine on the right—"},
    {"part": 3, "start": 115.40, "end": 118.50, "text": "collapsing complex rule graphs into a deterministic"},
    {"part": 3, "start": 118.50, "end": 121.24, "text": "context anchor of just 196 tokens,"},
    {"part": 3, "start": 121.24, "end": 123.80, "text": "strictly under our 300-token invariant,"},
    {"part": 3, "start": 123.80, "end": 126.15, "text": "completely eliminating context window exhaustion."},

    # (Silence Gap: 126.15s -> 127.35s)

    # =========================================================================
    # PART 4: Track 03 — Company Brain & Decision Provenance (127.35s -> 157.40s)
    # =========================================================================
    {"part": 4, "start": 127.35, "end": 130.20, "text": "For Track 03: Company Brain,"},
    {"part": 4, "start": 130.20, "end": 132.55, "text": "organizational knowledge is unified into a single traversable graph."},
    {"part": 4, "start": 132.55, "end": 135.50, "text": "A single Cypher query answers"},
    {"part": 4, "start": 135.50, "end": 137.91, "text": "'Who knows about Cloudflare Tunnel or NVENC?' in 3 milliseconds,"},
    {"part": 4, "start": 137.91, "end": 140.40, "text": "resolving system owners, specification authors,"},
    {"part": 4, "start": 140.40, "end": 142.31, "text": "and incident ticket resolvers."},
    {"part": 4, "start": 142.31, "end": 145.20, "text": "Furthermore, our Decision Trace resolves the complete lineage of RULE_730—"},
    {"part": 4, "start": 145.20, "end": 148.00, "text": "linking the active production rule directly back to"},
    {"part": 4, "start": 148.00, "end": 150.60, "text": "the Slack channel discussion, the Jira ticket,"},
    {"part": 4, "start": 150.60, "end": 153.20, "text": "and the originating incident root cause."},
    {"part": 4, "start": 153.20, "end": 157.40, "text": "Zero guesswork, 100% explainable provenance."},

    # (Silence Gap: 157.40s -> 158.60s)

    # =========================================================================
    # PART 5: Concurrency Benchmarks & Native FalkorDB Studio (158.60s -> 186.60s)
    # =========================================================================
    {"part": 5, "start": 158.60, "end": 161.50, "text": "To prove enterprise production readiness,"},
    {"part": 5, "start": 161.50, "end": 164.20, "text": "our concurrency stress test executes 100 parallel reads and writes"},
    {"part": 5, "start": 164.20, "end": 167.20, "text": "across three isolated multigraphs"},
    {"part": 5, "start": 167.20, "end": 169.72, "text": "at over 1,400 operations per second with zero failures."},
    {"part": 5, "start": 169.72, "end": 172.50, "text": "And to verify Rule 3 compliance,"},
    {"part": 5, "start": 172.50, "end": 175.20, "text": "here is the official FalkorDB Web Studio running live on port 3000."},
    {"part": 5, "start": 175.20, "end": 178.60, "text": "You can see our live multigraph nodes and relationships"},
    {"part": 5, "start": 178.60, "end": 182.20, "text": "populated directly in FalkorDB's native visualizer,"},
    {"part": 5, "start": 182.20, "end": 186.60, "text": "proving that FalkorDB is actively driving the entire cognitive substrate."},

    # (Silence Gap: 186.60s -> 187.80s)

    # =========================================================================
    # PART 6: Rule 10 Verification & Conclusion (187.80s -> 209.85s)
    # =========================================================================
    {"part": 6, "start": 187.80, "end": 190.50, "text": "Finally, our automated test suite passes 13 out of 13 tests"},
    {"part": 6, "start": 190.50, "end": 193.00, "text": "in under half a second."},
    {"part": 6, "start": 193.00, "end": 195.80, "text": "The entire stack spins up with a single command"},
    {"part": 6, "start": 195.80, "end": 197.96, "text": "via docker compose up under Rule 10,"},
    {"part": 6, "start": 197.96, "end": 201.80, "text": "exposing 7 Model Context Protocol tools for autonomous agents."},
    {"part": 6, "start": 201.80, "end": 204.50, "text": "The Universal Memory Mesh proves that when agents"},
    {"part": 6, "start": 204.50, "end": 207.20, "text": "think with FalkorDB graphs, they are faster, safer,"},
    {"part": 6, "start": 207.20, "end": 209.85, "text": "and mathematically explainable. Thank you!"}
]

PROC_DIR = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed"
with open(os.path.join(PROC_DIR, "part_offsets_v5.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

out_file = os.path.join(PROC_DIR, "authoritative_script_captions.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({
        "total_duration": meta["total_duration"],
        "parts": meta["parts"],
        "captions": CAPTIONS
    }, f, indent=2)

print(f"[OK] Authoritative script captions generated: {len(CAPTIONS)} phrases saved to {out_file}")
