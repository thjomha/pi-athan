import os
import time
import threading
import pygame
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)
# Initialize pygame mixer for audio playback
pygame.mixer.init()

# ============================
# ✅ Global Variables for Audio Control
# ============================
audio_channel = None  # Track audio channel for controlling playback

# ============================
# ✅ Function to Get Prayer Times from Database
# ============================
def get_prayer_times():
    # This function should query your database to get today's prayer times.
    # For demonstration, returning a mock response.
    return {
        'Fajr': '05:00 AM',
        'Sunrise': '06:30 AM',
        'Dhuhr': '12:00 PM',
        'Asr': '03:00 PM',
        'Maghrib': '06:15 PM',
        'Isha': '07:30 PM'
    }

# ============================
# ✅ Function to Play Audio Safely (with Lock)
# ============================
def play_audio(file_path):
    global audio_channel

    # Prevent duplicate audio from playing
    if audio_channel and audio_channel.get_busy():
        print("Audio is already playing. Ignoring duplicate request.")
        return

    def play():
        try:
            pygame.mixer.music.load(file_path)  # Load the audio file
            pygame.mixer.music.play()  # Start playing the audio
            print(f"Playing audio: {file_path}")
        except Exception as e:
            print(f"Error playing audio: {e}")

    # Run audio playback in a separate thread
    audio_thread = threading.Thread(target=play)
    audio_thread.start()

# ============================
# ✅ Function to Stop Audio
# ============================
def stop_audio():
    global audio_channel
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()  # Stop playing the audio
        print("Audio stopped successfully.")
    else:
        print("No audio is currently playing.")

# ============================
# ✅ Route to Stop Audio (POST for manual stop)
# ============================
@app.route("/stop_audio", methods=["POST"])
def stop_audio_server():
    stop_audio()
    return jsonify({"status": "success", "message": "Audio stopped successfully!"})

# ============================
# ✅ Routes to Trigger Audio
# ============================
@app.route("/play_athan_server", methods=["POST"])
def play_athan_server():
    audio_file = "static/athan.mp3"
    threading.Thread(target=play_audio, args=(audio_file,)).start()
    return jsonify({"status": "success", "message": "Athan is playing on the server!"})

@app.route("/play_adhkar_server", methods=["POST"])
def play_adhkar_server():
    audio_file = "static/adhkar.mp3"
    threading.Thread(target=play_audio, args=(audio_file,)).start()
    return jsonify({"status": "success", "message": "Adhkar is playing on the server!"})

@app.route("/webhook", methods=["POST"])
def webhook():
    audio_file = "static/morning.mp3"
    threading.Thread(target=play_audio, args=(audio_file,)).start()
    return jsonify({"status": "success", "message": "Morning Adhkar is playing on the server!"})

# ============================
# ✅ Route to Stop Audio via Webhook (POST for external trigger)
# ============================
@app.route("/stop_audio_webhook", methods=["POST"])
def stop_audio_webhook():
    stop_audio()
    return jsonify({"status": "success", "message": "Audio stopped via webhook!"})

# ============================
# ✅ Route to Render the Main Page
# ============================
@app.route("/")
def home():
    prayer_times = get_prayer_times()
    return render_template("index.html", prayer_times=prayer_times)

if __name__ == "__main__":
    app.run(debug=True)
