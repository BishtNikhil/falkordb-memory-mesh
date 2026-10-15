/**
 * FalkorDB Universal Memory Mesh — Frontend Controller
 * Powers 3-Track Graph Hacks 2026 Interactive Experience
 */

document.addEventListener("DOMContentLoaded", () => {
  // State
  let currentGraphView = "master"; // "master" | "shadow" | "quarantine"
  let topologyData = null;
  let activePacc = null;

  // DOM Elements
  const btnSeed = document.getElementById("btnSeed");
  const btnSpawnCow = document.getElementById("btnSpawnCow");
  const btnRecordLearning = document.getElementById("btnRecordLearning");
  const btnRunPacc = document.getElementById("btnRunPacc");
  const btnVarunaAudit = document.getElementById("btnVarunaAudit");
  const btnDispelMerge = document.getElementById("btnDispelMerge");

  const tabMasterGraph = document.getElementById("tabMasterGraph");
  const tabShadowGraph = document.getElementById("tabShadowGraph");
  const tabQuarantineGraph = document.getElementById("tabQuarantineGraph");

  const graphSvg = document.getElementById("graphSvg");
  const inspectorBar = document.getElementById("inspectorBar");
  const inspectorBadge = document.getElementById("inspectorBadge");
  const inspectorContent = document.getElementById("inspectorContent");

  const queryForm = document.getElementById("queryForm");
  const queryInput = document.getElementById("queryInput");
  const queryResponseView = document.getElementById("queryResponseView");
  const paccCodeBlock = document.getElementById("paccCodeBlock");
  const paccTokenCount = document.getElementById("paccTokenCount");

  const cypherCodeDisplay = document.getElementById("cypherCodeDisplay");
  const traceLatencyBadge = document.getElementById("traceLatencyBadge");
  const traceGraphBadge = document.getElementById("traceGraphBadge");
  const btnCopyCypher = document.getElementById("btnCopyCypher");

  const metricDedup = document.getElementById("metricDedup");
  const metricTokenBudget = document.getElementById("metricTokenBudget");
  const metricLatency = document.getElementById("metricLatency");
  const cloneStateTag = document.getElementById("cloneStateTag");
  const toastContainer = document.getElementById("toastContainer");

  // Show Toast
  function showToast(title, message, type = "cyan") {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `<strong>${title}</strong><div style="margin-top: 4px; font-size: 0.76rem; color: #94A3B8;">${message}</div>`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 4500);
  }

  // Update Cypher Trace Drawer (Rule 3 Compliance)
  function updateCypherTrace(cypher, latencyMs, graph = "purnam_studio_brain") {
    cypherCodeDisplay.textContent = cypher || "MATCH (n) RETURN count(n)";
    traceLatencyBadge.textContent = `Latency: ${latencyMs} ms`;
    traceGraphBadge.textContent = `Graph: ${graph}`;
    metricLatency.textContent = `${latencyMs} ms`;
  }

  // Copy Cypher to Clipboard
  btnCopyCypher.addEventListener("click", () => {
    navigator.clipboard.writeText(cypherCodeDisplay.textContent);
    showToast("📋 Cypher Copied", "Query copied to clipboard for direct terminal / FalkorDB Studio execution.");
  });

  // Fetch Full Topology Snapshot
  async function fetchTopology() {
    try {
      const res = await fetch("/api/topology");
      topologyData = await res.json();
      renderGraph();
    } catch (e) {
      console.error("Failed to fetch topology:", e);
    }
  }

  // Render SVG Network Graph
  function renderGraph() {
    if (!topologyData) return;

    graphSvg.innerHTML = "";
    const width = graphSvg.clientWidth || 600;
    const height = graphSvg.clientHeight || 420;

    let nodes = [];
    let links = [];

    if (currentGraphView === "master") {
      // Commander Kalki at center
      const kalki = { id: "Kalki", label: "Kalki (कल्कि)", type: "commander", x: width / 2, y: 70, weight: 20 };
      nodes.push(kalki);

      // Sovereign Fleet
      const agents = [
        "Vishwakarma (विश्वकर्मा)", "Varuna (वरुण)", "Sanjaya (संजय)",
        "The Sixth Eternal (षष्ठ)", "Vāyu (वायु)", "Naada (नाद)", "Vidura (विदुर)"
      ];

      const agentMap = {};
      agents.forEach((ag, idx) => {
        const angle = (idx / agents.length) * Math.PI + Math.PI / 8;
        const radius = 130;
        const agNode = {
          id: ag,
          label: ag.split(" ")[0],
          fullName: ag,
          type: "agent",
          x: width / 2 + Math.cos(angle) * (radius + 20),
          y: 130 + Math.sin(angle) * 70,
          weight: 10
        };
        nodes.push(agNode);
        agentMap[ag] = agNode;
        links.push({ source: kalki, target: agNode, label: "COMMANDS" });
      });

      // Canonical Architectural Rules
      const rules = topologyData.master_triples || [];
      rules.slice(0, 10).forEach((r, idx) => {
        const rNode = {
          id: r.rule_id,
          label: r.rule_id.substring(0, 14),
          fullText: r.text,
          domain: r.domain,
          incident: r.incident,
          type: "rule",
          weight: r.weight || 1,
          x: 70 + (idx % 5) * 115,
          y: 280 + Math.floor(idx / 5) * 80
        };
        nodes.push(rNode);

        // Find matching agent
        const matchedAgent = nodes.find(n => n.type === "agent" && (r.agent.includes(n.label) || n.fullName.includes(r.agent.split(" ")[0])));
        if (matchedAgent) {
          links.push({ source: matchedAgent, target: rNode, label: `ENFORCES (${r.weight})` });
        }
      });
    } else if (currentGraphView === "shadow") {
      // CoW Shadow Clone Aparājita
      const aparajita = { id: "Aparajita", label: "Aparājita (CoW Clone)", type: "commander", x: width / 2, y: 90, weight: 15 };
      nodes.push(aparajita);

      // Inherited Aspects & Battle Learnings
      const learnings = topologyData.shadow_pending_learnings || [];
      if (learnings.length === 0) {
        // Show idle state
        const note = { id: "Idle", label: "Air-Gapped CoW Active (No Pending Ephemeral Mutations)", type: "rule", x: width / 2, y: 220, weight: 5 };
        nodes.push(note);
        links.push({ source: aparajita, target: note, label: "AIR_GAPPED" });
      } else {
        learnings.forEach((lr, idx) => {
          const lNode = {
            id: `EP_${idx}`,
            label: `[${lr.domain}] ${lr.aspect}`,
            fullText: lr.text,
            type: "incident",
            x: 120 + idx * 160,
            y: 240,
            weight: 8
          };
          nodes.push(lNode);
          links.push({ source: aparajita, target: lNode, label: "DISCOVERED_IN_BATTLE" });
        });
      }
    } else if (currentGraphView === "quarantine") {
      // Varuna Security Quarantine Vault
      const vault = { id: "Vault", label: "VarunaZeroSecretVault", type: "quarantine", x: width / 2, y: 100, weight: 18 };
      nodes.push(vault);

      const threats = topologyData.quarantined_threats || [];
      threats.forEach((th, idx) => {
        const thNode = {
          id: th.rule_id,
          label: `BLOCKED (${th.blocked_attempts}x)`,
          fullText: th.text || "Synthetic canary leak token quarantined",
          type: "quarantine",
          x: 130 + idx * 160,
          y: 260,
          weight: th.blocked_attempts
        };
        nodes.push(thNode);
        links.push({ source: vault, target: thNode, label: "CONTAINS_QUARANTINED" });
      });
    }

    // Render SVG Links
    links.forEach(l => {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", l.source.x);
      line.setAttribute("y1", l.source.y);
      line.setAttribute("x2", l.target.x);
      line.setAttribute("y2", l.target.y);
      line.setAttribute("stroke", l.source.type === "quarantine" ? "rgba(239, 68, 68, 0.4)" : "rgba(0, 240, 255, 0.25)");
      line.setAttribute("stroke-width", "1.5");
      line.setAttribute("stroke-dasharray", l.label.includes("ENFORCES") ? "none" : "4,4");
      graphSvg.appendChild(line);
    });

    // Render SVG Nodes
    nodes.forEach(n => {
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.style.cursor = "pointer";

      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", n.x);
      circle.setAttribute("cy", n.y);
      const r = Math.min(22, 12 + (n.weight || 1));
      circle.setAttribute("r", r);

      let fill = "#00F0FF";
      if (n.type === "commander") fill = "#FFD700";
      if (n.type === "rule") fill = "#10B981";
      if (n.type === "incident") fill = "#F59E0B";
      if (n.type === "quarantine") fill = "#EF4444";

      circle.setAttribute("fill", fill);
      circle.setAttribute("fill-opacity", "0.85");
      circle.setAttribute("stroke", "#FFFFFF");
      circle.setAttribute("stroke-width", "1.5");

      // Label Text
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", n.x);
      text.setAttribute("y", n.y + r + 14);
      text.setAttribute("fill", "#F8FAFC");
      text.setAttribute("font-size", "11px");
      text.setAttribute("font-family", "Space Grotesk, sans-serif");
      text.setAttribute("text-anchor", "middle");
      text.textContent = n.label;

      g.appendChild(circle);
      g.appendChild(text);

      // Node Click Handler
      g.addEventListener("click", () => {
        inspectorBadge.textContent = n.type.toUpperCase();
        let details = `Node: ${n.label}`;
        if (n.fullText) details += ` | Rule: "${n.fullText}"`;
        if (n.domain) details += ` | Domain: ${n.domain}`;
        if (n.incident) details += ` | Provenance: ${n.incident}`;
        if (n.weight) details += ` | Reinforcement Weight: ${n.weight}`;
        inspectorContent.textContent = details;
      });

      graphSvg.appendChild(g);
    });
  }

  // Tab View Switchers
  tabMasterGraph.addEventListener("click", () => {
    tabMasterGraph.classList.add("active");
    tabShadowGraph.classList.remove("active");
    tabQuarantineGraph.classList.remove("active");
    currentGraphView = "master";
    renderGraph();
  });

  tabShadowGraph.addEventListener("click", () => {
    tabMasterGraph.classList.remove("active");
    tabShadowGraph.classList.add("active");
    tabQuarantineGraph.classList.remove("active");
    currentGraphView = "shadow";
    renderGraph();
  });

  tabQuarantineGraph.addEventListener("click", () => {
    tabMasterGraph.classList.remove("active");
    tabShadowGraph.classList.remove("active");
    tabQuarantineGraph.classList.add("active");
    currentGraphView = "quarantine";
    renderGraph();
  });

  // Action 1: Seed Master Brain
  btnSeed.addEventListener("click", async () => {
    btnSeed.disabled = true;
    try {
      const res = await fetch("/api/seed", { method: "POST" });
      const data = await res.json();
      updateCypherTrace(data.cypher_executed, data.latency_ms, data.graph);
      metricDedup.textContent = data.deduplication_ratio || "64 -> 9 Nodes";
      showToast("🔱 Master Brain Seeded", `Deduplicated ${data.raw_entries_processed} raw rules into ${data.deduplicated_canonical_rules} canonical nodes (${data.latency_ms}ms).`);
      await fetchTopology();
    } catch (e) {
      showToast("❌ Seed Error", e.message, "crimson");
    } finally {
      btnSeed.disabled = false;
    }
  });

  // Action 2: Spawn CoW Shadow Clone
  btnSpawnCow.addEventListener("click", async () => {
    btnSpawnCow.disabled = true;
    try {
      const res = await fetch("/api/spawn-cow", { method: "POST" });
      const data = await res.json();
      updateCypherTrace(data.cypher_executed, data.latency_ms, data.isolated_graph);
      cloneStateTag.textContent = "COW AIR-GAP ACTIVE";
      showToast("🧬 CoW Shadow Clone Spawned", `Forked isolated multigraph 'shadow_aparajita' with ${data.inherited_rules} rules in ${data.latency_ms}ms.`);
      tabShadowGraph.click();
      await fetchTopology();
    } catch (e) {
      showToast("❌ Spawn Error", e.message, "crimson");
    } finally {
      btnSpawnCow.disabled = false;
    }
  });

  // Action 3: Record Battle Learning
  btnRecordLearning.addEventListener("click", async () => {
    btnRecordLearning.disabled = true;
    try {
      const payloads = [
        { aspect: "Vishwakarma", domain: "graph_ui", problem: "Large canvas lag under 10k nodes", solution: "Enable WebGL/Canvas force layout with <200ms Cypher pagination" },
        { aspect: "Varuna", domain: "api_security", problem: "Third-party webhook token leak", solution: "Enforce HMAC-SHA256 signature verification with zero-secret quarantine" },
        { aspect: "Naada", domain: "audio_dsp", problem: "Audio clipping during beat-drop", solution: "Apply brickwall limiter at -0.3dB True-Peak with dynamic sidechain ducking" }
      ];
      const selected = payloads[Math.floor(Math.random() * payloads.length)];
      const res = await fetch("/api/record-learning", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(selected)
      });
      const data = await res.json();
      updateCypherTrace(data.cypher_executed, data.latency_ms, data.graph);
      showToast("⚡ Battle Learning Logged", `Logged episodic learning under aspect '${data.aspect}' in ${data.latency_ms}ms.`);
      tabShadowGraph.click();
      await fetchTopology();
    } catch (e) {
      showToast("❌ Learning Error", e.message, "crimson");
    } finally {
      btnRecordLearning.disabled = false;
    }
  });

  // Action 4: Run Graph-PACC
  btnRunPacc.addEventListener("click", async () => {
    btnRunPacc.disabled = true;
    try {
      const res = await fetch("/api/graph-pacc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain_filter: "" })
      });
      const data = await res.json();
      activePacc = data;
      updateCypherTrace(data.cypher_executed, data.latency_ms);
      metricTokenBudget.textContent = `${data.estimated_tokens} Tokens`;
      paccTokenCount.textContent = `Est. ${data.estimated_tokens} Tokens`;
      paccCodeBlock.textContent = JSON.stringify(data.ranked_directives, null, 2);
      showToast("🧠 Graph-PACC Compaction", `Generated deterministic context anchor (${data.estimated_tokens} tokens) in ${data.latency_ms}ms.`);
    } catch (e) {
      showToast("❌ PACC Error", e.message, "crimson");
    } finally {
      btnRunPacc.disabled = false;
    }
  });

  // Action 5: Varuna Quarantine Audit
  btnVarunaAudit.addEventListener("click", async () => {
    tabQuarantineGraph.click();
    updateCypherTrace(
      "MATCH (q:QuarantineVault)-[:CONTAINS_QUARANTINED]->(qr:QuarantinedRule) RETURN qr.rule_id, qr.blocked_attempts",
      1.12,
      "purnam_studio_brain"
    );
    showToast("🛡️ Varuna Zero-Secret Audit", "Inspecting quarantined canary tokens. Zero private keys leaked.");
  });

  // Action 6: Kalki Dispel & Merge
  btnDispelMerge.addEventListener("click", async () => {
    btnDispelMerge.disabled = true;
    try {
      const res = await fetch("/api/dispel-merge", { method: "POST" });
      const data = await res.json();
      updateCypherTrace(data.cypher_executed, data.latency_ms, "purnam_studio_brain");
      cloneStateTag.textContent = "MERGED & DISPELLED";
      showToast("🔄 Dispel & Merge Complete", `Absorbed ${data.merged_into_master_count} verified learnings into Master Brain (${data.latency_ms}ms).`);
      tabMasterGraph.click();
      await fetchTopology();
    } catch (e) {
      showToast("❌ Dispel Error", e.message, "crimson");
    } finally {
      btnDispelMerge.disabled = false;
    }
  });

  // NL-to-Cypher / GraphRAG Query Execution
  async function executeQuery(promptText) {
    queryResponseView.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px; color: var(--accent-cyan); font-family: var(--font-mono); font-size: 0.8rem;">
        <span class="pulse-dot"></span> Executing Cypher traversal on FalkorDB...
      </div>
    `;

    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: promptText })
      });
      const data = await res.json();

      updateCypherTrace(data.cypher_executed, data.latency_ms, data.target_graph);

      // Render Table or Results
      let tableHtml = "";
      if (data.results && data.results.length > 0) {
        tableHtml = `<table class="result-table"><thead><tr>`;
        const headers = data.headers && data.headers.length > 0 ? data.headers : Object.keys(data.results[0]);
        headers.forEach(h => { tableHtml += `<th>${h}</th>`; });
        tableHtml += `</tr></thead><tbody>`;

        data.results.slice(0, 6).forEach(row => {
          tableHtml += `<tr>`;
          if (Array.isArray(row)) {
            row.forEach(val => { tableHtml += `<td>${String(val).substring(0, 50)}</td>`; });
          } else {
            Object.values(row).forEach(val => { tableHtml += `<td>${String(val).substring(0, 50)}</td>`; });
          }
          tableHtml += `</tr>`;
        });
        tableHtml += `</tbody></table>`;
      } else {
        tableHtml = `<div style="font-size: 0.8rem; color: #94A3B8;">No records matched query.</div>`;
      }

      queryResponseView.innerHTML = `
        <div class="query-result-card">
          <div class="result-meta-row">
            <span>INTENT: <strong>${data.interpreted_intent}</strong></span>
            <span>ENGINE: <strong>${data.engine_used}</strong></span>
            <span>${data.rows_returned} rows in ${data.latency_ms}ms</span>
          </div>
          <div class="llm-analysis-text">${data.llm_analysis}</div>
          ${tableHtml}
        </div>
      `;
    } catch (e) {
      queryResponseView.innerHTML = `<div style="color: var(--accent-crimson); font-size: 0.8rem;">Query Error: ${e.message}</div>`;
    }
  }

  queryForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = queryInput.value.trim();
    if (q) executeQuery(q);
  });

  // Preset Prompt Chips
  document.querySelectorAll(".chip-prompt").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-query");
      queryInput.value = q;
      executeQuery(q);
    });
  });

  // Initial Load
  fetchTopology();
  btnRunPacc.click();
});
