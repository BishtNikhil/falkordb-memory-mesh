import os
from PIL import Image, ImageDraw, ImageFont

BRAIN_DIR = r"C:\Users\Saurav Bisht\.gemini\antigravity-ide\brain\9acd4efa-5a73-4be8-90f7-c8b6c0e60dd2"

W, H = 1920, 1080
DEEP_VOID = (6, 8, 12)
CARD_BG = (12, 16, 26)
BORDER_COL = (30, 41, 59)
CYAN = (0, 240, 255)
GOLD = (255, 184, 0)
GREEN = (16, 185, 129)
RED = (239, 68, 68)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)

FONT_HUGE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
FONT_CODE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 18)
FONT_CODE_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 20)

def draw_multiline(draw, text, xy, font, fill, max_width, line_spacing=6):
    words = text.split()
    lines = []
    cur_line = []
    
    for word in words:
        test_line = " ".join(cur_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur_line.append(word)
        else:
            if cur_line:
                lines.append(" ".join(cur_line))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))
    
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y

# ==============================================================================
# 1. FIXED SCENE 2: THE MULTI-AGENT MEMORY CRISIS
# ==============================================================================
im_crisis = Image.new("RGB", (W, H), DEEP_VOID)
d = ImageDraw.Draw(im_crisis)

d.text((W // 2 - 380, 75), "THE AUTONOMOUS MULTI-AGENT CRISIS", font=FONT_HUGE, fill=WHITE)
d.text((W // 2 - 300, 130), "Why Flat JSON Memory Destroys Scalability vs FalkorDB GraphBLAS", font=FONT_SUB, fill=MUTED)

# Left Column: The Flat JSON Failure (Red Alert)
cx1 = 120
d.rounded_rectangle([(cx1, 180), (cx1 + 800, 860)], radius=16, fill=(24, 12, 14), outline=RED, width=2)
d.rectangle([(cx1, 180), (cx1 + 800, 245)], fill=(38, 16, 20))
d.text((cx1 + 30, 198), "FLAT JSON MEMORY ARRAYS (THE CRISIS)", font=FONT_TITLE, fill=RED)

failures = [
    ("1. DUPLICATE RULE BLOAT", 
     "4,200 tokens stuffed into context window on every turn. Repeating rules 10x causes LLM hallucination and 10x API bills."),
    ("2. CROSS-AGENT SECRET LEAKS", 
     "Shared flat arrays expose private credentials. One agent exfiltrating an API key leaks it to the entire multi-agent swarm."),
    ("3. ZERO CAUSAL PROVENANCE", 
     "Black-box decisions. When a rule breaks production, developers cannot trace which agent created it, why, or what incident caused it.")
]

for idx, (f_title, f_desc) in enumerate(failures):
    fy = 270 + idx * 190
    card_x1 = cx1 + 25
    card_x2 = cx1 + 775
    card_w = card_x2 - card_x1
    
    d.rounded_rectangle([(card_x1, fy), (card_x2, fy + 165)], radius=10, fill=(32, 16, 22), outline=(75, 25, 35), width=1)
    d.text((card_x1 + 25, fy + 18), f_title, font=FONT_TITLE, fill=(255, 120, 120))
    # Multiline text with max_width = card_w - 50 (guarantees text remains strictly inside box!)
    draw_multiline(d, f_desc, (card_x1 + 25, fy + 60), FONT_SUB, (220, 180, 185), max_width=card_w - 50, line_spacing=6)

# Right Column: The FalkorDB Substrate Solution (Emerald / Cyan)
cx2 = 1000
d.rounded_rectangle([(cx2, 180), (cx2 + 800, 860)], radius=16, fill=(10, 22, 26), outline=GREEN, width=2)
d.rectangle([(cx2, 180), (cx2 + 800, 245)], fill=(14, 32, 38))
d.text((cx2 + 30, 198), "FALKORDB COGNITIVE SUBSTRATE (SOLUTION)", font=FONT_TITLE, fill=GREEN)

solutions = [
    ("1. CYPHER MERGE COLLAPSE (67ms)", 
     "Collapses 300 raw DNA inputs into 93 canonical rules in 67ms. Converts duplicate occurrences into edge reinforcement weights."),
    ("2. VARUNA AIR-GAPPED QUARANTINE", 
     "Intercepts canary tokens before AST parse. Tainted nodes locked in zero-secret vault, keeping main brain 100% clean."),
    ("3. COMPLETE CAUSAL LINEAGE (3ms)", 
     "Multi-hop graph traversal in 3 milliseconds. Instantly maps rules back to Jira tickets, Git commits, and Slack war-rooms.")
]

for idx, (s_title, s_desc) in enumerate(solutions):
    sy = 270 + idx * 190
    card_x1 = cx2 + 25
    card_x2 = cx2 + 775
    card_w = card_x2 - card_x1
    
    d.rounded_rectangle([(card_x1, sy), (card_x2, sy + 165)], radius=10, fill=(14, 30, 36), outline=(25, 60, 65), width=1)
    d.text((card_x1 + 25, sy + 18), s_title, font=FONT_TITLE, fill=GREEN)
    draw_multiline(d, s_desc, (card_x1 + 25, sy + 60), FONT_SUB, (180, 220, 215), max_width=card_w - 50, line_spacing=6)

im_crisis.save(os.path.join(BRAIN_DIR, "v5_scene_memory_crisis.png"))
print("[OK] Fixed v5_scene_memory_crisis.png (zero text overflow)")


# ==============================================================================
# 2. FIXED SCENE 4: TRACK 02 CYPHER MERGE INGESTION BENCHMARK
# ==============================================================================
im_ingest = Image.new("RGB", (W, H), DEEP_VOID)
d = ImageDraw.Draw(im_ingest)

d.text((120, 75), "TRACK 02: CYPHER MERGE INGESTION PIPELINE", font=FONT_HUGE, fill=CYAN)
d.text((120, 130), "Primary Track: PS5 + GTA VI  |  Collapses 300 Raw DNA Events into 93 Canonical Rules in 67ms", font=FONT_SUB, fill=MUTED)

# Pipeline Flow Diagram: 3 Steps
steps = [
    ("1. RAW DNA INPUT", "300 Dynamic Rules", 
     "Duplicate JSON events emitted by 7 parallel agents during high-velocity swarming.", 
     (25, 35, 55), MUTED),
    ("2. CYPHER MERGE PIPELINE", "GraphBLAS Core", 
     "MERGE clause execution collapses duplicates and increments edge weights in 67.24 ms.", 
     (20, 45, 60), CYAN),
    ("3. REINFORCED GRAPH", "93 Canonical Rules", 
     "Zero duplicate rules stored. Edge reinforcement weights prioritize vital rules.", 
     (18, 45, 38), GREEN)
]

for idx, (s_head, s_sub, s_desc, bg, col) in enumerate(steps):
    sx = 120 + idx * 580
    box_w = 515
    d.rounded_rectangle([(sx, 175), (sx + box_w, 415)], radius=14, fill=bg, outline=col, width=2)
    d.text((sx + 25, 195), s_head, font=FONT_SUB, fill=col)
    d.text((sx + 25, 230), s_sub, font=FONT_TITLE, fill=WHITE)
    # Multiline text cleanly wrapped inside box
    draw_multiline(d, s_desc, (sx + 25, 285), FONT_SMALL, (200, 215, 230), max_width=box_w - 50, line_spacing=5)
    
    if idx < 2:
        # Draw clean vector arrow in gap between boxes
        ax = sx + box_w + 14
        ay = 295
        d.line([(ax, ay), (ax + 28, ay)], fill=GOLD, width=4)
        d.polygon([(ax + 24, ay - 8), (ax + 38, ay), (ax + 24, ay + 8)], fill=GOLD)

# Cypher Code Block Box
d.rounded_rectangle([(120, 445), (W - 120, 860)], radius=14, fill=CARD_BG, outline=BORDER_COL, width=1)
d.rectangle([(120, 445), (W - 120, 500)], fill=(18, 24, 38))
d.text((150, 458), "PRODUCTION CYPHER MERGE EXECUTION SCRIPT [67ms]", font=FONT_TITLE, fill=GOLD)

code_lines = [
    ("// Step 1: Atomic Ingestion & Weight Incrementation via Linear-Algebra GraphBLAS"),
    ("UNWIND $raw_dna_events AS event"),
    ("MERGE (r:ArchitecturalRule {rule_id: event.rule_id})"),
    ("ON CREATE SET r.directive = event.directive, r.domain = event.domain, r.reinforcement_weight = 1"),
    ("ON MATCH SET r.reinforcement_weight = r.reinforcement_weight + 1, r.last_reinforced = timestamp()"),
    ("MERGE (a:SovereignAgent {id: event.agent_id})"),
    ("MERGE (a)-[rel:ENFORCES]->(r)"),
    ("RETURN count(DISTINCT r) AS canonical_rules, count(event) AS total_dna_collapsed;"),
    ("// RESULT: 300 Events Collapsed -> 93 Canonical Rules | Execution Latency: 67.24 ms | Memory Saved: 69.0%")
]
for idx, line in enumerate(code_lines):
    col = GREEN if line.startswith("// RESULT") else (MUTED if line.startswith("//") else (CYAN if "MERGE" in line else WHITE))
    d.text((150, 518 + idx * 36), line, font=FONT_CODE_BOLD, fill=col)

im_ingest.save(os.path.join(BRAIN_DIR, "v5_scene_ingestion_pipeline.png"))
print("[OK] Fixed v5_scene_ingestion_pipeline.png (zero text overflow)")


# ==============================================================================
# 3. FIXED SCENE 5: VARUNA ZERO-SECRET QUARANTINE GATEKEEPER
# ==============================================================================
im_varuna = Image.new("RGB", (W, H), DEEP_VOID)
d = ImageDraw.Draw(im_varuna)

# Main Card Outer
d.rounded_rectangle([(100, 65), (W - 100, 860)], radius=16, fill=(14, 18, 30), outline=(220, 38, 38), width=2)

# Title Header
d.text((140, 95), "[SECURITY SENTINEL] AGENT VARUNA — ZERO-SECRET QUARANTINE GATEKEEPER", font=FONT_TITLE, fill=(255, 90, 90))
d.text((140, 135), "Real-Time AST Gate & Secret Leak Interception Substrate (Rule 5 Security Law)", font=FONT_SUB, fill=MUTED)

# Top 3 Metrics Cards (Width 530px each)
top_cards = [
    ("CANARIES INTERCEPTED", "18 / 18", 
     "Synthetic API keys & credentials blocked before graph ingestion.", RED),
    ("AST PARSE LATENCY", "1.82 ms", 
     "Sub-2ms regex & AST scanner runs on every agent state emission.", CYAN),
    ("QUARANTINE ISOLATION", "100% AIR-GAPPED", 
     "Locked inside isolated VarunaZeroSecretVault multigraph.", GREEN)
]

for idx, (c_title, c_val, c_sub, col) in enumerate(top_cards):
    cx = 140 + idx * 560
    cw = 520
    d.rounded_rectangle([(cx, 185), (cx + cw, 375)], radius=12, fill=(18, 24, 40), outline=col, width=1)
    d.text((cx + 25, 205), c_title, font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16), fill=MUTED)
    d.text((cx + 25, 240), c_val, font=FONT_HUGE, fill=col)
    draw_multiline(d, c_sub, (cx + 25, 305), FONT_SMALL, (190, 205, 220), max_width=cw - 50, line_spacing=4)

# Bottom Vault Records Card
d.rounded_rectangle([(140, 410), (W - 140, 825)], radius=12, fill=(18, 24, 38), outline=BORDER_COL, width=1)
d.rectangle([(140, 410), (W - 140, 465)], fill=(24, 18, 26))
d.text((165, 425), "INTERCEPTED SYNTHETIC CANARY TOKENS (LOCKED IN QUARANTINE VAULT):", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16), fill=GOLD)

vault_records = [
    ("ID: CANARY_KEY_7701", "Payload: sk-proj-9921_SYNTHETIC_AGENT_LEAK_TOKEN", 
     "Source: Agent TheSixth | Resolution: BLOCKED AT AST PARSE (0.84ms)"),
    ("ID: CANARY_KEY_8824", "Payload: ghp_CANARY_PROD_DEPLOY_SECRET_KEY_992", 
     "Source: Agent Vidura | Resolution: REDIRECTED TO VAULT (1.12ms)"),
    ("ID: CANARY_KEY_9145", "Payload: SG.FAKE_SENDGRID_API_KEY_LEAK_ATTEMPT", 
     "Source: Agent Naada | Resolution: LOCKED IN AIR-GAP (0.95ms)")
]

for idx, (rec_id, rec_pay, rec_res) in enumerate(vault_records):
    ry = 485 + idx * 105
    d.rounded_rectangle([(165, ry), (W - 165, ry + 90)], radius=8, fill=(14, 20, 32), outline=(35, 45, 65), width=1)
    d.text((185, ry + 15), rec_id, font=FONT_CODE_BOLD, fill=CYAN)
    d.text((450, ry + 15), rec_pay, font=FONT_CODE, fill=(255, 110, 110))
    d.text((185, ry + 50), rec_res, font=FONT_SMALL, fill=MUTED)

im_varuna.save(os.path.join(BRAIN_DIR, "v5_scene_varuna_quarantine.png"))
# Also overwrite v4_varuna_quarantine.png just in case anything references it
im_varuna.save(os.path.join(BRAIN_DIR, "v4_varuna_quarantine.png"))
print("[OK] Fixed v5_scene_varuna_quarantine.png and v4_varuna_quarantine.png (zero text overflow)")
