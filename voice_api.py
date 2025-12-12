from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import subprocess
import os
import re

from voice_parser import parse_voice_command
from firebase_service import add_transaction

# --------------------------
# App setup
# --------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Load Whisper model ONCE
# --------------------------
model = whisper.load_model("small")

# --------------------------
# Helper: convert webm → wav
# --------------------------
def convert_to_wav(input_path, output_path):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            output_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

# --------------------------
# Voice command endpoint
# --------------------------
@app.post("/voice-command")
async def voice_command(
    file: UploadFile = File(...),
    user_id: str = "default-user"
):
    # 1️⃣ Read audio
    audio_bytes = await file.read()

    # 2️⃣ Save temp webm
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(audio_bytes)
        webm_path = tmp.name

    wav_path = webm_path.replace(".webm", ".wav")

    # 3️⃣ Convert to wav
    convert_to_wav(webm_path, wav_path)

    # 4️⃣ Whisper transcription
    result = model.transcribe(
        wav_path,
        language="en",
        task="transcribe",
        fp16=False
    )

    raw_text = result["text"].strip()

    # 5️⃣ Normalize text BEFORE parsing
    normalized = raw_text.lower()
    normalized = re.sub(r"[^a-z0-9 ]", " ", normalized)
    normalized = re.sub(r"(\d+)", r" \1 ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    print("🧠 RAW:", raw_text)
    print("🧠 NORMALIZED:", normalized)

    # 6️⃣ Cleanup temp files
    os.remove(webm_path)
    os.remove(wav_path)

    # 7️⃣ Parse command
    cmd = parse_voice_command(normalized)

    if "error" in cmd:
        return {
            "status": "failed",
            "transcript": raw_text,
            "reason": cmd["error"]
        }

    # 8️⃣ Save to Firebase
    add_transaction(
        user_id=user_id,
        customer_name=cmd["customer_name"],
        item=cmd["item"],
        amount=cmd["amount"],
        transaction_type=cmd["action"].replace("add_", "")
    )

    return {
        "status": "success",
        "transcript": raw_text,
        "parsed": cmd
    }