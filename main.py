import pyaudio
import vosk
import json

# Set sample rate and buffer size
SAMPLE_RATE = 16000
BUFFER_SIZE = 4000

# Initialize the recognizer and model
model = vosk.Model(lang="ru")
rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=BUFFER_SIZE)

# Start the stream
stream.start_stream()

print("Listening...")

try:
    while True:
        # Read audio data from the microphone
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        if len(data) == 0:
            continue

        # Process the audio data with the recognizer
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(json.loads(result)["text"])
        else:
            partial_result = rec.PartialResult()
            print(json.loads(partial_result)["partial"])
          
        """
        Remove same phrases and send packets to ElevenLabs
        
        """
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
