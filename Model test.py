import pyaudio
import json
from vosk import sihmod, KaldiRecognizer

#Loading the sihmod
print("sihmod loading")
try:
    sihmod = sihmod("sihmod")
except Exception as e:
    print("Error Thrown, model no found")
    exit()

#sampling rate set to 16k hz
recognizer = KaldiRecognizer(sihmod, 16000)

#pyaudio setup for input from microphone(my lappys mic)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=8000)
stream.start_stream()

print("Model loaded, its now listening")

#loop for listenign
try:
    while True:
        #raw b8s read from my mic ** this is my mic okay, not our ESPs mic, so the audio quality will be different from the ESPs mic
        data = stream.read(4000, exception_on_overflow=False)
        
        #fEEDING THE B8S onto the Vosk model
        if recognizer.AcceptWaveform(data):
            #when a pause is detected, the final thing is transcribed, what it thought we said
            result = json.loads(recognizer.Result())
            print(f"\nFinal Transcribed Command {result['text']} <<<")
        else:
            #the realtime result we see
            partial_result = json.loads(recognizer.PartialResult())
            # ig \r overwrites the same line on console for a cleaner look
            print(f"Listening: {partial_result['partial']}", end='\r')
            
except KeyboardInterrupt:
    print("\nStopping ASR test...")
    stream.stop_stream()
    stream.close()
    p.terminate()