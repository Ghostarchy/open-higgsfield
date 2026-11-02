"""Voice design previews (3 per speaker) and sound-effect stems for the series. Records every ID.

  python3 audio.py <series_dir> design     # voices/design/*.mp3 + manifest.json
  python3 audio.py <series_dir> sfx <ep>   # <ep>/audio/sfx/*.mp3 + manifest.json
"""
import base64, json, os, sys, pathlib, requests

root = pathlib.Path(sys.argv[1])
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}

VOICES = {
    "narrator": ("A deep, slow, epic movie-trailer narrator, a man with a resonant low bass voice, "
                 "gravelly and commanding, measured dramatic pacing, clean studio recording.",
                 "Every child in the clan faced the beast. Every child was rejected. For three hundred "
                 "years the ancient wolf bowed to no one, and the mountain waited in silence."),
    "kaelen": ("A cocky, bratty boy around nine years old with a bright, clear young voice, smug and "
               "teasing, spoiled chieftain's son, clean studio recording.",
               "Watch how a chieftain's son does it. Move aside, all of you. That old wolf is going to "
               "bow to me, just like everyone else does."),
    "asha": ("A woman in her forties with a low, husky, commanding voice, a hardened warrior chieftain, "
             "urgent and protective, Nordic-inflected English accent, clean studio recording.",
             "Not you, child. It will tear you apart. Stay behind me. Vorr hasn't bowed in three "
             "hundred years, and it will not bow today."),
    "mira": ("A soft, calm little girl around seven years old with a gentle, quiet, clear voice, "
             "completely unafraid, tender and wise beyond her years, clean studio recording.",
             "I can't see you. But I can hear you're lonely. It's all right. I'm not afraid of you. "
             "I've been listening for you for a very long time."),
}

SFX = {
    "wind": (22, "Howling icy mountain wind in a snowstorm, constant and deep, no music"),
    "crowd_murmur": (15, "Large crowd of fur-clad warriors murmuring tensely in a vast stone arena outdoors in wind"),
    "wolf_snarl": (4, "Huge monstrous wolf snarling low and menacing, deep throaty growl"),
    "child_scream_run": (4, "A small child screams in fear then runs away crying through snow"),
    "crowd_cheer": (4, "Crowd of warriors cheering and whooping in an outdoor arena"),
    "giant_roar": (5, "Enormous ancient wolf roaring, earth-shaking, with a blast of wind and snow"),
    "crowd_gasp": (3, "A large crowd gasps in shock all at once"),
    "kids_laugh": (4, "Several young children laughing and jeering mockingly"),
    "stick_tap": (5, "A small wooden walking stick tapping slowly on packed snow and stone"),
    "footsteps_snow": (7, "Light small footsteps crunching slowly through deep snow"),
    "wolf_breath": (12, "Slow, deep, heavy breathing of a giant beast, close up, in total silence"),
    "spears_raise": (3, "Many warriors raising spears at once, metal and leather rattling"),
    "runes_shimmer": (6, "Magical crystalline ice shimmer, glowing frost spreading, delicate and rising"),
    "spear_drop": (2, "A steel spear dropping into snow with a soft metal thud"),
    "clan_kneel": (6, "Hundreds of armored warriors kneeling slowly, fur and steel armor rustling, torches crackling"),
    "war_horns": (6, "Deep ancient war horns blowing across distant mountains, ominous, echoing"),
    "gate_crack": (5, "A massive iron gate wrapped in chains cracking open, chains snapping, deep metal groan"),
    "monster_growls": (5, "Many unseen monsters growling low in a dark cave, menacing chorus"),
    "wolf_growl_turn": (4, "Giant wolf growling protectively, low and rumbling"),
    "eye_glow": (4, "Rising magical shimmer and whoosh, ice crystals, building to a peak"),
    "drum_hit": (3, "One single huge low cinematic drum hit with a long tail, nothing else"),
}


def design():
    out = root / "voices/design"
    out.mkdir(parents=True, exist_ok=True)
    mp = out / "manifest.json"
    man = json.loads(mp.read_text()) if mp.exists() else {}
    for name, (desc, text) in VOICES.items():
        if name in man:
            continue
        r = requests.post("https://api.elevenlabs.io/v1/text-to-voice/design", headers=H, json={
            "model_id": "eleven_multilingual_ttv_v2", "voice_description": desc, "text": text,
            "guidance_scale": 5}, timeout=180)
        if not r.ok:
            print(f"{name}: HTTP {r.status_code} {r.text[:300]}", flush=True)
            continue
        man[name] = {"voice_description": desc, "text": text, "previews": []}
        for i, p in enumerate(r.json()["previews"], 1):
            f = out / f"{name}-option{i}.mp3"
            f.write_bytes(base64.b64decode(p["audio_base_64"]))
            man[name]["previews"].append({"option": i, "file": f.name,
                                          "generated_voice_id": p["generated_voice_id"]})
        mp.write_text(json.dumps(man, indent=2))
        print("designed", name, flush=True)


def sfx(ep):
    out = ep / "audio/sfx"
    out.mkdir(parents=True, exist_ok=True)
    mp = out / "manifest.json"
    man = json.loads(mp.read_text()) if mp.exists() else {}
    for name, (dur, prompt) in SFX.items():
        if name in man:
            continue
        r = requests.post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192",
                          headers=H, json={"text": prompt, "duration_seconds": dur,
                                           "prompt_influence": 0.5}, timeout=180)
        if not r.ok:
            print(f"{name}: HTTP {r.status_code} {r.text[:300]}", flush=True)
            continue
        (out / f"{name}.mp3").write_bytes(r.content)
        man[name] = {"prompt": prompt, "duration_s": dur, "file": f"{name}.mp3",
                     "request_id": r.headers.get("request-id")}
        mp.write_text(json.dumps(man, indent=2))
    print("sfx done:", len(man), "stems", flush=True)


if sys.argv[2] == "design":
    design()
else:
    sfx(pathlib.Path(sys.argv[3]))
