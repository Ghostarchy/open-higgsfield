"""Assemble Episode 1: 5 x 12 s Kling clips -> graded 1080x1920 24 fps, dialogue + sound design mix,
burned-in captions and title cards. Exactly 60 s.

Usage: python3 assemble.py <episode_dir>
Outputs: final/ep01.mp4, final/captions.ass, final/mix.wav, audio/dialogue/trimmed/*.wav
"""
import json, pathlib, subprocess, sys

ep = pathlib.Path(sys.argv[1])
final = ep / "final"
final.mkdir(exist_ok=True)
dlg = json.loads((ep / "audio/dialogue/manifest.json").read_text())
sfx_dir = ep / "audio/sfx"
FONT_DIR = "/usr/share/fonts/opentype/inter"


def run(cmd):
    subprocess.run(cmd, check=True)


def duration(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]))


# 1. Dialogue: trim leading/trailing silence everywhere; shorten pauses over 0.6 s to 0.5 s
#    (lines 09 and 10 came back with 1.0-1.5 s dead air inside them).
trim_dir = ep / "audio/dialogue/trimmed"
trim_dir.mkdir(exist_ok=True)
lines = []
for lid, d in sorted((k, v) for k, v in dlg.items() if k.isdigit()):
    src, dst = ep / "audio/dialogue" / d["file"], trim_dir / f"{lid}.wav"
    inner = ",silenceremove=stop_periods=-1:stop_duration=0.6:stop_threshold=-42dB:stop_silence=0.5" \
        if lid in ("09", "10") else ""
    af = ("silenceremove=start_periods=1:start_threshold=-45dB" + inner +
          ",areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "2", str(dst)])
    lines.append({**d, "id": lid, "wav": dst, "dur": duration(dst)})

for a, b in zip(lines, lines[1:]):
    end = a["start_s"] + a["dur"]
    if end > b["start_s"]:
        print(f"warning: line {a['id']} ends {end:.2f}s, after line {b['id']} starts {b['start_s']}s")

# 2. Captions: 2-5 words per card, timed by character share of each line.
def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

WEAK = {"the", "a", "an", "my", "his", "her", "your", "i", "of", "to", "in", "and", "do", "it"}


def chunks(words):
    # Split at punctuation first so no card ends mid-phrase, then keep each card at 2-5 words.
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if w[-1] in ",.?!" or w.endswith("..."):
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    out = []
    for ph in phrases:
        if out and len(out[-1]) + len(ph) <= 5 and (len(ph) < 2 or len(out[-1]) < 2):
            out[-1] += ph           # merge a one-word fragment into its neighbour
        elif len(ph) <= 5:
            out.append(ph)
        else:
            half = len(ph) // 2
            while half > 2 and ph[half - 1].lower().strip(",.?!") in WEAK:
                half -= 1
            out += [ph[:half], ph[half:]]
    return out

events = []
for k, ln in enumerate(lines):
    cards = chunks(ln["text"].split())
    total = sum(len(" ".join(c)) for c in cards)
    nxt = lines[k + 1]["start_s"] if k + 1 < len(lines) else 57.0
    t = ln["start_s"]
    for i, c in enumerate(cards):
        text = " ".join(c)
        end = t + max(ln["dur"] * len(text) / total, 0.6)   # cards follow each other, never overlap
        if i == len(cards) - 1:
            end = min(max(end + 0.4, end), nxt)              # let the last card linger a beat
        events.append(("Caption", t, end, text.upper()))
        t = end
events.append(("Title", 0.0, 2.0, "This book is 300 years old."))
events.append(("Title", 58.0, 60.0, "Part 2"))

ass = final / "captions.ass"
ass.write_text("\n".join([
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
    "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
    "Alignment, MarginL, MarginR, MarginV, Encoding",
    # Lower third: bottom-centre, raised clear of platform UI at the very bottom.
    "Style: Caption,Inter,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,2,2,80,80,520,1",
    "Style: Title,Inter Display,124,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,3,5,90,90,0,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    *[f"Dialogue: 0,{ts(s)},{ts(e)},{st},,0,0,0,,{tx}" for st, s, e, tx in events],
]) + "\n")

# 3. Sound design: (stem, start_s, gain_dB, seek_s, length_s or None, extra filter)
SFX = [
    ("room_candles", 0.0, -24, 0, 22, ""), ("room_candles", 22.0, -24, 0, 22, ""),
    ("room_candles", 44.0, -24, 0, 13.0, "afade=t=out:st=12.4:d=0.6"),
    ("page_turn", 1.5, -8, 0, None, ""),
    ("hum_build", 0.0, -14, 0, 12, ""),
    ("hum_build", 12.0, -14, 6, 7.7, ""),                 # hum carries on, cut dead on "wrote it"
    ("footstep_echo", 11.0, -6, 0, None, ""),
    ("footsteps_approach", 12.2, -10, 0, None, "afade=t=out:st=7:d=1"),
    ("flame_flicker", 15.0, -12, 0, None, ""),
    ("breath", 24.2, -10, 0, None, ""),
    ("leather_creak", 26.0, -10, 0, None, ""),
    ("heartbeat", 30.0, -20, 0, 6, "afade=t=in:d=1.5"),     # starts quietly
    ("heartbeat", 36.0, -11, 6, 13, "afade=t=out:st=11:d=2"),  # louder through shot 4
    ("clock_tick", 44.0, -14, 0, 13.0, ""),               # stops dead at 0:57
    ("candle_snuff", 49.0, -9, 0, None, ""), ("candle_snuff", 51.2, -9, 0, None, ""),
    ("candle_snuff", 53.0, -9, 0, None, ""), ("candle_snuff", 55.0, -9, 0, None, ""),
    ("candle_snuff", 56.6, -7, 0, None, ""),
    ("pages_flip", 50.2, -10, 0, None, ""),
    ("ink_writing", 53.4, -9, 0, 3.6, "afade=t=out:st=3.2:d=0.4"),
]

inputs, parts = [], []
for i, ln in enumerate(lines):
    inputs += ["-i", str(ln["wav"])]
    gain = 2 if ln["whisper"] else 0
    parts.append(f"[{i}:a]volume={gain}dB,adelay={int(ln['start_s'] * 1000)}:all=1[d{i}]")
base = len(lines)
for j, (stem, start, gain, seek, length, extra) in enumerate(SFX):
    inputs += ["-i", str(sfx_dir / f"{stem}.mp3")]
    chain = f"[{base + j}:a]aresample=48000,aformat=channel_layouts=stereo"
    if seek or length:
        chain += f",atrim=start={seek}" + (f":duration={length}" if length else "") + ",asetpts=PTS-STARTPTS"
    if extra:
        chain += "," + extra
    chain += f",volume={gain}dB,adelay={int(start * 1000)}:all=1[s{j}]"
    parts.append(chain)
labels = "".join(f"[d{i}]" for i in range(len(lines))) + "".join(f"[s{j}]" for j in range(len(SFX)))
parts.append(f"{labels}amix=inputs={len(lines) + len(SFX)}:normalize=0:duration=longest,"
             f"atrim=0:60,apad=whole_dur=60,"
             # 0:57-1:00 is silence: one beat after the clock stops, then the Part 2 card.
             f"volume=enable='gte(t,57)':volume=0,"
             f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]")
mix = final / "mix.wav"
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
     "-map", "[mix]", "-t", "60", "-ar", "48000", str(mix)])

# 4. Picture: each clip to exactly 12 s, 1080x1920, 24 fps, one shared grade, then captions.
vin, vparts = [], []
# Shot 5 is the 10 s first/last-frame render; 0:58-1:00 is a black card for "Part 2".
CLIPS = [("shot1.mp4", 12), ("shot2.mp4", 12), ("shot3.mp4", 12), ("shot4.mp4", 12), ("shot5-v2.mp4", 10)]
for n, (name, secs) in enumerate(CLIPS, 1):
    vin += ["-i", str(ep / "shots" / name)]
    vparts.append(
        f"[{n - 1}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,"
        f"trim=duration={secs},setpts=PTS-STARTPTS,setsar=1[v{n}]")
vparts.append("color=c=black:s=1080x1920:r=24:d=2,setsar=1[v6]")
GRADE = ("eq=contrast=1.08:saturation=0.92:gamma=0.97,"
         "colorbalance=rs=0.03:gs=0.0:bs=-0.05:rm=0.04:bm=-0.04:rh=0.06:gh=0.02:bh=-0.07,"
         "curves=all='0/0 0.12/0.06 0.5/0.48 1/0.97',"
         "noise=alls=7:allf=t")
vparts.append("[v1][v2][v3][v4][v5][v6]concat=n=6:v=1:a=0," + GRADE +
              # Last candle out: fade to full black by 0:58 and hold black for the Part 2 card.
              ",fade=t=out:st=57.2:d=0.8:color=black"
              f",ass={ass}:fontsdir={FONT_DIR}[vout]")
out = final / "ep01.mp4"
run(["ffmpeg", "-v", "error", "-y", *vin, "-i", str(mix), "-filter_complex", ";".join(vparts),
     "-map", "[vout]", "-map", "5:a", "-t", "60", "-r", "24",
     "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p", "-profile:v", "high",
     "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out)])
print("wrote", out, f"{duration(out):.3f}s")
