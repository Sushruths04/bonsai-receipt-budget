# Build Small Hackathon — Master Strategy Report

**For:** Sushruth | **Goal:** Win prize money, cover max sponsors, build 3 apps  
**Hackathon:** Build Small (Hugging Face × Gradio) | **Status:** LIVE NOW (June 2026)

-----

## 1. Hackathon Overview

|Detail                 |Info                                                       |
|-----------------------|-----------------------------------------------------------|
|**Host**               |Hugging Face × Gradio                                      |
|**Total Prize Pool**   |$48,000+ cash + physical prizes                            |
|**Tracks**             |Backyard AI + Adventure in Thousand Token Wood             |
|**Format**             |Gradio Spaces on HF org `build-small-hackathon`            |
|**Model constraint**   |Small models ≤ 32B parameters                              |
|**Participant credits**|$250 Modal + $100 Codex + $20 HF — for every registrant    |
|**Awards stack?**      |YES — one app can win track prize + multiple sponsor prizes|
|**Submissions**        |Submit as many apps as you like                            |

-----

## 2. Complete Sponsor & Prize Map

|Sponsor                |Prize                                                    |How to Qualify                                          |Models/Tools                                                              |
|-----------------------|---------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------------------------|
|**HuggingFace (Track)**|1st: $4k · 2nd: $2.5k · 3rd: $1.5k · 4th: $1k (per track)|Top placement in Backyard AI or Thousand Token Wood     |Any small model ≤32B                                                      |
|**OpenBMB**            |$5k pool per track ($10k total)                          |Use MiniCPM models as core brain                        |MiniCPM-V 4.6, MiniCPM-o 4.5, MiniCPM5-1B, MiniCPM4.1-8B, VoxCPM2         |
|**NVIDIA**             |Two RTX 5080 GPUs (physical, ~$1,000 each)               |Best space + community engagement using Nemotron        |Nemotron-Nano, Nemotron-Omni, Nemotron-ASR, Nemotron-Parse, Nemotron-Embed|
|**OpenAI**             |ChatGPT Pro subscription (1 year)                        |Codex-attributed commits in GitHub repo or Space history|OpenAI Codex (coding AI)                                                  |
|**Modal**              |$20k credits for winners + $250 per participant          |Build/deploy on Modal compute                           |Modal serverless GPU compute                                              |
|**Cohere**             |Part of prize pool                                       |Use Tiny Aya or Cohere Transcribe                       |Tiny Aya (multilingual LLM) · Cohere Transcribe (ASR/voice)               |
|**Black Forest Labs**  |Prize (via track judge picks)                            |Use FLUX.2-klein for image generation                   |FLUX.2-klein (4B/9B diffusion)                                            |
|**Community Choice**   |$2,000                                                   |Most likes/interactions on HF Space                     |Any — visual, shareable, emotional wins votes                             |

### Bonus Merit Badges (bonus on top — collect them all)

- **Tiny Titan**: All models ≤ 4B
- **Custom UI**: Frontend beyond default Gradio (use `gr.Server`)
- **Fine-tuned model**: Publish a fine-tuned model on HF
- **llama.cpp runtime**: Run model via llama.cpp
- **Agent trace**: Share agent trace on Hub
- **Blog post**: Publish a write-up on HF blog

-----

## 3. Your 3 Ideas — Evaluated

### Your Idea 1: Smart Budget + Junk Food Tracker

Receipt photo → OCR → categorize spending + junk food → budget advisor

|Dimension                |Score     |Notes                                                                      |
|-------------------------|----------|---------------------------------------------------------------------------|
|**Track fit**            |⭐⭐⭐⭐⭐     |Perfect Backyard AI — real problem for a real person                       |
|**Uniqueness**           |⭐⭐⭐⭐      |No existing app combines budget + junk food in one small-model Gradio Space|
|**Sponsor coverage**     |⭐⭐⭐⭐⭐     |OpenBMB (MiniCPM-V) + Cohere (multilingual) + Modal (background)           |
|**Your skills fit**      |⭐⭐⭐⭐⭐     |Your CV/OCR/anomaly detection + RAG experience is directly applicable      |
|**Buildability (3 days)**|⭐⭐⭐⭐      |Moderate — receipt OCR + budget logic + Gradio UI                          |
|**Prize potential**      |⭐⭐⭐⭐⭐     |Track prize ($4k) + OpenBMB ($2.5k) + Modal ($10k credits) + Cohere        |
|**Overall**              |**9.5/10**|**Your strongest idea — build this first**                                 |

### Your Idea 2: Kid Photo → Sketch + Painting Tool

Photo → FLUX.2-klein line art → in-app canvas painting for kids

|Dimension                |Score     |Notes                                                                |
|-------------------------|----------|---------------------------------------------------------------------|
|**Track fit**            |⭐⭐⭐⭐⭐     |Perfect Thousand Token Wood — whimsical, visual, kid-focused         |
|**Uniqueness**           |⭐⭐⭐       |Many apps do photo-to-sketch; your angle is the in-app painting on HF|
|**Sponsor coverage**     |⭐⭐⭐⭐      |Black Forest Labs (FLUX.2-klein) + OpenBMB (optional MiniCPM tips)   |
|**Your skills fit**      |⭐⭐⭐⭐      |Good — uses your CV/vision model experience                          |
|**Buildability (3 days)**|⭐⭐⭐       |Canvas JS overlay in Gradio is tricky but doable                     |
|**Prize potential**      |⭐⭐⭐⭐      |Track prize + Black Forest Labs + Community Choice if shareable      |
|**Overall**              |**7.5/10**|Good secondary project for Thousand Token Wood                       |

### Your Idea 3: Voice-Cloned Bedtime Stories

Mom records voice → MiniCPM generates story → VoxCPM2/XTTS narrates it in mom’s voice

|Dimension                |Score     |Notes                                                                                             |
|-------------------------|----------|--------------------------------------------------------------------------------------------------|
|**Track fit**            |⭐⭐⭐⭐⭐     |Thousand Token Wood — emotional, whimsical, clearly AI-powered                                    |
|**Uniqueness**           |⭐⭐⭐       |Many existing consumer apps (MomSays, Totora, MamaTales) do this, but none as small-model HF Space|
|**Sponsor coverage**     |⭐⭐⭐⭐⭐     |OpenBMB (MiniCPM + VoxCPM2) + Cohere (multilingual + Transcribe)                                  |
|**Your skills fit**      |⭐⭐⭐⭐      |Good — uses your NLP + audio pipeline skills                                                      |
|**Buildability (3 days)**|⭐⭐⭐       |Voice cloning setup is time-consuming; VoxCPM2 is easiest path                                    |
|**Prize potential**      |⭐⭐⭐⭐⭐     |Track prize + OpenBMB + Cohere + Community Choice (parents share viral clips)                     |
|**Overall**              |**8.5/10**|Strong secondary for Wood, especially with VoxCPM2 for OpenBMB alignment                          |

-----

## 4. Top 15 Ideas — Master Strategy Table

### Legend for Sponsor Coverage

`MB` = MiniCPM/OpenBMB · `NV` = NVIDIA Nemotron · `CO` = Cohere · `BF` = Black Forest Labs · `MD` = Modal · `CX` = OpenAI Codex

-----

### Track A: Backyard AI (Real problems for real people)

|Rank |App Name                                                       |Real Problem                                                                         |Core AI Stack                                                                                                   |Sponsors              |Win Chance|Difficulty|Unique Angle                                                                                               |
|-----|---------------------------------------------------------------|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------------------|----------|----------|-----------------------------------------------------------------------------------------------------------|
|**1**|**Smart Receipt + Budget Advisor** *(Your Idea 1)*             |Students/immigrants overspend on junk food; can’t manage monthly budget              |MiniCPM-V (OCR + classify) + Cohere Tiny Aya (multilingual advice) + Modal (background inference)               |MB · CO · MD          |**★★★★★** |Medium    |Combines budget + junk food + nutrition goals in one app. You = real user. Receipt photo is fast proof.    |
|**2**|**German Document Decoder**                                    |Immigrants/students can’t understand Behördenbriefe, rental contracts, insurance docs|MiniCPM-V (doc reading + summarize) + Cohere Tiny Aya (translate to Turkish/Arabic/Hindi) + VoxCPM2 (read aloud)|MB · CO               |**★★★★★** |Easy-Med  |Very relevant in Germany. You can demo with a real Aachen neighbor. Multilingual = Cohere prize sweet spot.|
|**3**|**Lab Anomaly Detection Dashboard** *(Perplexity Idea 3)*      |RWTH lab or student workshop has sensor/image data but no AI anomaly detection       |MiniCPM-V (visual inspection) + Nemotron-Nano (reasoning/explanation) + Modal (batch inference)                 |MB · NV · MD          |**★★★★**  |Hard      |Directly uses your robotics/CV/anomaly detection skills. NVIDIA GPU prize if Nemotron is core brain.       |
|**4**|**Research Paper RAG Assistant** *(Perplexity Idea 1 enhanced)*|MSc/PhD students overwhelmed by papers, need summaries, Q&A, study plans             |MiniCPM (RAG + Q&A on PDFs) + Nemotron-Embed (embedding) + Cohere Transcribe (voice Q&A) + Modal                |MB · NV · CO · MD · CX|**★★★★**  |Medium    |Uses your RAG thesis experience directly. Stack 4+ sponsors. Build with Codex → Codex prize.               |
|**5**|**Car Dashboard Warning Interpreter**                          |Non-technical drivers terrified by warning lights on dashboard                       |MiniCPM-V (photo → identify lights + explain + urgency) + Cohere (multilingual)                                 |MB · CO               |**★★★★**  |Easy      |Near-zero competition on HF. Every family member with a car is a real user. Fast to build.                 |
|**6**|**Local Shop Inventory AI**                                    |Small Aachen shop owner takes shelf photos → needs stock count + reorder advice      |MiniCPM-V (count items from image) + Nemotron-Nano (business reasoning) + Modal (background)                    |MB · NV · MD          |**★★★**   |Medium    |Targets NVIDIA Nemotron (GPU prize) + OpenBMB. Good B2B Backyard AI story.                                 |
|**7**|**On-Device Medication Helper (Elderly)**                      |Elderly parents confused by medication names, side effects, doctor notes             |MiniCPM-V (read prescription/label) + Cohere Transcribe (voice input) + VoxCPM2 (audio output)                  |MB · CO               |**★★★★**  |Medium    |Highly emotional story. “I built this for my grandparent.” Full voice-in/out pipeline = Cohere showcase.   |
|**8**|**ADHD Focus Journal + Task Breaker**                          |People with ADHD struggle with task management, brain dumps, daily planning          |Nemotron-Nano (break tasks into micro-steps) + Cohere Transcribe (voice dump) + MiniCPM (weekly insights)       |MB · NV · CO          |**★★★**   |Medium    |Note: competition exists (NeuroBait is already in hackathon). Differentiate with Nemotron reasoning.       |

-----

### Track B: Thousand Token Wood (Creative, whimsical, AI-as-the-core)

|Rank  |App Name                                                 |Concept                                                                                                                                |Core AI Stack                                                                                                                    |Sponsors         |Win Chance|Difficulty|Unique Angle                                                                                                                             |
|------|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|-----------------------------------------------------------------------------------------------------------------------------------------|
|**9** |**Dream Visualizer + Interpreter**                       |User types or speaks a dream → AI interprets symbols → generates surreal art → reads it back                                           |MiniCPM or Nemotron-Nano (symbolic analysis) + FLUX.2-klein (surreal art) + VoxCPM2 (narration) + Cohere Transcribe (voice input)|MB · NV · BF · CO|**★★★★★** |Medium    |Covers 4 sponsors in one app. Dreams are deeply personal and shareable. NVIDIA GPU prize via Nemotron. Strong Community Choice candidate.|
|**10**|**Voice-Cloned Bedtime Stories** *(Your Idea 3 enhanced)*|Mom records voice → kid picks genre/theme → MiniCPM writes story → VoxCPM2 narrates in mom’s voice                                     |MiniCPM5-1B (story gen) + VoxCPM2 (voice TTS with clone) + Cohere Tiny Aya (multilingual)                                        |MB · CO          |**★★★★★** |Med-Hard  |VoxCPM2 is OpenBMB’s own TTS → perfect OpenBMB alignment. Emotional = viral = Community Choice votes.                                    |
|**11**|**Kid Photo → Sketch + Paint** *(Your Idea 2 enhanced)*  |Photo → line art sketch → kid paints on it in-browser                                                                                  |FLUX.2-klein + line art LoRA + MiniCPM (fun story about drawing) + custom JS canvas                                              |MB · BF          |**★★★★**  |Med       |Black Forest Labs prize alignment. Add story narration (MiniCPM) to differentiate from plain photo-to-sketch apps.                       |
|**12**|**Interactive Branching Story + AI Illustrations**       |User picks genre + characters → Nemotron writes branching plot → FLUX.2-klein illustrates each scene                                   |Nemotron-Nano (story + branching logic) + FLUX.2-klein (scene images) + Cohere Tiny Aya (multilingual)                           |NV · BF · CO     |**★★★★**  |Medium    |NVIDIA GPU prize potential (Nemotron as story brain). Illustrated interactive fiction is visually stunning for demos.                    |
|**13**|**AI Plant Doctor + Fantasy Portrait**                   |Photo of plant → MiniCPM-V diagnoses health issue → FLUX.2-klein generates fantasy portrait of plant → care tips in plant’s “own voice”|MiniCPM-V (diagnosis) + FLUX.2-klein (portrait) + VoxCPM2 (plant voice TTS)                                                      |MB · BF          |**★★★★**  |Easy-Med  |Extremely shareable (plant lovers post everywhere). Easy to demo. Covers Black Forest Labs + OpenBMB. Fast to build.                     |
|**14**|**Micro-Fiction Zine Generator**                         |1-sentence prompt → 3-panel story (MiniCPM) → 3 illustrations (FLUX.2-klein) → downloadable mini-zine PDF                              |MiniCPM5-1B (story panels) + FLUX.2-klein (panel art) + Cohere (multilingual)                                                    |MB · BF · CO     |**★★★**   |Easy-Med  |PDF download is practical. Artists and writers will share their zines. Good Community Choice candidate.                                  |
|**15**|**AI Neighborhood Simulator**                            |Tiny MiniCPM agents (baker, doctor, café owner) live in a neighborhood; user actions trigger agent reactions                           |MiniCPM5-1B × multiple agents + Modal (background simulation loop) + Nemotron-Embed (agent memory)                               |MB · NV · MD     |**★★★**   |Hard      |Very creative — if it runs smoothly, it’s unforgettable. But risk of overengineering. Only attempt if time allows.                       |

-----

## 5. Recommended 3-App Strategy — Maximum Prize Money

The core principle: **each app should stack 3+ prize categories.** Awards stack completely.

-----

### App 1 — PRIMARY (Backyard AI) ⭐ Highest cash potential

**Build: Smart Receipt + Budget + Junk Food Advisor**

|Element                |Detail                                                                                                           |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
|**Track**              |Backyard AI                                                                                                      |
|**Real user**          |You or a student friend in Aachen — use real receipts from REWE/Aldi                                             |
|**Core model**         |MiniCPM-V 4.6 (OCR + item extract + junk food classify + advice)                                                 |
|**Sponsor 2**          |Cohere Tiny Aya — translate advice to user’s native language (Turkish/Hindi/etc.)                                |
|**Sponsor 3**          |Modal — run inference jobs in background (batch receipt processing)                                              |
|**Build with**         |OpenAI Codex — commit Codex-attributed code → qualifies for ChatGPT Pro prize                                    |
|**Badges to target**   |Tiny Titan (all models ≤4B) · Custom UI · Blog post                                                              |
|**Demo proof**         |5 real receipt photos → show junk food table, daily budget limit, monthly forecast                               |
|**Prize stack**        |Backyard AI 1st ($4,000) + OpenBMB Backyard ($2,500) + Modal winner credits ($10,000) + Cohere pool + ChatGPT Pro|
|**Estimated potential**|**~$17,000+ in cash + credits**                                                                                  |

**Feature scope (3 days):**

1. Receipt photo upload → MiniCPM-V extracts store, items, prices as JSON
1. Junk food classifier → table showing (chips, soda, cake) vs (bread, vegetables, etc.)
1. Budget tracker → set €500/month → shows daily limit, remaining budget, overspend warning
1. AI advice → “You spent €38 on chips this month. Cut to once a week → save €25/month.”
1. Optional: Cohere Tiny Aya → all advice output in user’s native language
1. Optional: Modal → run MiniCPM inference in background for batch receipts

-----

### App 2 — SECONDARY (Thousand Token Wood) ⭐ Emotional + multi-sponsor

**Build: Dream Visualizer + Interpreter**

|Element                |Detail                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
|**Track**              |Thousand Token Wood                                                                                                                             |
|**Concept**            |User types or speaks a dream → AI analyzes symbols → generates surreal art → narrates the interpretation                                        |
|**Core model**         |Nemotron-Nano (deep symbolic/psychological reasoning about dream content)                                                                       |
|**Sponsor 2**          |FLUX.2-klein (Black Forest Labs) — surreal/dreamlike image of the dream                                                                         |
|**Sponsor 3**          |VoxCPM2 (OpenBMB) — narrates the interpretation in a calm, atmospheric voice                                                                    |
|**Sponsor 4**          |Cohere Transcribe — user speaks their dream instead of typing                                                                                   |
|**Sponsor 5**          |Modal — run FLUX generation as background job                                                                                                   |
|**NVIDIA angle**       |Nemotron-Nano as the reasoning core → qualifies for RTX 5080 GPU prize                                                                          |
|**Demo proof**         |Record yourself speaking a dream → show generated art + interpretation → clip for social media                                                  |
|**Prize stack**        |Thousand Token Wood 1st ($4,000) + OpenBMB Wood ($2,500) + NVIDIA RTX 5080 GPU ($1,000) + Black Forest Labs + Cohere + Community Choice ($2,000)|
|**Estimated potential**|**~$10,000+ in cash + GPU + credits**                                                                                                           |

**Feature scope (3 days):**

1. Text input OR voice input (Cohere Transcribe) of a dream
1. Nemotron-Nano: analyze dream symbols → produce structured interpretation (themes, emotions, meaning)
1. FLUX.2-klein: generate a surreal dream-scene image from key symbols
1. VoxCPM2: narrate the interpretation in a calm, atmospheric voice
1. Gallery: show past dreams + their art
1. Share button → downloads art + text for social sharing (viral = Community Choice votes)

-----

### App 3 — BOOSTER (Thousand Token Wood or Backyard AI) ⭐ Cover remaining sponsors

**Build: Voice-Cloned Bedtime Stories** (Your Idea 3 — upgraded)

|Element                |Detail                                                                                                         |
|-----------------------|---------------------------------------------------------------------------------------------------------------|
|**Track**              |Thousand Token Wood                                                                                            |
|**Concept**            |Mom records voice (30 sec) → kid picks genre → MiniCPM generates story → VoxCPM2 narrates in mom’s cloned voice|
|**Core model**         |MiniCPM5-1B (story generation — short, age-appropriate, genre-based)                                           |
|**Sponsor 2**          |VoxCPM2 (OpenBMB’s own TTS/voice clone) — deepens OpenBMB prize case                                           |
|**Sponsor 3**          |Cohere Tiny Aya — multilingual (generate + narrate story in German/Hindi/Arabic)                               |
|**Why this as App 3**  |Covers OpenBMB (VoxCPM2) and Cohere again from a different angle, and is highly viral for Community Choice     |
|**Demo proof**         |Record mom/friend’s voice → show kid UI → play story in their voice → parents will share the clip              |
|**Prize stack**        |Thousand Token Wood 2nd/3rd ($1,500–$2,500) + Community Choice ($2,000) + Cohere pool                          |
|**Estimated potential**|**~$4,000–$6,000 in cash + credits**                                                                           |

**Feature scope (3 days):**

1. Voice recording UI (30-60 sec) — record or upload WAV
1. VoxCPM2 voice clone creation from reference audio
1. Kid-friendly genre selector: King, Animal, Space, Adventure, Fairy Tale
1. MiniCPM5-1B: generate 2-minute age-appropriate story from genre + kid’s name
1. VoxCPM2: TTS narration in cloned voice → audio player
1. Optional: Cohere Tiny Aya → generate story in German/Hindi/Turkish

-----

## 6. Prize Stacking Calculator (Realistic Estimate)

|Prize Category        |App 1 (Budget)|App 2 (Dreams)   |App 3 (Stories)|Total                                      |
|----------------------|--------------|-----------------|---------------|-------------------------------------------|
|Track 1st place       |$4,000        |—                |—              |$4,000                                     |
|Track 2nd/3rd         |—             |$2,500–$4,000    |$1,500–$2,500  |$4,000–$6,500                              |
|OpenBMB (per track)   |$2,500        |$2,500           |—              |$5,000                                     |
|NVIDIA RTX 5080 GPU   |—             |$1,000 (physical)|—              |$1,000                                     |
|Modal credits (winner)|$10,000       |$7,000           |—              |$17,000                                    |
|Cohere pool           |Partial       |Partial          |Partial        |~$1,500                                    |
|Community Choice      |—             |$2,000           |$2,000         |$2,000–$4,000                              |
|ChatGPT Pro (Codex)   |✓             |—                |—              |Subscription                               |
|**Realistic total**   |              |                 |               |**$30,000–$38,000 in cash + credits + GPU**|


> Note: Modal credits are cloud compute credits, not cash. Still very valuable for your thesis work.

-----

## 7. Design Guide — How to Make Each App Look Beautiful

Judges see hundreds of default Gradio apps. A great UI can win the **Custom UI merit badge** and push you from 3rd to 1st.

### General Rules for All 3 Apps

- Use `gr.Server` with custom CSS — move beyond default Gradio theme
- Custom font (Google Fonts CDN via `gr.HTML`) — Poppins or Inter looks clean
- Color scheme: pick 2 accent colors + white/dark background
- Add app logo (generate with FLUX.2-klein itself for irony points)
- Mobile-friendly (HF Spaces run on mobile too — judges may check on phone)

### App 1 — Budget Tracker

```
Color scheme: Deep navy (#1B2A4A) + Fresh green (#27AE60) + White
Layout:
  - Top: Upload receipt button + camera icon
  - Middle: 3-column dashboard (Spent / Remaining / Daily Limit) as big bold numbers
  - Bottom: Junk Food Table (red items) vs Healthy Table (green items)
  - Right panel: AI Advice chat bubble (conversational, not a wall of text)
```

- Make the budget numbers BIG (like a fitness app shows calories)
- Red/green color coding: junk = red row, healthy = green row
- Progress bar for monthly budget (like a fuel gauge)

### App 2 — Dream Visualizer

```
Color scheme: Deep purple (#1A0533) + Electric blue (#4A90E2) + Gold (#F5C518)
Layout:
  - Hero: Dark gradient background with floating particle effect (CSS)
  - Center: Mic button (voice input) OR text area — minimal, atmospheric
  - Result: Full-width dream art image with interpretation text overlaid at bottom
  - Footer: Gallery of past dreams (polaroid card style)
```

- This app should LOOK like a dream — dark, mystical, premium
- Generate the app header art itself with FLUX.2-klein
- Play a soft ambient sound loop on load (optional, via gr.Audio autoplay)

### App 3 — Bedtime Stories

```
Color scheme: Soft cream (#FFF8E7) + Sky blue (#5DADE2) + Moon yellow (#F9E04B)
Layout:
  - Step 1: Big "Record Mom's Voice" button with moon/star icons
  - Step 2: Genre cards with illustrations (4-5 colorful cards with kid icons)
  - Step 3: Story player — large play button, star animation while playing
  - Background: Subtle starfield animation (CSS keyframes)
```

- Use big rounded buttons, large font sizes (for kids but also for demo wow factor)
- Generate genre card illustrations with FLUX.2-klein
- Keep instructions in 3 steps only — no walls of text

-----

## 8. Execution Plan (3 Apps in ~7 Days)

|Day      |Tasks                                                                                                                  |
|---------|-----------------------------------------------------------------------------------------------------------------------|
|**Day 1**|Set up HF Space, Gradio scaffold, test MiniCPM-V API locally. Get first receipt OCR working for App 1.                 |
|**Day 2**|Complete App 1 core (OCR + junk food classifier + budget logic). Add Cohere multilingual. Polish UI.                   |
|**Day 3**|Deploy App 1 on Modal + HF Space. Record demo with real receipts. Publish blog post.                                   |
|**Day 4**|Build App 2 (Dream Visualizer) — Nemotron reasoning + FLUX.2-klein image gen. Voice input via Cohere Transcribe.       |
|**Day 5**|App 2 VoxCPM2 narration + UI polish (the dark atmospheric design). Add gallery. Deploy + share on social.              |
|**Day 6**|Build App 3 (Bedtime Stories) — VoxCPM2 voice clone + MiniCPM story gen + kid UI.                                      |
|**Day 7**|Final polish on all 3 apps. Write READMEs with frontmatter tags. Record demo videos. Post on social (Twitter/LinkedIn).|

-----

## 9. Winning Checklist for Each App

Before submitting each Space, verify:

- [ ] Deployed in `build-small-hackathon` org on HF
- [ ] README includes frontmatter tags (track, sponsors, model names)
- [ ] Demo video recorded and linked in README
- [ ] Real user proof in README (quote, screenshot, use case)
- [ ] GitHub repo connected with Codex-attributed commits (App 1 especially)
- [ ] Model size confirmed ≤ 32B (ideally ≤ 4B for Tiny Titan badge)
- [ ] Blog post published on HF blog (counts as merit badge)
- [ ] Social post shared (HF, Twitter/X, LinkedIn) to drive Community Choice votes
- [ ] Modal deployment configured (for App 1 and App 2)
- [ ] Cohere Transcribe or Tiny Aya integrated (App 1 + App 2 + App 3)

-----

## 10. Quick Model Reference

|Model            |Size |Use Case                                       |Sponsor          |API/Hosted               |
|-----------------|-----|-----------------------------------------------|-----------------|-------------------------|
|MiniCPM-V 4.6    |~8B  |OCR, image understanding, receipt reading      |OpenBMB          |HF hosted / OpenBMB API  |
|MiniCPM5-1B      |1B   |Text generation, story writing, advice         |OpenBMB          |Local / HF Spaces ZeroGPU|
|MiniCPM4.1-8B    |8B   |Reasoning, complex instructions                |OpenBMB          |HF hosted                |
|VoxCPM2          |Small|Voice cloning + TTS                            |OpenBMB          |HF Space                 |
|Nemotron-Nano    |8B   |Reasoning, deep analysis (dreams, anomalies)   |NVIDIA           |NVIDIA API               |
|Nemotron-Embed   |340M |Embeddings for RAG/memory                      |NVIDIA           |NVIDIA API               |
|FLUX.2-klein     |4B/9B|Image generation, dream art, portraits         |Black Forest Labs|HF Spaces ZeroGPU        |
|Cohere Tiny Aya  |3.35B|Multilingual text, translation                 |Cohere           |Cohere API (free tier)   |
|Cohere Transcribe|—    |Speech-to-text, voice input                    |Cohere           |Cohere API               |
|XTTS-v2          |335M |Alternative voice cloning (if VoxCPM2 too slow)|Open source      |HF: coqui/XTTS-v2        |

-----

*Report compiled June 2026. Hackathon is LIVE — start building today.*