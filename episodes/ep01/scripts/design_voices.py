"""Design custom ElevenLabs voices for Elena and Lucien (previews only, nothing saved to the library).

Writes each preview MP3 plus voices/design/manifest.json with every generated_voice_id.
Usage: python3 -I design_voices.py <episode_dir>
"""
import base64, json, os, sys, pathlib, requests

ep = pathlib.Path(sys.argv[1])
out = ep / "voices" / "design"
out.mkdir(parents=True, exist_ok=True)
KEY = os.environ["ELEVENLABS_API_KEY"]

CHARACTERS = {
    "elena": {
        "voice_description": (
            "A woman in her late twenties with a low, warm, intimate voice, slightly breathless, "
            "soft and close to the microphone, neutral American accent, quiet intensity, "
            "dark romance audiobook narrator, clean studio recording."
        ),
        "text": (
            "The book had my name in it. Written three hundred years before I was born. "
            "And the date I die is tonight. Who are you? Then why do I know your voice?"
        ),
    },
    "lucien": {
        "voice_description": (
            "A man in his thirties with a deep, calm, quiet voice, old-world and refined, "
            "subtle Received Pronunciation British accent, unhurried, never raises his voice, "
            "velvety low register, intimate and melancholic, clean studio recording."
        ),
        "text": (
            "You weren't supposed to find that. The man who wrote it. "
            "It says you die tonight, every time. Three hundred years, Elena. "
            "And you never remember me."
        ),
    },
}

manifest = {}
for name, spec in CHARACTERS.items():
    r = requests.post(
        "https://api.elevenlabs.io/v1/text-to-voice/design",
        headers={"xi-api-key": KEY},
        json={"model_id": "eleven_multilingual_ttv_v2", "guidance_scale": 5, **spec},
        timeout=180,
    )
    if not r.ok:
        sys.exit(f"{name}: HTTP {r.status_code} {r.text[:500]}")
    previews = r.json()["previews"]
    manifest[name] = {**spec, "previews": []}
    for i, p in enumerate(previews, 1):
        path = out / f"{name}-option{i}.mp3"
        path.write_bytes(base64.b64decode(p["audio_base_64"]))
        manifest[name]["previews"].append(
            {"option": i, "file": path.name, "generated_voice_id": p["generated_voice_id"],
             "duration_secs": p.get("duration_secs")}
        )
        print(name, i, p["generated_voice_id"], p.get("duration_secs"))

(out / "manifest.json").write_text(json.dumps(manifest, indent=2))
