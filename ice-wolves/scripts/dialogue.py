"""Save chosen designed voices to the ElevenLabs library (series-level) and render an episode's lines.

  python3 dialogue.py <series_dir> <ep_dir> narrator=3 asha=2
Voices land in <series_dir>/voices/voices.json (reuse for every episode); lines in
<ep_dir>/audio/dialogue/manifest.json with their request IDs. Speakers without a saved voice are skipped.
"""
import json, os, sys, pathlib, subprocess, requests

root, ep = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
picks = dict(a.split("=") for a in sys.argv[3:])
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
design = json.loads((root / "voices/design/manifest.json").read_text())

vp = root / "voices/voices.json"
voices = json.loads(vp.read_text()) if vp.exists() else {}
for name, opt in picks.items():
    if name in voices:
        continue
    gid = design[name]["previews"][int(opt) - 1]["generated_voice_id"]
    r = requests.post("https://api.elevenlabs.io/v1/text-to-voice", headers=H, json={
        "voice_name": f"Ice Wolves - {name.title()}", "generated_voice_id": gid,
        "voice_description": design[name]["voice_description"]}, timeout=120)
    if not r.ok:
        sys.exit(f"save {name}: HTTP {r.status_code} {r.text[:300]}")
    voices[name] = {"voice_id": r.json()["voice_id"], "from_design_option": int(opt), "generated_voice_id": gid}
    vp.write_text(json.dumps(voices, indent=2))
    print("saved", name, voices[name]["voice_id"], flush=True)

# (id, speaker, text, voice settings) - EP01 lines from the brief.
TRAILER = {"stability": 0.55, "similarity_boost": 0.85, "style": 0.4, "use_speaker_boost": True, "speed": 0.92}
URGENT = {"stability": 0.45, "similarity_boost": 0.85, "style": 0.5, "use_speaker_boost": True}
WHISPER = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.6, "use_speaker_boost": False}
CALM = {"stability": 0.6, "similarity_boost": 0.85, "style": 0.3, "use_speaker_boost": True}
LINES = [
    ("01", "narrator", "Every child in the clan faced the beast. Every child was rejected.", TRAILER),
    ("02", "kaelen", "Watch how a chieftain's son does it.", URGENT),
    ("03", "asha", "Not you, child. It will tear you apart.", URGENT),
    ("04", "mira", "I can't see you. But I can hear you're lonely.", CALM),
    ("05", "asha", "Vorr hasn't bowed in three hundred years.", WHISPER),
]

out = ep / "audio/dialogue"
out.mkdir(parents=True, exist_ok=True)
mp = out / "manifest.json"
man = json.loads(mp.read_text()) if mp.exists() else {}
for lid, who, text, settings in LINES:
    if who not in voices or lid in man:
        continue
    vid = voices[who]["voice_id"]
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_192",
                      headers=H, json={"text": text, "model_id": "eleven_multilingual_v2",
                                       "voice_settings": settings}, timeout=120)
    if not r.ok:
        sys.exit(f"line {lid}: HTTP {r.status_code} {r.text[:300]}")
    f = out / f"{lid}-{who}.mp3"
    f.write_bytes(r.content)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(f)]))
    man[lid] = {"speaker": who, "text": text, "voice_id": vid, "model_id": "eleven_multilingual_v2",
                "voice_settings": settings, "file": f.name, "duration_s": round(dur, 3),
                "request_id": r.headers.get("request-id")}
    mp.write_text(json.dumps(man, indent=2))
    print(lid, who, f"{dur:.2f}s", flush=True)
