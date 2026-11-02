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
    "MARA": ("MARA MARSH: Teo's wife, early 30s, wavy shoulder-length chestnut-brown hair, hazel eyes, light "
             "freckles across her nose, black wool coat over a grey knit sweater, a thin silver wedding band"),
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
    5: (3, ["CAR4", "TRACK"], "High wide shot looking straight down the pit straight from the gantry, the timing "
        "tower with blank orange position boards on the left, the packed grandstand throwing long shadows on the "
        "right. CAR 4 leads CAR 19 nose to tail far below, small in frame. Slow tilt following them. Emotion: "
        "two cars alone at the front."),
    6: (3, ["CAR4", "TRACK"], "Tracking shot alongside CAR 4 at wheel height, the front wheel spinning in the "
        "centre of frame, brake disc glowing faintly orange through the spokes, the grandstand streaking past "
        "behind in motion blur. Emotion: power, precision."),
    7: (3, ["MARA"], "Close-up of MARA MARSH pressed against the trackside fence among cheering fans, everyone "
        "around her shouting with raised arms while she alone is silent, lips pressed together, eyes fixed on "
        "the track, her hand with the wedding band gripping the steel rail. Shallow depth of field. Emotion: she "
        "knows something no one else does."),
    8: (3, ["DECLAN"], "Extreme close-up of a telemetry touchscreen on the pit wall: a red tyre-wear graph spikes "
        "then collapses into a flat line below a dotted warning threshold, red digital readouts flicker at the "
        "bottom. DECLAN HOLT's sweating face is reflected faintly in the glass behind the graph, and his finger "
        "taps the screen. Emotion: something is badly wrong."),
    9: (4, ["DECLAN"], "Close-up of DECLAN HOLT under the red glow of a warning light, sweat running down his "
        "temple. He presses the push-to-talk button on his handheld radio, brings it to his mouth and speaks "
        "urgently, jaw tight, lips moving clearly with the words. Slight handheld drift. Emotion: fear he is "
        "trying to hide."),
    10: (3, ["TEO"], "Symmetrical close-up through the windscreen into the cockpit of CAR 4: TEO MARSH in his "
         "helmet, visor down, strapped in by white harness belts, carbon steering wheel with small red lights "
         "in the foreground. His eyes behind the visor are fixed ahead; he does not answer. The car vibrates "
         "with the engine. Emotion: calm on the outside, something hidden inside."),
    11: (3, ["CAR19", "TRACK"], "Close-up of the black side mirror of CAR 4 at speed, the grandstand smeared into "
         "motion blur around it. In the mirror, CAR 19 grows larger and closer, amber headlights burning, the "
         "hazy city skyline behind it. Rack focus onto the mirror. Emotion: the hunter is coming."),
    12: (3, ["TRACK"], "Over-the-shoulder shot from behind a team strategist in a headset sitting at a wall of "
         "screens in the pit box: a live feed of two prototypes nose to tail through a corner, a track map "
         "with a moving dot, live telemetry traces. He grips his microphone. Emotion: the gap is closing."),
    13: (3, ["CAR4", "TRACK"], "Very wide, long-lens shot down an empty straight, the coastal city skyline and "
         "mountains in the haze behind the steel gantry. CAR 4 appears small in the distance and charges "
         "toward camera through heat haze. Emotion: loneliness at the front."),
    14: (3, ["ISLA"], "Extreme close-up of ISLA FERREIRA inside her cockpit, visor up a crack, dark eyes narrowed, "
         "sweat at her brow. In the reflection on her visor, a graphite car with a white number 4 grows ahead "
         "of her. She exhales slowly and her eyes harden. Emotion: three years of waiting end now."),
    15: (3, ["CAR4", "CAR19", "TRACK"], "Overhead drone shot looking almost straight down at a fast corner: CAR 4 "
         "and CAR 19 wheel to wheel, bodywork touching, CAR 19 on the outside riding the red-and-white kerb, "
         "tyre smoke pouring off both cars, the camera tracking with them. Emotion: contact at full speed."),
    16: (3, ["CAR4", "TRACK"], "Low chase camera skimming the asphalt behind CAR 4 as its rear steps out and it "
         "slides half sideways through a white wall of tyre smoke, rubber marks streaking under the lens, the "
         "grandstand blurred at the left. Emotion: this is where he crashes."),
    17: (3, ["CAR19", "TRACK"], "Ground-level shot at the exit of the corner: shards of black carbon fibre spin "
         "through the air toward camera out of a cloud of white smoke, CAR 19 bursts out of the smoke on the "
         "right, and CAR 4 straightens and emerges on the left, both still racing. Emotion: chaos, and both "
         "survived it."),
    18: (4, ["BRIAN"], "Medium close-up: BRIAN ASHCROFT jumps up out of his chair in the commentary booth, one "
         "hand pressed to his headset, the other pointing at the track, shouting into the microphone, lips "
         "moving clearly with his words, the colleague beside him on his feet too. Emotion: euphoric disbelief."),
    19: (3, ["CAR4", "CAR19", "TRACK"], "Low-angle long-lens head-on shot down the final straight: CAR 4 and "
         "CAR 19 side by side coming straight at camera, heat shimmer rising off the tarmac, the packed "
         "grandstand on its feet behind them. Emotion: dead heat."),
    20: (3, ["TEO"], "Extreme close-up through the visor of TEO MARSH: his eyes blink hard, then again, his pupils "
         "struggle to focus, a bead of sweat runs into his eye. His face stays still but his breathing quickens "
         "behind the visor. Emotion: something is wrong with him, not the car."),
    21: (3, ["CAR4"], "Close-up of the digital display in the centre of CAR 4's steering wheel, red shift lights "
         "blazing across the top, large gear and lap readouts in yellow; the numbers slowly smear, double and "
         "drift out of focus as if seen through failing eyes. Emotion: his vision is going."),
    22: (3, ["MARA"], "Close-up of MARA MARSH at the fence, the crowd behind her erupting in slow motion; she "
         "covers her mouth with one hand, eyes wet, not cheering, watching only his car. Shallow depth of "
         "field. Emotion: dread inside the celebration."),
    23: (4, ["CAR4", "CAR19", "TRACK"], "Track-level wide shot from the finish line, the dark start-finish light "
         "gantry hanging across the top of frame, the city skyline and green mountains in the haze behind. "
         "CAR 4 and CAR 19 come out of the last corner side by side, growing toward the line. Emotion: the last "
         "few hundred metres of twenty-four hours."),
    24: (5, ["DECLAN"], "Close-up of DECLAN HOLT pressing his headset to his ear with both hands, eyes closed, "
         "listening. Then his eyes open wide, his face drains, and his mouth falls slightly open in horror. "
         "He does not speak. Emotion: he has just heard the truth."),
    25: (6, ["TEO", "TRACK"], "Point of view from just behind TEO MARSH in the cockpit of CAR 4: gloved hands "
         "clenched on the carbon steering wheel, red lights blinking on the wheel, harness straps over his "
         "shoulders. Through the windscreen the finish line is lost in white tyre smoke and flashing red lights, "
         "and the whole view splits into two blurred, doubled images. Emotion: he is crossing the line blind."),
}

# (start_s, speaker, text, on_camera) - speakers on camera are lip-synced with Seedance.
DIALOGUE = [
    (0.6, "BRIAN (VO)", "Twenty-three hours and fifty-nine minutes.", False),
    (3.6, "BRIAN (VO)", "Three thousand miles... and it comes down to one.", False),
    (9.4, "BRIAN", "And the black number four still leads. Teo Marsh.", True),
    (16.3, "BRIAN (VO)", "Five times he has won here. Never by this little.", False),
    (25.4, "DECLAN", "Teo, your rears are down to the canvas. Do you copy?", True),
    (29.5, "DECLAN (VO)", "Teo. Do you copy?", False),
    (35.3, "STRATEGIST (VO)", "Ferreira is coming. Point four. Point three.", False),
    (38.3, "BRIAN (VO)", "Three years as his reserve driver. Three years in his shadow.", False),
    (44.6, "BRIAN (VO)", "They've touched!", False),
    (47.3, "BRIAN (VO)", "He's gone, he's sideways—", False),
    (53.4, "BRIAN", "He held it! I don't know how, but he held it!", True),
    (57.3, "BRIAN (VO)", "Side by side to the flag!", False),
    (74.0, "TEO (radio, VO)", "Declan... I can't see the line.", False),
]

CARD = ["HE'S BEEN DRIVING", "HALF BLIND FOR SIX HOURS."]

SOUND = [
    ("0-3", "Low wind roar through dust, grit pattering on the lens, a distant engine rising"),
    ("3-9", "Two engines screaming past the lens (doppler), gravel spray, then car 4's pass over the lens"),
    ("9-13", "Broadcast-booth room tone under Brian; muffled crowd through the glass"),
    ("13-22", "Crowd roar, PA echo; score: pulsing low synth and taiko at 120 bpm; the crowd ducks under Mara at 19"),
    ("22-29", "Score drops to a ticking hi-hat; telemetry beeps; radio squelch before and after Declan"),
    ("29-32", "Inside the cockpit: engine drone, helmet breathing, empty radio hiss (no reply)"),
    ("32-44", "Car 19's engine note growing; strategist's countdown; score swells with low strings"),
    ("44-50", "Carbon crunch on contact, tyre scream, the slide; score stops dead for the spin"),
    ("50-53", "Debris clatter, two engines bursting back to full revs; crowd explodes"),
    ("53-60", "Brian shouting over the roar; score slams back in, faster"),
    ("60-69", "Everything muffles to Teo's breathing; a high tinnitus tone; a heartbeat; crowd in slow motion"),
    ("69-73", "Two engines at the limiter, the crowd roar returning"),
    ("73-78", "Radio crackle under Teo's whisper; dead silence after it"),
    ("78-84", "Tinnitus tone rises over a distant chequered-flag roar; engine fades; heartbeat"),
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


def shot_at(t):
    rows, _ = timeline()
    return next(n for n, a, b in rows if a <= t < b)


def lipsync_shots():
    return sorted({shot_at(t) for t, _, _, on_camera in DIALOGUE if on_camera})


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
          "His wife Mara is the only person in the crowd who isn't cheering. "
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
           f"Shots with an on-camera line ({', '.join(str(n) for n in lipsync_shots())}) render with Seedance 2.0 "
           "image-to-video plus the shot-timed dialogue audio so the lips match the voice.", ""]
    for n, a, b in rows:
        secs, locks, _ = SHOTS[n]
        md += [f"**SHOT {n} — {a}–{b} s** · {secs} s · locks: {', '.join(locks)}", "", "```", prompt(n), "```", ""]
    md += ["### Sound and music", "", "| Time (s) | Cue |", "|---|---|"]
    md += [f"| {t} | {c} |" for t, c in SOUND]
    md += ["", "### Posting", "", f"**Caption:** {CAPTION}", "", f"**Pinned comment:** {PINNED}", "",
           "## Season arc (first 10)", "",
           "1. The Last Minute — Teo can't see the line; Isla is alongside.",
           "2. Hour 18 — the night stint where Teo first sees double, and hides it from Declan.",
           "3. The Podium — who crossed first, the trophy, and why the stewards are holding the result.",
           "4. Three Years Ago — the day Teo kept Isla out of the car.",
           "5. Declan's Choice — the engineer knew at hour 20 and told no one.",
           "6. The Team Owner — the contract clause that made Teo race no matter what.",
           "7. The Doctor — the scan Teo never opened.",
           "8. Isla's Radio — what her own engineer told her to do at the chicane.",
           "9. The Contact — slow-motion replay; it wasn't an accident.",
           "10. The Podium — one of them refuses to stand on it.", "",
           "## Production notes", "",
           "- References to lock first: Teo, Isla, Declan, Brian, Mara, car 4, car 19 (each car three-quarter front and side).",
           "- Never put real brands, real circuits or real broadcasters in frame; ask for plain flags and blank screens.",
           "- Lip sync: Seedance 2.0 `image-to-video` with `audio_urls` (tested: 1080p, 24 fps, full motion).",
           "- Helmeted drivers never need lip sync: their lines are radio voiceover.",
           "- Readable text (names, numbers on screens) is added in post; generated text is unreliable.",
           "- Reference screenshots stay local (`reference/`, git-ignored): they are another creator's frames."]
    pathlib.Path(__file__).with_name("SERIES-BIBLE.md").write_text("\n".join(md) + "\n")
    print("shots", len(SHOTS), "end", end, "max prompt", max(len(prompt(n)) for n in SHOTS))


if __name__ == "__main__":
    write_bible()
