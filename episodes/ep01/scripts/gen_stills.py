"""Generate one Soul Cinema reference still each for Elena and Lucien.

Records request IDs in stills/manifest.json the moment they are queued, then polls and downloads.
Usage: python3 -I gen_stills.py <episode_dir>
"""
import json, os, sys, time, pathlib, requests

ep = pathlib.Path(sys.argv[1])
out = ep / "stills"
out.mkdir(parents=True, exist_ok=True)
BASE = os.environ["HF_API_BASE_URL"].rstrip("/")
AUTH = {"Authorization": f"Key {os.environ['OPEN_HIGGSFIELD_API_KEY']}"}
MODEL = "higgsfield-ai/soul/cinema"

ELENA = ("a woman in her late twenties with long dark wavy hair, wearing a fitted black "
         "button-up blouse with a collar")
LUCIEN = ("a tall man in his thirties with sharp features and short dark hair, wearing a dark "
          "suit, tie pulled loose, top shirt button undone, no pocket square")
LOOK = ("standing in a candlelit antique library at night, towering dark bookshelves behind, "
        "warm amber candlelight on the face, deep black shadows, slight film grain, "
        "cinematic dark romance film still, waist-up portrait, looking toward camera, "
        "face clearly visible and sharp")

STILLS = {
    "elena": f"Character reference portrait of {ELENA}, {LOOK}.",
    "lucien": f"Character reference portrait of {LUCIEN}, {LOOK}.",
    # v2: v1 rendered a white pocket square and a dated film-stock grade.
    "lucien-v2": (f"Character reference portrait of {LUCIEN}, plain jacket breast pocket, "
                  f"white shirt open at the throat, {LOOK}, modern digital cinema look, "
                  "same warm amber grade as a contemporary period drama."),
}
ONLY = sys.argv[2:] or list(STILLS)
STILLS = {k: v for k, v in STILLS.items() if k in ONLY}

manifest_path = out / "manifest.json"
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

def save():
    manifest_path.write_text(json.dumps(manifest, indent=2))

for name, prompt in STILLS.items():
    body = {"prompt": prompt, "batch_size": 1, "resolution": "1080p",
            "aspect_ratio": "9:16", "enhance_prompt": False}
    r = requests.post(f"{BASE}/{MODEL}", headers=AUTH, json=body, timeout=60)
    if not r.ok:
        sys.exit(f"{name}: HTTP {r.status_code} {r.text[:500]}")
    rid = r.json()["request_id"]
    manifest[name] = {"model": MODEL, "request": body, "request_id": rid, "status": "queued"}
    save()
    print(name, "queued", rid)

for name, entry in [(k, manifest[k]) for k in STILLS]:
    while True:
        s = requests.get(f"{BASE}/requests/{entry['request_id']}/status", headers=AUTH, timeout=60).json()
        st = s.get("status")
        if st in ("completed", "failed", "nsfw", "cancelled"):
            break
        time.sleep(5)
    entry["status"] = st
    if st == "completed":
        url = s["images"][0]["url"]
        entry["url"] = url
        path = out / f"{name}-ref.png"
        path.write_bytes(requests.get(url, timeout=120).content)
        entry["file"] = path.name
    else:
        entry["error"] = s.get("error")
    save()
    print(name, st, entry.get("file"))
