#!/usr/bin/env python
"""
Model Context Protocol (MCP) Tool Registry & Server for FalkorDB Universal Memory Mesh
======================================================================================
Exposes standard MCP tool definitions and execution handler for agents
(Gemini, Claude, GPT, Cursor, Windsurf) to dynamically discover and invoke
FalkorDB graph algorithms and memory operations.
"""

from typing import Dict, Any, List
from falkor_memory_mesh import FalkorMemoryMesh

# Initialize Mesh singleton
mesh = FalkorMemoryMesh()

# MCP Tools Registry Specification (JSON-Schema format)
MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "falkor_shortest_path",
        "description": "Finds the directed shortest path between an incident and its remediation playbook or between any two graph nodes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_label": {"type": "string", "default": "Incident", "description": "Label of starting node"},
                "start_prop": {"type": "string", "default": "ref", "description": "Property name of starting node"},
                "start_val": {"type": "string", "default": "INC_20261012_730", "description": "Property value of start node"},
                "end_label": {"type": "string", "default": "ProceduralPlaybook", "description": "Label of target node"},
                "end_prop": {"type": "string", "default": "playbook_id", "description": "Property name of target node"},
                "end_val": {"type": "string", "default": "PLAY_730", "description": "Property value of target node"}
            },
            "required": ["start_val", "end_val"]
        }
    },
    {
        "name": "falkor_pagerank_centrality",
        "description": "Runs native FalkorDB PageRank algorithm across architectural rules and domains to determine structural authority.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node_label": {"type": "string", "default": "ArchitecturalRule", "description": "Node label to rank"},
                "rel_type": {"type": "string", "default": "BELONGS_TO", "description": "Relationship type to traverse"}
            }
        }
    },
    {
        "name": "falkor_blast_radius",
        "description": "Calculates multi-hop outage blast radius, affected services, and owning teams if a critical core system fails.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "system_name": {"type": "string", "description": "Name of system (e.g., AudioSyncEngine, TokenSentinel, CloudflareTunnelGateway)"}
            },
            "required": ["system_name"]
        }
    },
    {
        "name": "falkor_pacc_compact",
        "description": "Runs deterministic Graph-PACC compaction to synthesize high-weight graph memory into <300 token system context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain_filter": {"type": "string", "default": "", "description": "Optional domain filter (e.g., self_healing, ui, security)"}
            }
        }
    },
    {
        "name": "falkor_who_knows",
        "description": "Company Brain query: Identifies which agent owns a system, authored documentation, or resolved past incidents.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "system_name": {"type": "string", "default": "", "description": "Name or substring of system"}
            }
        }
    },
    {
        "name": "falkor_decision_provenance",
        "description": "Traces rule decisions back to originating incidents, GitHub/Jira tickets, and war-room chat threads.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rule_id": {"type": "string", "default": "RULE_730_INFRASTRUC", "description": "Rule identifier or keyword"}
            },
            "required": ["rule_id"]
        }
    },
    {
        "name": "falkor_varuna_quarantine",
        "description": "Audits graph for canary tokens or API key leaks and reports quarantined items in VarunaZeroSecretVault.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def execute_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatches MCP tool invocation to FalkorDB Universal Memory Mesh."""
    if tool_name == "falkor_shortest_path":
        return mesh.find_shortest_path(
            start_label=arguments.get("start_label", "Incident"),
            start_prop=arguments.get("start_prop", "ref"),
            start_val=arguments.get("start_val", "INC_20261012_730"),
            end_label=arguments.get("end_label", "ProceduralPlaybook"),
            end_prop=arguments.get("end_prop", "playbook_id"),
            end_val=arguments.get("end_val", "PLAY_730")
        )
    elif tool_name == "falkor_pagerank_centrality":
        return mesh.run_pagerank(
            node_label=arguments.get("node_label", "ArchitecturalRule"),
            rel_type=arguments.get("rel_type", "BELONGS_TO")
        )
    elif tool_name == "falkor_blast_radius":
        return mesh.calculate_blast_radius(
            system_name=arguments.get("system_name", "AudioSyncEngine")
        )
    elif tool_name == "falkor_pacc_compact":
        return mesh.run_graph_pacc(
            domain_filter=arguments.get("domain_filter", "")
        )
    elif tool_name == "falkor_who_knows":
        return mesh.query_who_knows(
            system_name=arguments.get("system_name", "")
        )
    elif tool_name == "falkor_decision_provenance":
        return mesh.trace_decision_provenance(
            rule_id=arguments.get("rule_id", "RULE_730_INFRASTRUC")
        )
    elif tool_name == "falkor_varuna_quarantine":
        top = mesh.get_topology_snapshot()
        return {
            "vault": "VarunaZeroSecretVault",
            "status": "ACTIVE_AIR_GAP",
            "quarantined_threats": top.get("quarantined_threats", []),
            "total_threats_blocked": len(top.get("quarantined_threats", []))
        }
    else:
        return {"error": f"Unknown MCP tool: {tool_name}", "available_tools": [t["name"] for t in MCP_TOOLS]}


if __name__ == "__main__":
    print(f"🔱 FalkorDB MCP Server registered {len(MCP_TOOLS)} tools.")
    for tool in MCP_TOOLS:
        print(f" - {tool['name']}: {tool['description']}")
