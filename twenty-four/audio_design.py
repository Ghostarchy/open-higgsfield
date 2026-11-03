"""Scores and sound-effect stems for TWENTY-FOUR episodes (ElevenLabs). Records every request ID.
Usage: python3 audio_design.py
"""
import json, os, pathlib, requests

H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
HERE = pathlib.Path(__file__).parent

SCORES = {
    1: ("Modern cinematic racing-film score, 84 seconds, instrumental only, no vocals. 0-9s: low wind-like synth "
        "drone and a rising engine-like riser. 9-25s: pulsing low synth bass and taiko drums at 120 bpm, building "
        "tension. 25-33s: drops to a ticking hi-hat and a single dark piano note. 33-44s: low strings swell, "
        "drums return, faster. 44-50s: full hit then sudden stop for 3 seconds of near silence. 53-60s: score "
        "slams back, driving, heroic. 60-69s: everything muffles to a slow heartbeat and a high sustained tone. "
        "69-78s: huge build. 78-84s: fades to a lone high tone."),
    2: ("Modern cinematic drama score, 84 seconds, instrumental only, no vocals. 0-5s: deep slow-motion drone. "
        "5-26s: triumphant strings and brass, a victory theme. 26-41s: tension under the victory, strings tighten. "
        "41-57s: drops to one sustained note, then sparse sad piano. 57-84s: dark rainy noir: low cello, "
        "distant pulsing synth, dread building to a final low hit."),
    3: ("Modern cinematic drama score, 84 seconds, instrumental only, no vocals. 0-16s: rain-soaked noir, low "
        "cello drone, distant pulse. 16-40s: slow tension, single piano notes over strings. 40-48s: strings "
        "swell with anger. 48-62s: sparse emotional piano, heartbreak. 62-67s: cold, sterile synth tone. "
        "67-77s: piano and strings resolve gently. 77-84s: ominous low synth rising to a dark hit."),
}

SFX = {
    1: {
        "dust_wind": (6, "Low wind roar through a dust storm, grit pattering on a camera lens at ground level"),
        "car_pass_close": (4, "Endurance race prototype screaming past a ground-level camera at 300 km/h, doppler"),
        "car_pass_over": (3, "Race car passing directly over a camera on the track, huge roar and gravel spray"),
        "booth_tone": (6, "Commentary booth room tone with a muffled racetrack crowd roar through glass"),
        "crowd_roar": (12, "Huge racetrack grandstand crowd roaring and cheering, air horns, PA echo"),
        "telemetry_beeps": (4, "Pit-wall telemetry warning beeps and soft electronic alerts"),
        "radio_squelch": (2, "Race team radio push-to-talk squelch click and crackle"),
        "cockpit_drone": (5, "Inside a race car cockpit: deep engine drone, vibration, helmet breathing"),
        "radio_hiss": (4, "Empty radio channel hiss and static, no voice"),
        "engine_approach": (6, "Race prototype engine note growing louder from behind, approaching fast"),
        "contact_crunch": (3, "Two race cars touching at speed, carbon fibre crunch and scrape, tyre scream"),
        "spin_slide": (4, "Race car sliding sideways, tyres screaming and smoking, engine bouncing off the limiter"),
        "debris": (3, "Carbon fibre debris clattering across tarmac, two engines roaring back to full revs"),
        "heartbeat": (10, "Slow deep human heartbeat with a high tinnitus ringing tone"),
        "limiter_pair": (5, "Two race engines side by side at full throttle on a straight, crowd behind"),
        "drum_hit": (3, "One single huge low cinematic drum hit with a long tail"),
    },
    2: {
        "slowmo_drone": (5, "Slow-motion race engine roar stretched into a deep underwater drone"),
        "victory_crowd": (12, "Racetrack crowd exploding in celebration, champagne pops, horns"),
        "shutters": (8, "Dozens of press camera shutters and flash guns firing, shouted reporter questions"),
        "buckle_click": (2, "Helmet chin strap buckle unclipping, close"),
        "gasp": (3, "A crowd falling silent, then one sharp collective gasp"),
        "rain_harbour": (15, "Heavy rain on corrugated metal roofs at a night harbour, distant ship horn, buzzing lamps"),
        "rain_car_roof": (12, "Rain drumming on a car roof from inside, paper rustling, phone vibrating once"),
        "car_arrival": (6, "Tyres rolling on wet gravel, a car door opening, footsteps in puddles, umbrella opening"),
        "drum_hit": (3, "One single huge low cinematic drum hit with a long tail"),
    },
    3: {
        "rain_car_roof": (12, "Heavy rain on a car roof from inside, an engine idling behind"),
        "knock_glass": (2, "Three knuckle raps on a wet car window"),
        "pier_rain": (15, "Wind and heavy rain across an open concrete pier at night, waves slapping below"),
        "boots_puddles": (5, "Boots walking fast through puddles on concrete, umbrella drumming in rain"),
        "umbrella_drop": (3, "An umbrella clattering onto wet concrete, knees hitting the ground, jacket fabric pulled"),
        "office_flashback": (5, "Muffled sterile office hum, a pen scratching a signature, two taps on paper"),
        "engine_start_far": (4, "A car engine starting far away in the rain, headlights hum"),
        "phone_vibrate": (4, "A phone vibrating in a wet jacket pocket, then a call connecting"),
        "drum_hit": (3, "One single huge low cinematic drum hit with a long tail"),
    },
}

for num in (1, 2, 3):
    base = HERE / f"ep{num:02d}" / "audio"
    for sub in ("music", "sfx"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    mm = base / "music" / "manifest.json"
    music = json.loads(mm.read_text()) if mm.exists() else {}
    if "score" not in music:
        r = requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", headers=H,
                          json={"prompt": SCORES[num], "music_length_ms": 84000, "force_instrumental": True},
                          timeout=900)
        if r.ok:
            (base / "music" / "score.mp3").write_bytes(r.content)
            music["score"] = {"prompt": SCORES[num], "file": "score.mp3", "request_id": r.headers.get("request-id")}
            mm.write_text(json.dumps(music, indent=2))
            print(f"EP{num} score done", flush=True)
        else:
            print(f"EP{num} score: HTTP {r.status_code} {r.text[:200]}", flush=True)
    sm = base / "sfx" / "manifest.json"
    sfx = json.loads(sm.read_text()) if sm.exists() else {}
    for name, (dur, prompt) in SFX[num].items():
        if name in sfx:
            continue
        r = requests.post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192", headers=H,
                          json={"text": prompt, "duration_seconds": dur, "prompt_influence": 0.5}, timeout=180)
        if not r.ok:
            print(f"EP{num} sfx {name}: HTTP {r.status_code} {r.text[:200]}", flush=True)
            continue
        (base / "sfx" / f"{name}.mp3").write_bytes(r.content)
        sfx[name] = {"prompt": prompt, "duration_s": dur, "file": f"{name}.mp3", "request_id": r.headers.get("request-id")}
        sm.write_text(json.dumps(sfx, indent=2))
    print(f"EP{num} sfx stems: {len(sfx)}", flush=True)
