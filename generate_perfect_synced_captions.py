import os
import json

# Exact Part Ranges in master_narration.wav (seconds):
# Part 1: [0.00s -> 33.91s]
# Gap: 0.45s
# Part 2: [34.36s -> 84.07s]
# Gap: 0.45s
# Part 3: [84.52s -> 122.64s]
# Gap: 0.45s
# Part 4: [123.09s -> 152.26s]
# Gap: 0.45s
# Part 5: [152.71s -> 179.91s]
# Gap: 0.45s
# Part 6: [180.36s -> 201.78s]

CAPTIONS = [
    # --- PART 1: INTRO & MULTI-AGENT MEMORY CRISIS (0.00s - 33.91s) ---
    (0.00, 1.80, "Welcome judges to the"),
    (1.80, 3.80, "FalkorDB Universal Memory Mesh,"),
    (3.80, 5.80, "architected for Graph Hacks 2026"),
    (5.80, 7.80, "across all three challenge tracks."),
    (7.80, 9.60, "When engineering autonomous"),
    (9.60, 11.40, "multi-agent systems,"),
    (11.40, 13.50, "the biggest bottleneck isn't LLMs;"),
    (13.50, 14.80, "it's flat JSON memory."),
    (14.80, 17.60, "Flat JSON arrays cause three compounding failures:"),
    (17.60, 19.80, "duplicate rule bloat,"),
    (19.80, 21.60, "cross-agent secret leaks,"),
    (21.60, 23.40, "and zero causal provenance."),
    (23.40, 25.50, "We solve this by placing our"),
    (25.50, 27.50, "sovereign agent fleet directly onto"),
    (27.50, 29.50, "FalkorDB's linear algebra graph engine,"),
    (29.50, 31.60, "turning prompt guesswork into"),
    (31.60, 33.91, "explainable millisecond graph engineering."),

    # --- PART 2: TRACK 02: INGESTION, QUARANTINE & COW SHADOW (34.36s - 84.07s) ---
    (34.36, 37.20, "For our primary track, Track 02:"),
    (37.20, 39.50, "Agent Memory and Coordination,"),
    (39.50, 42.00, "watch our ingestion pipeline."),
    (42.00, 44.80, "Instead of appending duplicate JSON strings,"),
    (44.80, 47.50, "our Cypher MERGE pipeline collapses"),
    (47.50, 50.20, "300 raw DNA inputs into 93 canonical rules"),
    (50.20, 53.00, "in just 67 milliseconds,"),
    (53.00, 55.80, "converting repeats into edge reinforcement weights."),
    (55.80, 58.50, "Simultaneously, our security sentinel Agent Varuna"),
    (58.50, 61.20, "automatically intercepts 18 synthetic canary leaks"),
    (61.20, 63.80, "and locks them into an isolated Quarantine Vault"),
    (63.80, 66.00, "before touching production memory."),
    (66.00, 68.80, "When agents need to battle-test risky workflows,"),
    (68.80, 71.80, "FalkorDB forks an air-gapped Copy-on-Write shadow graph:"),
    (71.80, 74.20, "shadow_aparajita in 25 milliseconds."),
    (74.20, 76.80, "Inside the sandbox, our 4-stage handoff relay"),
    (76.80, 79.20, "passes cryptographic state hashes across"),
    (79.20, 81.80, "Kalki, Varuna, Vishwakarma, and Sanjaya"),
    (81.80, 84.07, "in 11 milliseconds before clean merge!"),

    # --- PART 3: TRACK 01: GRAPH ALGORITHMS & BLAST RADIUS (84.52s - 122.64s) ---
    (84.52, 87.20, "For Track 01: Agents Acting on Connected Data,"),
    (87.20, 90.00, "FalkorDB does real algorithmic work under Rule 3."),
    (90.00, 93.00, "Clicking Native PageRank executes the in-engine C-procedure"),
    (93.00, 96.20, "CALL algo.pageRank directly in FalkorDB"),
    (96.20, 99.00, "in 5 milliseconds to calculate rule authority."),
    (99.00, 102.00, "When an outage occurs, our Blast Radius tool"),
    (102.00, 105.20, "traverses native directed shortestPath"),
    (105.20, 108.50, "from incident roots to remediation playbooks in 4 milliseconds."),
    (108.50, 111.80, "These algorithms power our Graph-PACC context engine,"),
    (111.80, 115.50, "collapsing complex rule graphs into an anchor"),
    (115.50, 118.50, "of just 196 tokens — strictly under our 300-token invariant,"),
    (118.50, 122.64, "completely eliminating context window exhaustion!"),

    # --- PART 4: TRACK 03: COMPANY BRAIN & PROVENANCE (123.09s - 152.26s) ---
    (123.09, 126.20, "For Track 03: Company Brain,"),
    (126.20, 129.50, "organizational knowledge is unified into a single traversable graph."),
    (129.50, 133.00, "A single Cypher query answers 'Who knows about Cloudflare Tunnel'"),
    (133.00, 136.20, "in 3 milliseconds, resolving system owners,"),
    (136.20, 139.20, "specification authors, and incident ticket resolvers."),
    (139.20, 142.50, "Furthermore, our Decision Trace resolves the complete lineage"),
    (142.50, 145.80, "of RULE_730, linking the active production rule"),
    (145.80, 148.80, "directly back to the Slack channel discussion, Jira ticket,"),
    (148.80, 152.26, "and originating incident root cause: 100% provenance."),

    # --- PART 5: CONCURRENCY BENCHMARK & STUDIO AUDIT (152.71s - 179.91s) ---
    (152.71, 155.80, "To prove enterprise production readiness,"),
    (155.80, 159.20, "our concurrency stress test executes 100 parallel operations"),
    (159.20, 162.80, "across 3 isolated multigraphs at over 1,400 ops/second"),
    (162.80, 165.50, "with zero failures."),
    (165.50, 168.80, "And to verify Rule 3 compliance, here is"),
    (168.80, 172.50, "the official FalkorDB Web Studio running live on port 3000."),
    (172.50, 176.20, "You can see our live multigraph nodes and relationships,"),
    (176.20, 179.91, "proving FalkorDB is driving 100% of the cognitive substrate."),

    # --- PART 6: RULE 10 & 13/13 TESTS (180.36s - 201.78s) ---
    (180.36, 183.80, "Finally, our automated test suite passes"),
    (183.80, 187.00, "13 out of 13 tests in under half a second."),
    (187.00, 190.50, "The entire stack spins up with a single Docker Compose up command,"),
    (190.50, 194.20, "exposing 7 Model Context Protocol tools for autonomous agents."),
    (194.20, 198.00, "The Universal Memory Mesh proves that with FalkorDB graphs,"),
    (198.00, 201.78, "agents are faster, safer, and mathematically explainable. Thank you!")
]

out_json = r"e:\Promptwars2026\Hackathon_falkordb\audio_processed\clean_synced_captions.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(CAPTIONS, f, indent=2)

print(f"Generated {len(CAPTIONS)} clean synchronized captions into {out_json}")
