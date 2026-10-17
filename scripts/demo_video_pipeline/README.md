# Demo Video Production Pipeline
==================================

This directory contains the production pipeline scripts used to render the official hackathon championship demonstration video:
`falkordb_championship_demo.mp4` (1080p Full HD @ 25 FPS, 3m 29s).

### Contents:
1. `render_demo_video.py`: Assembles the 14 visual scene decks, applies 1080p modal layouts, overlays rhythmically synchronized borderless pure white captions, and multiplexes 48 kHz stereo voiceover with 1.20s silence gaps.
2. `build_script_captions.py`: Generates word-by-word synchronized captions strictly aligned with the authoritative script in `DEMO_SCRIPT.md`.
3. `generate_custom_scenes.py`: Draws the obsidian glassmorphic architecture cards with bound text-wrapping and vector geometry.
