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
MASTER_WAV = os.path.join(AUDIO_DIR, "master_narration.wav")
CAPTIONS_JSON = os.path.join(AUDIO_DIR, "clean_synced_captions.json")
FINAL_MP4 = os.path.join(WORKSPACE, "falkordb_championship_demo.mp4")

W, H = 1920, 1080
FPS = 25

# Color Palette (Deep Void & Electric Accents)
DEEP_VOID = (6, 8, 12)
CYAN = (0, 240, 255)
GOLD = (255, 184, 0)
GREEN = (16, 185, 129)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
FONT_CAPTION = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)

# Load Synchronized Captions
with open(CAPTIONS_JSON, "r", encoding="utf-8") as f:
    RAW_CAPTIONS = json.load(f)

def get_caption_at_time(t):
    for c_start, c_end, c_text in RAW_CAPTIONS:
        if c_start <= t <= c_end:
            return c_text
    return ""

# Helper to crop centered modal cleanly and center onto 1920x1080
def prepare_centered_modal(img_path, target_h=830):
    im = Image.open(img_path)
    mw, mh = im.size
    # Crop central modal card
    box = (int(mw * 0.22), int(mh * 0.08), int(mw * 0.78), int(mh * 0.92))
    crop = im.crop(box)
    cw, ch = crop.size
    scale = target_h / ch
    target_w = int(cw * scale)
    crop_res = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    base = Image.new("RGB", (W, H), DEEP_VOID)
    bx = (W - target_w) // 2
    by = 50 + ((H - 120) - target_h) // 2
    base.paste(crop_res, (bx, by))
    return base

# Helper to crop left/right dashboard panel cleanly
def prepare_panel(img_path, crop_box, target_h=850):
    im = Image.open(img_path)
    crop = im.crop(crop_box)
    cw, ch = crop.size
    scale = min(1700 / cw, target_h / ch)
    target_w = int(cw * scale)
    target_h_scaled = int(ch * scale)
    crop_res = crop.resize((target_w, target_h_scaled), Image.Resampling.LANCZOS)
    
    base = Image.new("RGB", (W, H), DEEP_VOID)
    bx = (W - target_w) // 2
    by = 50 + ((H - 120) - target_h_scaled) // 2
    base.paste(crop_res, (bx, by))
    return base

# Pre-render Key Dynamic Scenes for maximum quality and speed
print("Pre-rendering high-resolution focused scene backdrops...")

# 1. Hero Topology View (Commander Kalki + Sovereign Fleet)
hero_topo_img = prepare_panel(
    os.path.join(BRAIN_DIR, "master_topology_1792059293367.png"),
    (30, 350, 1070, 1090),
    target_h=860
)

# 2. Control Deck (Ingestion 300 DNA -> 93 Rules in 67ms)
ingest_deck_img = prepare_panel(
    os.path.join(BRAIN_DIR, "master_topology_1792059293367.png"),
    (20, 140, 1850, 360),
    target_h=340
)
# Place control deck prominently with topology below
combined_p2_ingest = Image.new("RGB", (W, H), DEEP_VOID)
# Crop deck and top header
im_full = Image.open(os.path.join(BRAIN_DIR, "master_topology_1792059293367.png"))
deck_crop = im_full.crop((20, 60, 1852, 360))
dw, dh = deck_crop.size
deck_scale = 1860 / dw
deck_res = deck_crop.resize((int(dw * deck_scale), int(dh * deck_scale)), Image.Resampling.LANCZOS)
combined_p2_ingest.paste(deck_res, (30, 65))
# Bottom half: topology preview
topo_sub = im_full.crop((35, 360, 1070, 990))
tw, th = topo_sub.size
t_scale = 620 / th
topo_res = topo_sub.resize((int(tw * t_scale), int(th * t_scale)), Image.Resampling.LANCZOS)
combined_p2_ingest.paste(topo_res, ((W - int(tw * t_scale)) // 2, 335))

# 3. Relay Modal (Kalki -> Varuna -> Vishwakarma -> Sanjaya)
relay_modal_img = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "relay_modal_1792058246115.png"),
    target_h=850
)

# 4. Blast Radius Modal (Directed Shortest Path to Remediation Playbook)
blast_modal_img = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "blast_radius_modal_1792058269606.png"),
    target_h=850
)

# 5. Gemini Argon NL-to-Cypher Panel (Company Brain & Provenance)
argon_panel_img = prepare_panel(
    os.path.join(BRAIN_DIR, "master_topology_1792059293367.png"),
    (1075, 350, 1845, 1090),
    target_h=860
)

# 6. Concurrency Benchmark Modal (100 Ops, 1,401 Ops/Sec)
bench_modal_img = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "benchmark_modal_1792058223280.png"),
    target_h=850
)

# 7. Model Context Protocol (MCP) Tool Registry Modal (7 Tools)
mcp_modal_img = prepare_centered_modal(
    os.path.join(BRAIN_DIR, "mcp_modal_1792058290529.png"),
    target_h=850
)

print("[OK] All scene backdrops prepared at 1080p razor sharpness.")

# Scene Director: Chooses the optimal high-res focus for each timestamp
def get_scene_frame(t):
    # Part 1 (0.00s - 34.36s): Intro & Sovereign Fleet Topology
    if t < 12.0:
        return combined_p2_ingest, "FALKORDB UNIVERSAL MEMORY MESH — SOVEREIGN AGENT SUBSTRATE", "RULE 5: ALL 3 TRACKS", GOLD
    elif t < 34.36:
        return hero_topo_img, "4-TIER MULTIGRAPH TOPOLOGY: KALKI -> SOVEREIGN FLEET -> CANONICAL RULES", "RULE 5 UNIFIED", CYAN
    
    # Part 2 (34.36s - 84.07s): Track 02 (Primary Track)
    elif t < 55.0:
        return combined_p2_ingest, "TRACK 02: CYPHER MERGE COLLAPSES 300 DNA -> 93 RULES (67ms)", "PRIMARY TRACK 02", CYAN
    elif t < 66.0:
        return hero_topo_img, "TRACK 02: VARUNA QUARANTINE SENTINEL (18 CANARIES BLOCKED)", "PRIMARY TRACK 02", CYAN
    elif t < 84.07:
        return relay_modal_img, "TRACK 02: 4-AGENT COW HANDOFF RELAY (KALKI -> VARUNA -> VISHWAKARMA -> SANJAYA)", "PRIMARY TRACK 02", GOLD
    
    # Part 3 (84.52s - 122.64s): Track 01 (Graph Algorithms)
    elif t < 99.0:
        return argon_panel_img, "TRACK 01: CALL ALGO.PAGERANK & GRAPH-PACC (<300 TOKENS)", "TRACK 01: ALGORITHMS", GREEN
    elif t < 122.64:
        return blast_modal_img, "TRACK 01: DIRECTED SHORTESTPATH BLAST RADIUS & REMEDIATION (4ms)", "TRACK 01: ALGORITHMS", GREEN
    
    # Part 4 (123.09s - 152.26s): Track 03 (Company Brain & Provenance)
    elif t < 152.26:
        return argon_panel_img, "TRACK 03: COMPANY BRAIN & DECISION PROVENANCE (NL-TO-CYPHER)", "TRACK 03: PROVENANCE", GOLD
    
    # Part 5 (152.71s - 179.91s): Enterprise Concurrency Benchmark & Studio Audit
    elif t < 179.91:
        return bench_modal_img, "ENTERPRISE BENCHMARK: 1,401 OPS/SEC CONCURRENCY (ZERO FAILURES)", "RULE 3 VERIFIED", GOLD
    
    # Part 6 (180.36s - 201.78s): Rule 10 Verification & MCP Registry
    elif t < 194.0:
        return mcp_modal_img, "RULE 10 VERIFICATION: 7 MCP TOOLS REGISTERED FOR AUTONOMOUS AGENTS", "RULE 10 VERIFIED", GREEN
    else:
        return hero_topo_img, "13/13 UNIT TESTS PASSING IN 0.45s — READY FOR PRODUCTION", "100% READY", GREEN

def render_frame(t):
    base_img, title_text, badge_text, badge_color = get_scene_frame(t)
    im = base_img.copy()
    draw = ImageDraw.Draw(im)

    # 1. Subtle, Minimal Top HUD Bar (45px)
    draw.rectangle([(0, 0), (W, 45)], fill=(6, 8, 12, 230))
    draw.line([(0, 45), (W, 45)], fill=(24, 32, 47), width=1)
    
    # Live Green Indicator
    draw.ellipse([(20, 16), (32, 28)], fill=GREEN)
    draw.text((40, 10), title_text, font=FONT_TITLE, fill=CYAN)
    
    # Top-right Badge
    b_bbox = draw.textbbox((0, 0), badge_text, font=FONT_BADGE)
    bw = b_bbox[2] - b_bbox[0] + 20
    bx = W - 25 - bw
    draw.rounded_rectangle([(bx, 8), (bx + bw, 36)], radius=4, fill=(12, 16, 26), outline=badge_color, width=1)
    draw.text((bx + 10, 10), badge_text, font=FONT_BADGE, fill=badge_color)

    # 2. Simple White Caption (NO BOX, NO BORDER, JUST NORMAL WHITE TEXT)
    cap_text = get_caption_at_time(t)
    if cap_text:
        cap_box = draw.textbbox((0, 0), cap_text, font=FONT_CAPTION)
        cw = cap_box[2] - cap_box[0]
        cx = (W - cw) // 2
        cy = H - 75
        
        # Subtle 2px black drop shadow for crisp readability over any background
        draw.text((cx + 2, cy + 2), cap_text, font=FONT_CAPTION, fill=(0, 0, 0))
        # Pure simple white text
        draw.text((cx, cy), cap_text, font=FONT_CAPTION, fill=WHITE)

    return im

def build_video():
    print("\n" + "="*70)
    print("🎬 RENDERING CRYSTAL-CLEAR CHAMPIONSHIP VIDEO V3")
    print("   - Master Zero-Overlap Audio (48kHz Stereo)")
    print("   - Exact Word-Synchronized Fast-Paced Captions")
    print("   - Simple Pure White Typography (No Border, No Pill Box)")
    print("   - Unscaled 1080p Focused Panels (Razor-Sharp Text)")
    print("   - Visually Lossless Encoding (CRF 12, StillImage Tune)")
    print("="*70)

    # Probe duration of master audio
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", MASTER_WAV]
    total_duration = float(subprocess.check_output(dur_cmd).decode().strip())
    total_frames = int(total_duration * FPS)
    
    mins = int(total_duration // 60)
    secs = int(total_duration % 60)
    print(f"\nMaster Narration Audio: {MASTER_WAV}")
    print(f"Total Video Runtime: {mins}m {secs:02d}s ({total_duration:.2f}s, {total_frames} frames @ {FPS}fps)")

    # Direct Single-Pass Lossless Video Pipe into FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # raw video frames from python
        "-i", MASTER_WAV,  # single unified continuous audio
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "12",  # virtually lossless
        "-tune", "stillimage",  # shuts off deblocking blur for sharp text
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        FINAL_MP4
    ]

    print("\nStarting FFmpeg pipe encoder...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t_curr = f_idx / FPS
        frame = render_frame(t_curr)
        proc.stdin.write(frame.tobytes())
        
        if f_idx % 250 == 0 or f_idx == total_frames - 1:
            pct = (f_idx / total_frames) * 100
            print(f"  Frame {f_idx}/{total_frames} ({pct:.1f}%) | Time: {t_curr:.2f}s")

    proc.stdin.close()
    proc.wait()

    final_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    print("\n" + "="*70)
    print("🏆 CHAMPIONSHIP DEMO VIDEO V3 RENDER COMPLETE!")
    print("="*70)
    print(f"Output File: {FINAL_MP4}")
    print(f"File Size: {final_size_mb:.2f} MB")
    print(f"Duration: {mins}m {secs:02d}s")
    print(f"Resolution: 1920x1080 Full HD (CRF 12 Lossless Sharpness)")
    print(f"Captions: Simple White, Zero Borders, Perfectly Synchronized\n")

if __name__ == "__main__":
    build_video()
