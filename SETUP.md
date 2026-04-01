# Live Translator - Setup Guide

Complete step-by-step instructions for setting up Live Translator from scratch.

## Prerequisites Checklist

Before starting, make sure you have:
- Windows 10 or 11
- Internet connection
- Admin rights (for installing software)

---

## Step 1: Install Python

Python is required to run the speech recognition (ear.py).

### 1.1 Download Python

1. Go to: https://www.python.org/downloads/
2. Click the **"Download Python 3.12"** button (or latest version)
3. Save the file to your Downloads folder

### 1.2 Install Python

1. **Double-click** the downloaded `python-3.x.x.exe` file
2. **IMPORTANT**: Check the box at the bottom that says:
   > "Add python.exe to PATH"
   
   :warning: This is critical! Without this, the script won't work.

3. Click **"Install Now"**
4. Wait for installation to complete (1-2 minutes)
5. Click **"Close"**

### 1.3 Verify Python Installation

1. Press `Windows key + R`
2. Type `cmd` and press Enter
3. In the command prompt, type:
   ```
   python --version
   ```
4. You should see: `Python 3.x.x` (or similar)

If you see an error, Python wasn't added to PATH. Re-run the installer and make sure to check the box.

---

## Step 2: Install Node.js

Node.js is required to run the web server (bridge.js).

### 2.1 Download Node.js

1. Go to: https://nodejs.org/
2. Click the **"LTS"** button (recommended for most users)
3. Save the file to your Downloads folder

### 2.2 Install Node.js

1. **Double-click** the downloaded `node-v20.x.x-x64.msi` file
2. Click **"Next"**
3. Accept the license agreement
4. Click **"Next"** (default installation location is fine)
5. Click **"Next"** (default features are fine)
6. Click **"Install"**
7. Click **"Finish"**

### 2.3 Verify Node.js Installation

1. Press `Windows key + R`
2. Type `cmd` and press Enter
3. In the command prompt, type:
   ```
   node --version
   ```
4. You should see: `v20.x.x` (or similar)

---

## Step 3: Install Git LFS

Git LFS is needed to download the Whisper AI model.

### 3.1 Download Git

1. Go to: https://git-scm.com/download/win
2. Click **"Click to download"**
3. Save the file to your Downloads folder

### 3.2 Install Git

1. **Double-click** the downloaded `Git-2.x.x-64-bit.exe` file
2. Click **"Next"**
3. Select **"Use Git from the Windows Command Prompt"**
4. Click **"Next"**
5. Select **"Checkout Windows-style, commit Unix-style line endings"**
6. Click **"Next"**
7. Click **"Next"** (default terminal is fine)
8. Click **"Install"**
9. Click **"Finish"**

### 3.3 Install Git LFS

1. Open Command Prompt (cmd)
2. Run:
   ```
   git lfs install
   ```

---

## Step 4: Clone the Repository

### 4.1 Open Command Prompt

Press `Windows key + R`, type `cmd`, press Enter.

### 4.2 Navigate to Your Folder

Choose where you want the project to be installed:

```bash
# Go to Desktop
cd Desktop

# Or go to Documents
cd Documents

# Or create a new folder
mkdir StreamTools
cd StreamTools
```

### 4.3 Clone the Repository

```bash
git clone <PASTE_REPO_URL_HERE>
cd livetranslator
```

### 4.4 Download the AI Model

```bash
git lfs install
git lfs pull
```

This downloads the pre-trained Whisper model (~70MB).

---

## Step 5: Run the Application

### 5.1 Start Everything

1. Open File Explorer
2. Navigate to the `livetranslator` folder
3. **Double-click `start.bat`**

The script will:
- Install Node.js dependencies (first time only)
- Create Python virtual environment (first time only)
- Install Python packages (first time only)
- Ask you to choose a Whisper model
- Start all services

### 5.2 Choose Your Model

```
Choose your Whisper model:

[1] tiny      - 17 MB   (fastest, lower accuracy)
[2] small     - 70 MB   (recommended - balance)
[3] medium    - 300 MB  (slower, higher accuracy)
[4] large-v2  - 1.5 GB  (slowest, highest accuracy)
[5] large-v3  - 1.5 GB  (slowest, highest accuracy)

Enter choice (1-5) or press Enter for [2] small:
```

Press **Enter** to use the recommended "small" model (pre-installed).

### 5.3 Choose Audio Device

```
==================================================
[Audio Devices]
==================================================
  [0] Microphone (USB Audio Device)
      Channels: 2, Sample Rate: 48000
  [1] Virtual Cable Input
      Channels: 2, Sample Rate: 48000
==================================================

Enter the Device Index you want to use:
```

Type the number of your microphone and press Enter.

### 5.4 Choose Channels

```
Enter number of Channels (1 for Mono, 2 for Stereo):
```

- Use **1 (Mono)** if you're the only person speaking
- Use **2 (Stereo)** if you want to capture both speakers and music

### 5.5 Save Settings

```
Save these settings? (y/n):
```

Type **y** to save. Next time you run, it won't ask again.

### 5.6 Success!

```
==================================================
    All Checks Passed!
==================================================

[Bridge] Socket.io server on port 5050
[Web]    Overlay on port 8080
[Ear]    Speech recognition

Starting services...
```

Two new command windows will open - **don't close them!**

---

## Step 6: Setup OBS

### 6.1 Add Browser Source

1. Open OBS Studio
2. Click the **+** button in the Sources panel
3. Select **"Browser"**
4. Click **"OK"**

### 6.2 Configure Browser Source

| Setting | Value |
|---------|-------|
| URL | `http://localhost:8080` |
| Width | `1920` |
| Height | `1080` |
| FPS | `30` |

### 6.3 Optional CSS for Better Performance

Click **"OK"**, then right-click the browser source → **"Filter"** → **"CSS"**:

```css
body {
    background: transparent !important;
}
```

---

## Step 7: Using the Overlay

### 7.1 Settings Panel

Click the **gear icon** (top-right) to open settings:

| Section | Controls |
|---------|----------|
| **Appearance** | Text Only Mode, Hide Settings Icon |
| **Colors** | Background Color, Border Color, Text Color |
| **Size** | Opacity (0-100%), Scale (0.5x-2.0x), Width (300-1200px) |
| **Controls** | Lock Overlay, Centre Caption |
| **Footer** | Restore Defaults |

### 7.2 Customizing Appearance

- **Text Only Mode**: Hides background for clean text overlay
- **Hide Settings Icon**: Makes gear invisible but keeps it clickable
- **Colors**: Pick custom colors for background, border, and text
- **Opacity**: Adjust background transparency (0% = invisible, 100% = solid)
- **Scale**: Scale all text and padding proportionally (0.5x to 2.0x)
- **Width**: Set max width of caption box (300px to 1200px)

### 7.3 Draggable Caption Box

- **Click and drag** the caption box to position it anywhere
- **Snaps to center** when dragged near screen center (30px threshold)
- **Position saved** automatically to localStorage
- **Centre Caption button** resets to default center position

### 7.7 Auto-Save

**All settings are saved automatically** to localStorage:
- Colors (background, border, text)
- Size settings (opacity, scale, width)
- Caption box position
- Lock/unlock state
- Text Only mode
- Hide Settings Icon toggle

This means:
- Changes apply immediately
- Settings persist across browser refreshes
- Settings persist after closing OBS
- Use **"Restore Defaults"** to reset everything

### 7.4 Lock Mode

Click **Lock Overlay** when ready for OBS capture:
- Caption box becomes non-interactive (click-through)
- Settings button remains accessible for unlocking

Click **Unlock Overlay** to regain control.

### 7.5 Text Shadow

Text always has a shadow for readability on any background:
```css
text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9), 0 0 2px rgba(0, 0, 0, 0.8);
```

### 7.6 Ghost Mode (OBS)

If you want the settings completely hidden in OBS:

1. Right-click the browser source in OBS
2. Go to **"Filter"** → **"CSS"**
3. Add this CSS:
```css
.ui-element {
    display: none !important;
}
```

---

## Troubleshooting

### "Python is not installed" Error

1. Make sure you installed Python correctly
2. Close and reopen Command Prompt
3. Run `python --version` to verify

### "pip install failed" Error

1. Run Command Prompt as Administrator
2. Navigate to the project folder
3. Run:
   ```
   python -m pip install --upgrade pip
   venv\Scripts\pip install -r requirements.txt
   ```

### No Audio / Wrong Device

1. Close all running windows
2. Run `reset_settings.bat`
3. Choose your microphone again

### Model Download Failed

1. Check your internet connection
2. Add your HuggingFace token to `.env`:
   ```
   HF_TOKEN=hf_your_token_here
   ```

### OBS Shows Blank Screen

1. Make sure the Bridge window is running
2. Check if port 8080 is accessible
3. Try refreshing the browser source

### First Drag Jumps to Wrong Position

This can happen if localStorage has old position data. Click **"Restore Defaults"** in settings to reset.

---

## Changing Settings Later

To change model, audio device, or channels:

1. Run `reset_settings.bat`
2. Choose your new settings
3. Save when prompted

---

## Uninstalling

To remove everything:

1. Close all running windows (Bridge, Ear)
2. Delete the `livetranslator` folder
3. Uninstall Python via Windows Settings → Apps
4. Uninstall Node.js via Windows Settings → Apps
