"""TWENTY-FOUR production. Reads story.py (locks, shots, dialogue) so renders and the bible never drift.

  python3 produce.py refs [names...]        # locked references (Soul Cinema), series-level
  python3 produce.py voices                 # ElevenLabs voice designs, 3 options per speaker
Every request ID is recorded the moment it is queued (references.json, voices/design/manifest.json).
"""
import base64, json, os, pathlib, sys, threading
import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "pipeline" / "scripts"))
sys.path.insert(0, str(HERE))
import hf  # noqa: E402
import story  # noqa: E402

REFS_DIR = HERE / "references"
REFS_DIR.mkdir(exist_ok=True)
refs_ledger = hf.Ledger(HERE / "references.json")
L, STYLE = story.LOCK, story.STYLE

REFS = {
    "teo": f"Character reference, waist-up, front view, face clearly visible, standing in a pit garage, helmet "
           f"under his arm. {L['TEO']}. {STYLE}",
    "teo_night": f"Character reference, waist-up, front view, face clearly visible, standing in heavy rain at "
                 f"night on a harbour pier. {L['TEO_NIGHT']}. {STYLE}",
    "isla": f"Character reference, waist-up, front view, face clearly visible, standing in a pit garage, helmet "
            f"under her arm. {L['ISLA']}. {STYLE}",
    "isla_night": f"Character reference, waist-up, front view, face clearly visible, holding a black umbrella "
                  f"in the rain at night on a harbour pier. {L['ISLA_NIGHT']}. {STYLE}",
    "declan": f"Character reference, waist-up, front view, face clearly visible, a full head of short dark hair "
              f"receding at the temples, no beard and no goatee, only five-o'clock stubble, standing at a pit-wall desk "
              f"with monitors. {L['DECLAN']}. {STYLE}",
    "brian": f"Character reference, waist-up, front view, face clearly visible, seated in a TV commentary booth "
             f"overlooking a race track. {L['BRIAN']}. {STYLE}",
    "mara": f"Character reference, waist-up, front view, face clearly visible, standing at a trackside fence in "
            f"a crowd. {L['MARA']}. {STYLE}",
    "leo": f"Character reference, waist-up, front view, face clearly visible, in a pit lane holding a "
           f"microphone. {L['REPORTER']}. {STYLE}",
    "owner_hand": f"Prop reference, close-up of the hand resting on a glass desk. {L['OWNER']}. {STYLE}",
    "car4": f"Vehicle reference, three-quarter front view, parked on an empty pit straight. {L['CAR4']}. {STYLE}",
    "car19": f"Vehicle reference, three-quarter front view, parked on an empty pit straight, a modern 2026 Le Mans "
             f"hypercar-class prototype with the same long low proportions, enclosed canopy and tall rear wing as a "
             f"current endurance prototype, not a GT car. {L['CAR19']}. {STYLE}",
    "trophy": "Prop reference, studio shot of a tall sculptural endurance-race trophy: three ribbons of polished "
              "silver twisting around each other like flames rising upward, thin gold edges, on a black base, no "
              f"text, no columns, no fluting. {STYLE}",
}

VOICES = {
    "brian": ("A British male TV motorsport commentator in his early sixties, rich warm baritone, fast and "
              "excitable when the action peaks, classic broadcast delivery, clean studio recording.",
              "Twenty-three hours and fifty-nine minutes. Three thousand miles, and it comes down to one. And the "
              "black number four still leads. He held it! How did he hold that?!"),
    "declan": ("A man in his late forties, a race engineer on team radio, gruff and tense, low voice, trying to "
               "stay calm, slight Northern English accent, clean studio recording.",
               "Teo, your rears are gone. Do you copy? Teo. Do you copy? Box this lap if you can hear me. Teo, "
               "talk to me."),
    "teo": ("A man of thirty-eight, a world-weary champion racing driver, quiet, low and controlled, slightly "
            "husky, understated, neutral English accent, clean studio recording.",
            "Declan, I can't see the line. There won't be a seventh. Especially from you. I kept you out so they "
            "couldn't do this to you."),
    "isla": ("A woman of twenty-six, a fierce racing driver, strong and emotional, voice cracking with anger and "
             "hurt, slight Portuguese accent in English, clean studio recording.",
             "Where is he, Declan? You hid it from everyone. Even from me. You beat me half blind! Three years "
             "on the bench, and this is why?"),
    "leo": ("A male TV reporter in his early thirties, energetic, fast, loud, shouting a question over a crowd, "
            "neutral English accent, clean studio recording.",
            "Teo! Six wins! Is there a seventh? Teo, over here! The whole paddock wants to know, is this the end?"),
    "owner": ("A man in his sixties, wealthy and powerful, smooth, warm on the surface and cold underneath, slow "
              "and deliberate, refined English accent, phone-call intimacy, clean studio recording.",
              "Hello, Isla. Ready to drive for me? You signed it, Declan. Six months ago. Now get out of the car. "
              "I always get what I paid for."),
    "strategist": ("A man in his thirties, a race strategist calling gaps on the radio, clipped and urgent, "
                   "neutral English accent, clean studio recording.",
                   "Ferreira is coming. Point four. Point three. Point two. She's in the window, Declan. Tell him to "
                   "defend the inside into the chicane."),
}


def parallel(fn, items):
    def guarded(i):
        try:
            fn(i)
        except BaseException as e:  # hf.submit raises SystemExit, which a thread would swallow
            print(f"{fn.__name__}({i}) failed: {e}", flush=True)
    ts = [threading.Thread(target=guarded, args=(i,)) for i in items]
    [t.start() for t in ts]
    [t.join() for t in ts]


def run_ref(name):
    if refs_ledger.data.get(name, {}).get("status") == "completed":
        return
    hf.submit(refs_ledger, name, "higgsfield-ai/soul/cinema", {
        "prompt": REFS[name], "batch_size": 1, "resolution": "1080p",
        "aspect_ratio": "1:1" if name in ("owner_hand", "trophy") else "9:16", "enhance_prompt": False})
    hf.wait(refs_ledger, name, REFS_DIR / f"{name}.png", interval=5)


def run_voices():
    out = HERE / "voices" / "design"
    out.mkdir(parents=True, exist_ok=True)
    mp = out / "manifest.json"
    man = json.loads(mp.read_text()) if mp.exists() else {}
    H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
    for name, (desc, text) in VOICES.items():
        if name in man:
            continue
        r = requests.post("https://api.elevenlabs.io/v1/text-to-voice/design", headers=H, json={
            "model_id": "eleven_multilingual_ttv_v2", "voice_description": desc, "text": text,
            "guidance_scale": 5}, timeout=180)
        if not r.ok:
            print(f"voice {name}: HTTP {r.status_code} {r.text[:200]}", flush=True)
            continue
        man[name] = {"voice_description": desc, "text": text, "previews": []}
        for i, p in enumerate(r.json()["previews"], 1):
            f = out / f"{name}-option{i}.mp3"
            f.write_bytes(base64.b64decode(p["audio_base_64"]))
            man[name]["previews"].append({"option": i, "file": f.name, "generated_voice_id": p["generated_voice_id"]})
        mp.write_text(json.dumps(man, indent=2))
        print("voice", name, "designed", flush=True)


if __name__ == "__main__":
    stage, names = sys.argv[1], sys.argv[2:]
    if stage == "refs":
        parallel(run_ref, names or list(REFS))
    elif stage == "voices":
        run_voices()
