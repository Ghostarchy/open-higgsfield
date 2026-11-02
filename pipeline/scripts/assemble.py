"""Assemble an Ice Wolves episode: 14 Kling clips -> graded 1080x1920 24 fps, 90.000 s, with dialogue
(if rendered), sound design, burned-in captions, black end card, and the cover with title.

Usage: python3 assemble.py <ep_dir> [--preview]
  --preview  build without dialogue (captions still timed to the script windows)
Outputs: <ep_dir>/final/ep01.mp4 (or ep01-preview.mp4), final/captions.ass, cover/cover.png
"""
import json, pathlib, subprocess, sys

ep = pathlib.Path(sys.argv[1])
PREVIEW = "--preview" in sys.argv
series = ep.parent
final = ep / "final"
final.mkdir(exist_ok=True)
FONTS = series / "fonts"
SYS_FONTS = "/usr/share/fonts/opentype/inter"
EP_NUM = ep.name.replace("ep", "")

# Shot durations from the beat sheet; 86-90 s is the black cliffhanger card.
DURS = [5, 5, 5, 5, 5, 5, 5, 7, 8, 12, 10, 5, 5, 4]
TOTAL, CARD_AT = 90.0, 86.0

# (id, speaker, start_s, window_end_s, text) - start times from the brief.
LINES = [
    ("01", "narrator", 1.0, 5.0, "Every child in the clan faced the beast. Every child was rejected."),
    ("02", "kaelen", 17.0, 20.0, "Watch how a chieftain's son does it."),
    ("03", "asha", 31.0, 34.0, "Not you, child. It will tear you apart."),
    ("04", "mira", 44.0, 48.0, "I can't see you. But I can hear you're lonely."),
    # Moved from 63.0 so the whisper lands inside the lip-synced middle of shot 11.
    ("05", "asha", 64.7, 67.7, "Vorr hasn't bowed in three hundred years..."),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def duration(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


# 1. Dialogue (trimmed of leading/trailing silence).
dlg_dir = ep / "audio/dialogue"
dlg = {} if PREVIEW else json.loads((dlg_dir / "manifest.json").read_text())
lines = []
for lid, who, start, wend, text in LINES:
    item = {"id": lid, "who": who, "start": start, "dur": wend - start, "text": text, "wav": None}
    if not PREVIEW and lid in dlg:
        src, dst = dlg_dir / dlg[lid]["file"], dlg_dir / f"{lid}.trim.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
             "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
             "-ar", "48000", "-ac", "2", str(dst)])
        item.update(wav=dst, dur=duration(dst))
    lines.append(item)
for a, b in zip(lines, lines[1:]):
    if a["start"] + a["dur"] > b["start"]:
        print(f"warning: line {a['id']} overruns line {b['id']}")

# 2. Captions: punctuation-first split, 2-5 words per card, never overlapping.
WEAK = {"the", "a", "an", "my", "his", "her", "your", "i", "of", "to", "in", "and", "it", "how", "you"}


def chunks(words):
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if w[-1] in ",.?!":
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    out = []
    for ph in phrases:
        if out and len(out[-1]) + len(ph) <= 5 and (len(ph) < 2 or len(out[-1]) < 2):
            out[-1] += ph
        elif len(ph) <= 5:
            out.append(ph)
        else:
            half = len(ph) // 2
            while half > 2 and ph[half - 1].lower().strip(",.?!") in WEAK:
                half -= 1
            out += [ph[:half], ph[half:]]
    return out


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


events = []
for k, ln in enumerate(lines):
    cards = chunks(ln["text"].split())
    total = sum(len(" ".join(c)) for c in cards)
    nxt = lines[k + 1]["start"] if k + 1 < len(lines) else CARD_AT
    t = ln["start"]
    for i, c in enumerate(cards):
        text = " ".join(c)
        end = t + max(ln["dur"] * len(text) / total, 0.7)
        if i == len(cards) - 1:
            end = min(end + 0.4, nxt)
        events.append(("Caption", t, end, text.upper()))
        t = end
# Black card: line one, then line two, both fading in.
events.append(("Card", 86.4, 90.0, r"{\fad(500,0)}SHE WASN'T BLIND."))
events.append(("Card2", 87.6, 90.0, r"{\fad(500,0)}SHE WAS WAITING."))

ass = final / "captions.ass"
ass.write_text("\n".join([
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
    "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
    "Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Caption,Inter,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,2,2,80,80,520,1",
    "Style: Card,Cinzel,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,0,0,5,80,80,1020,1",
    "Style: Card2,Cinzel,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,0,0,5,80,80,860,1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    *[f"Dialogue: 0,{ts(s)},{ts(e)},{st},,0,0,0,,{tx}" for st, s, e, tx in events],
]) + "\n")
fontsdir = final / "fonts"
fontsdir.mkdir(exist_ok=True)
for f in list(FONTS.glob("*.ttf")) + list(pathlib.Path(SYS_FONTS).glob("Inter-Bold.otf")):
    (fontsdir / f.name).write_bytes(f.read_bytes())

# 3. Sound: (stem, start, gain_dB, seek, length or None, extra filter)
SFX = [
    # Wind under everything, dropping out for the power moment (50-62) and the black card.
    ("wind", 0.0, -20, 0, 22, ""), ("wind", 22.0, -20, 0, 22, ""),
    ("wind", 44.0, -20, 0, 6.0, "afade=t=out:st=4.8:d=1.2"),
    ("wind", 62.0, -20, 0, 22, "afade=t=in:d=1.5"), ("wind", 84.0, -20, 0, 2.0, ""),
    ("crowd_murmur", 5.0, -24, 0, 15, "afade=t=in:d=1"), ("crowd_murmur", 20.0, -24, 0, 15, ""),
    ("crowd_murmur", 35.0, -26, 0, 14.5, "afade=t=out:st=13:d=1.5"),
    ("wolf_snarl", 11.6, -6, 0, None, ""), ("child_scream_run", 12.4, -10, 0, None, ""),
    ("crowd_cheer", 15.4, -12, 0, None, ""),
    ("giant_roar", 20.3, -2, 0, None, ""), ("crowd_gasp", 22.4, -9, 0, None, ""),
    ("stick_tap", 25.3, -12, 0, None, ""), ("kids_laugh", 26.2, -12, 0, None, ""),
    ("footsteps_snow", 35.0, -12, 0, None, ""),
    ("wolf_snarl", 42.4, -8, 0, None, ""), ("spears_raise", 45.0, -12, 0, None, ""),
    # Power moment: total silence except the wolf's breath (plus a barely-there rune shimmer).
    ("wolf_breath", 50.0, -8, 0, 12, "afade=t=out:st=11:d=1"),
    ("runes_shimmer", 55.0, -24, 0, None, ""),
    ("spear_drop", 63.4, -8, 0, None, ""), ("clan_kneel", 68.5, -12, 0, None, ""),
    ("crowd_murmur", 66.0, -28, 0, 6, "afade=t=in:d=1,afade=t=out:st=5:d=1"),
    ("war_horns", 72.0, -4, 0, None, ""), ("gate_crack", 74.0, -6, 0, None, ""),
    ("monster_growls", 77.5, -8, 0, None, ""), ("wolf_growl_turn", 79.2, -6, 0, None, ""),
    ("eye_glow", 82.2, -10, 0, 3.8, ""),
    ("drum_hit", 86.0, -1, 0, None, ""),
]
sfx_dir = ep / "audio/sfx"
inputs, parts, labels = [], [], []
idx = 0
for ln in lines:
    if ln["wav"] is None:
        continue
    inputs += ["-i", str(ln["wav"])]
    parts.append(f"[{idx}:a]adelay={int(ln['start'] * 1000)}:all=1[a{idx}]")
    labels.append(f"[a{idx}]"); idx += 1
for stem, start, gain, seek, length, extra in SFX:
    inputs += ["-i", str(sfx_dir / f"{stem}.mp3")]
    chain = f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo"
    if seek or length:
        chain += f",atrim=start={seek}" + (f":duration={length}" if length else "") + ",asetpts=PTS-STARTPTS"
    if extra:
        chain += "," + extra
    chain += f",volume={gain}dB,adelay={int(start * 1000)}:all=1[a{idx}]"
    parts.append(chain); labels.append(f"[a{idx}]"); idx += 1
parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
             f"atrim=0:{TOTAL},apad=whole_dur={TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]")
mix = final / ("mix-preview.wav" if PREVIEW else "mix-current.wav")
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
     "-map", "[mix]", "-t", str(TOTAL), "-ar", "48000", str(mix)])

# 4. Picture: one shared grade (cool silver shadows, warm torch highlights, grain).
vin, vparts = [], []
# Edit list: (clip, in-point, duration). On-camera dialogue uses lip-synced (Speak) clips when present.
def shot(n):
    lip = ep / "clips" / f"shot{n:02d}-lipsync.mp4"
    return lip if lip.exists() else ep / "clips" / f"shot{n:02d}.mp4"


EDL = []
for n, secs in enumerate(DURS, 1):
    if n == 11 and (ep / "clips/shot11b-lipsync.mp4").exists():
        # Kling: spear drops -> Speak: whisper -> Kling: the clan kneels.
        EDL += [(ep / "clips/shot11.mp4", 0, 2.5), (ep / "clips/shot11b-lipsync.mp4", 0, 5),
                (ep / "clips/shot11.mp4", 7.5, 2.5)]
    else:
        EDL.append((ep / "clips" / f"shot{n:02d}.mp4" if n == 11 else shot(n), 0, secs))
assert abs(sum(d for _, _, d in EDL) - CARD_AT) < 1e-6, "edit list must end at the card"
for i, (clip, start, secs) in enumerate(EDL):
    vin += ["-i", str(clip)]
    vparts.append(f"[{i}:v]trim=start={start}:duration={secs},setpts=PTS-STARTPTS,"
                  f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,"
                  f"fps=24,setsar=1[v{i}]")
vparts.append("color=c=black:s=1080x1920:r=24:d=4,setsar=1[vcard]")
GRADE = ("eq=contrast=1.06:saturation=0.9,"
         "colorbalance=rs=-0.04:bs=0.05:rm=-0.02:bm=0.03:rh=0.04:gh=0.01:bh=-0.02,"
         "noise=alls=6:allf=t")
chain = "".join(f"[v{i}]" for i in range(len(EDL)))
vparts.append(f"{chain}concat=n={len(EDL)}:v=1:a=0,{GRADE}[graded]")
vparts.append(f"[graded][vcard]concat=n=2:v=1:a=0,ass={ass}:fontsdir={fontsdir}[vout]")
# A cut with any line still unvoiced is labelled interim so it is never mistaken for the final.
missing = [ln["id"] for ln in lines if ln["wav"] is None]
if PREVIEW:
    out = final / "ep01-preview.mp4"
elif missing:
    out = final / f"ep{EP_NUM}-interim.mp4"
    print("interim cut, caption-only lines:", ", ".join(missing))
else:
    out = final / f"ep{EP_NUM}.mp4"
run(["ffmpeg", "-v", "error", "-y", *vin, "-i", str(mix), "-filter_complex", ";".join(vparts),
     "-map", "[vout]", "-map", f"{len(EDL)}:a", "-t", str(TOTAL), "-r", "24",
     # 4 Mbps cap keeps a 90 s episode near 45 MB, under GitHub's 50 MB warning.
     "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "4M", "-bufsize", "8M",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
print("wrote", out, f"{duration(out):.3f}s")

# 5. Cover: art + silver Cinzel title + large episode number.
cover = ep / "cover" / "cover.png"
cinzel = FONTS / "Cinzel.ttf"
title_style = (f"fontfile={cinzel}:fontcolor=0xE6EBF2:shadowcolor=0x0B1626@0.85:shadowx=0:shadowy=4:"
               f"x=(w-text_w)/2")
# A soft top-down fade (no hard edge) keeps the silver title legible over the sky.
run(["ffmpeg", "-v", "error", "-y", "-i", str(ep / "cover/cover-art.png"), "-filter_complex",
     "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[art];"
     "color=c=0x0B1626:s=1080x1920,format=rgba,geq=r=11:g=22:b=38:a='190*pow(max(0,1-Y/950),1.5)'[fade];"
     "[art][fade]overlay,"
     f"drawtext=text='THE BLIND GIRL':fontsize=104:y=150:{title_style},"
     f"drawtext=text='THE ICE WOLVES':fontsize=104:y=275:{title_style},"
     f"drawtext=text='CHOSE':fontsize=104:y=400:{title_style},"
     f"drawtext=text='EP{EP_NUM}':fontsize=190:y=540:{title_style}",
     "-frames:v", "1", str(cover)])
print("wrote", cover)
