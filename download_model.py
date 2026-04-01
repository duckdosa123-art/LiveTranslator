#!/usr/bin/env python3
"""
Download Faster-Whisper model to local folder.
Run this once before using ear.py for the first time.

Usage:
    python download_model.py [model_size]
    
Default model: small (options: tiny, small, medium, large-v2, large-v3)

Set HF_TOKEN in .env file for faster downloads and higher rate limits.
"""

import sys
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")

try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing dotenv...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "-q"])
    from dotenv import load_dotenv

load_dotenv()

try:
    from huggingface_hub import snapshot_download, login
except ImportError:
    print("Installing huggingface_hub...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub", "-q"])
    from huggingface_hub import snapshot_download, login

MODEL_MAP = {
    "tiny": "Systran/faster-whisper-tiny",
    "small": "Systran/faster-whisper-small", 
    "medium": "Systran/faster-whisper-medium",
    "large-v2": "Systran/faster-whisper-large-v2",
    "large-v3": "Systran/faster-whisper-large-v3",
}

def get_token():
    token = os.getenv("HF_TOKEN")
    if token:
        print(">>> Using HuggingFace token from .env")
        login(token=token)
    else:
        print(">>> No HF_TOKEN found in .env (downloads may be slower)")
    return token

def download_model(model_name="small", output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).parent / "models" / model_name
    else:
        output_dir = Path(output_dir) / model_name
    
    output_dir = output_dir.resolve()
    
    if output_dir.exists() and any(output_dir.iterdir()):
        print(f">>> Model already exists at: {output_dir}")
        print(f">>> Size: {get_folder_size(output_dir):.1f} MB")
        return str(output_dir)
    
    model_id = MODEL_MAP.get(model_name, MODEL_MAP["small"])
    print(f">>> Downloading model: {model_name} ({model_id})")
    print(f">>> Destination: {output_dir}")
    print(">>> This may take a few minutes...")
    
    token = get_token()
    
    try:
        local_path = snapshot_download(
            repo_id=model_id,
            local_dir=str(output_dir),
            local_dir_use_symlinks=False,
            resume_download=True,
            token=token,
        )
        print(f">>> Model downloaded successfully!")
        print(f">>> Size: {get_folder_size(output_dir):.1f} MB")
        return str(local_path)
    except Exception as e:
        print(f"!!! Download failed: {e}")
        if output_dir.exists():
            import shutil
            shutil.rmtree(output_dir)
        raise

def get_folder_size(folder):
    total = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total / (1024 * 1024)

if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "small"
    if model_name not in MODEL_MAP:
        print(f"Unknown model: {model_name}")
        print(f"Available models: {', '.join(MODEL_MAP.keys())}")
        sys.exit(1)
    
    download_model(model_name)
