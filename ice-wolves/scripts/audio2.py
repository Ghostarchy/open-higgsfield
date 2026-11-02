"""EP01 v2 audio: dialogue for voices already saved, the 90 s score, and new sound effects.

  python3 audio2.py <series_dir> <ep_dir>
Records every ElevenLabs request ID in <ep_dir>/audio/*/manifest.json. Lines for speakers without a saved
voice (Sigrun, Grima until picked) are skipped and rendered on the next run.
"""
import json, os, sys, pathlib, subprocess, requests

root, ep = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
voices = json.loads((root / "voices/voices.json").read_text())

TRAILER = {"stability": 0.55, "similarity_boost": 0.85, "style": 0.4, "use_speaker_boost": True, "speed": 0.9}
SOFT = {"stability": 0.6, "similarity_boost": 0.85, "style": 0.35, "use_speaker_boost": True, "speed": 0.9}
PROUD = {"stability": 0.4, "similarity_boost": 0.85, "style": 0.55, "use_speaker_boost": True}
PLEAD = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.65, "use_speaker_boost": False}
SCREAM = {"stability": 0.25, "similarity_boost": 0.8, "style": 0.8, "use_speaker_boost": True}
TEARS = {"stability": 0.3, "similarity_boost": 0.8, "style": 0.7, "use_speaker_boost": False}
FEAR = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.6, "use_speaker_boost": False}

# (id, speaker, start_s, text, settings) - from SEASON-1-BIBLE.md section 4.2.
LINES = [
    ("01", "narrator", 0.5, "Once in a hundred years, the ancient wolf chooses a rider.", TRAILER),
    ("02", "narrator", 4.5, "For a hundred years, it has chosen no one.", TRAILER),
    ("03", "sigrun", 15.5, "Kneel, old wolf. Your rider is here.", PROUD),
    ("04", "narrator", 25.5, "No one noticed the smallest one. No one ever did.", SOFT),
    ("05", "asha", 32.0, "Mira. Little star. Stay with me. Please.", PLEAD),
    ("06", "asha", 37.5, "Mira!", SCREAM),
    ("07", "asha", 69.5, "He bowed. To my little girl.", TEARS),
    ("08", "grima", 75.0, "That scar. He got it the night we found her.", FEAR),
]

out = ep / "audio/dialogue"
out.mkdir(parents=True, exist_ok=True)
mp = out / "manifest.json"
man = json.loads(mp.read_text()) if mp.exists() else {}
for lid, who, start, text, settings in LINES:
    if who not in voices or lid in man:
        continue
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voices[who]['voice_id']}?output_format=mp3_44100_192",
        headers=H, json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": settings},
        timeout=120)
    if not r.ok:
        sys.exit(f"line {lid}: HTTP {r.status_code} {r.text[:300]}")
    f = out / f"{lid}-{who}.mp3"
    f.write_bytes(r.content)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(f)]))
    man[lid] = {"speaker": who, "start_s": start, "text": text, "voice_id": voices[who]["voice_id"],
                "voice_settings": settings, "file": f.name, "duration_s": round(dur, 3),
                "request_id": r.headers.get("request-id")}
    mp.write_text(json.dumps(man, indent=2))
    print("line", lid, who, f"{dur:.2f}s", flush=True)

# Score: one continuous 90 s instrumental so the episode flows like a film, not a montage.
music_dir = ep / "audio/music"
music_dir.mkdir(parents=True, exist_ok=True)
mm = music_dir / "manifest.json"
mman = json.loads(mm.read_text()) if mm.exists() else {}
SCORE = ("Epic dark Nordic fantasy film score, 90 seconds, instrumental only, no vocals except wordless "
         "distant female choir. 0-14s: deep sub-bass drone, slow war drums, low cellos, ominous and vast. "
         "14-25s: drums build, horns rise, then one huge orchestral hit at 20s. 25-36s: everything drops "
         "away; a gentle five-note lullaby melody on a solo nyckelharpa, tender and fragile. 36-53s: dread, "
         "low tremolo strings and a slow heartbeat drum rising in tension. 53-63s: near silence, one held high "
         "violin note. 63-74s: the lullaby returns in full, warm strings and soft female choir, emotional and "
         "triumphant. 74-87s: dark turn, low brass, war horns, pounding drums, rising to a peak. 87-90s: "
         "silence.")
if "score" not in mman:
    r = requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", headers=H,
                      json={"prompt": SCORE, "music_length_ms": 90000, "force_instrumental": True}, timeout=600)
    if r.ok:
        (music_dir / "score.mp3").write_bytes(r.content)
        mman["score"] = {"prompt": SCORE, "file": "score.mp3", "request_id": r.headers.get("request-id")}
        mm.write_text(json.dumps(mman, indent=2))
        print("score done", flush=True)
    else:
        print(f"score: HTTP {r.status_code} {r.text[:300]}", flush=True)

# Sound effects new to v2 (v1 stems are reused from ep01/audio/sfx).
SFX = {
    "eye_blink": (3, "Deep sub-bass swell then a heavy wet blink of a giant creature's eye, close"),
    "war_drum_slow": (12, "Slow single war drum hits, one per second, huge and echoing in a stone arena"),
    "chant_sigrun": (5, "Hundreds of women chanting a two-syllable name in rhythm, SIG-RUN, SIG-RUN, in a stone arena"),
    "sword_clatter": (2, "A steel sword clattering and sliding across icy stone"),
    "toddler_steps": (6, "Tiny light footsteps of a small child crunching slowly through snow, close"),
    "bowstrings": (4, "A line of archers drawing longbows, wood and bowstrings creaking under tension"),
    "chains_snap": (4, "Massive iron chains snapping one after another, deep metallic cracks and echoes"),
    "whoosh_hit": (2, "Cinematic transition whoosh into a deep impact boom"),
    "shimmer_rise": (4, "Magical ice crystal shimmer rising quickly to a bright peak"),
    "armor_kneel": (5, "Rows of warriors kneeling one after another, leather creaking, mail and furs rustling"),
}
sfx_dir = ep / "audio/sfx"
sfx_dir.mkdir(parents=True, exist_ok=True)
sm = sfx_dir / "manifest.json"
sman = json.loads(sm.read_text()) if sm.exists() else {}
for name, (dur, prompt) in SFX.items():
    if name in sman:
        continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192", headers=H,
                      json={"text": prompt, "duration_seconds": dur, "prompt_influence": 0.5}, timeout=180)
    if not r.ok:
        print(f"sfx {name}: HTTP {r.status_code} {r.text[:200]}", flush=True)
        continue
    (sfx_dir / f"{name}.mp3").write_bytes(r.content)
    sman[name] = {"prompt": prompt, "duration_s": dur, "file": f"{name}.mp3", "request_id": r.headers.get("request-id")}
    sm.write_text(json.dumps(sman, indent=2))
print("sfx stems:", len(sman), flush=True)
