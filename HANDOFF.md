# Bonsai — Handoff for the executing agent

Full design rationale: `~/.claude/plans/i-need-you-to-ancient-honey.md`.
This file is the **do-this-next checklist**. Deadline: **2026-06-15**.

## What's already built & tested ✅
The whole app skeleton is written and the data layer is verified end-to-end
(seed build, month/category aggregations, 3-month trend, insights, categoriser,
schema round-trip all pass with `pydantic`/`pandas` only).

| File | State |
|---|---|
| `config.py`, `schema.py`, `db.py`, `insights.py` | ✅ done & tested |
| `categorize.py` (OFF lookup + override map + model fallback) | ✅ done; fallback untested (needs endpoint) |
| `charts.py`, `ui/theme.py`, `ui/styles.css`, `app.py` | ✅ written; need a live run with gradio/plotly installed |
| `extract.py` | ✅ written; needs the live Modal endpoint to test |
| `modal_app.py` (vLLM serving MiniCPM-V) | ✅ written; **must be deployed + version-pinned** |
| `zerogpu_backend.py` | ✅ break-glass fallback |
| `scripts/build_off_lookup.py`, `scripts/build_seed.py`, `scripts/seed_receipts.csv` | ✅ done; seed.db built from the sample CSV |
| `README.md` (HF frontmatter + tags), `.env.example`, `requirements.txt` | ✅ done |

## Do these in order

1. **Deploy the GPU backend.**
   - In `modal_app.py`: confirm `VLLM_VERSION` against the **MiniCPM-V-4_5 model
     card**, set a real `API_KEY`. Then `modal token new` and `modal deploy modal_app.py`.
   - Smoke-test with a real receipt:
     `curl -H "Authorization: Bearer <API_KEY>" -X POST <url>/v1/chat/completions -d '{...}'`.
   - **Risk:** if vLLM won't take MiniCPM-V *image* inputs cleanly, switch to the
     transformers `model.chat()` Modal-class variant (plan B in the plan, Phase 1)
     — keep the same `/v1`-style contract `extract.py` expects, or point
     `extract.py` at it.

2. **Wire secrets.** Copy `.env.example` → `.env` locally; on the Space set
   `MODAL_ENDPOINT_URL` (= `<url>/v1`) and `MODAL_API_KEY`.

3. **Run locally.** `pip install -r requirements.txt && python app.py`.
   Upload a real receipt → check the Review grid → Save → Dashboard updates.
   (gradio/plotly/openai are NOT installed in the planning env — install them.)

4. **Build the OFF category lookup.** `pip install datasets && python scripts/build_off_lookup.py`
   → commit `off_lookup.json`. Improves auto-categorisation coverage.

5. **Seed with the USER'S REAL receipts** (this is the Backyard AI proof).
   Either run real images through the pipeline
   (`python scripts/build_seed.py --images 'receipts/*.jpg'`) and hand-correct,
   or fill `scripts/seed_receipts.csv` with real purchases and
   `BONSAI_DB_PATH=seed.db python scripts/build_seed.py --csv scripts/seed_receipts.csv`.
   Commit the resulting `seed.db`. Replace the placeholder sample rows.

6. **Deploy to HF.** Create a Gradio Space under `build-small-hackathon`, push
   this repo, set the two secrets. Verify it reaches Modal (check Modal logs) and
   **test on mobile**.

7. **Submission assets (required to be eligible).**
   - Record a 60–90s demo video (upload → review → dashboard); link in README.
   - Post once on social; link it in README.
   - Confirm README frontmatter tags are present.

8. **Stretch only if 1–7 are done & deployed:** fine-tune the categoriser LoRA on
   Open Food Facts via Modal, publish to HF, flag-swap it into `categorize.py`.
   (Plan Phase 9. Don't start early.)

## Gotchas
- Don't add torch/vllm to `requirements.txt` — GPU is on Modal; the Space is CPU.
- `seed.db` is re-applied on rebuild; new entries persist only if HF persistent
  storage is enabled.
- Keep the look non-generic (custom CSS is in `ui/styles.css`) — that's the Off
  Brand badge and an explicit user requirement.
- Don't claim Tiny Titan — MiniCPM-V is ~8B, not ≤4B.
