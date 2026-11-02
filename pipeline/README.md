# Production pipeline

Story-agnostic tooling kept from earlier projects. Story-specific content (prompts, character locks, shot
lists, timings) lives in each new project's bible and must be replaced before reuse.

| Script | What it does |
|---|---|
| `scripts/hf.py` | Higgsfield client: submit, record the request ID immediately (merge-safe manifest), poll, download |
| `scripts/produce2.py` | References, start frames (Flux 2 Pro), Kling 3 Pro clips, Seedance 2.0 lip-synced clips; reads the bible |
| `scripts/audio.py`, `audio2.py`, `dialogue.py` | ElevenLabs voice design, dialogue, score and sound effects |
| `scripts/assemble.py` | Edit list, grade, mix, burned-in captions, end card, cover |
| `fonts/` | Cinzel (SIL OFL, licence included) |

Lessons that carry over:
- Kling image-to-video uses its image as the first frame: build a start frame per shot from locked references.
- Lip sync: Seedance 2.0 `image-to-video` with `audio_urls` (full motion, 1080p/24 fps). Not Speak (animates a still).
- Audio/image URLs must be publicly reachable (raw GitHub works while the repo is public). WAV, not MP3.
- ElevenLabs blocks designing child voices; plan child characters as non-speaking.
- Titles and cards go in post; generated text is unreliable.
- A thread swallows SystemExit: `parallel()` reports failures instead.
