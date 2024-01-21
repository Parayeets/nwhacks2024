from flask import Flask, send_file, request, jsonify
from textToSpeech import generateSpeech, generateText
import os
app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello World!'

@app.route('/tts/')
def tts():
    text = request.args.get('text')
    voice = request.args.get('voice')
    speech = generateSpeech("output.wav", text, voice)
    return send_file(speech, mimetype='audio/wav')

@app.route('/stt', methods=['POST'])
def stt():
    audio_data = request.data

    if not audio_data:
        return jsonify({'error': 'No audio file provided'}), 400
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_data)
    result_text = generateText("temp_audio.wav")
    os.remove("temp_audio.wav")

    return jsonify({'result': result_text})

if __name__ == '__main__':
    app.run(debug=True)