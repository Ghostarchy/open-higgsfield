"""Generate Episode 1 sound-design stems with ElevenLabs sound effects; records request IDs.
Usage: python3 sfx.py <episode_dir>
"""
import json, os, sys, pathlib, requests

ep = pathlib.Path(sys.argv[1])
out = ep / "audio/sfx"
out.mkdir(parents=True, exist_ok=True)
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}

STEMS = {
    "room_candles": (22, "Quiet room tone of a vast old library at night with soft crackling candle flames, gentle distant rain on tall windows, no music"),
    "page_turn": (2, "A single brittle old parchment page turning slowly, close up"),
    "hum_build": (12, "Low ominous sub-bass drone that slowly rises in intensity and pressure, cinematic tension, no melody"),
    "footstep_echo": (2, "One single heavy footstep on an old wooden floor echoing in a large dark hall"),
    "footsteps_approach": (8, "Slow deliberate men's footsteps on creaking old wooden floorboards, approaching from behind"),
    "flame_flicker": (3, "Candle flames fluttering in a sudden draft, soft airy whoosh"),
    "breath": (4, "A woman's soft nervous breath, close and intimate, a shaky inhale and slow exhale"),
    "leather_creak": (3, "An old leather book cover creaking under a tight nervous grip, close up"),
    "heartbeat": (22, "Slow, quiet, deep human heartbeat, steady, cinematic, no music"),
    "clock_tick": (15, "An old grandfather clock ticking slowly in a silent dark room, steady tick tock"),
    "candle_snuff": (2, "A single candle flame being snuffed out, short soft hiss and puff"),
    "pages_flip": (4, "Pages of a heavy old book flipping rapidly on their own in a gust, then stopping"),
    "ink_writing": (5, "A quill pen scratching slowly on old parchment, ink writing a line by itself, eerie and close"),
}

man_path = out / "manifest.json"
manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
for name, (dur, prompt) in STEMS.items():
    if name in manifest:
        continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192",
                      headers=H, json={"text": prompt, "duration_seconds": dur, "prompt_influence": 0.5},
                      timeout=180)
    if not r.ok:
        sys.exit(f"{name}: HTTP {r.status_code} {r.text[:400]}")
    (out / f"{name}.mp3").write_bytes(r.content)
    manifest[name] = {"prompt": prompt, "duration_s": dur, "file": f"{name}.mp3",
                      "request_id": r.headers.get("request-id")}
    man_path.write_text(json.dumps(manifest, indent=2))
    print("sfx", name, flush=True)
