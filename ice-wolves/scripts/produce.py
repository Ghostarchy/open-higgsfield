"""The Blind Girl the Ice Wolves Chose: character references, start frames, Kling 3 Pro clips, cover.

  python3 produce.py <ep_dir> refs                 # 4 locked character references (Soul Cinema)
  python3 produce.py <ep_dir> frames 1 2 ...       # per-shot start frames (Flux 2 Pro + references)
  python3 produce.py <ep_dir> clips 1 2 ...        # Kling 3 Pro image-to-video, sound off
  python3 produce.py <ep_dir> cover                # cover art (title added in post)
Every request ID is written to <ep_dir>/manifest.json the moment it is queued.
"""
import sys, pathlib, threading
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import hf

ep = pathlib.Path(sys.argv[1])
stage, which = sys.argv[2], sys.argv[3:]
for d in ("refs", "frames", "clips", "cover"):
    (ep / d).mkdir(parents=True, exist_ok=True)
ledger = hf.Ledger(ep / "manifest.json")
# References are series-level: episode 1 creates them, later episodes reuse the same URLs.
series_ledger = hf.Ledger(ep.parent / "references.json")

STYLE = ("epic cinematic fantasy, frozen mountain clan, snow falling, pale blue and silver tones with "
         "warm torchlight, shallow depth of field, film grain, photorealistic, 9:16 vertical")

MIRA = ("Mira, a 7-year-old girl with pale silver-blonde braided hair, cloudy pale blue eyes, a small "
        "scar on her chin, an oversized grey fur cloak and wrapped leather boots")
ASHA = ("Asha the chieftain, a woman in her 40s with dark braided hair threaded with bone beads, a war "
        "paint stripe across her eyes, a heavy fur mantle over steel armor, carrying a spear")
KAELEN = ("Kaelen, a smug 9-year-old boy with red hair in a fine fur coat with a gold clasp, the "
          "chieftain's son")
VORR = ("Vorr, an ancient ice wolf the size of a house, white fur with a frost-crusted mane, one torn "
        "ear, glowing amber eyes")

REFS = {
    "mira": f"Character reference, full body, front view, {MIRA}, standing in deep snow in a mountain "
            f"clan village at dawn, face clearly visible, eyes open and unfocused. {STYLE}",
    "asha": f"Character reference, full body, front view, {ASHA}, standing in a frozen stone arena, "
            f"face clearly visible, stern. {STYLE}",
    "kaelen": f"Character reference, full body, front view, {KAELEN}, standing in snow, arms crossed, "
              f"smirking, face clearly visible. {STYLE}",
    "vorr": f"Creature reference, full body, three-quarter view, {VORR}, lying in snow beside a "
            f"warrior for scale who reaches only to its shoulder. {STYLE}",
}


def ref_url(name):
    return series_ledger.data[name]["url"]


# n: (duration_s, [reference names], start-frame prompt, motion prompt)
SHOTS = {
    1: (5, ["vorr", "mira"],
        "Extreme close-up of one giant glowing amber wolf eye, half closed, frost crystals in the white "
        "fur around it, swirling snowstorm, a tiny child's hand at the edge of frame.",
        "Extreme close-up. The giant amber wolf eye snaps open through swirling snow, frost on its white "
        "fur, a tiny child's hand slowly reaches into frame toward it."),
    2: (5, ["vorr"],
        f"Wide establishing shot of a frozen stone arena carved into a mountainside, hundreds of fur-clad "
        f"clan warriors holding torches watching from stone tiers, in the snowy center lies {VORR}.",
        f"Wide establishing shot, slow aerial push in. A frozen stone arena carved into a mountainside, "
        f"hundreds of fur-clad clan warriors with torches watching from stone tiers, {VORR} lying in the "
        f"center, its breath steaming."),
    3: (5, ["vorr"],
        f"Medium shot in the snowy arena: a small child in furs walking nervously toward {VORR}, which "
        f"is lying down, the clan watching behind.",
        f"Medium shot. A small child in furs walks toward the giant white wolf. The wolf lifts its head "
        f"and snarls, the child screams and runs back to the crowd crying."),
    4: (5, ["kaelen"],
        f"Medium shot: {KAELEN} swaggering into the snowy stone arena, chin up, warriors with torches "
        f"behind him.",
        f"Medium shot. {KAELEN} swaggers into the arena with his chin up, warriors behind him cheer and "
        f"raise torches. He does not speak, mouth closed."),
    5: (5, ["vorr", "kaelen"],
        f"Low angle shot: {VORR} rising to its feet and towering over {KAELEN}, who stands frozen in "
        f"the snow, the crowd on the tiers behind.",
        f"Low angle. The giant white wolf rises and roars down at the red-haired boy, snow blasting off "
        f"its mane. The boy falls backward into the snow. The crowd gasps."),
    6: (5, ["mira"],
        f"Medium shot: {MIRA} stepping out from the edge of the crowd holding a wooden walking stick, "
        f"her eyes unfocused, her small face clean with no paint or markings, children in furs beside "
        f"her pointing at her.",
        f"Medium shot. The blind girl steps out from the crowd tapping a walking stick on the snow. "
        f"Children nearby point at her and laugh."),
    7: (5, ["asha", "mira"],
        f"Two-shot: {ASHA} kneeling in the snow in front of {MIRA}, gripping the girl's shoulder, "
        f"worried, Asha's face in profile. Only Asha wears war paint; the girl's face is clean with no "
        f"paint or markings.",
        f"Two-shot. The chieftain kneels and grips the little girl's shoulder, shaking her head, worried. "
        f"Her face is in profile and her mouth is hidden by her fur mantle. The girl stays calm."),
    8: (7, ["mira", "vorr"],
        f"Tracking shot from behind: {MIRA} walking alone across the empty snowy arena with her walking "
        f"stick, small footprints behind her, the huge shape of {VORR} ahead in the fog.",
        "Tracking shot from behind. The little girl in the grey fur cloak walks alone across the empty "
        "snowy arena toward the giant wolf, leaving small footprints, the wolf's huge shape ahead in fog."),
    9: (8, ["mira", "vorr"],
        f"Tension shot: {VORR} lowering its huge head until its bared teeth are inches from the face of "
        f"{MIRA}, its breath fogging her hair, warriors raising spears in the background, she stands "
        f"perfectly still.",
        "The giant wolf lowers its head until its bared teeth are inches from the little girl's face, "
        "its breath fogging her hair. Warriors in the background raise their spears. The girl stands "
        "perfectly still and does not flinch. Her lips stay closed."),
    10: (12, ["mira", "vorr"],
         f"Power moment: {MIRA} raising her small hand toward {VORR}, whose massive head is lowered "
         f"close to her, snow falling in silence.",
         "Power moment. The little girl slowly raises her small hand. The giant wolf goes silent, closes "
         "its amber eyes and presses its nose gently into her palm. Glowing ice-blue frost runes spread "
         "up her arm. Slow orbiting camera."),
    11: (10, ["asha", "kaelen"],
         f"Reaction shot: {ASHA} standing frozen in silent shock, wide eyes, lips barely parted, her "
         f"spear slipping from her loosened fingers toward the snow; behind her {KAELEN} staring with his "
         f"mouth open; clan warriors with torches on the stone tiers.",
         "Reaction shot. The chieftain drops her spear into the snow. The red-haired boy's mouth falls "
         "open. Then the entire clan of warriors slowly kneels on the stone tiers, torches lowering."),
    12: (5, [],
         "Far up a snowy mountain pass, a massive black iron gate wrapped in heavy chains, set into the "
         "cliff, storm clouds above.",
         "Deep war horns blow across the mountains. Far up the snowy pass, the massive black iron gate "
         "wrapped in chains cracks open, snow falling from the chains."),
    13: (5, ["vorr"],
         f"Split depth: in the foreground {VORR} turning its head toward a distant black gateway high on "
         f"the mountain pass, darkness inside the gate.",
         "Inside the dark gateway, dozens of glowing red eyes open one by one in the blackness. The giant "
         "white wolf turns its head and growls toward the pass, hackles rising."),
    14: (4, ["mira"],
         f"Extreme close-up on the face of {MIRA}, cloudy pale blue eyes, snowflakes on her lashes.",
         "Extreme close-up on the little girl's face. Her cloudy eyes slowly turn bright glowing ice-blue "
         "and she smiles slightly."),
}

COVER = (f"Snowy mountain valley at dawn, pale blue and silver tones. In the center stands {MIRA}, tiny "
         f"in the frame. Behind her {VORR} towers and lowers its head. Two clan warriors in full "
         f"fur-and-steel armor kneel on either side of her. Empty sky in the top third of the frame "
         f"for a title. No text, no letters. {STYLE}")


def run_refs():
    def one(name):
        if series_ledger.data.get(name, {}).get("status") == "completed":
            return
        hf.submit(series_ledger, name, "higgsfield-ai/soul/cinema", {
            "prompt": REFS[name], "batch_size": 1, "resolution": "1080p",
            "aspect_ratio": "9:16", "enhance_prompt": False})
        hf.wait(series_ledger, name, ep.parent / "references" / f"{name}.png", interval=5)
    (ep.parent / "references").mkdir(exist_ok=True)
    parallel(one, list(REFS))


def run_frame(n):
    n = int(n)
    secs, refs, frame, _ = SHOTS[n]
    key = f"shot{n:02d}-frame"
    body = {"prompt": f"{frame} {STYLE}", "aspect_ratio": "9:16", "resolution": "2k"}
    if refs:
        body["image_urls"] = [ref_url(r) for r in refs]
        body["prompt"] += " Match the characters exactly to the reference images: " + ", ".join(
            f"reference {i + 1} is {r.title()}" for i, r in enumerate(refs)) + "."
    hf.submit(ledger, key, "flux-2-pro", body)
    hf.wait(ledger, key, ep / "frames" / f"shot{n:02d}.png", interval=5)


def run_clip(n):
    n = int(n)
    secs, _, _, motion = SHOTS[n]
    key = f"shot{n:02d}-clip"
    body = {"prompt": f"{motion} {STYLE}", "sound": "off", "duration": secs, "cfg_scale": 0.5,
            "multi_shots": False, "image_url": ledger.data[f"shot{n:02d}-frame"]["url"]}
    end = ledger.data.get(f"shot{n:02d}-end-frame", {}).get("url")
    if end:
        body["last_image_url"] = end
    hf.submit(ledger, key, "kling-video/v3.0/pro/image-to-video", body)
    hf.wait(ledger, key, ep / "clips" / f"shot{n:02d}.mp4", interval=15)


def run_end_frame_14():
    # Shot 14 is pinned to an end frame so the eyes reliably finish glowing ice-blue.
    key = "shot14-end-frame"
    hf.submit(ledger, key, "flux-2-pro", {
        "prompt": f"The same extreme close-up of the same girl, now her eyes glow bright ice-blue with "
                  f"light, a slight knowing smile, snowflakes on her lashes. {STYLE}",
        "aspect_ratio": "9:16", "resolution": "2k",
        "image_urls": [ledger.data["shot14-frame"]["url"], ref_url("mira")]})
    hf.wait(ledger, key, ep / "frames" / "shot14-end.png", interval=5)


def run_cover():
    hf.submit(ledger, "cover", "flux-2-pro", {
        "prompt": COVER + " Reference 1 is Mira, reference 2 is Vorr.", "aspect_ratio": "9:16",
        "resolution": "2k", "image_urls": [ref_url("mira"), ref_url("vorr")]})
    hf.wait(ledger, "cover", ep / "cover" / "cover-art.png", interval=5)


def parallel(fn, items):
    threads = [threading.Thread(target=fn, args=(i,)) for i in items]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if stage == "refs":
    run_refs()
elif stage == "frames":
    parallel(run_frame, which)
elif stage == "end14":
    run_end_frame_14()
elif stage == "clips":
    parallel(run_clip, which)
elif stage == "cover":
    run_cover()
