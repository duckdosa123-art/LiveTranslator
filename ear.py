import os
from dotenv import load_dotenv
load_dotenv()

import socketio
import numpy as np
import sounddevice as sd
from scipy import signal
import queue
import time
import sys
import json
import torch
from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download

SERVER_URL = "http://localhost:5050"
SAMPLE_RATE = 16000
BUFFER_SIZE = 4096
SILENCE_THRESHOLD = 0.003
MAX_PHRASE_SECONDS = 3
MIN_SILENCE_FRAMES = 5
SETTINGS_FILE = "ear_settings.json"

def find_available_models():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    
    available = []
    for model_name in ["large-v3", "large-v2", "medium", "small", "tiny"]:
        model_path = os.path.join(models_dir, model_name)
        if os.path.exists(model_path) and os.listdir(model_path):
            available.append((model_name, model_path))
    
    return available

audio_queue = queue.Queue()
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1)

@sio.on("connect")
def on_connect():
    print(">>> Connected to bridge!")

@sio.on("disconnect")
def on_disconnect():
    print("!!! Disconnected from bridge")

@sio.on("connect_error")
def on_connect_error(err):
    print(f"!!! Connection error: {err}")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def get_model_choice():
    available = find_available_models()
    
    if not available:
        return None, None
    
    if len(available) == 1:
        model_name, model_path = available[0]
        print(f">>> Found model: {model_name}")
        return model_name, model_path
    
    print("\n" + "=" * 50)
    print("[Multiple Models Found]")
    print("=" * 50)
    for i, (model_name, _) in enumerate(available, 1):
        print(f"  [{i}] {model_name}")
    print("=" * 50)
    
    while True:
        try:
            choice = input("Enter the model number you want to use: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                model_name, model_path = available[idx]
                print(f">>> Selected model: {model_name}")
                return model_name, model_path
            else:
                print("!!! Invalid choice. Please enter a valid number.\n")
        except ValueError:
            print("!!! Invalid input. Please enter a number.\n")

def save_settings(device_index, channels, model_name=None):
    try:
        data = {"device_index": device_index, "channels": channels}
        if model_name:
            data["model_name"] = model_name
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
        print(f">>> Settings saved to {SETTINGS_FILE}")
    except Exception as e:
        print(f"!!! Could not save settings: {e}")

def list_devices():
    print("\n" + "=" * 50)
    print("[Audio Devices]")
    print("=" * 50)
    try:
        devices = sd.query_devices()
        hostapi = sd.query_hostapis()
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                api_name = hostapi[dev['hostapi']]['name']
                print(f"  [{i}] {dev['name']}")
                print(f"      Channels: {dev['max_input_channels']}, "
                      f"Sample Rate: {int(dev['default_samplerate'])}")
    except Exception as e:
        print(f"  Error: {e}")
    print("=" * 50 + "\n")

def get_device_and_model():
    settings = load_settings()
    selected_model_name = None
    selected_model_path = None
    
    if settings:
        print(f">>> Using saved settings:")
        print(f">>>   Device: {settings['device_index']}")
        print(f">>>   Channels: {settings['channels']}")
        if "model_name" in settings:
            print(f">>>   Model: {settings['model_name']}")
            return settings["device_index"], settings["channels"], settings["model_name"], None
        
        model_name, model_path = get_model_choice()
        return settings["device_index"], settings["channels"], model_name, model_path
    
    model_name, model_path = get_model_choice()
    
    list_devices()
    
    while True:
        try:
            choice = input("Enter the Device Index you want to use: ").strip()
            device_index = int(choice)
            break
        except ValueError:
            print("!!! Invalid input. Please enter a number.\n")
    
    while True:
        try:
            ch = input("Enter number of Channels (1 for Mono, 2 for Stereo): ").strip()
            channels = int(ch)
            if channels not in [1, 2]:
                print("!!! Please enter 1 or 2.\n")
                continue
            break
        except ValueError:
            print("!!! Invalid input. Please enter 1 or 2.\n")
    
    while True:
        save = input("Save these settings? (y/n): ").strip().lower()
        if save == "y":
            save_settings(device_index, channels, model_name)
            break
        elif save == "n":
            break
        else:
            print("!!! Please enter 'y' or 'n'.\n")
    
    return device_index, channels, model_name, model_path

def load_whisper(model_path=None):
    if torch.cuda.is_available():
        device = "cuda"
        compute_type = "float16"
    else:
        device = "cpu"
        compute_type = "int8"
    
    print(f">>> MODE: {device.upper()} | PRECISION: {compute_type}")
    
    if model_path and os.path.exists(model_path) and any(os.listdir(model_path)):
        print(f">>> Loading model from: {model_path}")
        model = WhisperModel(
            model_path,
            device=device,
            compute_type=compute_type
        )
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "models", "small")
        if not os.path.exists(model_path) or not any(os.listdir(model_path)):
            print(f">>> No model found, downloading small to: {model_path}")
            os.makedirs(model_path, exist_ok=True)
            download_and_save_model("small", model_path)
        print(f">>> Loading model from: {model_path}")
        model = WhisperModel(
            model_path,
            device=device,
            compute_type=compute_type
        )
    
    return model


def download_and_save_model(model_size, output_path):
    model_ids = {
        "tiny": "Systran/faster-whisper-tiny",
        "small": "Systran/faster-whisper-small",
        "medium": "Systran/faster-whisper-medium",
        "large-v2": "Systran/faster-whisper-large-v2",
        "large-v3": "Systran/faster-whisper-large-v3",
    }
    
    model_id = model_ids.get(model_size, model_ids["small"])
    token = os.getenv("HF_TOKEN")
    
    print(f">>> Downloading {model_size} model...")
    
    snapshot_download(
        repo_id=model_id,
        local_dir=output_path,
        local_dir_use_symlinks=False,
        resume_download=True,
        token=token,
    )
    print(f">>> Model saved to: {output_path}")

def audio_callback(indata, frames, time_info, status, channels):
    if status:
        pass
    if channels == 2 and indata.ndim > 1:
        indata = (indata[:, 0] + indata[:, 1]) / 2
    elif indata.ndim > 1:
        indata = indata[:, 0]
    audio_queue.put(np.asarray(indata, dtype=np.float32).flatten())

def send_translation(original, translated):
    try:
        payload = {
            "original": original,
            "translated": translated,
            "timestamp": time.time()
        }
        sio.emit("new-translation", payload)
    except Exception:
        pass

def get_rms(data):
    try:
        if data is None or len(data) == 0:
            return 0.0
        flat = np.asarray(data, dtype=np.float32).flatten()
        if len(flat) == 0:
            return 0.0
        return float(np.sqrt(np.mean(flat ** 2)))
    except Exception:
        return 0.0

def process_audio(model):
    while True:
        try:
            audio_chunks = []
            silence_count = 0
            is_speaking = False
            phrase_start_time = time.time()

            while True:
                try:
                    data = audio_queue.get(timeout=0.1)
                    audio_chunks.append(data)

                    rms = get_rms(data)
                    elapsed = time.time() - phrase_start_time

                    if elapsed >= MAX_PHRASE_SECONDS:
                        break

                    if rms > SILENCE_THRESHOLD:
                        if not is_speaking:
                            is_speaking = True
                            try:
                                sio.emit("stt-listening")
                            except Exception:
                                pass
                        silence_count = 0
                    elif is_speaking:
                        silence_count += 1
                        if silence_count >= MIN_SILENCE_FRAMES:
                            break

                except queue.Empty:
                    if audio_chunks:
                        break

            if not audio_chunks:
                continue

            combined = np.concatenate([np.asarray(c, dtype=np.float32).flatten() for c in audio_chunks])
            
            target_length = int(len(combined) * SAMPLE_RATE / 16000)
            resampled = signal.resample(combined, target_length)
            resampled = np.clip(resampled, -1.0, 1.0).astype(np.float32)
            
            try:
                segments, _ = model.transcribe(
                    resampled,
                    language="pt",
                    task="translate",
                    vad_filter=False,
                    vad_parameters=dict(min_silence_duration_ms=2000),
                    condition_on_previous_text=True,
                    temperature=[0.0, 0.2, 0.4],
                    beam_size=1,
                    best_of=1
                )
                
                en_text = ""
                for segment in segments:
                    if segment.text.strip():
                        en_text += segment.text.strip() + " "
                
                en_text = en_text.strip()
                
                if len(en_text) < 2:
                    continue
                    
                print(f">>> {en_text}")
                
            except Exception:
                continue

            send_translation("", en_text)

        except Exception:
            time.sleep(0.1)

if __name__ == "__main__":
    device_index, channels, model_name, model_path = get_device_and_model()
    
    model = load_whisper(model_path)
    
    try:
        sio.connect(SERVER_URL, transports=["websocket"], headers={"client": "python-ear"})
    except Exception:
        pass

    with sd.InputStream(
        device=device_index,
        samplerate=SAMPLE_RATE,
        channels=channels,
        dtype='float32',
        blocksize=BUFFER_SIZE,
        callback=lambda indata, frames, time_info, status: audio_callback(indata, frames, time_info, status, channels)
    ):
        process_audio(model)
