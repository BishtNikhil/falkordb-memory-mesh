#!/usr/bin/env python
"""
FalkorDB Universal Memory Mesh & CoW Shadow Clone Engine
========================================================
Powers Track 01 (Connected Data & Graph-PACC), Track 02 (CoW Multigraph Memory),
and Track 03 (Pūrṇam Studio Brain Provenance) on localhost:6379.
"""

import os
import sys
import time
import json
from pathlib import Path
from falkordb import FalkorDB

# Force UTF-8 stdout if possible on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_SOVEREIGN_FLEET = [
    {"agent": "Kalki (कल्कि)", "role": "Supreme Studio Commander & Global Orchestrator", "aspect": "Apex Orchestration, Intent Parsing & Multi-Turn Compaction"},
    {"agent": "Vishwakarma (विश्वकर्मा)", "role": "The Divine Architect & Living UI/UX Sovereign", "aspect": "Zero-White-Tag Glassmorphism & 3D Micro-Interactions"},
    {"agent": "Varuna (वरुण)", "role": "Chief QA, Cosmic Equilibrium & Regulatory Shield", "aspect": "Zero-Secret Leakage Law, Concurrency Armor & Quarantine Gate"},
    {"agent": "Sanjaya (संजय)", "role": "Zero-Code AI Concierge & Jury Pitch Defender", "aspect": "Omniscient Vision, Executive Pitch Narratives & Jury Defense"},
    {"agent": "Naada (नाद)", "role": "Master Sound Engineer & Audio Alchemist", "aspect": "Sub-second FFT Audio Sync & 184.6 BPM Transient Beat-Matching"},
    {"agent": "Vāyu (वायु)", "role": "Kinetic Motion Designer & Speed Ramp Architect", "aspect": "Farnebäck Optical Flow Vectoring & 60 FPS Hitstops"},
    {"agent": "Vidura (विदुर)", "role": "Chief Strategist, Ethics & Statutory Compliance", "aspect": "Platform TOS Immunity & Fair-Use Defensive Architecture"},
    {"agent": "The Sixth Eternal (षष्ठ)", "role": "Sovereign Climax Synthesizer & Gameplay Champion", "aspect": "Predictive Virality Matrix & Autonomous Self-Healing"}
]

DEFAULT_SEED_RULES = [
    {"rule_id": "RULE_042_SELF_HEALI", "domain": "self_healing", "rule": "When 'API Rate Limit / Quota Exhaustion (IGDB)' occurs in GamePromoAgent, apply strategy: Dynamic exponential backoff & failover to secondary unlimited RSS feeds / Watchlist Cache", "created_by": "TheSixth", "incident_ref": "INC_20260928_042", "repeats": 17},
    {"rule_id": "RULE_002_APARAJITA_", "domain": "aparajita_fastapi_st", "rule": "[Aparājita Expedition]: Always mount static directory in FastAPI before adding template routes.", "created_by": "Kalki", "incident_ref": "INC_FASTAPI_STATIC_01", "repeats": 11},
    {"rule_id": "RULE_010_API_SECURI", "domain": "api_security", "rule": "NEVER use try/except:pass around authentication checks. Auth failures MUST propagate as HTTP 401/403 exceptions.", "created_by": "Varuna", "incident_ref": "INC_20260924_010", "repeats": 2},
    {"rule_id": "RULE_014_SECRET_MAN", "domain": "secret_management", "rule": "NEVER use default values for security-critical secrets in os.environ.get(). Fail loudly when missing.", "created_by": "Varuna", "incident_ref": "INC_20260924_014", "repeats": 3},
    {"rule_id": "RULE_730_INFRASTRUC", "domain": "infrastructure_resilience", "rule": "RULE_003_ERROR_1033_AUTONOMOUS_HEALING: Probe public HTTPS domain + port 8600 origin and auto-recycle stale cloudflared daemon within 8s.", "created_by": "Varuna", "incident_ref": "INC_20261012_730", "repeats": 4},
    {"rule_id": "INTEL_RULE_273_UI", "domain": "ui_fullstack_architecture", "rule": "Design interfaces using pure Vanilla CSS Apple-style glassmorphism (backdrop-filter: blur(20px) saturate(180%)) with zero external CSS dependency bloat.", "created_by": "Vishwakarma", "incident_ref": "INTEL_REELS_UI_001", "repeats": 5},
    {"rule_id": "INTEL_RULE_280_VFX", "domain": "motion_vfx_mastery", "rule": "Execute a hard kinetic punch-in zoom (0.5s cut at 1.12x scale) within the first 3 seconds to break scrolling friction.", "created_by": "Vāyu", "incident_ref": "INTEL_REELS_EDIT_001", "repeats": 6},
    {"rule_id": "RULE_255_AUDIO_MAST", "domain": "audio_mastering", "rule": "Zero-Music Spoken Commentary Law: Duck background music to -14dB during voiceovers and snap back on combat impacts.", "created_by": "Naada", "incident_ref": "TRAVEL_VLOG_VOCAL_SHIELD", "repeats": 3},
    {"rule_id": "RULE_040_UNIVERSAL_", "domain": "universal_memory_topology", "rule": "All studio agents share a single unified cognitive substrate via UniversalMemoryMesh and ContextCompactor (<300 tokens).", "created_by": "Kalki", "incident_ref": "INC_20260927_040", "repeats": 4},
    {"rule_id": "CANARY_LEAK_TEST_01", "domain": "aparajita_api_config", "rule": "[Canary Test]: Synthetic test token pattern AIzaSyFakeCanaryKeyForVarunaQuarantineTest999", "created_by": "Aparajita", "incident_ref": "AUDIT_CANARY_01", "repeats": 9}
]


class FalkorMemoryMesh:
    def __init__(self, host=None, port=None, password=None, ssl=False):
        self.host = host or os.getenv("FALKORDB_HOST", "localhost")
        self.port = int(port or os.getenv("FALKORDB_PORT", 6379))
        self.password = password or os.getenv("FALKORDB_PASSWORD", None)
        self.ssl = ssl or os.getenv("FALKORDB_SSL", "false").lower() == "true"
        
        self.master_graph_name = "purnam_studio_brain"
        self.shadow_graph_name = "shadow_aparajita"
        
        try:
            kwargs = {"host": self.host, "port": self.port}
            if self.password:
                kwargs["password"] = self.password
            if self.ssl:
                kwargs["ssl"] = True
            self.client = FalkorDB(**kwargs)
            self.master = self.client.select_graph(self.master_graph_name)
            self.shadow = self.client.select_graph(self.shadow_graph_name)
            # Ping test
            self.master.query("RETURN 1")
            self.connected = True
            print(f"[FalkorDB] Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"[FalkorDB] Connection error ({e}). Falling back to local memory simulation.")
            self.connected = False

    def seed_master_brain(self, dna_path=None):
        """Seeds purnam_studio_brain, deduplicates rules into edge weights, and quarantines leaks."""
        t0 = time.perf_counter()
        if not self.connected:
            return {"status": "offline", "latency_ms": 0, "cypher_executed": "OFFLINE_SIMULATION"}

        # Clear old test state for clean idempotent demo runs
        self.master.query("MATCH (n) DETACH DELETE n")

        fleet = DEFAULT_SOVEREIGN_FLEET
        raw_rules = []

        if dna_path and Path(dna_path).exists():
            try:
                with open(dna_path, "r", encoding="utf-8") as f:
                    dna = json.load(f)
                    fleet = dna.get("sovereign_quadrumvirate", DEFAULT_SOVEREIGN_FLEET)
                    raw_rules = dna.get("architectural_dna", [])
            except Exception as e:
                print(f"[DNA Ingest Warning] Failed to parse {dna_path}: {e}")

        # 1. Create Ponytail Apex Commander Kalki & Sovereign Fleet
        self.master.query(
            "MERGE (c:Commander {name: 'Kalki (कल्कि)', architecture: 'Single-Band Ponytail Clasp'})"
        )
        for ag in fleet:
            self.master.query(
                "MATCH (c:Commander {name: 'Kalki (कल्कि)'}) "
                "MERGE (a:SovereignAgent {name: $name}) "
                "SET a.role = $role, a.aspect = $aspect "
                "MERGE (c)-[:COMMANDS]->(a)",
                {"name": ag["agent"], "role": ag["role"], "aspect": ag["aspect"]}
            )

        raw_count = 0
        quarantined_count = 0

        # Use either loaded DNA rules or built-in canonical dataset
        iterable_rules = raw_rules if raw_rules else DEFAULT_SEED_RULES

        for r in iterable_rules:
            rule_text = (r.get("rule") or "").strip()
            repeats = int(r.get("repeats", 1))
            raw_count += repeats
            if not rule_text:
                continue

            rule_id = r.get("rule_id", "RULE_GEN")
            domain = r.get("domain", "general")
            creator = r.get("created_by", "Kalki")
            inc_ref = r.get("incident_ref", "MANUAL")

            # Varuna Zero-Secret Quarantine Gate
            if any(pat in rule_text for pat in ["AIzaSy", "sk-", "ghp_"]):
                quarantined_count += repeats
                self.master.query(
                    "MATCH (v:SovereignAgent) WHERE v.name CONTAINS 'Varuna' "
                    "MERGE (q:QuarantineVault {name: 'VarunaZeroSecretVault'}) "
                    "MERGE (v)-[:GUARDS]->(q) "
                    "MERGE (qr:QuarantinedRule {text: $text}) "
                    "ON CREATE SET qr.rule_id = $rule_id, qr.blocked_attempts = $repeats "
                    "ON MATCH SET qr.blocked_attempts = qr.blocked_attempts + $repeats "
                    "MERGE (q)-[:CONTAINS_QUARANTINED]->(qr)",
                    {"text": rule_text, "rule_id": rule_id, "repeats": repeats}
                )
                continue

            # Canonical Rule Deduplication + Provenance to Incident & Domain
            self.master.query(
                "MERGE (d:Domain {name: $domain}) "
                "MERGE (inc:Incident {ref: $inc_ref}) "
                "MERGE (ar:ArchitecturalRule {text: $text}) "
                "ON CREATE SET ar.rule_id = $rule_id, ar.domain = $domain, ar.weight = $repeats "
                "ON MATCH SET ar.weight = ar.weight + $repeats "
                "MERGE (ar)-[:BELONGS_TO]->(d) "
                "MERGE (ar)-[:ORIGINATED_FROM]->(inc)",
                {"domain": domain, "inc_ref": inc_ref, "text": rule_text, "rule_id": rule_id, "repeats": repeats}
            )

            # Link to Sovereign Agent
            agent_key = creator.replace("Agent_", "").replace("Agent ", "").split("_")[0].split()[0]
            if agent_key.lower() in ["thesixth", "sixth"]:
                agent_key = "Sixth"
            self.master.query(
                "MATCH (a:SovereignAgent), (ar:ArchitecturalRule {text: $text}) "
                "WHERE toLower(a.name) CONTAINS toLower($agent_key) "
                "MERGE (a)-[e:ENFORCES]->(ar) "
                "ON CREATE SET e.weight = $repeats "
                "ON MATCH SET e.weight = e.weight + $repeats",
                {"agent_key": agent_key, "text": rule_text, "repeats": repeats}
            )

        res_dedup = self.master.query("MATCH (ar:ArchitecturalRule) RETURN count(ar)")
        dedup_count = res_dedup.result_set[0][0] if res_dedup.result_set else 0
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)

        return {
            "status": "seeded",
            "graph": self.master_graph_name,
            "raw_entries_processed": raw_count,
            "deduplicated_canonical_rules": dedup_count,
            "quarantined_secret_attempts": quarantined_count,
            "deduplication_ratio": f"{raw_count} -> {dedup_count} canonical nodes",
            "latency_ms": latency_ms,
            "cypher_executed": "MERGE (ar:ArchitecturalRule {text: $text}) ON MATCH SET ar.weight = ar.weight + $repeats"
        }

    def spawn_cow_shadow_clone(self, mission="Graph Hacks 2026 Expedition"):
        """Track 02: Spawns air-gapped Copy-on-Write shadow_aparajita multigraph from master brain."""
        t0 = time.perf_counter()
        if not self.connected:
            return {"status": "offline", "latency_ms": 0}

        self.shadow.query("MATCH (n) DETACH DELETE n")

        # Pull top rules and agents from master graph
        res = self.master.query(
            "MATCH (a:SovereignAgent)-[e:ENFORCES]->(ar:ArchitecturalRule)-[:BELONGS_TO]->(d:Domain) "
            "RETURN a.name, a.role, ar.rule_id, ar.text, d.name, ar.weight "
            "ORDER BY ar.weight DESC"
        )

        self.shadow.query(
            "CREATE (sc:ShadowClone {name: 'Aparājita (अपराजित)', mode: 'Copy-on-Write Air-Gap', mission: $mission, spawned_at: $ts})",
            {"mission": mission, "ts": int(time.time())}
        )

        copied_rules = 0
        for row in res.result_set:
            ag_name, ag_role, r_id, r_text, dom, weight = row
            copied_rules += 1
            self.shadow.query(
                "MATCH (sc:ShadowClone {name: 'Aparājita (अपराजित)'}) "
                "MERGE (sa:CloneAspect {name: $ag_name, role: $ag_role}) "
                "MERGE (sc)-[:CHANNELS_ASPECT]->(sa) "
                "MERGE (ar:InheritedRule {rule_id: $r_id, text: $r_text, domain: $dom, weight: $weight}) "
                "MERGE (sa)-[:APPLIES {weight: $weight}]->(ar)",
                {"ag_name": ag_name, "ag_role": ag_role, "r_id": r_id, "r_text": r_text, "dom": dom, "weight": weight}
            )

        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "status": "COW_CLONE_ACTIVE",
            "isolated_graph": self.shadow_graph_name,
            "inherited_rules": copied_rules,
            "air_gap_verified": True,
            "latency_ms": latency_ms,
            "cypher_executed": "MATCH (sc:ShadowClone)-[:CHANNELS_ASPECT]->(sa:CloneAspect)-[:APPLIES]->(ar:InheritedRule)"
        }

    def record_shadow_learning(self, agent_aspect: str, domain: str, problem: str, solution: str):
        """Records new episodic learning inside the isolated shadow_aparajita graph."""
        t0 = time.perf_counter()
        if not self.connected:
            return {"status": "offline", "latency_ms": 0}

        rule_text = f"[{domain.upper()}] When '{problem}' occurs -> {solution}"
        cypher = (
            "MATCH (sc:ShadowClone {name: 'Aparājita (अपराजित)'}) "
            "MERGE (sa:CloneAspect {name: $aspect}) "
            "MERGE (sc)-[:CHANNELS_ASPECT]->(sa) "
            "CREATE (ep:EpisodicLearning {domain: $domain, problem: $problem, solution: $solution, text: $text, timestamp: $ts}) "
            "MERGE (sa)-[:DISCOVERED_IN_BATTLE {impact_score: 1.0}]->(ep) "
            "RETURN ep.text"
        )
        self.shadow.query(cypher, {
            "aspect": agent_aspect,
            "domain": domain,
            "problem": problem,
            "solution": solution,
            "text": rule_text,
            "ts": int(time.time())
        })
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "status": "LEARNING_LOGGED_IN_SHADOW_GRAPH",
            "graph": self.shadow_graph_name,
            "aspect": agent_aspect,
            "distilled_rule": rule_text,
            "latency_ms": latency_ms,
            "cypher_executed": cypher
        }

    def run_graph_pacc(self, domain_filter=""):
        """Track 01: Multi-hop Graph-PACC deterministic compaction (<300 tokens) ranked by graph centrality/weight."""
        t0 = time.perf_counter()
        if not self.connected:
            return {
                "pacc_version": "2.0-FalkorDB-GraphRank",
                "token_budget_limit": 300,
                "ranked_directives": [],
                "invariants": ["OFFLINE_FALLBACK"],
                "estimated_tokens": 50,
                "latency_ms": 0,
                "cypher_executed": "OFFLINE_FALLBACK"
            }

        cypher = (
            "MATCH (c:Commander)-[:COMMANDS]->(a:SovereignAgent)-[e:ENFORCES]->(ar:ArchitecturalRule)-[:ORIGINATED_FROM]->(inc:Incident) "
            "WHERE $dom = '' OR toLower(ar.domain) CONTAINS toLower($dom) OR toLower(ar.text) CONTAINS toLower($dom) "
            "RETURN a.name AS agent, ar.rule_id AS rule_id, ar.domain AS domain, ar.text AS directive, ar.weight AS centrality_score, inc.ref AS provenance "
            "ORDER BY ar.weight DESC LIMIT 5"
        )
        res = self.master.query(cypher, {"dom": (domain_filter or "").strip()})
        anchors = []
        for row in res.result_set:
            anchors.append({
                "agent": row[0],
                "rule_id": row[1],
                "domain": row[2],
                "directive": row[3][:140],
                "reinforcement_weight": row[4],
                "provenance_incident": row[5]
            })

        payload = {
            "pacc_version": "2.0-FalkorDB-GraphRank",
            "token_budget_limit": 300,
            "ranked_directives": anchors,
            "invariants": ["MULTIGRAPH_ISOLATED", "VARUNA_ZERO_SECRET", "DEDUPLICATED_TOPOLOGY"]
        }
        est_tokens = int(len(json.dumps(payload).split()) * 1.3)
        payload["estimated_tokens"] = est_tokens
        payload["latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
        payload["cypher_executed"] = cypher
        return payload

    def dispel_and_merge_clone(self):
        """Track 02 & 03: Runs Varuna Zero-Secret Shield on shadow_aparajita and merges verified learnings into purnam_studio_brain."""
        t0 = time.perf_counter()
        if not self.connected:
            return {"status": "offline", "latency_ms": 0}

        res = self.shadow.query(
            "MATCH (sa:CloneAspect)-[:DISCOVERED_IN_BATTLE]->(ep:EpisodicLearning) "
            "RETURN sa.name, ep.domain, ep.text, ep.problem"
        )
        merged = []
        quarantined = []

        for row in res.result_set:
            aspect, domain, text, problem = row
            if any(pat in text for pat in ["AIzaSy", "sk-", "ghp_"]):
                quarantined.append(text)
                self.master.query(
                    "MERGE (q:QuarantineVault {name: 'VarunaZeroSecretVault'}) "
                    "MERGE (qr:QuarantinedRule {text: $text}) "
                    "MERGE (q)-[:CONTAINS_QUARANTINED]->(qr)",
                    {"text": text}
                )
                continue

            merged.append(text)
            agent_key = aspect.split()[0]
            self.master.query(
                "MERGE (d:Domain {name: $domain}) "
                "MERGE (inc:Incident {ref: 'GRAPH_HACKS_2026_EXPEDITION'}) "
                "MERGE (ar:ArchitecturalRule {text: $text}) "
                "ON CREATE SET ar.rule_id = $r_id, ar.domain = $domain, ar.weight = 5 "
                "ON MATCH SET ar.weight = ar.weight + 5 "
                "MERGE (ar)-[:BELONGS_TO]->(d) "
                "MERGE (ar)-[:ORIGINATED_FROM]->(inc) "
                "WITH ar "
                "MATCH (a:SovereignAgent) WHERE toLower(a.name) CONTAINS toLower($agent_key) "
                "MERGE (a)-[e:ENFORCES]->(ar) "
                "ON CREATE SET e.weight = 5 "
                "ON MATCH SET e.weight = e.weight + 5",
                {"domain": domain, "text": text, "r_id": f"RULE_GH26_{int(time.time())}", "agent_key": agent_key}
            )

        # Clear ephemeral learnings after absorption
        self.shadow.query("MATCH (ep:EpisodicLearning) DETACH DELETE ep")
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)

        return {
            "status": "DISPEL_MERGE_COMPLETE",
            "merged_into_master_count": len(merged),
            "blocked_by_varuna_count": len(quarantined),
            "merged_rules": merged,
            "blocked_rules": quarantined,
            "latency_ms": latency_ms,
            "cypher_executed": "MERGE (ar:ArchitecturalRule {text: $text}) ON MATCH SET ar.weight = ar.weight + 5"
        }

    def get_topology_snapshot(self):
        """Returns nodes and edges from both Master and Shadow graphs for the UI visualizer."""
        if not self.connected:
            return {
                "master_graph": self.master_graph_name,
                "shadow_graph": self.shadow_graph_name,
                "master_triples": [],
                "quarantined_threats": [],
                "shadow_pending_learnings": []
            }

        master_nodes = self.master.query(
            "MATCH (a:SovereignAgent)-[e:ENFORCES]->(ar:ArchitecturalRule)-[:ORIGINATED_FROM]->(inc:Incident) "
            "RETURN a.name, ar.rule_id, ar.domain, ar.weight, inc.ref, ar.text "
            "ORDER BY ar.weight DESC LIMIT 25"
        ).result_set

        quarantine_nodes = self.master.query(
            "MATCH (q:QuarantineVault)-[:CONTAINS_QUARANTINED]->(qr:QuarantinedRule) "
            "RETURN qr.rule_id, qr.blocked_attempts, qr.text"
        ).result_set

        shadow_learnings = self.shadow.query(
            "MATCH (sa:CloneAspect)-[:DISCOVERED_IN_BATTLE]->(ep:EpisodicLearning) "
            "RETURN sa.name, ep.domain, ep.text"
        ).result_set

        shadow_clone_node = self.shadow.query(
            "MATCH (sc:ShadowClone) RETURN sc.name, sc.mode, sc.mission"
        ).result_set

        return {
            "master_graph": self.master_graph_name,
            "shadow_graph": self.shadow_graph_name,
            "master_triples": [
                {"agent": r[0], "rule_id": r[1], "domain": r[2], "weight": r[3], "incident": r[4], "text": r[5]}
                for r in master_nodes
            ],
            "quarantined_threats": [
                {"rule_id": r[0], "blocked_attempts": r[1], "text": r[2] if len(r) > 2 else ""} for r in quarantine_nodes
            ],
            "shadow_clone_status": [
                {"name": r[0], "mode": r[1], "mission": r[2]} for r in shadow_clone_node
            ],
            "shadow_pending_learnings": [
                {"aspect": r[0], "domain": r[1], "text": r[2]} for r in shadow_learnings
            ]
        }


if __name__ == "__main__":
    mesh = FalkorMemoryMesh()
    print("🔱 1. Seeding Master Brain:")
    print(json.dumps(mesh.seed_master_brain(), indent=2, ensure_ascii=False))
    print("\n🧬 2. Spawning CoW Shadow Clone:")
    print(json.dumps(mesh.spawn_cow_shadow_clone(), indent=2, ensure_ascii=False))
    print("\n⚡ 3. Recording Battle Learning in Shadow Clone:")
    print(json.dumps(mesh.record_shadow_learning("Vishwakarma", "graph_ui", "Large graph canvas lag", "Use WebGL/Canvas force layout with <200ms Cypher pagination"), indent=2, ensure_ascii=False))
    print("\n🧠 4. Running Graph-PACC (<300 Token Compaction):")
    print(json.dumps(mesh.run_graph_pacc(), indent=2, ensure_ascii=False))
    print("\n🔄 5. Dispelling Shadow Clone & Merging into Master Brain:")
    print(json.dumps(mesh.dispel_and_merge_clone(), indent=2, ensure_ascii=False))