from fastapi import FastAPI, File, UploadFile, Query
import os
import speech_recognition as sr
from pydub import AudioSegment
import redis
import json
import subprocess
import os
print(os.path.abspath("temp/denoised_Conference.wav"))


app = FastAPI()

# Initialize Redis for autocomplete search ranking
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Function to apply noise reduction using DeepFilterNet
def denoise_audio(input_path: str, output_path: str):
    try:
        command = f"deepFilter {input_path} -o {output_path}"
        subprocess.run(command, shell=True, check=True)
        return output_path
    except Exception as e:
        print(f"Noise reduction failed: {e}")
        return input_path  # Return original if denoising fails

@app.post("/api/voice-to-text")
async def upload_test(audio: UploadFile = File(...)):
    file_path = f"temp/{audio.filename}"
    
    try:
        os.makedirs("temp", exist_ok=True)  # Ensure the folder exists
        print(f"Received file: {audio.filename}, Content Type: {audio.content_type}")

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            while chunk := await audio.read(1024):
                buffer.write(chunk)

        file_size = os.path.getsize(file_path)
        print(f"File saved: {file_path}, Size: {file_size} bytes")

        if file_size < 1000:
            return {"error": "File saved but seems too small"}

        # Noise reduction
        denoised_path = denoise_audio(file_path, f"temp/denoised_{audio.filename}")

        # Convert audio to WAV format (if necessary)
        recognizer = sr.Recognizer()
        audio_wav_path = denoised_path

        if not file_path.endswith(".wav"):
            audio_wav_path = file_path.rsplit(".", 1)[0] + ".wav"
            sound = AudioSegment.from_file(denoised_path)
            sound.export(audio_wav_path, format="wav")

        # Speech recognition (using Google API or OpenAI Whisper)
        with sr.AudioFile(audio_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Store search query in Redis for autocomplete ranking
        redis_client.zincrby("search_history", 1, text)

        return {"message": "File received and transcribed successfully", "text": text}

    except sr.UnknownValueError:
        return {"error": "Could not understand the audio"}
    except sr.RequestError:
        return {"error": "Speech Recognition API error"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/autocomplete")
async def autocomplete(q: str = Query(..., min_length=2)):
    try:
        # Fetch stored searches from Redis
        stored_suggestions = redis_client.zrevrange("search_history", 0, 4, withscores=False)
        print(f"Redis Suggestions: {stored_suggestions}")  # Debugging

        # Predefined fallback suggestions (for better user experience)
        default_suggestions = [
            "Find me a red dress", 
            "What's the weather today?", 
            "Set an alarm for 6 AM", 
            "Translate hello to Spanish",
            "Show me nearby restaurants"
        ]

        # Combine Redis data & predefined suggestions
        all_suggestions = stored_suggestions + default_suggestions  # Prioritize Redis data first
        filtered_suggestions = [s for s in all_suggestions if s.lower().startswith(q.lower())]

        print(f"Filtered Suggestions: {filtered_suggestions}")  # Debugging
        return {"suggestions": filtered_suggestions[:5]}  # Return top 5 results
    except Exception as e:
        return {"error": str(e)}


    
# Run FastAPI using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

