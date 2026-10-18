import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_BASE = "https://falkordb.purnamstudio.com"

LEARNINGS = [
    {
        "aspect": "Kalki (कल्कि)",
        "domain": "multigraph_mesh",
        "problem": "Flat JSON and vector RAG cause token bloat and schema blindness in multi-agent workflows",
        "solution": "Deploy FalkorDB GraphBLAS sparse matrix linear algebra as cognitive substrate, combining sub-millisecond Cypher traversals with 3-tier memory."
    },
    {
        "aspect": "Aparājita (अपराजित)",
        "domain": "cow_sandboxing",
        "problem": "Experimental agent trials risk state pollution and contaminate canonical production memory",
        "solution": "Implement Copy-on-Write (CoW) shadow forking (shadow_aparajita) inheriting canonical rules in 25.8 ms for air-gapped simulation."
    },
    {
        "aspect": "Varuna (वरुण)",
        "domain": "zero_secret_security",
        "problem": "Autonomous agent outputs accidentally introduce synthetic canary keys (AIzaSy, sk-, ghp_) into long-term graph memory",
        "solution": "Pre-commit regex and AST interceptor routing unverified secrets to VarunaZeroSecretVault node, enforcing 100% zero-leak guarantee."
    },
    {
        "aspect": "Vishwakarma (विश्वकर्मा)",
        "domain": "graph_pacc_compaction",
        "problem": "Long-running agent loops exceed LLM context window limits and spike inference latency",
        "solution": "Engineer Graph-PACC context compaction using native algo.pageRank centrality to deterministically compress rules into <300 tokens (tested at 201)."
    },
    {
        "aspect": "Sanjaya (संजय)",
        "domain": "agent_state_relay",
        "problem": "Asynchronous multi-agent handoffs suffer from state drift and unverified transitions",
        "solution": "Establish 4-agent sequential handoff chain (Kalki->Varuna->Vishwakarma->Sanjaya) with SHA256 state token hashes on :HANDED_OFF_TO edges."
    },
    {
        "aspect": "Vishwakarma (विश्वकर्मा)",
        "domain": "connected_data_remediation",
        "problem": "Service dependencies during incidents require multi-system debugging to trace blast radius and shortest path",
        "solution": "Native Cypher shortestPath and multi-hop blast radius traversals resolving root-cause service chains in sub-5ms."
    },
    {
        "aspect": "Sanjaya (संजय)",
        "domain": "decision_provenance",
        "problem": "Organizational knowledge fragmentation across Jira, Slack, and post-mortems obscures rule rationale",
        "solution": "Unify tickets, chat threads, incidents, and constraints in a 4-tier graph (:LED_TO_RULE, :DECIDED_RULE, :ORIGINATED_FROM) resolving in 2.18 ms."
    },
    {
        "aspect": "Kalki (कल्कि)",
        "domain": "model_context_protocol",
        "problem": "Modern LLM agents (Claude, Cursor, Gemini) lack standard interfaces to query and manipulate graph state",
        "solution": "Deploy 7-tool Model Context Protocol (MCP) server over /api/mcp/tools enabling native graph compaction and sandboxing from LLM prompts."
    },
    {
        "aspect": "Vishwakarma (विश्वकर्मा)",
        "domain": "concurrency_performance",
        "problem": "Concurrent agent fleets cause database connection contention and latency bottlenecks",
        "solution": "FalkorDB Redis-wire protocol with thread pool optimization achieving 1,401.32 ops/sec concurrent throughput with 0 errors across 50 workers."
    },
    {
        "aspect": "Sanjaya (संजय)",
        "domain": "infrastructure_deployment",
        "problem": "Hosting public production endpoints from local hardware without exposing open router ports or static IP",
        "solution": "Cloudflare Zero-Trust Named Tunnel (falkordb.purnamstudio.com) connected to Docker cluster with automated HTTPS and DDoS protection."
    }
]

def post_json(url, data_dict):
    payload = json.dumps(data_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    print("=" * 70)
    print("[PURNA STUDIO FLEET] IMPARTING EPISODIC LEARNINGS TO APARAJITA")
    print("=" * 70)

    # 1. Verify shadow clone is active
    print("\n[Step 1] Ensuring Copy-on-Write Shadow Clone (shadow_aparajita) is active...")
    spawn_res = post_json(f"{API_BASE}/api/spawn-cow", {})
    print(f"Shadow clone status: {spawn_res.get('status')} ({spawn_res.get('latency_ms')} ms)")

    # 2. Impart all 10 episodic learnings into shadow_aparajita
    print("\n[Step 2] Recording 10 Core Architectural Learnings into Aparajita's Shadow Graph...")
    for idx, item in enumerate(LEARNINGS, 1):
        res = post_json(f"{API_BASE}/api/record-learning", item)
        aspect = item["aspect"]
        domain = item["domain"]
        lat = res.get("latency_ms")
        print(f"  [{idx:02d}/10] Aspect: {aspect:<25} Domain: {domain:<26} ({lat} ms)")

    # 3. Simulate 4-agent state handoff relay to lock in the battle simulation
    print("\n[Step 3] Running 4-Agent Sequential State Handoff Relay across Shadow Clone...")
    relay_res = post_json(f"{API_BASE}/api/handoff-relay", {
        "mission_task": "Full Expedition Knowledge Synthesis & Zero-Secret Audit"
    })
    total_lat = relay_res.get('latency_ms')
    chain = relay_res.get('relay_chain', [])
    print(f"Relay Chain Status: {relay_res.get('status')} across {len(chain)} steps ({total_lat} ms)")
    for step in chain:
        print(f"    * Step {step['step']}: {step['agent']:<25} | Role: {step['role']:<35} | Hash: {step['state_hash']}")

    # 4. Check snapshot of shadow graph before dispel
    print("\n[Step 4] Checking Pre-Dispel Topology Snapshot...")
    req = urllib.request.Request(f"{API_BASE}/api/topology", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        top = json.loads(resp.read().decode("utf-8"))
        pending = len(top.get("shadow_pending_learnings", []))
        print(f"Aparajita Shadow Graph holds: {pending} episodic learnings waiting for Varuna audit.")

    # 5. Execute Kalki Dispel & Merge (Varuna Audited)
    print("\n[Step 5] EXECUTING KALKI DISPEL & MERGE (VARUNA AUDITED)...")
    dispel_res = post_json(f"{API_BASE}/api/dispel-merge", {})
    print(f"Dispel Status: {dispel_res.get('status')} ({dispel_res.get('latency_ms')} ms)")
    print(f"Merged into Master Brain: {dispel_res.get('merged_into_master_count')} architectural rules")
    print(f"Blocked by Varuna Shield: {dispel_res.get('blocked_by_varuna_count')} threats")
    
    # 6. Verify Master Brain assimilated everything
    print("\n[Step 6] Verifying Master Brain Topology Post-Assimilation...")
    req = urllib.request.Request(f"{API_BASE}/api/topology", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        top_after = json.loads(resp.read().decode("utf-8"))
        print(f"Master Triples in Active Memory: {len(top_after.get('master_triples', []))}")
        print(f"Company Systems Online: {len(top_after.get('company_systems', []))}")
        print(f"Quarantined Threats: {len(top_after.get('quarantined_threats', []))}")

    print("\n" + "=" * 70)
    print("SUCCESS: ALL EXPEDITION KNOWLEDGE HAS BEEN PERMANENTLY ABSORBED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
