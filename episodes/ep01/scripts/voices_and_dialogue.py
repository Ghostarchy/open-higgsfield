"""Save the chosen designed voices to the ElevenLabs library, then render every Episode 1 line.

Writes voices/voices.json (permanent voice IDs, reuse for all 30 episodes) and
audio/dialogue/manifest.json (one entry per line with its ElevenLabs request ID).
Usage: python3 voices_and_dialogue.py <episode_dir>
"""
import json, os, sys, pathlib, subprocess, requests

ep = pathlib.Path(sys.argv[1])
KEY = os.environ["ELEVENLABS_API_KEY"]
H = {"xi-api-key": KEY}
design = json.loads((ep / "voices/design/manifest.json").read_text())
CHOICE = {"elena": 2, "lucien": 1}

voices_path = ep / "voices/voices.json"
voices = json.loads(voices_path.read_text()) if voices_path.exists() else {}
for name, option in CHOICE.items():
    if name in voices:
        continue
    gid = design[name]["previews"][option - 1]["generated_voice_id"]
    r = requests.post("https://api.elevenlabs.io/v1/text-to-voice", headers=H, json={
        "voice_name": f"Ledger of Names - {name.title()}",
        "voice_description": design[name]["voice_description"],
        "generated_voice_id": gid,
    }, timeout=120)
    if not r.ok:
        sys.exit(f"save {name}: HTTP {r.status_code} {r.text[:400]}")
    voices[name] = {"voice_id": r.json()["voice_id"], "from_design_option": option,
                    "generated_voice_id": gid}
    voices_path.write_text(json.dumps(voices, indent=2))
    print("saved", name, voices[name]["voice_id"], flush=True)

NORMAL = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}
WHISPER = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.55, "use_speaker_boost": False}

# (id, speaker, shot, start_in_episode_s, delivery, text)
LINES = [
    ("01", "elena", 1, 0.0, NORMAL, "The book had my name in it."),
    ("02", "elena", 1, 3.0, NORMAL, "Written three hundred years before I was born."),
    ("03", "elena", 1, 7.0, NORMAL, "And the date I die... is tonight."),
    ("04", "lucien", 2, 13.0, NORMAL, "You weren't supposed to find that."),
    ("05", "elena", 2, 16.0, NORMAL, "Who are you?"),
    ("06", "lucien", 2, 19.0, NORMAL, "The man who wrote it."),
    ("07", "elena", 3, 25.0, WHISPER, "It says I die tonight."),
    ("08", "lucien", 3, 28.0, NORMAL, "No."),
    ("09", "lucien", 3, 30.0, NORMAL, "It says you die tonight. Every time."),
    ("10", "lucien", 4, 37.0, WHISPER, "Three hundred years, Elena."),
    ("11", "lucien", 4, 40.0, WHISPER, "And you never remember me."),
    ("12", "elena", 4, 44.0, WHISPER, "Then why do I know your voice?"),
    ("13", "elena", 5, 50.0, NORMAL, "He said the book never lies."),
    ("14", "elena", 5, 54.0, NORMAL, "So why did it just write his name?"),
]

out = ep / "audio/dialogue"
out.mkdir(parents=True, exist_ok=True)
man_path = out / "manifest.json"
manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
for lid, who, shot, start, settings, text in LINES:
    vid = voices[who]["voice_id"]
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_192",
        headers=H, json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": settings},
        timeout=120,
    )
    if not r.ok:
        sys.exit(f"line {lid}: HTTP {r.status_code} {r.text[:400]}")
    f = out / f"{lid}-{who}.mp3"
    f.write_bytes(r.content)
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).strip())
    manifest[lid] = {"speaker": who, "shot": shot, "start_s": start, "text": text,
                     "voice_id": vid, "model_id": "eleven_multilingual_v2",
                     "whisper": settings is WHISPER, "file": f.name, "duration_s": round(dur, 3),
                     "request_id": r.headers.get("request-id")}
    man_path.write_text(json.dumps(manifest, indent=2))
    print(lid, who, f"{dur:.2f}s", text, flush=True)
