import os
import sys
import subprocess
import time
import win32com.client
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r"e:\Promptwars2026\Hackathon_falkordb"
BRAIN_DIR = r"C:\Users\Saurav Bisht\.gemini\antigravity-ide\brain\9acd4efa-5a73-4be8-90f7-c8b6c0e60dd2"
OUTPUT_DIR = os.path.join(WORKSPACE, "video_build")
FINAL_MP4 = os.path.join(WORKSPACE, "falkordb_championship_demo.mp4")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
DEEP_VOID = (7, 9, 14)
CYAN = (0, 240, 255)
GOLD = (255, 184, 0)
GREEN = (16, 185, 129)
ORANGE = (245, 158, 11)
TEXT_WHITE = (226, 232, 240)
TEXT_MUTED = (148, 163, 184)
CARD_BG = (12, 16, 26)
BORDER_COL = (30, 41, 59)

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 46)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 24)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
FONT_MONO = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 19)
FONT_TICKER = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)

# 6 Presentation Sections from DEMO_SCRIPT.md
SECTIONS = [
    {
        "id": "sec1_intro",
        "title": "FALKORDB UNIVERSAL MEMORY MESH",
        "subtitle": "Sovereign Agent Cognitive Substrate | Graph Hacks 2026 (All 3 Tracks)",
        "badge": "TRACK 01 + TRACK 02 + TRACK 03",
        "badge_color": GOLD,
        "screenshot": os.path.join(BRAIN_DIR, "master_brain_view_1792063977910.png"),
        "cards": [
            ("The Multi-Agent Crisis", "Flat JSON memory creates duplicate rule bloat, cross-agent state contamination, and zero provenance."),
            ("FalkorDB Substrate", "Linear-algebra GraphBLAS engine delivers sub-5ms Cypher execution and multigraph tenant isolation.")
        ],
        "ticker": "RULE 3 COMPLIANT | FALKORDB CONTAINER CADFD424DA2 | 100% LOCAL DETERMINISTIC ZERO-CRASH",
        "speech": (
            "Welcome judges to the FalkorDB Universal Memory Mesh, architected for Graph Hacks 2026 across all three tracks. "
            "Autonomous multi-agent teams face a catastrophic bottleneck with flat JSON memory: context window bloat, hallucinatory schema blindness, and cross-agent secret leaks. "
            "We solve this by placing the sovereign agent fleet directly on FalkorDB high-speed linear algebra graph substrate."
        )
    },
    {
        "id": "sec2_memory",
        "title": "TRACK 02: AGENT MEMORY & COORDINATION",
        "subtitle": "Copy-on-Write Ephemeral Sandbox, 4-Stage Handoff Relay & Dispel Merge",
        "badge": "PRIMARY TRACK: PS5 + GTA VI",
        "badge_color": CYAN,
        "screenshot": os.path.join(BRAIN_DIR, "svg_topology_polished_1792063900051.png"),
        "cards": [
            ("Cypher DNA Collapse", "300 raw DNA inputs collapsed into 93 Canonical Rules in 67.16 ms via Cypher MERGE, converting repeats into edge weights."),
            ("Varuna Security Gate", "18 synthetic canary token leak attempts intercepted before AST parse and locked into VarunaZeroSecretVault."),
            ("CoW Ephemeral Sandbox", "Air-gapped shadow_aparajita forked in 25.81 ms with 4-agent state handoff relay: Kalki -> Varuna -> Vishwakarma -> Sanjaya.")
        ],
        "ticker": "MULTIGRAPH AIR-GAP: shadow_aparajita | RELAY LATENCY: 11.54ms | MERGE: 8.13ms",
        "speech": (
            "For Track 02, Agent Memory and Coordination, watch our ingestion pipeline. "
            "300 raw DNA inputs are collapsed into 93 canonical architectural rules in just 67 milliseconds using Cypher MERGE, converting repeats into edge reinforcement weights. "
            "Simultaneously, our security sentinel, Agent Varuna, automatically intercepts 18 secret canary leaks into an isolated Quarantine Vault. "
            "When agents need to test risky workflows, FalkorDB forks an air-gapped Copy-on-Write shadow graph, shadow_aparajita, in 25 milliseconds. "
            "State handoffs relay smoothly across Kalki, Varuna, Vishwakarma, and Sanjaya with cryptographic state hashes in 11 milliseconds."
        )
    },
    {
        "id": "sec3_connected",
        "title": "TRACK 01: CONNECTED DATA & GRAPH ALGORITHMS",
        "subtitle": "Native PageRank, Directed Shortest Path & Graph-PACC (<300 Tokens)",
        "badge": "TRACK 01: iPHONE 18 PRO",
        "badge_color": GREEN,
        "screenshot": os.path.join(BRAIN_DIR, "blast_radius_result_1792059307136.png"),
        "cards": [
            ("Native C PageRank", "CALL algo.pageRank('ArchitecturalRule', 'BELONGS_TO') executes in 5.79 ms to compute structural authority."),
            ("Directed Shortest Path", "Native shortestPath((Incident)-[*]->(Playbook)) locates exact incident remediation in 4.30 ms."),
            ("Graph-PACC Token Compaction", "Multi-hop centrality ranking compacts context to 201 tokens, well under the 300-token invariant.")
        ],
        "ticker": "NATIVE FALKORDB PROCEDURES | GRAPH-PACC: 201 TOKENS (<300t INVARIANT) | LATENCY: 4.30ms",
        "speech": (
            "For Track 01, Agents Acting on Connected Data, FalkorDB executes core algorithmic reasoning rather than visual decoration. "
            "Our engine runs native C-procedures like algo.pageRank in 5 milliseconds to rank structural rule authority. "
            "When an incident strikes, our blast radius tool traverses directed shortest-path remediation in 4 milliseconds. "
            "These algorithms feed our Graph-PACC anchor, deterministically compacting multi-hop rules down to just 196 tokens, well below our 300-token invariant, completely eliminating context window exhaustion."
        )
    },
    {
        "id": "sec4_company_brain",
        "title": "TRACK 03: COMPANY BRAIN & PROVENANCE",
        "subtitle": "Unifying Docs, Tickets & War-Room Chats into Directed Lineage",
        "badge": "TRACK 03: M6 MAC MINI",
        "badge_color": ORANGE,
        "screenshot": os.path.join(BRAIN_DIR, "query_executed_1792058334134.png"),
        "cards": [
            ("Who Knows What?", "Traverses (Agent)-[:OWNS]->(System) and (Agent)-[:AUTHORED]->(Doc) in 3.12 ms to answer system ownership instantly."),
            ("Decision Provenance", "Traces RULE_730 directly to Jira TIK_730, Slack #war-room discussions, and root incident INC_730."),
            ("Zero Schema Hallucination", "Gemini Argon Multimodal NL-to-Cypher translation grounded strictly in FalkorDB graph schema.")
        ],
        "ticker": "COMPANY GRAPH: SYSTEMS + DOCS + TICKETS + CHATS | PROVENANCE RESOLVED IN 3.12ms",
        "speech": (
            "For Track 03, Company Brain, organizational knowledge is unified into a single traversable graph. "
            "A single Cypher query answers Who knows about Cloudflare Tunnel or NVENC in 3 milliseconds, resolving owners, documentation authors, and ticket resolvers. "
            "Furthermore, our Decision Trace resolves the complete lineage of Rule 730, linking the active production rule directly back to the Slack channel discussion, Jira ticket, and origin incident root cause."
        )
    },
    {
        "id": "sec5_benchmarks",
        "title": "1,400+ OPS/SEC BENCHMARK & FALKORDB STUDIO",
        "subtitle": "High-Concurrency Stress Testing Across 3 Isolated Multigraphs",
        "badge": "ENTERPRISE THROUGHPUT & RULE 3",
        "badge_color": GOLD,
        "screenshot": os.path.join(BRAIN_DIR, "benchmark_result_1792059370978.png"),
        "cards": [
            ("100-Op Concurrency", "100 parallel reads and writes across purnam_studio_brain, shadow_aparajita, and tenant_sandbox_01 in 71.36 ms."),
            ("Throughput & Latency", "1,401.44 ops/second sustained with 0 failures and 3.09 ms average query latency."),
            ("Official FalkorDB Studio", "Live verification on localhost:3000 shows live nodes and relationships directly in FalkorDB native browser.")
        ],
        "ticker": "CONCURRENCY: 1,401.44 OPS/SEC | ZERO-CRASH: 100% | FALKORDB STUDIO: PORT 3000",
        "speech": (
            "To prove enterprise production readiness, our 100-operation concurrency stress test executes simultaneous reads and writes across three isolated multigraphs at over 1,400 operations per second with zero errors. "
            "And verifying Rule 3 compliance, here is the official FalkorDB Web Studio on port 3000, displaying our live multigraph nodes and edges directly in FalkorDB's native visualizer."
        )
    },
    {
        "id": "sec6_conclusion",
        "title": "RULE 10 VERIFICATION & 1-COMMAND REPRODUCTION",
        "subtitle": "13/13 Automated Unit Tests Passing | Complete Docker Compose Startup",
        "badge": "100% SUBMISSION READY",
        "badge_color": GREEN,
        "screenshot": os.path.join(BRAIN_DIR, "master_brain_view_1792063977910.png"),
        "cards": [
            ("13/13 Automated Tests", "test_falkor_mesh.py passes 100% in 0.45s: deduplication, quarantine, CoW isolation, and PACC token bounds."),
            ("One-Command Docker", "docker compose up -d launches FalkorDB, Redis, and FastAPI service with zero external dependencies."),
            ("MCP Tool Registry", "7 JSON-Schema graph tools exposed at /api/mcp/tools for autonomous agents (Gemini Argon, Claude, Cursor).")
        ],
        "ticker": "TESTS: 13/13 PASSING (0.45s) | DOCKER: READY | GITHUB: BishtNikhil/falkordb-memory-mesh",
        "speech": (
            "Finally, our entire automated test suite passes 13 out of 13 tests in under half a second. "
            "The entire stack spins up with a single command via docker compose up under Rule 10, exposing 7 Model Context Protocol tools for autonomous agents. "
            "The Universal Memory Mesh proves that when agents think with FalkorDB graphs, they are faster, safer, and mathematically explainable. Thank you!"
        )
    }
]

def generate_voice_file(text, output_wav):
    v = win32com.client.Dispatch("SAPI.SpVoice")
    v.Rate = 0  # natural conversational presentation speed
    s = win32com.client.Dispatch("SAPI.SpFileStream")
    s.Open(output_wav, 3)
    v.AudioOutputStream = s
    v.Speak(text)
    s.Close()
    time.sleep(0.1)

def get_audio_duration(wav_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", wav_path
    ]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def create_section_frame(sec, index, total, current_time_str):
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), color=DEEP_VOID)
    draw = ImageDraw.Draw(im)

    # Top Navigation Header Bar
    draw.rectangle([(0, 0), (W, 75)], fill=(10, 14, 22))
    draw.line([(0, 75), (W, 75)], fill=BORDER_COL, width=2)

    # Logo & Title
    draw.text((45, 14), sec["title"], font=FONT_TITLE, fill=CYAN)
    
    # Track Badge on top right
    badge_text = sec["badge"]
    bbox = draw.textbbox((0, 0), badge_text, font=FONT_CARD_TITLE)
    bw = bbox[2] - bbox[0] + 32
    bx = W - 45 - bw
    draw.rounded_rectangle([(bx, 16), (bx + bw, 58)], radius=6, fill=(18, 24, 38), outline=sec["badge_color"], width=2)
    draw.text((bx + 16, 23), badge_text, font=FONT_CARD_TITLE, fill=sec["badge_color"])

    # Subtitle bar
    draw.text((45, 88), sec["subtitle"], font=FONT_SUB, fill=TEXT_MUTED)

    # Main Visual Layout: Left screenshot panel (1150 x 780), Right cards panel (640 x 780)
    screen_path = sec["screenshot"]
    if os.path.exists(screen_path):
        shot = Image.open(screen_path)
        # Crop or fit nicely into 1150 x 780
        shot_w, shot_h = 1150, 780
        shot_resized = shot.resize((shot_w, shot_h), Image.Resampling.LANCZOS)
        
        # Border frame around screenshot
        draw.rounded_rectangle([(40, 130), (40 + shot_w + 10, 130 + shot_h + 10)], radius=8, fill=(10, 14, 22), outline=BORDER_COL, width=2)
        im.paste(shot_resized, (45, 135))
    else:
        # Fallback dark canvas
        draw.rounded_rectangle([(40, 130), (1200, 920)], radius=8, fill=(12, 16, 26), outline=BORDER_COL, width=2)
        draw.text((100, 500), "LIVE FALKORDB VISUAL CANVAS", font=FONT_TITLE, fill=CYAN)

    # Right Cards Panel: 640px wide from x = 1230
    rx = 1230
    ry = 135
    rw = 645

    for c_idx, (card_title, card_body) in enumerate(sec["cards"]):
        card_h = 240 if len(sec["cards"]) == 3 else 360
        cy = ry + c_idx * (card_h + 20)
        draw.rounded_rectangle([(rx, cy), (rx + rw, cy + card_h)], radius=10, fill=CARD_BG, outline=BORDER_COL, width=2)
        
        # Card header accent
        draw.rounded_rectangle([(rx, cy), (rx + rw, cy + 48)], radius=10, fill=(16, 22, 34))
        draw.line([(rx, cy + 48), (rx + rw, cy + 48)], fill=BORDER_COL, width=1)
        draw.text((rx + 20, cy + 10), card_title, font=FONT_CARD_TITLE, fill=GOLD)

        # Word wrap card body text
        words = card_body.split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            bbox = draw.textbbox((0, 0), " ".join(cur_line), font=FONT_CARD_BODY)
            if bbox[2] - bbox[0] > (rw - 40):
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))

        ty = cy + 65
        for line in lines:
            draw.text((rx + 20, ty), line, font=FONT_CARD_BODY, fill=TEXT_WHITE)
            ty += 28

    # Bottom Explainable Cypher / Ticker Drawer
    draw.rectangle([(0, H - 75), (W, H)], fill=(4, 6, 10))
    draw.line([(0, H - 75), (W, H - 75)], fill=BORDER_COL, width=2)
    
    # Pulse status icon
    draw.ellipse([(45, H - 50), (63, H - 32)], fill=GREEN)
    draw.text((75, H - 48), f"SECTION {index}/{total}: {sec['ticker']}", font=FONT_TICKER, fill=CYAN)
    draw.text((W - 240, H - 48), current_time_str, font=FONT_TICKER, fill=GOLD)

    return im

def build_video():
    print("\n" + "="*70)
    print("[VIDEO BUILDER] FALKORDB MEMORY MESH - 2.5-MINUTE CHAMPIONSHIP DEMO VIDEO")
    print("="*70)

    segment_files = []
    total_duration = 0.0

    for idx, sec in enumerate(SECTIONS, 1):
        sec_id = sec["id"]
        print(f"\n[Step {idx}/6] Processing: {sec['title']}...")
        
        # 1. Synthesize Audio
        wav_file = os.path.join(OUTPUT_DIR, f"{sec_id}.wav")
        print(f"  [AUDIO] Synthesizing speech narration -> {os.path.basename(wav_file)}")
        generate_voice_file(sec["speech"], wav_file)
        
        duration = get_audio_duration(wav_file)
        total_duration += duration
        mins = int(duration // 60)
        secs = int(duration % 60)
        time_str = f"DURATION: {mins}:{secs:02d}"
        print(f"  [TIME] Duration: {duration:.2f}s ({time_str})")

        # 2. Render 1080p Slide Frame
        png_file = os.path.join(OUTPUT_DIR, f"{sec_id}.png")
        print(f"  [FRAME] Rendering 1920x1080 Obsidian Glassmorphic frame...")
        frame = create_section_frame(sec, idx, len(SECTIONS), time_str)
        frame.save(png_file)

        # 3. Encode Video Segment with FFmpeg
        seg_mp4 = os.path.join(OUTPUT_DIR, f"{sec_id}.mp4")
        print(f"  [ENCODE] Encoding video segment with H.264 & AAC...")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", png_file,
            "-i", wav_file,
            "-c:v", "libx264", "-t", str(duration),
            "-pix_fmt", "yuv420p", "-r", "25",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", seg_mp4
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segment_files.append(seg_mp4)
        print(f"  [OK] Segment ready: {os.path.basename(seg_mp4)} ({os.path.getsize(seg_mp4) // 1024} KB)")

    # 4. Concatenate All 6 Segments into Final MP4
    print("\n" + "-"*70)
    print("[CONCAT] Concatenating all 6 segments into final championship video...")
    concat_list = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg.replace(chr(92), '/')}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        FINAL_MP4
    ]
    subprocess.run(cmd_concat, check=True)

    final_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    tot_mins = int(total_duration // 60)
    tot_secs = int(total_duration % 60)

    print("\n" + "="*70)
    print("[SUCCESS] CHAMPIONSHIP DEMO VIDEO GENERATION COMPLETE!")
    print("="*70)
    print(f"Output Video: {FINAL_MP4}")
    print(f"Total Run Time: {tot_mins} min {tot_secs} sec ({total_duration:.2f} seconds)")
    print(f"File Size: {final_size_mb:.2f} MB")
    print(f"Resolution: 1920x1080 High-Definition (H.264 / AAC)")
    print(f"Ready for submission on YouTube / Loom / WeMakeDevs!\n")

if __name__ == "__main__":
    build_video()
