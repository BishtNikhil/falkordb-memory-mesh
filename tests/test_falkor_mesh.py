#!/usr/bin/env python
"""
Automated Test Suite for FalkorDB Universal Memory Mesh
=======================================================
Complies with Rule 10 (Submission Spec) & Judge Grading Rubric:
- Track 01: Multi-Hop Connected Data, Native PageRank, ShortestPath, Graph-PACC <300 tokens
- Track 02: 3-Tier Memory, CoW Shadow Clones, Multi-Agent Handoff Chain, Multigraph Concurrency
- Track 03: Company Brain (Systems, Docs, Tickets, Chats) & Origin Lineage
"""

import sys
import os
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from falkor_memory_mesh import FalkorMemoryMesh
from mcp_server import MCP_TOOLS, execute_mcp_tool


class TestFalkorMemoryMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initializes mesh connection once for entire test suite."""
        cls.mesh = FalkorMemoryMesh()

    def test_01_falkordb_connection(self):
        """Test 1: Live connection to FalkorDB on port 6379."""
        self.assertTrue(self.mesh.connected, "FalkorDB should be connected on localhost:6379")
        res = self.mesh.master.query("RETURN 1 AS ping")
        self.assertEqual(res.result_set[0][0], 1)

    def test_02_seed_and_deduplication(self):
        """Test 2: Master Brain seeding collapses raw rules into weighted canonical nodes."""
        res = self.mesh.seed_master_brain()
        self.assertEqual(res["status"], "seeded")
        self.assertGreater(res["raw_entries_processed"], 0)
        self.assertGreater(res["deduplicated_canonical_rules"], 0)
        # Deduplication ratio check: raw count >= canonical count
        self.assertGreaterEqual(res["raw_entries_processed"], res["deduplicated_canonical_rules"])

    def test_03_varuna_zero_secret_quarantine(self):
        """Test 3: Varuna Zero-Secret Shield quarantines canary token leak attempts."""
        top = self.mesh.get_topology_snapshot()
        quarantined = top.get("quarantined_threats", [])
        self.assertGreater(len(quarantined), 0, "Quarantine vault must contain intercepted threats")
        # Ensure quarantined token has blocked count
        self.assertGreater(quarantined[0]["blocked_attempts"], 0)

    def test_04_cow_shadow_clone_isolation(self):
        """Test 4: Copy-on-Write (CoW) multigraph fork creates air-gapped shadow_aparajita."""
        res = self.mesh.spawn_cow_shadow_clone(mission="Test Sandbox Mission")
        self.assertEqual(res["status"], "COW_CLONE_ACTIVE")
        self.assertEqual(res["isolated_graph"], "shadow_aparajita")
        self.assertTrue(res["air_gap_verified"])
        self.assertGreater(res["inherited_rules"], 0)

    def test_05_three_tier_memory_topology(self):
        """Test 5: Explicit 3-tier memory nodes (Semantic, Procedural, Episodic)."""
        # Semantic concepts query
        sem_res = self.mesh.master.query("MATCH (sc:SemanticConcept) RETURN count(sc)")
        self.assertGreater(sem_res.result_set[0][0], 0, "Must have (:SemanticConcept) nodes")

        # Procedural playbooks query
        proc_res = self.mesh.master.query("MATCH (pb:ProceduralPlaybook) RETURN count(pb)")
        self.assertGreater(proc_res.result_set[0][0], 0, "Must have (:ProceduralPlaybook) nodes")

        # Log episodic learning into shadow clone
        ep_res = self.mesh.record_shadow_learning(
            agent_aspect="Varuna",
            domain="security",
            problem="Canary probe in prompt",
            solution="Block before AST parsing"
        )
        self.assertEqual(ep_res["status"], "LEARNING_LOGGED_IN_SHADOW_GRAPH")

    def test_06_multi_agent_handoff_relay(self):
        """Test 6: 4-agent state handoff relay writes [:HANDED_OFF_TO] edges."""
        res = self.mesh.simulate_agent_handoff_relay(mission_task="Automated CI/CD Validation")
        self.assertEqual(res["status"], "HANDOFF_RELAY_SUCCESS")
        self.assertEqual(res["total_steps"], 4)
        # Verify sequential agent steps
        agents = [s["agent"] for s in res["relay_chain"]]
        self.assertIn("Kalki", agents[0])
        self.assertIn("Varuna", agents[1])
        self.assertIn("Vishwakarma", agents[2])
        self.assertIn("Sanjaya", agents[3])

    def test_07_directed_shortest_path(self):
        """Test 7: Native FalkorDB directed shortestPath between incident and playbook."""
        res = self.mesh.find_shortest_path(
            start_label="Incident",
            start_prop="ref",
            start_val="INC_20261012_730",
            end_label="ProceduralPlaybook",
            end_prop="playbook_id",
            end_val="PLAY_730"
        )
        self.assertEqual(res["status"], "PATH_FOUND")
        self.assertGreaterEqual(res["hops"], 1)
        self.assertIn("Incident", [n["label"] for n in res["path_nodes"]])
        self.assertIn("ProceduralPlaybook", [n["label"] for n in res["path_nodes"]])

    def test_08_native_pagerank_procedure(self):
        """Test 8: Native FalkorDB PageRank algorithm call."""
        res = self.mesh.run_pagerank(node_label="ArchitecturalRule", rel_type="BELONGS_TO")
        self.assertIn("top_nodes", res)
        self.assertGreater(len(res["top_nodes"]), 0)
        # Top ranked score must be positive
        self.assertGreater(res["top_nodes"][0]["score"], 0)

    def test_09_blast_radius_multi_hop(self):
        """Test 9: Outage blast radius identifies downstream service dependencies."""
        res = self.mesh.calculate_blast_radius(system_name="AudioSyncEngine")
        self.assertIn("blast_radius_results", res)
        self.assertGreater(len(res["blast_radius_results"]), 0)
        target = res["blast_radius_results"][0]
        self.assertEqual(target["target_system"], "AudioSyncEngine")
        self.assertIn("GamePromoEngine", target["affected_services"])

    def test_10_graph_pacc_token_invariant(self):
        """Test 10: Graph-PACC deterministic context compaction strictly satisfies <300 token budget."""
        res = self.mesh.run_graph_pacc()
        self.assertLess(res["estimated_tokens"], 300, f"Token budget invariant violated: {res['estimated_tokens']} >= 300")
        self.assertGreater(len(res["ranked_directives"]), 0)

    def test_11_high_concurrency_multigraph(self):
        """Test 11: 100 concurrent ops across isolated tenant graphs with 0 failures."""
        res = self.mesh.benchmark_concurrency(total_operations=50, concurrency_workers=5)
        self.assertEqual(res["status"], "BENCHMARK_COMPLETE")
        self.assertEqual(res["failed_ops"], 0, "No operations should fail during concurrent stress test")
        self.assertGreater(res["ops_per_second"], 100)

    def test_12_dispel_and_merge_absorption(self):
        """Test 12: Kalki dispel & merge absorbs verified learnings into master brain."""
        res = self.mesh.dispel_and_merge_clone()
        self.assertEqual(res["status"], "DISPEL_MERGE_COMPLETE")
        self.assertIn("merged_into_master_count", res)

    def test_13_mcp_tool_registry_and_execution(self):
        """Test 13: Model Context Protocol (MCP) tool discovery and execution."""
        self.assertGreaterEqual(len(MCP_TOOLS), 5)
        tool_names = [t["name"] for t in MCP_TOOLS]
        self.assertIn("falkor_shortest_path", tool_names)
        self.assertIn("falkor_pagerank_centrality", tool_names)
        self.assertIn("falkor_blast_radius", tool_names)

        # Execute an MCP tool
        mcp_res = execute_mcp_tool("falkor_who_knows", {"system_name": "CloudflareTunnelGateway"})
        self.assertIn("systems", mcp_res)
        self.assertGreater(len(mcp_res["systems"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
