# 🎤 Traskryptor - Offline Transcription & Translation

A Windows desktop application (Tkinter GUI) for speech-to-text transcription and document translation, designed to work **completely offline** after initial model download.

---

## ⚠️ WARNING - PRIVATE USE ONLY

**This project is intended exclusively for private and personal use.**

- ❌ **PROHIBITED:** Copying, distribution, or commercial use without the author's consent
- ❌ **PROHIBITED:** Publishing in other repositories or on any platforms
- ❌ **PROHIBITED:** Any form of resale or monetization of this code
- ✅ **PERMITTED:** Personal use, self-learning, private testing

**© All rights reserved. Unauthorized use will be prosecuted.**

---

## 🌟 Key Features

- ✅ **100% Offline** — no internet required after initial model download
- ✅ **Three modes:** audio file transcription, live microphone transcription, document translation
- ✅ **AI transcription** — faster-whisper (CTranslate2, CPU, int8) — no PyTorch required
- ✅ **Offline translation** — `translate` library — no PyTorch, no API keys
- ✅ **Portable bundle** — embedded Python 3.13 in `Traskryptor_WinPython/`
- ✅ **Multilingual** — Polish, English (transcription); PL→EN/RU/UK (translation)

---

## 📦 Quick Start

### Option 1: Portable Bundle (RECOMMENDED) ⭐

Everything is pre-packaged — no installation needed.

1. Download: [Traskryptor_WinPython_v1.1.zip (366 MB)](https://github.com/guzik1234/traskryptor/releases)
2. Extract the folder
3. Run `Uruchom_Traskryptor.bat` or `Traskryptor.exe`
4. Done! 🎉 Works 100% offline after first model download

### Option 2: Virtual Environment (Development)

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

> You can also use `Uruchom_Traskryptor.bat` — it activates `.venv` automatically and launches `main.py`.

### Option 3: Build EXE (PyInstaller)

```bash
pip install pyinstaller
pyinstaller traskryptor.spec
```

The spec file builds `Traskryptor.exe` from `launcher.py`, which in turn runs the app from the portable Python bundle.

---

## 📋 Features

### 1️⃣ Audio File Transcription

Convert an audio file to text and save it as DOCX and PDF.

- **Input formats:** MP3, WAV, M4A, FLAC, OGG (loaded via `librosa`)
- **Languages:** Polish, English
- **Output:** DOCX + PDF (PDF requires `docx2pdf`; falls back to DOCX only if unavailable)
- **AI model:** `Systran/faster-whisper-small` (PL), `Systran/faster-whisper-base.en` (EN)
- **Offline?** ✅ Yes (after first download from HuggingFace)

**How to use:**
1. Click "Transkrypcja z pliku audio" in the main menu
2. Select an audio file
3. Choose language (Polish / English)
4. Click "Start"
5. DOCX and PDF are saved in the same folder as the input file

---

### 2️⃣ Live Microphone Transcription → Microsoft Word

Record speech in real time and insert the transcribed text directly into an open Word document.

- **Languages:** Polish, English
- **Requires:** Microsoft Word open before starting (connected via COM automation)
- **Activation:** Hold **Left Shift** to record, release to transcribe and insert
- **Optional real-time translation:** PL→EN (via `translate` library, offline)
- **Audio:** 16 kHz, mono, captured with `sounddevice`
- **Offline?** ✅ Yes (transcription + translation, after model download)

**How to use:**
1. Open a document in Microsoft Word
2. Click "Transkrypcja na żywo" in the main menu
3. Select language; optionally enable "Włącz tłumaczenie PL→EN"
4. Click "Start"
5. Hold **Left Shift** to record, release to insert transcribed text into Word
6. Click "Zakończ nasłuchiwanie" to stop

---

### 3️⃣ Document Translation

Translate Word documents while preserving paragraph structure.

- **Input formats:** DOCX, ODT
- **Output:** Translated DOCX (opened in Word via COM)
- **Languages:** Polish → English (`_en`), Russian (`_ru`), Ukrainian (`_uk`)
- **Engine:** `translate 3.8.0` (offline, no PyTorch)
- **Offline?** ✅ Yes

**How to use:**
1. Click "Tłumaczenie dokumentów" in the main menu
2. Select a DOCX or ODT file
3. Choose target language
4. Click "Tłumacz" or "Start tłumaczenia"
5. Progress bar shows translation status; result opens in Word

---

## 🏗️ Project Structure

```
traskryptor/
├── main.py                      # Main menu (Tkinter, 550×600)
├── gui.py                       # Live transcription GUI (700×900)
├── audio_file_transcription.py  # Audio file transcription GUI + logic
├── speech_to_word.py            # Live transcription loop (keyboard + Word)
├── transcription_model.py       # faster-whisper model loader & wrapper
├── translation_gui.py           # Document translation GUI (650×650)
├── pdf_translator.py            # Translation engine (translate library + Word COM)
├── audio_handler.py             # Microphone capture (sounddevice, 16kHz queue)
├── word_handler.py              # Microsoft Word COM: connect + insert text
├── compare_docs.py              # CLI utility: compare two docs paragraph-by-paragraph
├── launcher.py                  # Portable bundle launcher (sets PYTHONHOME etc.)
├── install_languages.py         # Argos Translate package installer (PL→EN, PL→RU)
├── traskryptor.spec             # PyInstaller spec → builds Traskryptor.exe
├── Uruchom_Traskryptor.bat      # Launcher script (.venv → python main.py)
├── requirements.txt             # Python dependencies
└── Traskryptor_WinPython/       # Portable bundle
    ├── python/                  # Embedded Python 3.13 + packages
    ├── app/                     # Application code copy
    └── Uruchom_Traskryptor.bat  # Bundle entry point
```

---

## ⚙️ Requirements

### System
- **OS:** Windows only (pywin32 / Word COM required)
- **Microsoft Word:** Required for live transcription and document translation
- **Microphone:** Required for live transcription

### Python Dependencies (`requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| `faster-whisper` | 1.2.1 | AI transcription engine (CTranslate2) |
| `sounddevice` | 0.5.3 | Microphone audio capture |
| `librosa` | latest | Audio file loading & resampling |
| `SpeechRecognition` | 3.14.4 | Audio utilities |
| `keyboard` | 0.13.5 | Left Shift hotkey detection |
| `pywin32` | 311 | Microsoft Word COM automation |
| `translate` | 3.8.0 | Offline text translation |
| `libretranslatepy` | 2.1.1 | LibreTranslate API support |
| `python-docx` | latest | DOCX reading/writing |
| `pymupdf` | latest | PDF reading (fitz) |
| `docx2pdf` | latest | DOCX → PDF conversion (optional) |

> **No PyTorch required** — faster-whisper uses CTranslate2 (CPU, int8).

### Python Version
- Python 3.8+ (tested on 3.13)

---

## 🤖 AI Models

Models are downloaded automatically from HuggingFace on first use:

| Language | Model | Size |
|----------|-------|------|
| Polish | `Systran/faster-whisper-small` | ~244 MB |
| Polish (better quality) | `Systran/faster-whisper-medium` | ~769 MB |
| English | `Systran/faster-whisper-base.en` | ~74 MB |

Models are cached locally after first download and work fully offline.

---

## 🚀 Installing Language Packages

To install offline argostranslate packages (for extended translation support):

```bash
python install_languages.py
```

This downloads and installs:
- 🇵🇱 Polish → 🇬🇧 English
- 🇵🇱 Polish → 🇷🇺 Russian

> Note: The main app uses the `translate` library for translation. `install_languages.py` uses `argostranslate` as an alternative offline backend.

---

## 🛠️ Utility: compare_docs.py

Command-line tool to compare two documents paragraph by paragraph (useful for verifying translation accuracy):

```bash
python compare_docs.py original.docx translated.docx
```

Requires Microsoft Word (COM) to read ODT/DOCX files.

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Transcription does not start
- Check that your microphone is working and not blocked
- First launch must be online to download the AI model (~74–769 MB)
- Make sure `.venv` is activated or use `Uruchom_Traskryptor.bat`

### Live transcription: "Open Word before running"
- Microsoft Word must be open with an active document before clicking Start

### Translation freezes or crashes
- Close all Word windows before starting translation
- Make sure the input file is not open elsewhere
- Check `ROZWIAZANIE_PROBLEMU.md` for detailed fixes

### PDF output missing
- `docx2pdf` requires Word to be installed
- If unavailable, only DOCX output is generated (no error)

---

## 📄 Additional Documentation

- [ROZWIAZANIE_PROBLEMU.md](ROZWIAZANIE_PROBLEMU.md) — Detailed troubleshooting
- [INSTALL_LANGUAGES.md](INSTALL_LANGUAGES.md) — Language package installation guide
- [OFFLINE_MODE.md](OFFLINE_MODE.md) — Offline operation details
- [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) — Translation feature guide
- [LICENSES.md](LICENSES.md) — Open source license information

---

## 📜 License

### External Dependencies
All third-party libraries are open source:
- **MIT, Apache 2.0, BSD, ISC, PSF**

Full list: [LICENSES.md](LICENSES.md)

### Traskryptor Application Code

**© All rights reserved**

This source code is private property, available solely for:
- ✅ Private personal use
- ✅ Self-learning and personal education
- ✅ Local environment testing

**PROHIBITED without written consent of the author:**
- ❌ Copying or redistributing the code
- ❌ Commercial use
- ❌ Publishing in other repositories
- ❌ Creating public derivative works
- ❌ Sublicensing

**WARNING:** Violation of the above terms may result in legal consequences.

---

## 🔧 Tech Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| **GUI** | Tkinter | Pure Python, no external GUI lib |
| **Transcription** | faster-whisper 1.2.1 (CTranslate2) | CPU, int8, no PyTorch |
| **AI Models** | Systran/faster-whisper-* (HuggingFace) | Auto-downloaded on first use |
| **Translation** | translate 3.8.0 | Offline, no API key |
| **Alt. Translation** | argostranslate | Via install_languages.py |
| **Audio capture** | sounddevice 0.5.3 | 16kHz, mono |
| **Audio loading** | librosa | MP3/WAV/M4A/FLAC/OGG |
| **Documents** | python-docx + pymupdf | DOCX read/write, PDF read |
| **PDF export** | docx2pdf | Optional, requires Word |
| **Word integration** | pywin32 311 (COM automation) | Windows only |
| **Hotkeys** | keyboard 0.13.5 | Left Shift to record |
| **Packaging** | PyInstaller (traskryptor.spec) | Builds Traskryptor.exe |

---

## 📌 Notes

- **Windows only** — pywin32 and Word COM are Windows-exclusive
- **First launch requires internet** — AI models downloaded from HuggingFace (~74 MB–770 MB)
- **All subsequent use is offline** — models cached locally
- **Microsoft Word must be running** for live transcription and document translation
- **Left Shift** is the push-to-talk key for live transcription

**Version:** 1.1  
**Last updated:** April 2026

---

## 🔒 Copyright & Disclaimer

This project was created for **private and personal use only**. Any attempt to use this code, its fragments, or concepts for commercial, public, or distribution purposes without the explicit written consent of the author is **strictly prohibited**.

**Monitoring:**
- All copies of this repository are being monitored
- Unauthorized use is subject to identification and legal action

**© 2026 - All rights reserved**
