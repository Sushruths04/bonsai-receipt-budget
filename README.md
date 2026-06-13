---
title: Bonsai
emoji: 🧾
colorFrom: green
colorTo: gray
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
tags:
  - backyard-ai
  - openbmb
  - minicpm
  - modal
  - off-brand
---

# Bonsai — see where it goes, receipt by receipt

Bonsai is a budget tracker for people who don't track. You snap a photo of a
grocery receipt; it reads every line item, tags each one (groceries, fresh,
drinks, snacks, household, going out), and shows you the breakdown — percentages
this month and a three-month trend — against a monthly budget. No moralising,
no calorie counting. Just *where the money actually went.*

## The person I built it for

Me. I'm a student in Aachen who spends ~€500/month and genuinely couldn't tell
you how much of that is Späti runs and snacks. Budgeting apps want me to type in
every purchase; I never do. A receipt photo I *will* take. The seed data in this
Space is three months of my own real REWE/Aldi/Späti receipts. After a week of
using it I moved snacks from ~22% to ~14% of my spend — not by being disciplined,
just by *seeing* it.

## How it works

```
Receipt photo ──▶ MiniCPM-V 4.5 (on Modal, vLLM + guided JSON) ──▶ structured items
                         │
       Open Food Facts lookup ──▶ category per item (model fallback for unknowns)
                         │
                  review & fix ──▶ SQLite ──▶ dashboard (donut + 3-month trend + budget)
```

- **OCR + extraction:** `openbmb/MiniCPM-V-4_5` — SOTA small-model document OCR.
  Served on **Modal** with **vLLM** and `guided_json` constrained decoding, so the
  extracted JSON is schema-valid by construction (no fragile regex repair).
- **Categorisation:** an offline lookup built from **Open Food Facts** (NOVA
  processing group + Nutri-Score + category path) handles the common case with no
  GPU call; MiniCPM fills the gaps.
- **Frontend:** a Gradio Space with a custom design system (no default theme).

## Models (all < 32B)

| Model | Size | Role |
|---|---|---|
| `openbmb/MiniCPM-V-4_5` | ~8B | Receipt OCR + structured extraction + category fallback |

## Run it locally

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in MODAL_ENDPOINT_URL + MODAL_API_KEY
modal deploy modal_app.py   # serves MiniCPM-V on a GPU; prints the endpoint URL
python app.py
```

Optional data steps:

```bash
python scripts/build_off_lookup.py                 # writes off_lookup.json
BONSAI_DB_PATH=seed.db python scripts/build_seed.py --csv scripts/seed_receipts.csv
```

## Deploying to the hackathon org

Create a Gradio Space under `build-small-hackathon`, push this repo, and set the
secrets `MODAL_ENDPOINT_URL` and `MODAL_API_KEY`. The GPU runs on Modal, so the
Space itself only needs a CPU container. (A ZeroGPU fallback exists behind
`USE_ZEROGPU_FALLBACK=1` — see `zerogpu_backend.py`.)

## Notes

- HF Spaces storage is ephemeral unless persistent storage is enabled; the
  bundled `seed.db` is re-applied on rebuild and new entries persist only with
  persistent storage on.
- Demo video: _<link>_ · Social post: _<link>_

## Tech & sponsors

Backyard AI · OpenBMB (MiniCPM-V core) · Modal (serverless GPU runtime) ·
Open Food Facts (category labels) · Off Brand (custom UI).
