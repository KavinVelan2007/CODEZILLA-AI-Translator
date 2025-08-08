# 🌍 Creative Language Translator

> A Streamlit-based AI-powered translation system that not only translates text between multiple languages but also preserves tone, dialect, and creative writing styles.

---

## ✨ Overview

**Creative Language Translator** goes beyond conventional translation tools by offering the ability to:
- Translate between 30+ languages with tone/style preservation.
- Adapt the translation to regional dialects and idiomatic expressions.
- Transform content into poems, lyrics, Shakespearean prose, and more using LLM-based generation.
- Offer AI-based verification for tone and fidelity.

This project was developed for the **GAI2 Hackathon Challenge** focused on creative, nuanced multilingual generation.

---

## 🧠 Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 🔁 Language Translation        | Translate between 10+ supported languages.                                 |
| 🎭 Style Adaptation            | Convert writing style (Formal, Poetic, Casual, Storytelling, etc.).        |
| 🌐 Dialect Control             | Choose specific dialects (e.g., UK English, Latin American Spanish).       |
| 🧠 LLM-Powered Generation      | Uses `Ollama` with `phi3` model for nuanced translation and adaptation.    |
| 🤖 Verification                | Built-in AI checks for tone/style/accuracy validation.                     |
| 🧾 History Logging             | Keeps a CSV record of all translations by user session.                    |
| 💬 Idiomatic Support           | Translates with idioms/slang when desired.                                 |
| 🎨 UI                          | Clean modern interface with customizable themes and background.            |

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend/AI**:
  - [`deep_translator`](https://github.com/nidhaloff/deep-translator) (Google Translate API wrapper)
  - [`ollama`](https://ollama.com) (Local LLM generation)
  - [`langid` / `langdetect`] for auto-language detection
- **Language Model**: `phi3` running locally via Ollama
- **Storage**: `pandas` for translation logs

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.9+
- Ollama with phi3 installed and running
- Virtual environment recommended

### 📦 Install Dependencies

Install Ollama.exe from https://ollama.com/

```bash
pip install streamlit deep-translator pandas langid langdetect ollama
ollama run phi3
streamlit run login.py





