"""EP01 v2 production, driven entirely by SEASON-1-BIBLE.md (locks, shot list, prompts).

  python3 produce2.py <ep_dir> refs                # new series references: mira4, sigrun, grima, toy
  python3 produce2.py <ep_dir> frames 1 2 ...      # start frames (Flux 2 Pro + locked references)
  python3 produce2.py <ep_dir> clips 1 2 ...       # Kling 3 Pro (no dialogue) / Seedance 2.0 + audio (dialogue)
  python3 produce2.py <ep_dir> snow                # drifting-snow particle plate for the overlay layer
Every request ID is recorded the moment it is queued (ep manifest, or series references.json).
"""
import re, sys, pathlib, threading
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import hf

ep = pathlib.Path(sys.argv[1])
series = ep.parent
stage, which = sys.argv[2], sys.argv[3:]
for d in ("frames", "clips", "audio/shots"):
    (ep / d).mkdir(parents=True, exist_ok=True)
ledger = hf.Ledger(ep / "manifest.json")
refs_ledger = hf.Ledger(series / "references.json")
bible = (series / "SEASON-1-BIBLE.md").read_text()

# Locks: the blockquotes in section 3, keyed by the bold name above each.
LOCK = {}
for name, quote in re.findall(r"\*\*([A-Z][A-Z ]+?)\*\*[^\n]*\n((?:> .*\n)+)", bible):
    LOCK[name.strip()] = " ".join(l[2:].strip() for l in quote.strip().splitlines())
STYLE = LOCK.pop("STYLE LINE")

# Shots: header line, Start frame text, and the fenced Kling prompt.
SHOTS = {}
for m in re.finditer(
        r"\*\*SHOT (\d+) — [^*]*\*\* · (\d+) s · refs: ([^\n·]+)(·[^\n]*)?\nStart frame: (.*?)\n\n```\n(.*?)\n```",
        bible, re.S):
    n, secs, refs, extra, start, motion = m.groups()
    names = [] if refs.strip() == "none" else [r.strip().lower() for r in refs.split(",")]
    SHOTS[int(n)] = {"secs": int(secs), "refs": names, "lipsync": "LIP SYNC" in (extra or ""),
                     "end_frame": "first+last" in (extra or ""), "start": " ".join(start.split()),
                     "motion": motion.strip()}
assert len(SHOTS) == 16, f"parsed {len(SHOTS)} shots from the bible"

# Reference image per name used in the shot list.
REF_KEY = {"mira": "mira4", "vorr": "vorr", "asha": "asha", "sigrun": "sigrun", "grima": "grima"}
REF_LOCK = {"mira": "MIRA", "vorr": "VORR", "asha": "ASHA", "sigrun": "SIGRUN", "grima": "GRIMA"}

NEW_REFS = {
    "mira4": f"Character reference, full body, front view, a real four-year-old preschool girl (not a baby, "
             f"natural healthy child proportions, slender), gentle sweet sad expression, soft unfocused gaze, "
             f"thick grey wool leggings under the tunic, standing alone in deep snow outside a stone hall at "
             f"dawn, face clearly visible, no face paint. {LOCK['MIRA']}. {STYLE}",
    "sigrun": f"Character reference, three-quarter view showing the left side of her head, which is shaved "
              f"close to the scalp, the rest of her copper-red hair swept to the right into one thick braid, "
              f"standing in a snowy stone arena, confident, face clearly visible. {LOCK['SIGRUN']}. {STYLE}",
    "grima": f"Character reference, waist-up, front view, face clearly visible: her LEFT eye is clouded milky "
             f"white and her RIGHT eye is a sharp clear grey, rows of small blue dot tattoos across her forehead "
             f"and down her chin, a grave and wise expression, real elderly woman, standing in falling snow "
             f"beside a stone wall. {LOCK['GRIMA']}. {STYLE}",
    "toy": "Prop reference, close-up three-quarter view of a palm-sized hand-carved pale birch-wood figurine "
           "of a sitting wolf, unmistakably a wolf: long pointed snout, two tall upright pointed ears, carved "
           "eyes, a bushy tail curled around its paws, visible knife marks. Its left ear has a clear V-shaped "
           "notch cut out of the tip; the right ear is whole. Resting on grey wolf fur in soft daylight, "
           f"shallow depth of field, photorealistic. {STYLE}",
}


def ref_url(name):
    return refs_ledger.data[REF_KEY.get(name, name)]["url"]


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
        "prompt": NEW_REFS[name], "batch_size": 1, "resolution": "1080p",
        "aspect_ratio": "1:1" if name == "toy" else "9:16", "enhance_prompt": False})
    hf.wait(refs_ledger, name, series / "references" / f"{name}.png", interval=5)


def frame_prompt(n):
    s = SHOTS[n]
    parts = [s["start"]]
    parts += [LOCK[REF_LOCK[r]] + "." for r in s["refs"]]
    if "mira" in s["refs"] and "asha" in s["refs"]:
        parts.append("Only Asha wears war paint; Mira's small face is clean with no paint or markings.")
    if s["refs"]:
        # Mira's reference carries the wooden wolf toy; the standalone toy renders never read as a wolf.
        parts.append("Match the reference images exactly: " + ", ".join(
            f"reference {i + 1} is {r.title()}" for i, r in enumerate(s["refs"])) + ".")
    parts.append(STYLE)
    return " ".join(parts)


def run_frame(n):
    n = int(n)
    s = SHOTS[n]
    refs = s["refs"]
    body = {"prompt": frame_prompt(n), "aspect_ratio": "9:16", "resolution": "2k"}
    if refs:
        body["image_urls"] = [ref_url(r) for r in refs]
    key = f"shot{n:02d}-frame"
    hf.submit(ledger, key, "flux-2-pro", body)
    hf.wait(ledger, key, ep / "frames" / f"shot{n:02d}.png", interval=5)
    if s["end_frame"]:
        k2 = f"shot{n:02d}-end-frame"
        hf.submit(ledger, k2, "flux-2-pro", {
            "prompt": "The same close-up of the same little girl, same framing and lighting, now her eyes glow "
                      "bright ice-blue with light and one small arm is raised, pointing past the camera, calm "
                      f"and certain. {LOCK['MIRA']}. {STYLE}",
            "aspect_ratio": "9:16", "resolution": "2k",
            "image_urls": [ledger.data[key]["url"], ref_url("mira")]})
        hf.wait(ledger, k2, ep / "frames" / f"shot{n:02d}-end.png", interval=5)


RAW = ("https://raw.githubusercontent.com/Ghostarchy/open-higgsfield/claude/fervent-johnson-ls3c84/"
       "ice-wolves/{ep}/audio/shots/{name}")


def run_clip(n):
    n = int(n)
    s = SHOTS[n]
    key = f"shot{n:02d}-clip"
    start = ledger.data[f"shot{n:02d}-frame"]["url"]
    if s["lipsync"]:
        # Seedance 2.0 image-to-video driven by the shot-timed dialogue: full motion, mouths on the words.
        model = "bytedance/seedance-2.0/image-to-video"
        body = {"prompt": s["motion"] + " The speaking character's lips move precisely in sync with the "
                "dialogue audio; everyone else keeps their mouth closed.",
                "image_url": start, "audio_urls": [RAW.format(ep=ep.name, name=f"shot{n:02d}.wav")],
                "duration": max(4, s["secs"]), "resolution": "1080p", "generate_audio": False}
    else:
        model = "kling-video/v3.0/pro/image-to-video"
        body = {"prompt": s["motion"], "sound": "off", "duration": s["secs"], "cfg_scale": 0.5,
                "multi_shots": False, "image_url": start}
        end = ledger.data.get(f"shot{n:02d}-end-frame", {}).get("url")
        if end:
            body["last_image_url"] = end
    hf.submit(ledger, key, model, body)
    hf.wait(ledger, key, ep / "clips" / f"shot{n:02d}.mp4", interval=15)


def run_snow():
    hf.submit(ledger, "snow-plate", "kling-video/v3.0/pro/text-to-video", {
        "prompt": "Large and small soft snowflakes drifting slowly downward and slightly sideways in the "
                  "wind, a few close to camera and out of focus, isolated on a pure black background, no "
                  "ground, no objects, no people, seamless, cinematic particle plate, 9:16 vertical.",
        "sound": "off", "duration": 15, "cfg_scale": 0.5, "multi_shots": False, "aspect_ratio": "9:16"})
    hf.wait(ledger, "snow-plate", ep / "clips" / "snow-plate.mp4", interval=15)


if stage == "refs":
    parallel(run_ref, which or list(NEW_REFS))
elif stage == "frames":
    parallel(run_frame, which)
elif stage == "clips":
    parallel(run_clip, which)
elif stage == "snow":
    run_snow()
elif stage == "show":
    n = int(which[0]); print(frame_prompt(n)); print(SHOTS[n])
