# EmemediaForge — Word Alignment Engine

EmemediaForge ships a **zero-dependency** word alignment engine.
No Whisper model download. No GPU. No internet. No extra install.

---

## How the Default Engine Works

1. **Load audio** with librosa (22050 Hz mono)
2. **RMS energy** — compute per-frame amplitude envelope
3. **Voice detection** — frames above 12% of peak energy = voiced
4. **Segment merge** — voiced frames < 100ms apart are merged
5. **Proportional distribution** — words allocated by character count
   - Longer words (more chars) get proportionally more time
   - Short inter-word gaps (~3% of speech duration) are inserted
6. **Boundary clamp** — last word clamped to actual audio end

### Why This Works for Nigerian Languages

Standard ML aligners (MFA, Montreal Forced Aligner, Whisper) fail on
Yoruba, Igbo, Hausa, and Pidgin because they weren't trained on those
languages. The energy-based engine is **100% language-agnostic** — it
only looks at when sound is present, not what language is being spoken.

---

## Optional: stable-ts (High Accuracy)

For demos where precise word timing matters:

```bash
pip install "ememediaforge[stable_ts]"
forge build project.yaml --stable-ts
```

- Downloads **Whisper tiny** (~150MB) on first use
- CPU-compatible (no GPU required)
- 3–5× more accurate than energy-based alignment
- Works best for English, code-switching, and clean audio
- May still struggle with tonal languages (Yoruba, Igbo)

---

## Transcript Format

Plain UTF-8 text. Exactly what is spoken. One continuous string.

```
# samples/yoruba.txt
Mo fẹ́ jẹun nísisiyi àti gbé oúnjẹ tó dára jùlọ
```

Punctuation is stripped automatically from word edges.
Line breaks are treated as spaces.

---

## Tips for Best Karaoke Sync

1. **Match transcript exactly** to what's spoken (no extra words)
2. **Use WAV format** for cleanest audio analysis
3. **Normalize audio** to -3dBFS before generating
4. **Avoid background music** — it confuses the energy detector
5. **Add `--stable-ts`** for fast speech or lots of short words
