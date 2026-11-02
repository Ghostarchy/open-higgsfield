"""TWENTY-FOUR, Episode 1: single source for locks, shots, dialogue and sound.

`python3 story.py` writes SERIES-BIBLE.md with every prompt fully expanded (copy-paste ready).
The production scripts in pipeline/ read the same data, so the bible and the renders never drift.
"""
import pathlib

STYLE = ("Ultra-photorealistic live-action motorsport cinema, shot on ARRI Alexa with anamorphic lenses, "
         "Hollywood racing-film production quality, real-world physics, natural motion blur, heat haze over "
         "the tarmac, realistic reflections on bodywork, natural facial expressions, realistic skin texture, "
         "shallow depth of field, cool desaturated grade with warm highlights, subtle film grain, 9:16 vertical "
         "composition. No real-world brand logos, no readable sponsor text.")

LOCK = {
    "TEO": ("TEO MARSH: a 38-year-old male endurance racing driver, lean face, short dark-blond hair greying at "
            "the temples, pale grey-green eyes, a thin white scar through his left eyebrow, three-day stubble, "
            "matte graphite racing suit with thin silver piping, matte graphite helmet with one silver stripe "
            "over the crown and a white number 4 on the chin bar"),
    "ISLA": ("ISLA FERREIRA: a 26-year-old female endurance racing driver, olive skin, intense dark brown eyes, "
             "straight black eyebrows, black hair in a tight low bun, white racing suit with orange shoulder "
             "panels, white helmet with an orange chevron over the visor and a black number 19 on the chin bar"),
    "DECLAN": ("DECLAN HOLT: Teo's race engineer, a heavy-set man in his late 40s, short dark receding hair, "
               "five-o'clock shadow, sweat on his forehead and temples, black team softshell jacket with a small "
               "silver monogram, black over-ear headset with a boom microphone"),
    "BRIAN": ("BRIAN ASHCROFT: the lead TV commentator, a man in his early 60s, silver swept-back hair, tanned "
              "lined face, light blue eyes, navy suit, white shirt, dark green tie, black broadcast headset with "
              "a boom microphone, a hand microphone with a plain black flag"),
    "CAR4": ("CAR 4, the WRAITH: a matte graphite-black Le Mans-style hypercar prototype, long low body, "
             "enclosed cockpit with a dark tinted canopy, thin white LED light slits, tall rear wing, one thin "
             "silver stripe nose to tail, a large white number 4 on the nose and doors, streaks of dust and tyre "
             "rubber on the bodywork"),
    "CAR19": ("CAR 19: a white Le Mans-style hypercar prototype with sharp orange chevrons over the front "
              "fenders, black underside and splitter, round amber LED headlights, tall rear wing, a large black "
              "number 19 on white door roundels"),
    "TRACK": ("KESTREL BAY CIRCUIT: a modern endurance circuit beside a hazy coastal city skyline with "
              "mountains behind, a long main straight under a covered grandstand, a steel overhead gantry bridge, "
              "blue-and-white kerbs, tarmac streaked with rubber, late-afternoon haze and blowing dust"),
}

# n: (seconds, locks, camera + action + emotion)
SHOTS = {
    1: (3, ["TRACK"], "Lens resting on the asphalt at ground level, extreme low angle along the main straight. A "
        "wall of brown dust and grit rolls toward the camera, small debris and gravel tumble and bounce past the "
        "lens, the concrete pit wall fades into the haze on the left. Handheld micro-shake. Emotion: something "
        "violent is coming out of that dust."),
    2: (3, ["CAR4", "CAR19", "TRACK"], "Same ground-level lens on the asphalt. Two prototypes explode out of the "
        "dust toward camera; CAR 19 roars past the right edge of frame in a blur so close it fills half the "
        "image, CAR 4 follows behind it, headlights cutting through the haze. Motion blur, dust swirling in "
        "their wake. Emotion: speed, danger, closeness."),
    3: (3, ["CAR4", "TRACK"], "Ground-level head-on shot. CAR 4 comes straight at the camera out of the dust "
        "cloud, nose low, light slits glowing, gravel spraying from under the splitter, then passes directly "
        "over the lens. Emotion: the leader, unstoppable."),
    4: (4, ["BRIAN"], "Close-up in a broadcast booth high above the circuit, glass behind him, monitors glowing. "
        "BRIAN ASHCROFT leans into his microphone and speaks with rising intensity, eyes fixed on the track "
        "below, lips moving clearly with his words. Slow push in. Emotion: history is happening."),
    5: (4, ["CAR4", "TRACK"], "High wide shot looking down the pit straight from the gantry, the timing tower on "
        "the left, the packed grandstand on the right. A pack of prototypes in different liveries streams past "
        "in the distance while CAR 4 blasts through the foreground in a heavy motion blur. Slow tilt following "
        "it. Emotion: one car above all the others."),
    6: (4, ["CAR4", "TRACK"], "Tracking shot alongside CAR 4 at wheel height, the front wheel spinning in the "
        "centre of frame, brake disc glowing faintly orange through the spokes, the grandstand streaking past "
        "behind in motion blur. Emotion: power, precision."),
    7: (4, ["CAR4", "TRACK"], "Medium shot from behind a crowd of fans at the fence, a grey-and-silver flag waving "
        "in the foreground out of focus, a woman with long blonde hair smiling up at a giant screen. On the "
        "screen CAR 4 thunders toward the camera. Rack focus from the flag to the screen. Emotion: everyone "
        "is cheering for him."),
    8: (4, ["DECLAN"], "Extreme close-up of a telemetry touchscreen on the pit wall: a red tyre-wear graph spikes "
        "then collapses into a flat line below a dotted warning threshold, red digital readouts flicker at the "
        "bottom. DECLAN HOLT's sweating face is reflected faintly in the glass behind the graph, and his finger "
        "taps the screen. Emotion: something is badly wrong."),
    9: (4, ["DECLAN"], "Close-up of DECLAN HOLT under the red glow of a warning light, sweat running down his "
        "temple. He presses the push-to-talk button on his handheld radio, brings it to his mouth and speaks "
        "urgently, jaw tight, lips moving clearly with the words. Slight handheld drift. Emotion: fear he is "
        "trying to hide."),
    10: (4, ["TEO"], "Symmetrical close-up through the windscreen into the cockpit of CAR 4: TEO MARSH in his "
         "helmet, visor down, strapped in by white harness belts, carbon steering wheel with small red lights "
         "in the foreground. His eyes behind the visor are fixed ahead; he does not answer. The car vibrates "
         "with the engine. Emotion: calm on the outside, something hidden inside."),
    11: (4, ["DECLAN"], "Medium shot of the pit wall: DECLAN HOLT in the foreground leans over the desk with "
         "both hands flat on a stack of papers, a second engineer in a headset behind him stares at the "
         "monitors, the coiled radio cable swinging. Nobody moves. Emotion: the whole team holding its breath."),
    12: (4, ["CAR19", "TRACK"], "Close-up of the black side mirror of CAR 4 at speed, the grandstand smeared into "
         "motion blur around it. In the mirror, CAR 19 grows larger and closer, amber headlights burning, the "
         "hazy city skyline behind it. Rack focus onto the mirror. Emotion: the hunter is coming."),
    13: (4, ["TRACK"], "Over-the-shoulder shot from behind a team strategist in a headset sitting at a wall of "
         "screens in the pit box: a live feed of two prototypes nose to tail through a corner, a track map "
         "with a moving dot, live telemetry traces. He grips his microphone. Emotion: the gap is closing."),
    14: (4, ["CAR4", "TRACK"], "Very wide, long-lens shot down an empty straight, the coastal city skyline and "
         "mountains in the haze behind the steel gantry. CAR 4 appears small in the distance and charges "
         "toward camera through heat haze. Emotion: loneliness at the front."),
    15: (4, ["ISLA"], "Extreme close-up of ISLA FERREIRA inside her cockpit, visor up a crack, dark eyes narrowed, "
         "sweat at her brow. In the reflection on her visor, a graphite car with a white number 4 grows ahead "
         "of her. She exhales slowly and her eyes harden. Emotion: three years of waiting end now."),
    16: (6, ["CAR4", "CAR19", "TRACK"], "Low-angle tracking shot in slow motion: CAR 4 and CAR 19 side by side "
         "into the braking zone, wheels inches apart, sparks spraying from both floors, dust and rubber smoke "
         "kicking up, the grandstand roaring behind. Emotion: the moment everything is decided."),
    17: (4, ["TEO"], "Extreme close-up through the visor of TEO MARSH: his eyes blink hard, then again, his pupils "
         "struggle to focus, a bead of sweat runs into his eye. His face stays still but his breathing quickens "
         "behind the visor. Emotion: something is wrong with him, not the car."),
    18: (4, ["BRIAN"], "Medium close-up: BRIAN ASHCROFT jumps up out of his chair in the commentary booth, one "
         "hand pressed to his headset, the other pointing at the track, shouting into the microphone, lips "
         "moving clearly with his words, the colleague beside him on his feet too. Emotion: euphoric disbelief."),
    19: (4, ["CAR4", "CAR19", "TRACK"], "High angle crane shot over the final chicane: CAR 4 brakes late, its rear "
         "end steps out and smokes, it slides wide over the blue-and-white kerb, CAR 19 dives up the inside and "
         "the two cars touch with a puff of carbon fibre. Emotion: chaos."),
    20: (5, ["DECLAN"], "Close-up of DECLAN HOLT pressing his headset to his ear with both hands, eyes closed, "
         "listening. Then his eyes open wide, his face drains, and his mouth falls slightly open in horror. "
         "He does not speak. Emotion: he has just heard the truth."),
    21: (4, ["TEO"], "Point of view through the dark tinted visor of CAR 4 at speed: the finish gantry ahead "
         "splits into two blurred images, the edges of the world smear and double, low sun flares across the "
         "visor scratches, the steering wheel lights glow at the bottom of frame. Emotion: dread."),
}

# (start_s, speaker, text, on_camera) - speakers on camera are lip-synced with Seedance.
DIALOGUE = [
    (0.6, "BRIAN (VO)", "Twenty-three hours and fifty-nine minutes.", False),
    (3.6, "BRIAN (VO)", "Three thousand miles... and it comes down to one.", False),
    (9.4, "BRIAN", "And the black number four still leads. Teo Marsh.", True),
    (17.4, "BRIAN (VO)", "Five times he has won here. Never by this little.", False),
    (29.4, "DECLAN", "Teo, your rears are down to the canvas. Do you copy?", True),
    (34.0, "DECLAN (VO)", "Teo. Do you copy?", False),
    (45.4, "STRATEGIST (VO)", "Ferreira is coming. Point four. Point three.", False),
    (49.6, "BRIAN (VO)", "Three years as his reserve driver. Three years in his shadow.", False),
    (67.4, "BRIAN", "Side by side! Nobody in this place is breathing!", True),
    (75.8, "TEO (radio, VO)", "Declan... I can't see the line.", False),
]

CARD = ["HE'S BEEN DRIVING", "HALF BLIND FOR SIX HOURS."]

SOUND = [
    ("0-3", "Low wind roar through dust, grit pattering on the lens, a distant engine rising"),
    ("3-9", "Two engines screaming past the lens (doppler), gravel spray, then car 4's pass over the lens"),
    ("9-13", "Broadcast-booth room tone under Brian; muffled crowd through the glass"),
    ("13-25", "Crowd roar, flags snapping, PA echo; score: pulsing low synth and taiko at 120 bpm"),
    ("25-33", "Score drops to a ticking hi-hat; telemetry beeps; radio squelch before and after Declan"),
    ("33-37", "Inside the cockpit: engine drone, helmet breathing, empty radio hiss (no reply)"),
    ("41-49", "Engine note of car 19 growing; score swells with low strings; strategist's countdown"),
    ("57-63", "Two engines at the limiter; at 58 everything drops to slow motion: one heartbeat, a sub boom"),
    ("63-67", "Teo's breathing loud and close; a high tinnitus tone fades in"),
    ("67-75", "Brian shouting over a roaring crowd; tyre squeal, carbon crunch at 73, crowd gasp; score cuts out"),
    ("75-80", "Radio crackle under Teo's whisper; dead silence after it"),
    ("80-84", "Tinnitus tone rises; engine fades; heartbeat"),
    ("84-90", "Hard cut to black on one low drum hit; nothing after"),
]

CAPTION = ("He led for 23 hours and 59 minutes. Then the radio went quiet. 🏁 EP01 | TWENTY-FOUR "
           "#racing #motorsport #lemans #shortdrama #aistory #cinematic")
PINNED = "EP02 tomorrow. How long has his team known? 👀"


def timeline():
    t, rows = 0, []
    for n, (secs, _, _) in SHOTS.items():
        rows.append((n, t, t + secs))
        t += secs
    return rows, t


def prompt(n):
    secs, locks, action = SHOTS[n]
    return " ".join([action] + [LOCK[k] + "." for k in locks] + [STYLE])


def write_bible():
    rows, end = timeline()
    assert end + 6 == 90, f"shots end at {end}s; the card needs the last 6 s"
    md = ["# TWENTY-FOUR — Series Bible and Episode 1", "",
          "Original endurance-racing drama for TikTok, Reels and Shorts (9:16, 90 s episodes). The visual language "
          "follows the supplied reference frames (ground-level dust shots, pit-wall close-ups, broadcast booth, "
          "mirror reveals, helmet visor close-ups, italic centred subtitles); the characters, cars, team, circuit "
          "and story are original.", "",
          "## Premise", "",
          "Teo Marsh, five-time winner of the Kestrel Bay 24 Hours, leads his final race by seconds with one minute "
          "left. His tyres are gone and his radio has gone silent. Closing in is Isla Ferreira, the reserve driver he "
          "kept on the bench for three years. The secret nobody in his team knows: Teo is losing the sight in one "
          "eye, and for the last six hours he has been driving from memory.", "",
          "Series engine: every episode is one stretch of a single 24-hour race, told out of order, each ending on a "
          "revelation that changes what the last episode meant.", "",
          "## Locked descriptions", "",
          "Paste these word for word. Every prompt below already contains the ones it needs.", ""]
    md += [f"**{k}**\n> {v}\n" for k, v in LOCK.items()]
    md += [f"**STYLE**\n> {STYLE}\n", "## Episode 1 — \"The Last Minute\"", "",
           "| Time | Shot | Beat |", "|---|---|---|"]
    for n, a, b in rows:
        md.append(f"| {a}–{b} s | {n} | {SHOTS[n][2].split('. ')[0]} |")
    md += [f"| 84–90 s | card | Black. {' / '.join(CARD)} |", "",
           "### Dialogue and voiceover", "",
           "| Time | Who | Line | Lip sync |", "|---|---|---|---|"]
    md += [f"| {s:.1f} s | {w} | \"{t}\" | {'Seedance (on camera)' if oc else '—'} |" for s, w, t, oc in DIALOGUE]
    md += ["", "Subtitles: white italic sans, centred in the lower middle, 1–6 words per card, timed to the line "
           "(the reference style).", "", "### Shot prompts", "",
           "Kling 3.0 Pro image-to-video, sound off, from a start frame made from the locked references. "
           "Shots with an on-camera line (4, 9, 18) render with Seedance 2.0 image-to-video plus the shot-timed "
           "dialogue audio so the lips match the voice.", ""]
    for n, a, b in rows:
        secs, locks, _ = SHOTS[n]
        md += [f"**SHOT {n} — {a}–{b} s** · {secs} s · locks: {', '.join(locks)}", "", "```", prompt(n), "```", ""]
    md += ["### Sound and music", "", "| Time (s) | Cue |", "|---|---|"]
    md += [f"| {t} | {c} |" for t, c in SOUND]
    md += ["", "### Posting", "", f"**Caption:** {CAPTION}", "", f"**Pinned comment:** {PINNED}", "",
           "## Season arc (first 10)", "",
           "1. The Last Minute — Teo can't see the line; Isla is alongside.",
           "2. Hour 18 — the night stint where Teo first sees double, and hides it from Declan.",
           "3. The Finish — who crossed first, and why the stewards are holding the result.",
           "4. Three Years Ago — the day Teo kept Isla out of the car.",
           "5. Declan's Choice — the engineer knew at hour 20 and told no one.",
           "6. The Team Owner — the contract clause that made Teo race no matter what.",
           "7. The Doctor — the scan Teo never opened.",
           "8. Isla's Radio — what her own engineer told her to do at the chicane.",
           "9. The Contact — slow-motion replay; it wasn't an accident.",
           "10. The Podium — one of them refuses to stand on it.", "",
           "## Production notes", "",
           "- References to lock first: Teo, Isla, Declan, Brian, car 4, car 19 (each car three-quarter front and side).",
           "- Never put real brands, real circuits or real broadcasters in frame; ask for plain flags and blank screens.",
           "- Lip sync: Seedance 2.0 `image-to-video` with `audio_urls` (tested: 1080p, 24 fps, full motion).",
           "- Helmeted drivers never need lip sync: their lines are radio voiceover.",
           "- Readable text (names, numbers on screens) is added in post; generated text is unreliable.",
           "- Reference screenshots stay local (`reference/`, git-ignored): they are another creator's frames."]
    pathlib.Path(__file__).with_name("SERIES-BIBLE.md").write_text("\n".join(md) + "\n")
    print("shots", len(SHOTS), "end", end, "max prompt", max(len(prompt(n)) for n in SHOTS))


if __name__ == "__main__":
    write_bible()
