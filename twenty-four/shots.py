"""TWENTY-FOUR shot production and assembly, driven by story.py.

  python3 shots.py frames <ep> [shot ...]     # start frames: Flux 2 Pro + locked references
  python3 shots.py clips <ep> [shot ...]      # Kling 3 Pro (no dialogue) or Seedance 2.0 + audio (lip sync)
  python3 shots.py assemble <ep>              # edit list, grade, mix, subtitles, name titles, end card
Request IDs go to ep<NN>/manifest.json the moment each job is queued.
"""
import json, pathlib, subprocess, sys, threading

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "pipeline" / "scripts"))
sys.path.insert(0, str(HERE))
import hf  # noqa: E402
import story  # noqa: E402

RAW = ("https://raw.githubusercontent.com/Ghostarchy/open-higgsfield/claude/fervent-johnson-ls3c84/"
       "twenty-four/{path}")
# Lock name -> reference image key in references.json.
REF_FOR = {"TEO": "teo", "TEO_NIGHT": "teo_night", "ISLA": "isla", "ISLA_NIGHT": "isla_night",
           "DECLAN": "declan", "BRIAN": "brian", "MARA": "mara", "REPORTER": "leo", "OWNER": "owner_hand",
           "CAR4": "car4", "CAR19": "car19"}
refs = json.loads((HERE / "references.json").read_text())


def episode(num):
    return next(e for e in story.EPISODES if e["num"] == num)


def epdir(num):
    d = HERE / f"ep{num:02d}"
    for sub in ("frames", "clips", "final"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    return d


def parallel(fn, items):
    def guarded(i):
        try:
            fn(i)
        except BaseException as e:  # hf.submit raises SystemExit, which a thread would swallow
            print(f"{fn.__name__}({i}) failed: {e}", flush=True)
    ts = [threading.Thread(target=guarded, args=(i,)) for i in items]
    [t.start() for t in ts]
    [t.join() for t in ts]


def shot_refs(shots, n):
    _, locks, action = shots[n]
    keys = [REF_FOR[k] for k in locks if k in REF_FOR and refs.get(REF_FOR[k], {}).get("status") == "completed"
            and not refs[REF_FOR[k]].get("needs_redo")]
    if "trophy" in action.lower() and refs.get("trophy", {}).get("status") == "completed" \
            and not refs["trophy"].get("needs_redo"):
        keys.append("trophy")
    return keys


def frames(num, which):
    ep, d = episode(num), epdir(num)
    ledger = hf.Ledger(d / "manifest.json")

    def one(n):
        n = int(n)
        keys = shot_refs(ep["shots"], n)
        prompt = story.prompt(ep["shots"], n)
        body = {"prompt": prompt, "aspect_ratio": "9:16", "resolution": "2k"}
        if keys:
            body["image_urls"] = [refs[k]["url"] for k in keys]
            body["prompt"] = ("Start frame of the shot described, the first moment before any movement. " + prompt +
                              " Match the reference images exactly: " +
                              ", ".join(f"reference {i + 1} is {k.replace('_', ' ')}" for i, k in enumerate(keys)) + ".")
        key = f"shot{n:02d}-frame"
        hf.submit(ledger, key, "flux-2-pro", body)
        hf.wait(ledger, key, d / "frames" / f"shot{n:02d}.png", interval=5)
    parallel(one, which or list(ep["shots"]))


def lipsync_track(num, n):
    man = json.loads((HERE / f"ep{num:02d}/audio/dialogue/manifest.json").read_text())
    for line in man.values():
        if line.get("lipsync", {}).get("shot") == n:
            return f"ep{num:02d}/audio/shots/shot{n:02d}.wav"
    return None


def clips(num, which):
    ep, d = episode(num), epdir(num)
    ledger = hf.Ledger(d / "manifest.json")

    def one(n):
        n = int(n)
        secs = ep["shots"][n][0]
        start = ledger.data[f"shot{n:02d}-frame"]["url"]
        track = lipsync_track(num, n)
        if track:
            model = "bytedance/seedance-2.0/image-to-video"
            body = {"prompt": story.prompt(ep["shots"], n) + " The speaking character's lips move precisely in sync "
                    "with the dialogue audio; everyone else keeps their mouth closed.",
                    "image_url": start, "audio_urls": [RAW.format(path=track)],
                    "duration": max(4, secs), "resolution": "1080p", "generate_audio": False}
        else:
            model = "kling-video/v3.0/pro/image-to-video"
            body = {"prompt": story.prompt(ep["shots"], n), "sound": "off", "duration": max(3, secs),
                    "cfg_scale": 0.5, "multi_shots": False, "image_url": start}
        key = f"shot{n:02d}-clip"
        hf.submit(ledger, key, model, body)
        hf.wait(ledger, key, d / "clips" / f"shot{n:02d}.mp4", interval=15)
    parallel(one, which or list(ep["shots"]))


# Sound-effect cues per episode: (stem, start_s, gain_dB, length_s or None)
CUES = {
    1: [("dust_wind", 0, -12, 6), ("car_pass_close", 3.0, -4, None), ("car_pass_over", 6.0, -3, None),
        ("booth_tone", 9, -20, 4), ("crowd_roar", 13, -16, 9), ("telemetry_beeps", 22, -14, None),
        ("radio_squelch", 25.0, -10, None), ("radio_squelch", 28.6, -10, None), ("cockpit_drone", 29, -12, None),
        ("radio_hiss", 30.5, -20, None), ("engine_approach", 32, -8, None), ("engine_approach", 38, -10, None),
        ("contact_crunch", 44.4, -3, None), ("spin_slide", 47, -4, None), ("debris", 50, -5, None),
        ("crowd_roar", 50.5, -14, 10), ("heartbeat", 60, -10, 9), ("limiter_pair", 69, -6, None),
        ("radio_squelch", 73.6, -10, None), ("heartbeat", 78, -12, 6), ("drum_hit", 84, 0, None)],
    2: [("slowmo_drone", 0, -8, None), ("victory_crowd", 5, -12, 12), ("shutters", 15, -12, 8),
        ("shutters", 23, -10, 8), ("victory_crowd", 26, -20, 11), ("buckle_click", 40, -6, None),
        ("gasp", 45.5, -8, None), ("rain_harbour", 57, -10, 15), ("rain_car_roof", 62, -12, 12),
        ("car_arrival", 78, -8, None), ("drum_hit", 84, 0, None)],
    3: [("rain_car_roof", 0, -12, 12), ("knock_glass", 4.2, -4, None), ("pier_rain", 12, -12, 15),
        ("boots_puddles", 20, -10, None), ("pier_rain", 27, -14, 15), ("umbrella_drop", 40.2, -6, None),
        ("pier_rain", 42, -16, 15), ("office_flashback", 62, -10, None), ("pier_rain", 57, -16, 15),
        ("engine_start_far", 72, -10, None), ("phone_vibrate", 77, -8, None), ("drum_hit", 84, 0, None)],
}


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def chunks(words):
    # Split at sentence ends only, then into balanced cards of at most 5 words (never a lone word).
    sentences, cur = [], []
    for w in words:
        cur.append(w)
        if w[-1] in ".?!" or w.endswith("—"):
            sentences.append(cur); cur = []
    if cur:
        sentences.append(cur)
    out = []
    for snt in sentences:
        n = -(-len(snt) // 5)
        size = -(-len(snt) // n)
        out += [snt[i:i + size] for i in range(0, len(snt), size)]
    merged = []
    for c in out:
        if merged and (len(c) == 1 or len(merged[-1]) == 1) and len(merged[-1]) + len(c) <= 6:
            merged[-1] += c
        else:
            merged.append(c)
    return merged


def duration(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]))


def assemble(num):
    ep, d = episode(num), epdir(num)
    rows, end = story.timeline(ep["shots"])
    man = json.loads((d / "audio/dialogue/manifest.json").read_text())
    start_of = {n: a for n, a, _ in rows}

    # Dialogue: on-camera lines sit exactly where the lip-sync track put them; voiceover at its script time.
    placed = []
    for key, line in sorted(man.items()):
        if "lipsync" in line:
            t = start_of[line["lipsync"]["shot"]] + line["lipsync"]["offset_in_shot_s"]
            src = d / "audio/shots" / f"shot{line['lipsync']['shot']:02d}-line.wav"
        else:
            t, src = line["start_s"], d / "audio/dialogue" / line["file"]
        placed.append((t, src, line["text"], duration(src)))

    # Subtitles (white italic, lower middle), name titles (thin, top left, underlined), end card.
    events = []
    for k, (t, _, text, dur) in enumerate(placed):
        cards = chunks(text.split())
        total = sum(len(" ".join(c)) for c in cards)
        nxt = placed[k + 1][0] if k + 1 < len(placed) else end
        for i, c in enumerate(cards):
            seg = dur * len(" ".join(c)) / total
            e = t + max(seg, 0.6)
            if i == len(cards) - 1:
                e = min(e + 0.3, nxt)
            events.append(("Sub", t, e, " ".join(c)))
            t = e
    for a, b, text in ep["graphics"]:
        events.append(("Name", a, b, r"{\fad(300,300)\u1}" + text))
    events.append(("Card", end + 0.4, 90.0, r"{\fad(500,0)}" + ep["card"][0]))
    events.append(("Card2", end + 1.6, 90.0, r"{\fad(500,0)}" + ep["card"][1]))
    ass = d / "final" / "subs.ass"
    ass.write_text("\n".join([
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 1", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        "Style: Sub,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,-1,0,0,100,100,1,0,1,2,2,2,70,70,700,1",
        "Style: Name,Inter ExtraLight,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,1,1,7,56,56,150,1",
        "Style: Card,Inter,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,3,0,1,0,0,5,80,80,1020,1",
        "Style: Card2,Inter,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,3,0,1,0,0,5,80,80,880,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        *[f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{tx}" for st, a, b, tx in events]]) + "\n")

    # Mix: dialogue, score under it, sound-effect cues; normalised to -14 LUFS.
    inputs, parts, labels = [], [], []
    for i, (t, src, _, _) in enumerate(placed):
        inputs += ["-i", str(src)]
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(t * 1000)}:all=1[a{i}]")
        labels.append(f"[a{i}]")
    idx = len(placed)
    inputs += ["-i", str(d / "audio/music/score.mp3")]
    parts.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{end},"
                 f"afade=t=out:st={end - 1.5}:d=1.5,volume=-17dB[a{idx}]")
    labels.append(f"[a{idx}]"); idx += 1
    for stem, t, gain, length in CUES[num]:
        inputs += ["-i", str(d / "audio/sfx" / f"{stem}.mp3")]
        trim = f",atrim=0:{length}" if length else ""
        parts.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo{trim},volume={gain}dB,"
                     f"adelay={int(t * 1000)}:all=1[a{idx}]")
        labels.append(f"[a{idx}]"); idx += 1
    parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:90,"
                 "apad=whole_dur=90,loudnorm=I=-14:TP=-1.5:LRA=11[mix]")
    mix = d / "final" / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts), "-map", "[mix]",
                    "-t", "90", "-ar", "48000", str(mix)], check=True)

    # Picture: every shot trimmed to its slot, 1080x1920, 24 fps, one grade, then the black card.
    vin, vparts = [], []
    for i, (n, a, b) in enumerate(rows):
        vin += ["-i", str(d / "clips" / f"shot{n:02d}.mp4")]
        vparts.append(f"[{i}:v]trim=duration={b - a},setpts=PTS-STARTPTS,scale=1080:1920:"
                      f"force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=24,setsar=1[v{i}]")
    vparts.append(f"color=c=black:s=1080x1920:r=24:d={90 - end},setsar=1[vcard]")
    chain = "".join(f"[v{i}]" for i in range(len(rows)))
    vparts.append(f"{chain}concat=n={len(rows)}:v=1:a=0,eq=contrast=1.05:saturation=0.9,"
                  "colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02,noise=alls=5:allf=t[graded]")
    vparts.append(f"[graded][vcard]concat=n=2:v=1:a=0,ass={ass}:fontsdir=/usr/share/fonts/opentype/inter[vout]")
    out = d / "final" / f"ep{num:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *vin, "-i", str(mix), "-filter_complex", ";".join(vparts),
                    "-map", "[vout]", "-map", f"{len(rows)}:a", "-t", "90", "-r", "24", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "20", "-maxrate", "4M", "-bufsize", "8M", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print("wrote", out, f"{duration(out):.3f}s")


if __name__ == "__main__":
    stage, num, rest = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    {"frames": lambda: frames(num, rest), "clips": lambda: clips(num, rest),
     "assemble": lambda: assemble(num)}[stage]()
