#!/usr/bin/env python
"""
FalkorDB Universal Memory Mesh — FastAPI Service
================================================
Powers Track 01, Track 02 & Track 03 for Graph Hacks 2026.
Serves the Obsidian Glassmorphism UI and FalkorDB Graph Operations API.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from falkor_memory_mesh import FalkorMemoryMesh

# App Initialization
app = FastAPI(
    title="FalkorDB Memory Mesh Engine",
    description="Universal Memory Mesh & CoW Shadow Clone Orchestrator for Graph Hacks 2026",
    version="2.0.0"
)

# Initialize FalkorDB connection
mesh = FalkorMemoryMesh()

# Models
class LearningRequest(BaseModel):
    aspect: str = "Vishwakarma"
    domain: str = "graph_ui"
    problem: str = "Canvas latency under 10k nodes"
    solution: str = "Enable WebGL instancing with sub-millisecond Cypher viewport bounding box"

class PaccRequest(BaseModel):
    domain_filter: Optional[str] = ""

class QueryRequest(BaseModel):
    prompt: str = "Show all sovereign agents and their enforced rules"
    target_graph: Optional[str] = "purnam_studio_brain"


@app.get("/api/health")
def get_health():
    """Returns FalkorDB connection telemetry and graph state."""
    return {
        "status": "ONLINE" if mesh.connected else "OFFLINE",
        "host": mesh.host,
        "port": mesh.port,
        "master_graph": mesh.master_graph_name,
        "shadow_graph": mesh.shadow_graph_name,
        "zero_secret_law": "ACTIVE",
        "timestamp": int(time.time())
    }


@app.post("/api/seed")
def api_seed():
    """Seeds Master Brain, deduplicates into edge weights, and runs Varuna quarantine."""
    # Look for optional clone_dna.json in current or parent folder
    dna_candidates = [
        Path("clone_dna.json"),
        Path("../.aparajita/clone_dna.json")
    ]
    dna_path = None
    for p in dna_candidates:
        if p.exists():
            dna_path = str(p)
            break

    res = mesh.seed_master_brain(dna_path=dna_path)
    return res


@app.post("/api/spawn-cow")
def api_spawn_cow():
    """Track 02: Spawns isolated Copy-on-Write shadow_aparajita multigraph."""
    res = mesh.spawn_cow_shadow_clone(mission="Graph Hacks 2026 Expedition")
    return res


@app.post("/api/record-learning")
def api_record_learning(req: LearningRequest):
    """Track 02: Records episodic learning in isolated shadow graph."""
    res = mesh.record_shadow_learning(
        agent_aspect=req.aspect,
        domain=req.domain,
        problem=req.problem,
        solution=req.solution
    )
    return res


@app.post("/api/graph-pacc")
def api_graph_pacc(req: PaccRequest):
    """Track 01: Multi-hop Graph-PACC compaction (<300 tokens) scored by graph centrality."""
    res = mesh.run_graph_pacc(domain_filter=req.domain_filter or "")
    return res


@app.post("/api/dispel-merge")
def api_dispel_merge():
    """Track 02 & Track 03: Varuna-audited merge of shadow learning into master brain."""
    res = mesh.dispel_and_merge_clone()
    return res


@app.get("/api/topology")
def api_topology():
    """Returns full multi-graph topology for the interactive visualizer."""
    return mesh.get_topology_snapshot()


@app.post("/api/query")
def api_nl_query(req: QueryRequest):
    """
    Hybrid GraphRAG / NL-to-Cypher Endpoint.
    Uses Gemini Argon if GEMINI_API_KEY is configured in os.environ,
    otherwise uses 100% Zero-Crash deterministic Cypher router.
    """
    t0 = time.perf_counter()
    prompt_lower = req.prompt.lower().strip()
    graph_to_use = mesh.shadow if req.target_graph == "shadow_aparajita" else mesh.master
    graph_name = req.target_graph or mesh.master_graph_name

    # Determine Cypher query via local intent router
    cypher = ""
    intent = "custom"
    
    if any(k in prompt_lower for k in ["agent", "sovereign", "fleet", "commander", "who"]):
        intent = "query_fleet"
        cypher = (
            "MATCH (c:Commander)-[:COMMANDS]->(a:SovereignAgent) "
            "RETURN a.name AS agent, a.role AS role, a.aspect AS aspect"
        )
    elif any(k in prompt_lower for k in ["quarantine", "leak", "secret", "vault", "varuna", "blocked"]):
        intent = "query_quarantine"
        cypher = (
            "MATCH (q:QuarantineVault)-[:CONTAINS_QUARANTINED]->(qr:QuarantinedRule) "
            "RETURN qr.rule_id AS rule_id, qr.blocked_attempts AS blocked_count, qr.text AS canary_token"
        )
    elif any(k in prompt_lower for k in ["incident", "provenance", "origin", "track 3", "brain"]):
        intent = "query_provenance"
        cypher = (
            "MATCH (ar:ArchitecturalRule)-[:ORIGINATED_FROM]->(inc:Incident) "
            "RETURN ar.rule_id AS rule_id, inc.ref AS incident_origin, ar.weight AS weight, ar.text AS directive "
            "ORDER BY ar.weight DESC LIMIT 10"
        )
    elif any(k in prompt_lower for k in ["pacc", "compact", "rule", "context", "weight", "top"]):
        intent = "query_pacc_directives"
        cypher = (
            "MATCH (a:SovereignAgent)-[e:ENFORCES]->(ar:ArchitecturalRule)-[:BELONGS_TO]->(d:Domain) "
            "RETURN a.name AS enforcing_agent, ar.rule_id AS rule_id, d.name AS domain, ar.weight AS weight, ar.text AS rule "
            "ORDER BY ar.weight DESC LIMIT 5"
        )
    elif prompt_lower.startswith("match") or prompt_lower.startswith("return"):
        intent = "raw_cypher"
        cypher = req.prompt
    else:
        intent = "keyword_search"
        cypher = (
            "MATCH (ar:ArchitecturalRule) "
            "WHERE toLower(ar.text) CONTAINS $q OR toLower(ar.domain) CONTAINS $q "
            "RETURN ar.rule_id AS rule_id, ar.domain AS domain, ar.weight AS weight, ar.text AS text "
            "ORDER BY ar.weight DESC LIMIT 6"
        )

    # Optional Gemini LLM Translation if API key is present
    gemini_key = os.environ.get("GEMINI_API_KEY")
    engine_name = "Deterministic FalkorDB Local Router (Zero-Crash)"
    llm_reasoning = ""

    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            # Fetch Graph-PACC anchor to provide graph context to Gemini
            pacc_data = mesh.run_graph_pacc()
            context_str = json.dumps(pacc_data.get("ranked_directives", []))
            
            gemini_prompt = (
                f"You are the Cypher translation core for FalkorDB graph memory.\n"
                f"Graph Context: {context_str}\n"
                f"User Intent: {req.prompt}\n"
                f"Respond with a concise answer explaining the graph traversal."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=gemini_prompt
            )
            llm_reasoning = response.text
            engine_name = "Gemini Argon Multimodal (Connected)"
        except Exception as e:
            llm_reasoning = f"Local router fallback engaged ({e})"

    # Execute Cypher on FalkorDB
    results = []
    headers = []
    if mesh.connected:
        try:
            params = {"q": prompt_lower.split()[-1] if prompt_lower else ""}
            query_res = graph_to_use.query(cypher, params if "$q" in cypher else None)
            headers = [col[1] if isinstance(col, tuple) else str(col) for col in query_res.header] if hasattr(query_res, "header") else []
            results = query_res.result_set
        except Exception as e:
            results = [["ERROR", str(e)]]

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    return {
        "user_prompt": req.prompt,
        "interpreted_intent": intent,
        "engine_used": engine_name,
        "target_graph": graph_name,
        "cypher_executed": cypher,
        "headers": headers,
        "rows_returned": len(results),
        "results": results,
        "llm_analysis": llm_reasoning or f"Traversed {len(results)} nodes in {graph_name} with zero schema hallucination.",
        "latency_ms": latency_ms
    }


# Mount Static Files for Obsidian Glassmorphic Web UI
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.api_route("/", methods=["GET", "HEAD"])
def get_root():
    """Serves the main Obsidian Glassmorphism Dashboard."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "FalkorDB Memory Mesh Backend Active. Open /static/index.html"}

@app.api_route("/style.css", methods=["GET", "HEAD"])
def get_css():
    """Fallback route for root style.css request."""
    return FileResponse(static_dir / "style.css", media_type="text/css")

@app.api_route("/app.js", methods=["GET", "HEAD"])
def get_js():
    """Fallback route for root app.js request."""
    return FileResponse(static_dir / "app.js", media_type="application/javascript")

@app.api_route("/favicon.ico", methods=["GET", "HEAD"])
def get_favicon():
    """Return 204 for favicon to prevent 404 logs."""
    from fastapi import Response
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("🔱 FALKORDB MEMORY MESH — FASTAPI SERVER STARTING ON PORT 8000")
    print("="*70)
    print("📡 Web Dashboard: http://localhost:8000")
    print("⚡ FalkorDB Engine: localhost:6379")
    print("🖥️ FalkorDB Studio: http://localhost:3000\n")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
