import os
import sys
import subprocess
import json
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = r"e:\Promptwars2026\Hackathon_falkordb"
BRAIN_DIR = r"C:\Users\Saurav Bisht\.gemini\antigravity-ide\brain\9acd4efa-5a73-4be8-90f7-c8b6c0e60dd2"
AUDIO_DIR = os.path.join(WORKSPACE, "audio_processed")
BUILD_DIR = os.path.join(WORKSPACE, "video_build_v2")
FINAL_MP4 = os.path.join(WORKSPACE, "falkordb_championship_demo.mp4")

os.makedirs(BUILD_DIR, exist_ok=True)

# 1080p Resolution
W, H = 1920, 1080
FPS = 25

# Color Palette (Obsidian Glassmorphic + Electric Cyan & Gold)
DEEP_VOID = (7, 9, 14)
CYAN = (0, 240, 255)
GOLD = (255, 184, 0)
GREEN = (16, 185, 129)
ORANGE = (245, 158, 11)
WHITE = (255, 255, 255)
TEXT_MUTED = (148, 163, 184)
CARD_BG = (12, 16, 26)
BORDER_COL = (30, 41, 59)

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
FONT_CARD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
FONT_CARD_BODY = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
FONT_CAPTION_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)

# 6 Sections Definition with High-Res Native Captures & Exact Synchronized Captions
SECTIONS = [
    {
        "id": "part_1",
        "audio": os.path.join(AUDIO_DIR, "part_1_norm.wav"),
        "title": "FALKORDB UNIVERSAL MEMORY MESH — SOVEREIGN AGENT SUBSTRATE",
        "badge": "RULE 5 UNIFIED: ALL 3 TRACKS",
        "badge_color": GOLD,
        "screenshot": os.path.join(BRAIN_DIR, "master_brain_view_1792063977910.png"),
        "cards": [
            ("The Multi-Agent Crisis", "Flat JSON memory creates duplicate rule bloat, secret leaks, and zero provenance."),
            ("FalkorDB Substrate", "Sub-5ms Cypher execution on linear-algebra GraphBLAS multigraph engine.")
        ],
        "captions": [
            (0.0, 3.92, "Welcome judges to the FalkorDB Universal Memory Mesh,"),
            (3.92, 8.12, "architected for Graph Hacks 2026 across all three challenge tracks."),
            (8.12, 12.36, "When engineering autonomous multi-agent systems, the biggest bottleneck isn't the LLM;"),
            (12.36, 13.88, "it's flat JSON memory."),
            (13.88, 18.16, "Storing agent memory in flat JSON arrays causes three compounding failures:"),
            (18.16, 22.44, "duplicate rule bloat, cross-agent secret leaks, and zero causal provenance."),
            (22.44, 27.36, "We solve this by placing our sovereign agent fleet directly onto FalkorDB's"),
            (27.36, 33.91, "high-performance linear algebra substrate, turning prompt guesswork into explainable millisecond graph engineering.")
        ]
    },
    {
        "id": "part_2",
        "audio": os.path.join(AUDIO_DIR, "part_2_norm.wav"),
        "title": "TRACK 02: AGENT MEMORY & COORDINATION (PRIMARY TRACK: PS5 + GTA VI)",
        "badge": "PRIMARY TRACK 02",
        "badge_color": CYAN,
        "screenshot": os.path.join(BRAIN_DIR, "svg_topology_polished_1792063900051.png"),
        "cards": [
            ("300 DNA -> 93 Rules", "Cypher MERGE collapses 300 inputs into 93 rules in 67ms, converting repeats into edge weights."),
            ("Varuna Quarantine Vault", "18 canary leak attempts intercepted before AST parse and locked in VarunaZeroSecretVault."),
            ("CoW Ephemeral Sandbox", "shadow_aparajita forked in 25ms with 4-agent relay: Kalki -> Varuna -> Vishwakarma -> Sanjaya.")
        ],
        "captions": [
            (0.0, 5.12, "For our primary track, Track 02: Agent Memory and Coordination, watch our ingestion pipeline."),
            (5.12, 10.56, "Instead of appending duplicate JSON strings, our Cypher MERGE pipeline collapses"),
            (10.56, 16.88, "300 raw DNA inputs into 93 canonical rules in just 67 milliseconds, converting repeats into edge weights."),
            (16.88, 22.72, "Simultaneously, our security sentinel, Agent Varuna, automatically intercepts 18 synthetic"),
            (22.72, 27.60, "canary leak attempts and locks them into an isolated QuarantineVault before touching memory."),
            (27.60, 31.52, "When agents need to battle-test risky workflows,"),
            (31.52, 37.20, "FalkorDB forks an air-gapped Copy-on-Write shadow graph — shadow_aparajita — in 25 milliseconds."),
            (37.20, 42.32, "Inside the sandbox, our 4-stage handoff relay passes cryptographic state hashes"),
            (42.32, 47.36, "across Kalki, Varuna, Vishwakarma, and Sanjaya in 11 milliseconds,"),
            (47.36, 49.71, "before clean dispel and merge back into the master brain.")
        ]
    },
    {
        "id": "part_3",
        "audio": os.path.join(AUDIO_DIR, "part_3_norm.wav"),
        "title": "TRACK 01: AGENTS ACTING ON CONNECTED DATA (iPHONE 18 PRO)",
        "badge": "TRACK 01: GRAPH ALGORITHMS",
        "badge_color": GREEN,
        "screenshot": os.path.join(BRAIN_DIR, "blast_radius_result_1792059307136.png"),
        "cards": [
            ("Native C PageRank", "CALL algo.pageRank('ArchitecturalRule', 'BELONGS_TO') executes in 5.79 ms in-engine."),
            ("Directed Shortest Path", "shortestPath((Incident)-[*]->(Playbook)) locates remediation in 4.30 ms."),
            ("Graph-PACC (<300 Tokens)", "Centrality ranking compacts multi-hop rules to 196 tokens (<300t invariant).")
        ],
        "captions": [
            (0.0, 2.64, "For Track 01: Agents Acting on Connected Data,"),
            (2.64, 6.16, "FalkorDB does real algorithmic work under Rule 3."),
            (6.16, 10.96, "Clicking Native PageRank executes the in-engine C-procedure CALL algo.pageRank"),
            (10.96, 15.16, "directly in FalkorDB in 5 milliseconds to calculate structural rule authority."),
            (15.16, 19.48, "When an outage occurs, our Blast Radius tool traverses native directed shortestPath"),
            (19.48, 23.92, "from incident roots to remediation playbooks in 4 milliseconds."),
            (23.92, 29.20, "These algorithms power our Graph-PACC context engine on the right,"),
            (29.20, 33.60, "collapsing complex rule graphs into a deterministic context anchor of just 196 tokens,"),
            (33.60, 38.12, "strictly under our 300-token invariant, completely eliminating context window exhaustion.")
        ]
    },
    {
        "id": "part_4",
        "audio": os.path.join(AUDIO_DIR, "part_4_norm.wav"),
        "title": "TRACK 03: COMPANY BRAIN & PROVENANCE (M6 MAC MINI)",
        "badge": "TRACK 03: PROVENANCE",
        "badge_color": ORANGE,
        "screenshot": os.path.join(BRAIN_DIR, "query_executed_1792058334134.png"),
        "cards": [
            ("Who Knows What?", "Traverses system owners, document authors, and ticket resolvers in 3.12 ms."),
            ("Decision Provenance", "Traces RULE_730 to Jira TIK_730, Slack #war-room discussions, and incident roots."),
            ("Zero Hallucination", "Gemini Argon Multimodal NL-to-Cypher translation grounded in graph schema.")
        ],
        "captions": [
            (0.0, 4.40, "For Track 03: Company Brain, organizational knowledge is unified into a single traversable graph."),
            (4.40, 10.56, "A single Cypher query answers 'Who knows about Cloudflare Tunnel or NVENC?' in 3 milliseconds,"),
            (10.56, 15.00, "resolving system owners, specification authors, and incident ticket resolvers."),
            (15.00, 19.84, "Furthermore, our Decision Trace resolves the complete lineage of RULE_730,"),
            (19.84, 24.60, "linking the active production rule directly back to the Slack channel discussion, the Jira ticket,"),
            (24.60, 29.16, "and the originating incident root cause: zero guesswork, 100% explainable provenance.")
        ]
    },
    {
        "id": "part_5",
        "audio": os.path.join(AUDIO_DIR, "part_5_norm.wav"),
        "title": "ENTERPRISE CONCURRENCY BENCHMARK & FALKORDB WEB STUDIO",
        "badge": "1,401 OPS/SEC THROUGHPUT",
        "badge_color": GOLD,
        "screenshot": os.path.join(BRAIN_DIR, "benchmark_result_1792059370978.png"),
        "cards": [
            ("100-Op Concurrency", "100 parallel reads and writes across 3 multigraphs in 71.36 ms (1,401.44 ops/sec)."),
            ("Zero Failure Guarantee", "100% Zero-Crash compliance across master, shadow clone, and tenant sandboxes."),
            ("FalkorDB Studio (Port 3000)", "Live verification in official FalkorDB Web Studio confirms real graph execution.")
        ],
        "captions": [
            (0.0, 5.40, "To prove enterprise production readiness, our concurrency stress test executes"),
            (5.40, 11.20, "100 parallel reads and writes across 3 isolated multigraphs at over 1,400 operations per second with zero failures."),
            (11.20, 15.28, "And to verify Rule 3 compliance, here is the official FalkorDB Web Studio running live on port 3000."),
            (15.28, 20.96, "You can see our live multigraph nodes and relationships populated directly in FalkorDB's native visualizer,"),
            (20.96, 27.20, "proving that FalkorDB is actively driving the entire cognitive substrate.")
        ]
    },
    {
        "id": "part_6",
        "audio": os.path.join(AUDIO_DIR, "part_6_norm.wav"),
        "title": "RULE 10 VERIFICATION & 1-COMMAND REPRODUCTION",
        "badge": "100% PASSING & READY",
        "badge_color": GREEN,
        "screenshot": os.path.join(BRAIN_DIR, "master_brain_view_1792063977910.png"),
        "cards": [
            ("13/13 Unit Tests Passing", "tests/test_falkor_mesh.py passes 100% in 0.45s: deduplication, quarantine, and CoW."),
            ("One-Command Docker Run", "docker compose up -d launches FalkorDB and the full stack in seconds."),
            ("7 MCP Tools Exposed", "/api/mcp/tools enables autonomous agents (Gemini Argon, Claude, Cursor) to traverse graph.")
        ],
        "captions": [
            (0.0, 5.20, "Finally, our automated test suite passes 13 out of 13 tests in under half a second."),
            (5.20, 10.44, "The entire stack spins up with a single command via Docker Compose up under Rule 10,"),
            (10.44, 14.00, "exposing 7 Model Context Protocol tools for autonomous agents."),
            (14.00, 18.36, "The Universal Memory Mesh proves that when agents think with FalkorDB graphs,"),
            (18.36, 21.42, "they are faster, safer, and mathematically explainable. Thank you!")
        ]
    }
]

def get_caption_at_time(captions, t):
    for c_start, c_end, c_text in captions:
        if c_start <= t <= c_end:
            return c_text
    return ""

def render_composite_frame(sec, t_sec, shot_img):
    im = Image.new("RGB", (W, H), color=DEEP_VOID)
    
    # 1. Full-Bleed 1080p Screen Capture at 1:1 Pixel Sharpness
    if shot_img:
        # Scale smoothly without crushing
        sw, sh = shot_img.size
        # Target area: fill screen with 1:1 crisp ratio
        # Native aspect ratio: 1872x993 or 1872x1210
        scale = min(W / sw, (H - 120) / sh)
        new_w = int(sw * scale)
        new_h = int(sh * scale)
        shot_res = shot_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        pos_x = (W - new_w) // 2
        pos_y = 50 + ((H - 120) - new_h) // 2
        im.paste(shot_res, (pos_x, pos_y))

    draw = ImageDraw.Draw(im)

    # 2. Sleek Translucent Top HUD (50px height)
    draw.rectangle([(0, 0), (W, 50)], fill=(7, 9, 14, 230))
    draw.line([(0, 50), (W, 50)], fill=BORDER_COL, width=1)
    
    # Live Indicator dot
    draw.ellipse([(25, 18), (37, 30)], fill=GREEN)
    draw.text((45, 12), sec["title"], font=FONT_TITLE, fill=CYAN)

    # Top-right Badge
    b_text = sec["badge"]
    b_bbox = draw.textbbox((0, 0), b_text, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 24
    bx = W - 30 - bw
    draw.rounded_rectangle([(bx, 10), (bx + bw, 40)], radius=5, fill=(16, 22, 34), outline=sec["badge_color"], width=1)
    draw.text((bx + 12, 13), b_text, font=FONT_BADGE, fill=sec["badge_color"])

    # 3. Floating Telemetry Card (Top-right unobtrusive glass card)
    if sec["cards"]:
        card_w = 460
        card_x = W - card_w - 25
        card_y = 65
        
        # Draw 1 or 2 high-signal highlight badges
        c_title, c_desc = sec["cards"][0]
        c_h = 70
        draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + c_h)], radius=6, fill=(10, 14, 22, 225), outline=CYAN, width=1)
        draw.text((card_x + 14, card_y + 8), c_title.upper(), font=FONT_CARD_TITLE, fill=GOLD)
        draw.text((card_x + 14, card_y + 36), c_desc[:65] + ("..." if len(c_desc) > 65 else ""), font=FONT_CARD_BODY, fill=WHITE)

    # 4. Synchronized Caption Bar (Bottom Center)
    cap_text = get_caption_at_time(sec["captions"], t_sec)
    if cap_text:
        cap_box = draw.textbbox((0, 0), cap_text, font=FONT_CAPTION_BOLD)
        cw = cap_box[2] - cap_box[0] + 48
        ch = 54
        cx = (W - cw) // 2
        cy = H - 95
        
        # Translucent dark pill box with cyan border
        draw.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=8, fill=(4, 6, 10, 240), outline=CYAN, width=2)
        # Drop shadow for text
        draw.text((cx + 25, cy + 12), cap_text, font=FONT_CAPTION_BOLD, fill=(0, 0, 0))
        draw.text((cx + 24, cy + 11), cap_text, font=FONT_CAPTION_BOLD, fill=WHITE)

    return im

def build_championship_video():
    print("\n" + "="*70)
    print("🎬 RENDERING CRYSTAL-CLEAR CHAMPIONSHIP VIDEO V2 WITH USER VOICEOVER")
    print("="*70)

    seg_mp4s = []
    total_sec = 0.0

    for idx, sec in enumerate(SECTIONS, 1):
        sec_id = sec["id"]
        wav_path = sec["audio"]
        
        # Probe exact duration of normalized audio
        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_path]
        duration = float(subprocess.check_output(dur_cmd).decode().strip())
        total_sec += duration
        
        print(f"\n[Part {idx}/6] {sec['title']}")
        print(f"  Duration: {duration:.2f}s | Audio: {os.path.basename(wav_path)}")
        
        # Preload screenshot
        shot_img = None
        if os.path.exists(sec["screenshot"]):
            shot_img = Image.open(sec["screenshot"])
            print(f"  Loaded Native Screenshot: {os.path.basename(sec['screenshot'])} ({shot_img.size})")

        # Render video segment using FFmpeg image2pipe for maximum speed & quality
        seg_mp4 = os.path.join(BUILD_DIR, f"{sec_id}.mp4")
        
        # FFmpeg command feeding raw video frames from Python pipe directly into H.264
        cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{W}x{H}",
            "-pix_fmt", "rgb24",
            "-r", str(FPS),
            "-i", "-",  # pipe from python
            "-i", wav_path,  # user audio
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",  # visually lossless
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "256k",
            "-shortest",
            seg_mp4
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        total_frames = int(duration * FPS)
        print(f"  Rendering {total_frames} frames ({FPS} fps)...")
        
        for f_idx in range(total_frames):
            t_curr = f_idx / FPS
            frame = render_composite_frame(sec, t_curr, shot_img)
            proc.stdin.write(frame.tobytes())

        proc.stdin.close()
        proc.wait()
        
        seg_mp4s.append(seg_mp4)
        print(f"  [OK] Segment ready: {os.path.basename(seg_mp4)} ({os.path.getsize(seg_mp4) // 1024} KB)")

    # Concatenate all 6 segments
    print("\n" + "-"*70)
    print("Concatenating all 6 segments into final video...")
    concat_txt = os.path.join(BUILD_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        for s in seg_mp4s:
            f.write(f"file '{s.replace(chr(92), '/')}'\n")

    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        FINAL_MP4
    ]
    subprocess.run(concat_cmd, check=True)

    final_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    mins = int(total_sec // 60)
    secs = int(total_sec % 60)

    print("\n" + "="*70)
    print("🏆 FINAL CHAMPIONSHIP DEMO VIDEO WITH USER VOICEOVER COMPLETE!")
    print("="*70)
    print(f"Output Video: {FINAL_MP4}")
    print(f"Duration: {mins}m {secs:02d}s ({total_sec:.2f} seconds)")
    print(f"File Size: {final_size_mb:.2f} MB")
    print(f"Resolution: 1920x1080 Full HD (Crisp, Lossless CRF 18)")
    print(f"Audio: User Voiceover Normalized to EBU R128 (-16 LUFS)")
    print(f"Captions: Synchronized Open Captions with Pure Precision\n")

if __name__ == "__main__":
    build_championship_video()
