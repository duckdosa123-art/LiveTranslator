# Live Translator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Real-time speech-to-text translation overlay for OBS using Faster-Whisper. Translates ALL LANGUAGES to English live.

## Features

- Real-time speech recognition (FOR Ex: pt-BR → en)
- Multiple Whisper model support (tiny, small, medium, large-v2, large-v3)
- Draggable caption overlay with center-anchored positioning
- Snap-to-center when dragging near screen middle
- Lock mode for OBS capture
- Elite glassmorphism styling with backdrop blur
- Customizable colors (background, border, text)
- Proportional scaling (0.5x to 2.0x)
- Ghost mode for invisible settings in OBS
- One-click setup

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git + Git LFS

**For detailed installation instructions, see [SETUP.md](SETUP.md)**

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd livetranslator

# 2. Download the AI model
git lfs install
git lfs pull

# 3. Run one-click setup
start.bat
```

**First time setup? Read [SETUP.md](SETUP.md) for step-by-step instructions.**

## Files

| File | Description |
|------|-------------|
| `start.bat` | One-click launcher - installs deps, starts services |
| `reset_settings.bat` | Resets audio device and model settings |
| `ear.py` | Speech recognition (Faster-Whisper) |
| `bridge.js` | Socket.io server + web server |
| `index.html` | OBS overlay (Browser Source) |

## OBS Setup

1. Add a "Browser Source" in OBS
2. URL: `http://localhost:8080`
3. Width: 1920, Height: 1080
4. FPS: 30

## Overlay Controls

Click the **gear icon** (top-right) to open settings:

| Section | Controls |
|---------|----------|
| **Appearance** | Text Only Mode, Hide Settings Icon |
| **Colors** | Background, Border, Text color pickers |
| **Size** | Opacity (0-100%), Scale (0.5x-2.0x), Width (300-1200px) |
| **Controls** | Lock Overlay, Centre Caption |
| **Footer** | Restore Defaults |

### Key Features

- **Drag** the caption box to position it anywhere
- **Snap-to-center** when dragged near screen middle (30px threshold)
- **Text Only Mode** hides background for clean overlay
- **Scale** affects all text and padding proportionally
- **Ghost Mode** in OBS: use Custom CSS to hide UI elements
- **All settings auto-save** to localStorage immediately

### OBS Custom CSS (Optional)

To hide settings UI in OBS, add to Browser Source Custom CSS:
```css
.ui-element { display: none !important; }
```

## Elite Styling

The overlay features a "glassmorphism" aesthetic:

- Backdrop blur (8px) for glass effect
- Subtle glass border and shadows
- Text shadow always applied for readability
- Purple accent color (#9146ff)
- Proportional scaling via CSS variables

## Model Selection

The `start.bat` script lets you choose a Whisper model:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 17 MB | Fastest | Lower |
| small | 70 MB | Fast | Balanced |
| medium | 300 MB | Slower | Higher |
| large-v2 | 1.5 GB | Slowest | Highest |
| large-v3 | 1.5 GB | Slowest | Highest |

The "small" model is pre-installed with the repo. Other models download on demand.

## Changing Settings

Run `reset_settings.bat` to:
- Select a different model
- Change audio device
- Change channel settings (Mono/Stereo)

## HuggingFace Token (Optional)

For faster model downloads, add your token to `.env`:
```
HF_TOKEN=hf_your_token_here
```

Get a token at: https://huggingface.co/settings/tokens

## Architecture

```
ear.py ──► bridge.js ──► index.html
(Speech)    (Socket.io)  (OBS Browser Source)
```

- **ear.py**: Microphone input, Faster-Whisper transcription/translation
- **bridge.js**: Socket.io server on port 5050, serves overlay on port 8080
- **index.html**: Draggable captions with Elite styling and lock mode
