"""Episode 1 shots: per-shot start frames (Flux 2 Pro, approved stills as references) and Kling 3 Pro clips.

  python3 shots.py <episode_dir> frames 1 2 3 4   # start frames
  python3 shots.py <episode_dir> clips 1 2 3 4 5  # Kling clips (1-4 need their frame)
Request IDs go to shots/manifest.json as soon as they are queued.
"""
import sys, pathlib, json, threading
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import hf

ep = pathlib.Path(sys.argv[1])
stage, which = sys.argv[2], sys.argv[3:]
out = ep / "shots"
out.mkdir(exist_ok=True)
ledger = hf.Ledger(out / "manifest.json")
stills = json.loads((ep / "stills/manifest.json").read_text())
ELENA_REF, LUCIEN_REF = stills["elena"]["url"], stills["lucien-v2"]["url"]

# Character descriptions verbatim from the brief; Lucien's wardrobe clarification follows his.
E = ("a woman in her late twenties with long dark wavy hair, wearing a fitted black button-up "
     "blouse with a collar")
L = ("a tall man in his thirties with sharp features and short dark hair, wearing a dark suit, "
     "tie pulled loose, top shirt button undone, no pocket square, plain jacket breast pocket, "
     "white shirt open at the throat")
GRADE = ("candlelit, warm amber highlights, deep black shadows, slight film grain, "
         "cinematic dark romance film, vertical 9:16 frame")
NO_TALK = "No one speaks; lips stay closed."

SHOTS = {
    "1": {
        "refs": [ELENA_REF],
        "frame": (f"Extreme close-up looking down at an antique leather ledger with yellowed pages "
                  f"on a wooden desk, faded handwritten brown ink on the page reads "
                  f"\"Elena Marlowe — died 1 November\". The index finger of {E} rests on the "
                  f"ink; only her hand and black blouse cuff are visible. A single candle flame at "
                  f"the edge of frame. Use the woman in the reference image. {GRADE}."),
        "motion": (f"Extreme close-up, candlelight. The finger of {E} slowly traces the faded "
                   f"handwritten ink on the yellowed ledger page and trembles. Slow push in. Near the "
                   f"end the camera tilts up to her face as she looks up sharply, eyes wide, face lit "
                   f"from below by the candle. {NO_TALK} {GRADE}."),
    },
    "2": {
        "refs": [ELENA_REF, LUCIEN_REF],
        "frame": (f"Medium shot at eye level, 85mm lens, chest-height camera. {E} stands in a "
                  f"narrow aisle between towering antique bookshelves, clutching an old leather "
                  f"ledger to her chest, facing camera. Behind her, deeper in the aisle, {L} is "
                  f"stepping out of the shadows, half his face in candlelight, his mouth in shadow. "
                  f"The woman is the woman in the first reference image; the man is the man in the "
                  f"second reference image. {GRADE}."),
        "motion": (f"Medium shot, eye level, 85mm. {E} clutches the leather ledger to her chest. "
                   f"Behind her, {L} steps slowly out of the shadows toward her, half his face in "
                   f"candlelight; candle flames flicker as he passes. She turns around to face him, "
                   f"her face turning away from camera. {NO_TALK} {GRADE}."),
    },
    "3": {
        "refs": [ELENA_REF, LUCIEN_REF],
        "frame": (f"Extreme close-up of hands on an antique leather ledger. The smooth, youthful "
                  f"hand of a tall man in his thirties in a dark suit sleeve hovers just above and "
                  f"beside the slender hand of a woman in "
                  f"her late twenties wearing a fitted black blouse sleeve as she grips the ledger. "
                  f"Candlelight, very shallow depth of field. Sleeves match the people in the "
                  f"reference images. {GRADE}."),
        "motion": (f"Extreme close-up, the hand of a tall man in his thirties in a dark suit sleeve "
                   f"slowly slides over the hand of a woman in her late twenties wearing a fitted "
                   f"black blouse sleeve as she holds the antique leather ledger. Candlelight, "
                   f"shallow depth of field, intimate tension, slow motion. {GRADE}."),
    },
    "4": {
        "refs": [ELENA_REF, LUCIEN_REF],
        "frame": (f"Close-up. {L} leans in behind {E}, his lips near her ear, the lower half of his "
                  f"face hidden behind her long dark wavy hair. Her eyes are closed, lips parted "
                  f"slightly. Candlelit library, warm amber light. The woman is the woman in the "
                  f"first reference image; the man is the man in the second. {GRADE}."),
        "motion": (f"Close-up. {L} leans in behind {E}, his lips near her ear, his mouth hidden "
                   f"behind her hair. Her eyes stay closed and her breath catches. Very slow push "
                   f"in on her face. Candlelit library, warm amber light, cinematic dark romance. "
                   f"{NO_TALK} {GRADE}."),
    },
    "5": {
        "motion": (f"The antique leather ledger lies open alone on a wooden reading desk at the end "
                   f"of a dark library aisle lined with lit candles. One by one the candles go out, "
                   f"moving toward the camera. The pages flip on their own and stop on a blank page. "
                   f"Ink bleeds onto the paper and writes a new line by itself in old handwriting: "
                   f"\"Lucien — died 1 November\". The last candle goes out into total "
                   f"darkness. No people. {GRADE}."),
    },
}


def frame(n):
    key = f"shot{n}-frame"
    hf.submit(ledger, key, "flux-2-pro", {
        "prompt": SHOTS[n]["frame"], "aspect_ratio": "9:16", "resolution": "2k",
        "image_urls": SHOTS[n]["refs"]})
    hf.wait(ledger, key, out / f"shot{n}-frame.png", interval=5)


def clip(n):
    key = f"shot{n}-clip"
    body = {"prompt": SHOTS[n]["motion"], "sound": "off", "duration": 12,
            "cfg_scale": 0.5, "multi_shots": False}
    if n == "5":
        model = "kling-video/v3.0/pro/text-to-video"
        body["aspect_ratio"] = "9:16"
    else:
        model = "kling-video/v3.0/pro/image-to-video"
        body["image_url"] = ledger.data[f"shot{n}-frame"]["url"]
    hf.submit(ledger, key, model, body)
    hf.wait(ledger, key, out / f"shot{n}.mp4", interval=15)


job = {"frames": frame, "clips": clip}[stage]
threads = [threading.Thread(target=job, args=(n,)) for n in which]
for t in threads:
    t.start()
for t in threads:
    t.join()
