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
    "REPORTER": ("LEO VANCE: a pit-lane TV reporter in his early 30s, sharp jawline, short dark-brown hair swept "
                 "up, brown eyes, navy suit, open-collared light-grey shirt, holding a black foam-covered "
                 "microphone with no logo"),
    "PODIUM": ("THE PODIUM: a wet black stage under a grey sky, a huge dark-blue backdrop printed with a gold "
               "laurel wreath and a star and no readable words, gold and blue confetti on the wet floor, "
               "photographers and TV cameras crowding the front edge"),
    "HARBOUR": ("THE HARBOUR: a rain-soaked industrial dock at night, rusted corrugated warehouses, stacked "
                "containers, tall cranes against low black clouds, sodium lamps reflecting in puddles, mist"),
    "ISLA_NIGHT": ("ISLA FERREIRA off duty: a 26-year-old woman, olive skin, intense dark brown eyes, straight "
                   "black eyebrows, black hair loose and soaked to her shoulders, small gold stud earring, black "
                   "waterproof jacket over a dark hoodie, black jeans, black boots"),
    "TEO_NIGHT": ("TEO MARSH off duty: a 38-year-old man, lean face, short dark-blond hair greying at the "
                  "temples soaked flat by rain, a thin white scar through his left eyebrow, three-day stubble, "
                  "his LEFT eye clouded milky grey and his right eye pale grey-green, charcoal hooded rain jacket "
                  "over a grey t-shirt"),
    "OWNER": ("THE OWNER'S HAND: a man's hand in a dark charcoal suit cuff, a heavy gold signet ring engraved "
              "with a hawk on the little finger, an expensive steel watch"),
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
    (25.4, "DECLAN", "Teo, your rears are gone. Do you copy?", True),
    (29.5, "DECLAN (VO)", "Teo. Do you copy?", False),
    (35.3, "STRATEGIST (VO)", "Ferreira is coming. Point four. Point three.", False),
    (38.3, "BRIAN (VO)", "Three years as his reserve driver. Three years in his shadow.", False),
    (44.6, "BRIAN (VO)", "They've touched!", False),
    (47.3, "BRIAN (VO)", "He's gone, he's sideways—", False),
    (53.4, "BRIAN", "He held it! How did he hold that?!", True),
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


# Name titles: thin white sans, top left, underlined (the reference's lower-third style). (start, end, text)
GRAPHICS = [
    (9.2, 12.6, "BRIAN ASHCROFT"),
    (16.0, 19.0, "TEO MARSH"),
    (19.0, 22.0, "MARA MARSH"),
    (25.0, 29.0, "DECLAN HOLT  ·  RACE ENGINEER"),
    (41.0, 44.0, "ISLA FERREIRA"),
]

# ---------------------------------------------------------------- Episode 2: "The Line"
SHOTS2 = {
    1: (5, ["CAR4", "CAR19", "TRACK"], "Extreme slow motion, track-level camera exactly on the white finish line: "
        "the noses of CAR 4 and CAR 19 cross the line side by side through white tyre smoke, confetti-like "
        "sparks and rubber fragments hanging in the air. Emotion: no one knows who won."),
    2: (3, ["CAR4"], "Extreme close-up of the steering-wheel display in CAR 4: red shift lights fade out one by "
        "one, the gear readout drops to N, the lap counter flickers. Emotion: it is over, but how?"),
    3: (4, ["BRIAN"], "Close-up of BRIAN ASHCROFT in the commentary booth, both hands on his headset, staring "
        "at a monitor off-screen, mouth open, then speaking slowly and clearly into the microphone, lips moving "
        "with his words. Emotion: disbelief turning into awe."),
    4: (3, ["MARA"], "Close-up of MARA MARSH at the fence, eyes closed, tears on her cheeks, her hand with the "
        "wedding band over her mouth, the crowd behind her erupting. Emotion: relief she cannot show."),
    5: (4, ["TEO", "PODIUM"], "Low wide shot from the confetti-covered wet floor up to the podium: TEO MARSH stands "
        "alone in his graphite race suit with his helmet still on and visor down, holding a tall twisted silver "
        "and gold trophy, photographers' flashes firing from both sides. Emotion: a champion who will not show "
        "his face."),
    6: (3, ["TEO"], "Macro close-up of the trophy in a gloved hand: twisted ribbons of polished silver with gold "
        "edges, water droplets on the metal, the reflection of camera flashes sliding across it, Teo's visor "
        "blurred behind. Emotion: the prize."),
    7: (4, ["TEO", "PODIUM"], "High-angle shot over the heads of a crush of photographers and TV crews as TEO MARSH "
        "walks down the podium steps into them, helmet on, trophy under his arm, microphones and lenses pushed "
        "toward him from every side, team staff in grey vests behind. Emotion: the world wants him."),
    8: (4, ["REPORTER", "PODIUM"], "Handheld close-up of LEO VANCE pushing to the front of the scrum, thrusting his "
        "microphone toward camera and speaking fast and loud, eyes wide, lips moving clearly with his words, "
        "flash guns going off behind him. Emotion: the question everyone wants answered."),
    9: (4, ["TEO"], "Tight close-up on TEO MARSH's helmet facing camera, a forest of microphones in the foreground, "
        "rain drops on the dark visor; behind the visor only his eyes are visible, still and unreadable. "
        "Emotion: he is about to say something no one expects."),
    10: (3, ["ISLA"], "Medium shot of ISLA FERREIRA at the edge of the scrum, helmet under her arm, black hair "
         "coming loose, sweat on her face, staring at Teo with her jaw set. Emotion: she lost by nothing."),
    11: (4, ["TEO"], "Macro shot of TEO MARSH's helmet chin bar in soft focus, the white number 4 sharp in the "
         "centre, then his gloved hands slowly unfasten the strap. Emotion: the mask is coming off."),
    12: (6, ["TEO", "PODIUM"], "Slow push in as TEO MARSH lifts his helmet off in front of the press: his "
         "dark-blond hair is wet with sweat, and as he raises his face to the flashes his left eye is clouded "
         "milky grey while his right eye is clear. The flashes stop. Emotion: the secret, in front of everyone."),
    13: (3, ["REPORTER"], "Close-up of LEO VANCE slowly lowering his microphone, mouth open, frozen. Emotion: "
         "shock."),
    14: (3, ["MARA"], "Close-up of MARA MARSH at the back of the crowd, nodding very slightly at Teo through her "
         "tears, as if to say: tell them. Emotion: she has carried this with him."),
    15: (4, ["DECLAN"], "Close-up of DECLAN HOLT in the crowd of team staff, not surprised, looking away from Teo "
         "and down at the ground, guilt all over his face. Emotion: he knew."),
    16: (5, ["HARBOUR"], "Hard cut to night. High wide shot over THE HARBOUR in heavy rain, cranes and lights in "
         "the mist, a single dark car parked alone beside a rusted warehouse with its interior light on. Slow "
         "drift down toward the car. Emotion: far from the cheering."),
    17: (6, ["DECLAN", "HARBOUR"], "Inside the car at night, rain streaming down the windscreen, DECLAN HOLT alone "
         "in the driver's seat lit by the dome light, opening a creased white envelope and pulling out a medical "
         "eye scan printout. His hands are shaking. Emotion: evidence."),
    18: (4, ["DECLAN"], "Extreme close-up of the eye-scan printout in Declan's hands: a grey retinal image with a "
         "dark shadow across it, a handwritten signature at the bottom and a date stamp, rain-light rippling "
         "across the paper. Emotion: this is older than anyone admitted."),
    19: (6, ["DECLAN", "HARBOUR"], "Close-up of DECLAN HOLT holding his phone to his ear in the dark car, rain "
         "shadows running down his face, listening, eyes closed, his mouth hidden behind his hand. Emotion: "
         "the voice on the other end is someone powerful."),
    20: (6, ["HARBOUR"], "Low angle through the rain-streaked windscreen: headlights of a black car slowly pull up "
         "behind Declan's car and stop, light flooding the interior, a figure gets out and walks toward the "
         "driver's door holding an umbrella, face hidden. Emotion: danger."),
}

DIALOGUE2 = [
    (0.4, "BRIAN (VO)", "Who won? Nobody in this circuit knows who won.", False),
    (8.4, "BRIAN", "Number four. By three thousandths of a second.", True),
    (15.4, "BRIAN (VO)", "Six wins. And he still won't take his helmet off.", False),
    (26.4, "LEO", "Teo! Six wins! Is there a seventh?", True),
    (30.6, "TEO (behind visor, VO)", "There won't be a seventh.", False),
    (43.2, "BRIAN (VO)", "Oh my word...", False),
    (47.4, "TEO (VO)", "I've been half blind since spring.", False),
    (72.6, "PHONE VOICE (VO)", "You signed it, Declan. Six months ago.", False),
    (79.4, "PHONE VOICE (VO)", "Now get out of the car.", False),
]

CARD2 = ["THE TEAM KNEW.", "FOR SIX MONTHS."]

SOUND2 = [
    ("0-5", "Slow-motion engine roar stretched into a deep drone; crowd held under water"),
    ("5-15", "Silence breaks on the dashboard; Brian; the crowd explodes; Mara's breath"),
    ("15-26", "Podium: champagne pops, photographers' shutters, chanting; score: triumphant strings"),
    ("26-37", "Scrum: overlapping shouted questions, shutter bursts; Teo's line muffled inside the helmet"),
    ("37-41", "Buckle clicks; the crowd quietens; score drops to one sustained note"),
    ("41-57", "Shutters stop dead; a single gasp; heartbeat; Teo's voice close and quiet"),
    ("57-62", "Hard cut: heavy rain on metal roofs, distant ship horn, buzzing sodium lamps"),
    ("62-78", "Inside the car: rain on the roof, paper rustling, a phone vibrating; the voice through the speaker"),
    ("78-84", "Tyres on wet gravel, a car door, footsteps in puddles, an umbrella opening"),
    ("84-90", "Hard cut to black on one low drum hit"),
]

GRAPHICS2 = [
    (8.2, 11.8, "BRIAN ASHCROFT"),
    (26.0, 29.6, "LEO VANCE  ·  PIT LANE"),
    (34.0, 37.0, "ISLA FERREIRA  ·  2ND, +0.003s"),
    (62.0, 65.0, "DECLAN HOLT"),
]

CAPTION2 = ("He won by 0.003 seconds. Then he took off his helmet. 🏁 EP02 | TWENTY-FOUR "
            "#racing #motorsport #shortdrama #aistory #cinematic")
PINNED2 = "EP03 tomorrow. Who was in the second car? 👀"

# ---------------------------------------------------------------- Episode 3: "The Car Behind"
SHOTS3 = {
    1: (4, ["DECLAN", "HARBOUR"], "From inside Declan's car at night, over DECLAN HOLT's shoulder: rain sheets "
        "down the driver's window, headlights glare behind, and a figure under a black umbrella walks up to the "
        "door, face hidden by the umbrella. Emotion: who is it?"),
    2: (4, ["ISLA_NIGHT", "HARBOUR"], "Outside the car in the rain, low angle: a knuckle raps on the wet window, "
        "the black umbrella tilts back and reveals ISLA FERREIRA, rain running off its edge, eyes hard. "
        "Emotion: not who we expected."),
    3: (4, ["ISLA_NIGHT", "HARBOUR"], "Close-up of ISLA FERREIRA under her umbrella at the open car window, sodium "
        "light on one side of her face, speaking low and angry, lips moving clearly with her words. Emotion: "
        "she is done being polite."),
    4: (4, ["DECLAN"], "Close-up of DECLAN HOLT in the dark car, silent, slowly turning his eyes toward the end of "
        "the pier beyond the windscreen, rain shadows on his face. Emotion: he gives Teo away without a word."),
    5: (4, ["HARBOUR"], "Very wide shot down a long concrete pier in heavy rain at night: at the far end a lone "
        "hooded figure sits on the edge with his legs over the black water, cranes and harbour lights blurred "
        "in the mist behind. Emotion: a man at the end of everything."),
    6: (4, ["ISLA_NIGHT", "HARBOUR"], "Tracking shot from behind ISLA FERREIRA walking fast down the wet pier "
        "under her black umbrella, boots splashing through puddles that reflect the lamps. Emotion: urgency."),
    7: (4, ["ISLA_NIGHT", "TEO_NIGHT", "HARBOUR"], "Over-the-shoulder from behind TEO MARSH sitting on the pier "
        "edge, his hooded shoulder blurred in the foreground; ISLA FERREIRA stops a few steps away under her "
        "umbrella, rain dripping from it, staring down at him. Emotion: the confrontation begins."),
    8: (4, ["TEO_NIGHT", "HARBOUR"], "Close-up of TEO MARSH in profile, hood down, rain running over his face, "
        "his clouded left eye toward camera, staring out at the black water; he does not turn around. Emotion: "
        "he knew she would come."),
    9: (4, ["ISLA_NIGHT"], "Close-up of ISLA FERREIRA, umbrella lowered, rain on her face, speaking with her voice "
        "cracking, lips moving clearly with her words, eyes wet. Emotion: betrayal."),
    10: (4, ["TEO_NIGHT"], "Close-up of TEO MARSH slowly turning to face her, his clouded left eye catching the "
         "lamp light, speaking quietly, lips moving clearly with his words. Emotion: the truth, finally."),
    11: (4, ["ISLA_NIGHT", "TEO_NIGHT", "HARBOUR"], "ISLA FERREIRA throws her umbrella aside, drops to her knees "
         "on the wet concrete and grabs the collar of TEO MARSH's jacket with both fists, pulling his face "
         "inches from hers, shouting, lips moving clearly with her words, rain pouring on both of them; his mouth "
         "stays closed. Emotion: three years of anger."),
    12: (4, ["TEO_NIGHT"], "Tight close-up of TEO MARSH, her fists gripping his collar at the edges of frame, a "
         "faint broken smile, speaking softly, lips moving clearly with his words. Emotion: a sad joke."),
    13: (5, ["ISLA_NIGHT", "TEO_NIGHT", "HARBOUR"], "Two-shot in profile, foreheads almost touching, rain dripping "
         "from their noses and hair, harbour lights in soft bokeh behind them; neither speaks; slowly her grip "
         "on his collar loosens. Emotion: the anger drains into grief."),
    14: (5, ["TEO_NIGHT"], "Close-up of TEO MARSH looking straight at her, rain and tears indistinguishable, "
         "speaking slowly and clearly, lips moving with his words. Emotion: the confession."),
    15: (4, ["ISLA_NIGHT"], "Extreme close-up of ISLA FERREIRA's eyes as the realization lands, her breath "
         "catching, tears mixing with rain, lips parted but silent. Emotion: everything she believed was wrong."),
    16: (5, ["OWNER"], "Desaturated flashback insert in a sterile office: a doctor's pen signs a medical form on a "
         "glass desk while THE OWNER'S HAND rests beside it, the gold hawk signet ring catching the light, then "
         "taps the paper twice. Emotion: someone powerful arranged all of this."),
    17: (5, ["TEO_NIGHT"], "Close-up of TEO MARSH, his hand closing over hers on his collar, speaking with quiet "
         "intensity, lips moving clearly with his words. Emotion: he protected her."),
    18: (5, ["ISLA_NIGHT", "TEO_NIGHT", "HARBOUR"], "Medium shot: ISLA FERREIRA lets go and sits back on her heels "
         "in the rain, staring at TEO MARSH; far behind them down the pier, out of focus, the headlights of a "
         "black car switch on. Emotion: they are being watched."),
    19: (7, ["OWNER", "HARBOUR"], "From inside the black car through the rain-streaked windscreen: headlights flood "
         "the pier and the two small silhouettes at its end; in the foreground THE OWNER'S HAND holds a phone and "
         "presses call, the gold hawk ring gleaming. Down the pier a phone lights up in Isla's pocket. Emotion: "
         "he wants her next."),
}

DIALOGUE3 = [
    (8.4, "ISLA", "Where is he, Declan?", True),
    (32.4, "ISLA", "You hid it from everyone. Even from me.", True),
    (36.4, "TEO", "Especially from you.", True),
    (40.4, "ISLA", "You beat me half blind!", True),
    (44.4, "TEO", "With one good eye.", True),
    (53.4, "TEO", "Three years ago they offered you my seat. With my doctor.", True),
    (67.4, "TEO", "I kept you out so they couldn't do this to you.", True),
    (79.6, "OWNER (phone, VO)", "Hello, Isla. Ready to drive for me?", False),
]

CARD3 = ["THEY DIDN'T WANT HIS SEAT.", "THEY WANTED HER IN IT."]

SOUND3 = [
    ("0-8", "Heavy rain on the car roof, an engine idling behind; three knuckle raps on glass"),
    ("8-16", "Rain louder through the open window; Isla close; Declan's silence; a distant ship horn"),
    ("16-28", "Wind and rain across the open pier; boots in puddles; umbrella drumming; low cello drone enters"),
    ("28-40", "Waves slapping the pier; voices close and dry over the rain"),
    ("40-48", "Umbrella clatters away; knees hit wet concrete; fabric pulled; score swells"),
    ("48-53", "Only rain and breathing; a single piano note"),
    ("53-62", "Teo's confession over sparse piano; Isla's breath catching"),
    ("62-67", "Flashback: muffled office hum, pen scratch, two taps on paper"),
    ("67-77", "Back to the rain; piano and strings resolve; a car engine starts far away"),
    ("77-84", "Headlights hum; a phone vibrating in a wet pocket; the call connects; the owner's voice, warm and cold"),
    ("84-90", "Hard cut to black on one low drum hit"),
]

GRAPHICS3 = [
    (0.0, 3.0, "KESTREL BAY HARBOUR  ·  02:14"),
    (8.2, 11.6, "ISLA FERREIRA"),
    (28.0, 31.0, "TEO MARSH"),
]

CAPTION3 = ("She found him at the end of the pier. Then he told her why he kept her out of the car. EP03 | "
            "TWENTY-FOUR #racing #shortdrama #aistory #cinematic")
PINNED3 = "EP04 tomorrow. Who wears the hawk ring?"

EPISODES = [
    {"num": 1, "title": "The Last Minute", "shots": SHOTS, "dialogue": DIALOGUE, "card": CARD,
     "sound": SOUND, "graphics": GRAPHICS, "caption": CAPTION, "pinned": PINNED},
    {"num": 2, "title": "The Line", "shots": SHOTS2, "dialogue": DIALOGUE2, "card": CARD2,
     "sound": SOUND2, "graphics": GRAPHICS2, "caption": CAPTION2, "pinned": PINNED2},
    {"num": 3, "title": "The Car Behind", "shots": SHOTS3, "dialogue": DIALOGUE3, "card": CARD3,
     "sound": SOUND3, "graphics": GRAPHICS3, "caption": CAPTION3, "pinned": PINNED3},
]


def timeline(shots):
    t, rows = 0, []
    for n, (secs, _, _) in shots.items():
        rows.append((n, t, t + secs))
        t += secs
    return rows, t


def shot_at(shots, t):
    rows, _ = timeline(shots)
    return next(n for n, a, b in rows if a <= t < b)


def lipsync_shots(ep):
    return sorted({shot_at(ep["shots"], t) for t, _, _, on_camera in ep["dialogue"] if on_camera})


def prompt(shots, n):
    secs, locks, action = shots[n]
    return " ".join([action] + [LOCK[k] + "." for k in locks] + [STYLE])


def episode_md(ep):
    shots = ep["shots"]
    rows, end = timeline(shots)
    assert end + 6 == 90, f"EP{ep['num']}: shots end at {end}s; the card needs the last 6 s"
    md = [f"## Episode {ep['num']} — \"{ep['title']}\"", "", "| Time | Shot | Beat |", "|---|---|---|"]
    md += [f"| {a}–{b} s | {n} | {shots[n][2].split('. ')[0]} |" for n, a, b in rows]
    md += [f"| 84–90 s | card | Black. {' / '.join(ep['card'])} |", "",
           "### Dialogue and voiceover", "", "| Time | Who | Line | Lip sync |", "|---|---|---|---|"]
    md += [f"| {s:.1f} s | {w} | \"{t}\" | {'Seedance (on camera)' if oc else '—'} |"
           for s, w, t, oc in ep["dialogue"]]
    md += ["", "### Graphics", "",
           "Subtitles: white italic sans, centred in the lower middle, 1–6 words per card, timed to each line.",
           "Name titles: large thin white sans at the top left with a thin underline, fading in over 0.3 s:", ""]
    md += [f"- {a:.1f}–{b:.1f} s: {t}" for a, b, t in ep["graphics"]]
    md += ["", "### Shot prompts", "",
           "Kling 3.0 Pro image-to-video, sound off, from a start frame made from the locked references. "
           f"Shots with an on-camera line ({', '.join(str(n) for n in lipsync_shots(ep))}) render with Seedance "
           "2.0 image-to-video plus the shot-timed dialogue audio so the lips match the voice.", ""]
    for n, a, b in rows:
        secs, locks, _ = shots[n]
        md += [f"**SHOT {n} — {a}–{b} s** · {secs} s · locks: {', '.join(locks)}", "", "```",
               prompt(shots, n), "```", ""]
    md += ["### Sound and music", "", "| Time (s) | Cue |", "|---|---|"]
    md += [f"| {t} | {c} |" for t, c in ep["sound"]]
    md += ["", "### Posting", "", f"**Caption:** {ep['caption']}", "", f"**Pinned comment:** {ep['pinned']}", ""]
    return md


def check(ep):
    rows, _ = timeline(ep["shots"])
    starts = []
    for t, who, text, oc in ep["dialogue"]:
        n = shot_at(ep["shots"], t)
        a, b = next((a, b) for k, a, b in rows if k == n)
        est = len(text.split()) / 2.6  # ~2.6 words/s for these deliveries
        starts.append((t, t + est, who))
        if oc and t + est > b:
            print(f"warning EP{ep['num']}: on-camera line at {t}s may outrun shot {n} ({a}-{b})")
    for (a0, a1, w0), (b0, _, w1) in zip(starts, starts[1:]):
        if a1 > b0:
            print(f"warning EP{ep['num']}: '{w0}' at {a0}s may run into '{w1}' at {b0}s")


def write_bible():
    md = ["# TWENTY-FOUR — Series Bible", "",
          "Original endurance-racing drama for TikTok, Reels and Shorts (9:16, 90 s episodes). The visual language "
          "follows the supplied reference frames (ground-level dust shots, pit-wall close-ups, broadcast booth, "
          "mirror reveals, helmet visor close-ups, the podium press scrum, name titles, the hard cut to a dark "
          "night location, the rain-soaked face-to-face confrontation); the characters, cars, team, circuit and story are original.", "",
          "## Premise", "",
          "Teo Marsh, five-time winner of the Kestrel Bay 24 Hours, leads his final race by seconds with one minute "
          "left. His tyres are gone and his radio has gone silent. Closing in is Isla Ferreira, the reserve driver he "
          "kept on the bench for three years. The secret: Teo is losing the sight in one eye, and for the last six "
          "hours he has been driving from memory. His wife Mara is the only person in the crowd who isn't cheering. "
          "And the team has known far longer than anyone will admit.", "",
          "## Locked descriptions", "", "Paste these word for word. Every prompt already contains the ones it needs.", ""]
    md += [f"**{k}**\n> {v}\n" for k, v in LOCK.items()]
    md += [f"**STYLE**\n> {STYLE}\n"]
    for ep in EPISODES:
        check(ep)
        md += episode_md(ep)
    md += ["## Season arc", "",
           "1. The Last Minute — Teo can't see the line; Isla is alongside.",
           "2. The Line — he wins by 0.003 s, takes off his helmet, and the team's secret surfaces at the harbour.",
           "3. The Car Behind — Isla finds Teo at the end of the pier; why he kept her out of the car; the hawk ring.",
           "4. The Hawk — who owns the team, and what he offered Isla three years ago.",
           "5. Three Years Ago — the day Teo kept Isla out of the car.",
           "6. The Contract — the clause that made Teo race no matter what.",
           "7. The Doctor — who signed the scan, and who paid them.",
           "8. Isla's Radio — what her own engineer told her at the chicane.",
           "9. The Stewards — the result is under review.",
           "10. The Seventh — Teo's choice.", "",
           "## Production notes", "",
           "- References to lock first: Teo (helmet on, helmet off, off duty), Isla (race suit, off duty), Declan, "
           "Brian, Mara, Leo, the owner's hand and ring, car 4, car 19, the trophy, the podium, the harbour.",
           "- Two-person dialogue scenes: one speaker per shot, so Seedance only has one mouth to drive.",
           "- Never put real brands, series, circuits or broadcasters in frame (the reference's podium shows real "
           "championship logos; ours uses a plain laurel and star).",
           "- Lip sync: Seedance 2.0 `image-to-video` with `audio_urls` (tested: 1080p, 24 fps, full motion).",
           "- Helmeted or hidden mouths never need lip sync: those lines are voiceover.",
           "- Readable text (names, numbers, screens, name titles) is added in post; generated text is unreliable.",
           "- Reference screenshots stay local (`reference/`, git-ignored): they are another creator's frames."]
    pathlib.Path(__file__).with_name("SERIES-BIBLE.md").write_text("\n".join(md) + "\n")
    for ep in EPISODES:
        print(f"EP{ep['num']}: {len(ep['shots'])} shots, lip sync {lipsync_shots(ep)}, max prompt "
              f"{max(len(prompt(ep['shots'], n)) for n in ep['shots'])}")


if __name__ == "__main__":
    write_bible()
