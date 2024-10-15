from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import requests
import time

start_time = time.perf_counter()
CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/vL6RHefgA7aaBaziduNC"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ""
}

data = {
  "text": "text",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
end_time = time.perf_counter()
print(f"Total response execution time: {(end_time - start_time) * 1000:.2f} ms")
start_time = time.perf_counter()
audio_data = BytesIO()
for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    if chunk:
        audio_data.write(chunk)

audio_data.seek(0)  # Rewind the buffer
audio_segment = AudioSegment.from_file(audio_data, format="mp3")

end_time = time.perf_counter()
print(f"Total audio processing execution time: {(end_time - start_time) * 1000:.2f} ms")

play(audio_segment)



