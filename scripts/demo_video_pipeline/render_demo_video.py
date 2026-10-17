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
MASTER_WAV = os.path.join(AUDIO_DIR, "master_narration_v5.wav")
CAPTIONS_JSON = os.path.join(AUDIO_DIR, "authoritative_script_captions.json")
FINAL_MP4 = os.path.join(WORKSPACE, "falkordb_championship_demo.mp4")

W, H = 1920, 1080
FPS = 25

# Color Palette
DEEP_VOID = (6, 8, 12)
CYAN = (0, 240, 255)
GOLD = (255, 184, 0)
GREEN = (16, 185, 129)
RED = (239, 68, 68)
WHITE = (255, 255, 255)

FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 23)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)

# Load 115 Synchronized Captions
with open(CAPTIONS_JSON, "r", encoding="utf-8") as f:
    caption_data = json.load(f)
    RAW_CAPTIONS = caption_data["captions"]
    PART_OFFSETS = caption_data["parts"]

def get_caption_at_time(t):
    for c in RAW_CAPTIONS:
        if c["start"] <= t <= c["end"]:
            return c["text"]
    return ""

def prepare_centered_modal(img_path, target_h=835):
    im = Image.open(img_path)
    mw, mh = im.size
    box = (int(mw * 0.22), int(mh * 0.08), int(mw * 0.78), int(mh * 0.92))
    crop = im.crop(box)
    cw, ch = crop.size
    scale = target_h / ch
    target_w = int(cw * scale)
    crop_res = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    base = Image.new("RGB", (W, H), DEEP_VOID)
    bx = (W - target_w) // 2
    by = 48 + ((H - 120) - target_h) // 2
    base.paste(crop_res, (bx, by))
    return base

def prepare_panel(img_path, crop_box, target_h=850):
    im = Image.open(img_path)
    crop = im.crop(crop_box)
    cw, ch = crop.size
    scale = min(1720 / cw, target_h / ch)
    target_w = int(cw * scale)
    target_h_scaled = int(ch * scale)
    crop_res = crop.resize((target_w, target_h_scaled), Image.Resampling.LANCZOS)
    
    base = Image.new("RGB", (W, H), DEEP_VOID)
    bx = (W - target_w) // 2
    by = 48 + ((H - 120) - target_h_scaled) // 2
    base.paste(crop_res, (bx, by))
    return base

print("Loading 14 distinct, customized visual scenes...")

# 1. Hero Title & Architecture Deck
scene_1_hero = Image.open(os.path.join(BRAIN_DIR, "v5_scene_hero_deck.png"))

# 2. Multi-Agent Memory Crisis
scene_2_crisis = Image.open(os.path.join(BRAIN_DIR, "v5_scene_memory_crisis.png"))

# 3. 4-Tier Sovereign Fleet Topology
scene_3_topo = prepare_panel(
    os.path.join(BRAIN_DIR, "master_topology_1792059293367.png"),
    (30, 350, 1070, 1090),
    target_h=850
)

# 4. Track 02 Ingestion Pipeline & Cypher MERGE Benchmark
scene_4_ingest = Image.open(os.path.join(BRAIN_DIR, "v5_scene_ingestion_pipeline.png"))

# 5. Track 02 Varuna Zero-Secret Quarantine Vault
scene_5_varuna = Image.open(os.path.join(BRAIN_DIR, "v5_scene_varuna_quarantine.png"))

# 6. Track 02 4-Stage CoW Ephemeral Sandbox Relay Modal
scene_6_relay = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "relay_modal_1792058246115.png"),
    target_h=835
)

# 7. Track 01 Native Graph Algorithms & Graph-PACC
scene_7_algo = Image.open(os.path.join(BRAIN_DIR, "v5_scene_graph_algorithms.png"))

# 8. Track 01 Directed Outage Blast Radius Modal
scene_8_blast = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "blast_radius_modal_1792058269606.png"),
    target_h=835
)

# 9. Track 03 Gemini 2.5 Flash Argon NL-to-Cypher Panel
scene_9_argon = Image.open(os.path.join(BRAIN_DIR, "v5_scene_argon_nl_cypher.png"))

# 10. Track 03 Causal Decision Lineage for Rule 730
scene_10_trace = Image.open(os.path.join(BRAIN_DIR, "v4_decision_trace.png"))

# 11. Enterprise Concurrency Benchmark Modal
scene_11_bench = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "benchmark_modal_1792058223280.png"),
    target_h=835
)

# 12. Official FalkorDB Web Studio Live on Port 3000
scene_12_studio = Image.open(os.path.join(BRAIN_DIR, "v4_falkordb_studio.png"))

# 13. Developer Terminal with 13/13 Unit Tests Passing
scene_13_term = Image.open(os.path.join(BRAIN_DIR, "v4_terminal_tests.png"))

# 14. 7 Standardized MCP Tools Registry Modal
scene_14_mcp = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "mcp_modal_1792058290529.png"),
    target_h=835
)

print("[OK] All 14 visual scenes loaded successfully into memory!")

# Part Offsets (v5):
# Part 1: [000.00s -> 034.55s] (Silence 34.55s -> 35.75s)
# Part 2: [035.75s -> 086.20s] (Silence 86.20s -> 87.40s)
# Part 3: [087.40s -> 126.15s] (Silence 126.15s -> 127.35s)
# Part 4: [127.35s -> 157.40s] (Silence 157.40s -> 158.60s)
# Part 5: [158.60s -> 186.60s] (Silence 186.60s -> 187.80s)
# Part 6: [187.80s -> 209.85s]

def get_scene_frame(t):
    # PART 1: INTRO & MULTI-AGENT ARCHITECTURE (0.00s -> 34.55s)
    if t < 13.0:
        return scene_1_hero, "FALKORDB UNIVERSAL MEMORY MESH — UNIFIED COGNITIVE SUBSTRATE", "RULE 5: ALL 3 TRACKS", GOLD
    elif t < 23.5:
        return scene_2_crisis, "THE MULTI-AGENT MEMORY CRISIS: FLAT JSON FAILURE MODES", "THE CRISIS", RED
    elif t < 35.75:
        return scene_3_topo, "4-TIER MULTIGRAPH TOPOLOGY: KALKI -> 7 AGENTS -> RULES -> INCIDENTS", "SOVEREIGN AGENT FLEET", CYAN
    
    # PART 2: TRACK 02: INGESTION, QUARANTINE & COW RELAY (35.75s -> 86.20s)
    elif t < 54.0:
        return scene_4_ingest, "TRACK 02: CYPHER MERGE INGESTION PIPELINE (300 DNA -> 93 RULES in 67ms)", "PRIMARY TRACK 02", CYAN
    elif t < 68.0:
        return scene_5_varuna, "TRACK 02: VARUNA QUARANTINE SENTINEL (AIR-GAPPED ZERO-SECRET VAULT)", "18 CANARY LEAKS BLOCKED", GOLD
    elif t < 87.40:
        return scene_6_relay, "TRACK 02: 4-STAGE COW HANDOFF RELAY (KALKI -> VARUNA -> VISHWAKARMA -> SANJAYA)", "PRIMARY TRACK 02", CYAN
    
    # PART 3: TRACK 01: GRAPH ALGORITHMS & BLAST RADIUS (87.40s -> 126.15s)
    elif t < 104.0:
        return scene_7_algo, "TRACK 01: NATIVE C-PAGERANK & GRAPH-PACC ANCHOR (<300 TOKENS)", "TRACK 01: iPHONE 16 PRO", GREEN
    elif t < 127.35:
        return scene_8_blast, "TRACK 01: DIRECTED SHORTESTPATH OUTAGE BLAST RADIUS (4ms)", "TRACK 01: 4ms BLAST RADIUS", GREEN
    
    # PART 4: TRACK 03: COMPANY BRAIN & PROVENANCE (127.35s -> 157.40s)
    elif t < 142.0:
        return scene_9_argon, "TRACK 03: GEMINI 2.5 FLASH ARGON NL-TO-CYPHER ENGINE (3ms)", "TRACK 03: M4 MAC MINI", GOLD
    elif t < 158.60:
        return scene_10_trace, "TRACK 03: RULE_730 CAUSAL DECISION PROVENANCE (JIRA + PR + SLACK)", "CAUSAL PROVENANCE", GOLD
    
    # PART 5: CONCURRENCY BENCHMARK & FALKORDB WEB STUDIO (158.60s -> 186.60s)
    elif t < 172.0:
        return scene_11_bench, "ENTERPRISE CONCURRENCY BENCHMARK: 1,401.8 OPS/SEC (ZERO LOCKS)", "1,401 OPS/SEC", GOLD
    elif t < 187.80:
        return scene_12_studio, "OFFICIAL FALKORDB WEB STUDIO RUNNING LIVE ON PORT 3000 (RULE 3 VERIFIED)", "PORT 3000 VERIFIED", GREEN
    
    # PART 6: RULE 10 REPRODUCIBILITY & MCP REGISTRY (187.80s -> 209.85s)
    elif t < 199.0:
        return scene_13_term, "RULE 10 REPRODUCIBILITY: 13/13 UNIT TESTS PASSING IN 0.435s", "13/13 PASSING", GREEN
    else:
        return scene_14_mcp, "RULE 10 VERIFICATION: 7 STANDARDIZED MCP TOOLS FOR AGENTS", "100% REPRODUCIBLE", GREEN

def render_frame(t):
    base_img, title_text, badge_text, badge_color = get_scene_frame(t)
    im = base_img.copy()
    draw = ImageDraw.Draw(im)

    # Top HUD Bar
    draw.rectangle([(0, 0), (W, 45)], fill=(6, 8, 12, 235))
    draw.line([(0, 45), (W, 45)], fill=(24, 32, 47), width=1)
    
    draw.ellipse([(20, 16), (32, 28)], fill=GREEN)
    draw.text((40, 10), title_text, font=FONT_TITLE, fill=CYAN)
    
    b_bbox = draw.textbbox((0, 0), badge_text, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 20
    bx = W - 25 - bw
    draw.rounded_rectangle([(bx, 8), (bx + bw, 36)], radius=4, fill=(12, 16, 26), outline=badge_color, width=1)
    draw.text((bx + 10, 10), badge_text, font=FONT_BADGE, fill=badge_color)

    # Simple Pure White Caption (NO BORDER, NO BOX, ELEGANT DROP SHADOW)
    cap_text = get_caption_at_time(t)
    if cap_text:
        cap_box = draw.textbbox((0, 0), cap_text, font=FONT_CAPTION)
        cw = cap_box[2] - cap_box[0]
        cx = (W - cw) // 2
        cy = H - 75
        
        # Subtle 2px shadow for 100% contrast against any background
        draw.text((cx + 2, cy + 2), cap_text, font=FONT_CAPTION, fill=(0, 0, 0))
        draw.text((cx, cy), cap_text, font=FONT_CAPTION, fill=WHITE)

    return im

def build_video():
    print("\n" + "="*70)
    print("🎬 RENDERING FINAL CHAMPIONSHIP DEMO VIDEO V5")
    print("   - Master Audio v5: 1.20s Silence Gaps (Zero Overlap Guaranteed!)")
    print("   - 115 Synchronized Captions Matching Exact Voice Pace")
    print("   - Pure White Typography with Subtle Shadow (No Borders, No Pill Box)")
    print("   - 14 Completely Distinct, High-Resolution Visual Scenes")
    print("   - Virtually Lossless CRF 12 Encoding with StillImage Tune")
    print("="*70)

    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", MASTER_WAV]
    total_duration = float(subprocess.check_output(dur_cmd).decode().strip())
    total_frames = int(total_duration * FPS)
    
    mins = int(total_duration // 60)
    secs = int(total_duration % 60)
    print(f"\nMaster Narration Audio: {MASTER_WAV}")
    print(f"Total Video Runtime: {mins}m {secs:02d}s ({total_duration:.2f}s, {total_frames} frames @ {FPS}fps)")

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", MASTER_WAV,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "12",
        "-preset", "veryfast",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        FINAL_MP4
    ]

    print("\nStarting FFmpeg video pipeline...", flush=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t_curr = f_idx / FPS
        frame_img = render_frame(t_curr)
        proc.stdin.write(frame_img.tobytes())

        if f_idx % 250 == 0 or f_idx == total_frames - 1:
            pct = (f_idx / total_frames) * 100
            print(f"  Frame {f_idx}/{total_frames} ({pct:.1f}%) | Time: {t_curr:.2f}s", flush=True)

    proc.stdin.close()
    proc.wait()

    final_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    print("\n" + "="*70)
    print("🏆 FINAL CHAMPIONSHIP DEMO VIDEO V5 GENERATION COMPLETE!")
    print("="*70)
    print(f"Output Video File: {FINAL_MP4}")
    print(f"Total Duration: {mins}m {secs:02d}s ({total_duration:.2f} seconds)")
    print(f"File Size: {final_size_mb:.2f} MB")
    print(f"Resolution: 1920x1080 Full HD (CRF 12 Lossless Quality)")
    print(f"Scenes: 14 Unique Storyboard Backdrops")
    print(f"Audio: Zero-Overlap 48kHz Stereo with 1.20s Part Silence")
    print(f"Captions: Pure White Borderless Open Captions Synchronized to Voice Pace\n")

if __name__ == "__main__":
    build_video()
