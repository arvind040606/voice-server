from flask import Flask, request, jsonify, send_file
import os
import uuid
import whisper
from gtts import gTTS

app = Flask(__name__)

# ⚠️ DO NOT load Whisper at startup
model = None

def get_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("tiny")  # tiny = MUCH less RAM
    return model


@app.route("/")
def home():
    return "Voice server running"


@app.route("/stt", methods=["POST"])
def stt():
    if "audio" not in request.files:
        return jsonify({"error": "No audio"}), 400

    audio = request.files["audio"]
    filename = f"/tmp/{uuid.uuid4()}.wav"
    audio.save(filename)

    model = get_model()
    result = model.transcribe(filename)

    return jsonify({"text": result["text"]})


@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    gTTS(text).save(filename)
    return send_file(filename, mimetype="audio/mpeg")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
