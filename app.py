from flask import Flask, request, jsonify, send_file
import whisper
from gtts import gTTS
import uuid

app = Flask(__name__)

model = whisper.load_model("base")

@app.route("/")
def home():
    return "Voice server running"

@app.route("/stt", methods=["POST"])
def stt():
    audio = request.files["audio"]
    filename = f"/tmp/{uuid.uuid4()}.wav"
    audio.save(filename)

    result = model.transcribe(filename)
    return jsonify({"text": result["text"]})

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json["text"]
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    gTTS(text).save(filename)
    return send_file(filename, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
