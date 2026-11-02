"""Tiny Higgsfield platform client: submit, record the request ID immediately, poll, download."""
import fcntl, json, os, time, pathlib, requests

BASE = os.environ["HF_API_BASE_URL"].rstrip("/")
AUTH = {"Authorization": f"Key {os.environ['OPEN_HIGGSFIELD_API_KEY']}"}
DONE = ("completed", "failed", "nsfw", "cancelled")


class Ledger:
    """A JSON manifest that is rewritten after every change, so request IDs survive a crash."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def set(self, key, **fields):
        # Several runs can share one manifest: re-read under a lock and merge, never overwrite.
        with open(self.path.with_suffix(".lock"), "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if self.path.exists():
                self.data = json.loads(self.path.read_text())
            self.data.setdefault(key, {}).update(fields)
            self.path.write_text(json.dumps(self.data, indent=2))
        return self.data[key]


def submit(ledger, key, model, body):
    r = requests.post(f"{BASE}/{model}", headers=AUTH, json=body, timeout=60)
    if not r.ok:
        raise SystemExit(f"{key}: HTTP {r.status_code} {r.text[:500]}")
    rid = r.json()["request_id"]
    ledger.set(key, model=model, request=body, request_id=rid, status="queued")
    print(key, "queued", rid, flush=True)
    return rid


def wait(ledger, key, dest, interval=8):
    rid = ledger.data[key]["request_id"]
    while True:
        s = requests.get(f"{BASE}/requests/{rid}/status", headers=AUTH, timeout=60).json()
        if s.get("status") in DONE:
            break
        time.sleep(interval)
    st = s["status"]
    if st != "completed":
        ledger.set(key, status=st, error=s.get("error"))
        print(key, st, s.get("error"), flush=True)
        return None
    url = (s.get("video") or {}).get("url") or s["images"][0]["url"]
    pathlib.Path(dest).write_bytes(requests.get(url, timeout=300).content)
    ledger.set(key, status=st, url=url, file=pathlib.Path(dest).name)
    print(key, "completed", dest, flush=True)
    return url
