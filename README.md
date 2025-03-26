# Briskk AI Speech-to-Text

This project is a **FastAPI-based Speech-to-Text** service that supports:
- **Real-time speech recognition** using `speech_recognition` and `Whisper`.
- **Noise reduction** via `DeepFilterNet`.
- **Smart search autocomplete** with **Redis** ranking.

---

## 🚀 Features
- Upload an **audio file** and get **transcribed text**.
- **Noise reduction** before processing.
- **Autocomplete API** using Redis to store past searches.

---

## 🛠 Installation Guide

### 1⃣ Clone the Repository
```sh
git clone https://github.com/gunapriya07/briskk-speech-assignment.git
cd briskk-speech-assignment
```

### 2⃣ Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4⃣ Install Redis (For Autocomplete)
Redis is used for storing and ranking past search queries.

#### 🔵 **For Linux/macOS**
```sh
sudo apt update && sudo apt install redis -y
```
Start Redis:
```sh
redis-server
```

#### 🔴 **For Windows**
Download Redis from [https://github.com/microsoft/WSL](https://github.com/microsoft/WSL) and run:
```sh
redis-server
```

---

## 🎤 Running the FastAPI Server
Start the API using **Uvicorn**:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🏷 API Endpoints

### 🎧 **1. Upload Audio & Transcribe**
- **Endpoint:** `POST /api/voice-to-text`
- **Usage:** Upload an audio file (`.wav`, `.mp3`, etc.).
- **Response:**
```json
{
  "message": "File received and transcribed successfully",
  "text": "Hello, how are you?"
}
```

### 🔍 **2. Get Autocomplete Suggestions**
- **Endpoint:** `GET /api/autocomplete?q=your_search`
- **Response:**
```json
{
  "suggestions": ["What's the weather today?", "Set an alarm for 6 AM"]
}
```

---

## ⚡ Notes
- If **Redis is not installed**, **autocomplete won't work**.
- Noise reduction is done using **DeepFilterNet** (ensure it’s installed).
- Speech recognition uses **Google Speech API** (can be replaced with Whisper).

---

## 🎯 Future Enhancements
- Support for **streaming speech recognition**.
- Whisper-based transcription for **more accuracy**.
- User **history tracking** and **custom ranking** in Redis.
---



