from flask import Flask, request, jsonify
import whisper
import os
import tempfile
from flask_cors import CORS # For handling Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app) # This will allow requests from your frontend, even if it's on a different port during development

# Load the Whisper model (base model, CPU)
# This can take some time the first time it's run as it downloads the model.
# Consider loading the model once when the app starts if performance is critical.
print("Loading Whisper model (base, CPU)...")
try:
    # Specify device="cpu" to ensure it runs on CPU
    model = whisper.load_model("base", device="cpu")
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    model = None # Set model to None if loading fails

@app.route('/')
def home():
    return "Whisper Transcription Backend is running!"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if model is None:
        return jsonify({"error": "Whisper model is not available."}), 500

    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file part in the request"}), 400

    file = request.files['audio_file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            # Create a temporary file to save the upload
            # Whisper's transcribe function expects a file path
            temp_dir = tempfile.mkdtemp()
            temp_filepath = os.path.join(temp_dir, file.filename)
            file.save(temp_filepath)
            print(f"Audio file saved temporarily to: {temp_filepath}")

            # Transcribe the audio file
            # You can adjust parameters like `language` if needed
            # result = model.transcribe(temp_filepath, language="en", fp16=False) # fp16=False for CPU
            print(f"Transcribing with model: {model.device}")
            result = model.transcribe(temp_filepath, fp16=False) # fp16=False for CPU

            transcription_text = result["text"]
            print(f"Transcription: {transcription_text}")

            # Clean up the temporary file and directory
            os.remove(temp_filepath)
            os.rmdir(temp_dir)

            return jsonify({"transcription": transcription_text})

        except Exception as e:
            print(f"Error during transcription: {e}")
            # Clean up temp file in case of error too
            if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            return jsonify({"error": f"An error occurred during transcription: {str(e)}"}), 500
    
    return jsonify({"error": "File processing failed"}), 500

if __name__ == '__main__':
    # Make sure to run on 0.0.0.0 to be accessible on your network if needed,
    # or 127.0.0.1 for local access only.
    # Default port is 5000.
    app.run(debug=True, host='0.0.0.0', port=5000)
