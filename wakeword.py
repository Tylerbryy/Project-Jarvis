import pvporcupine
import pyaudio
import struct
import subprocess
import os
from face_recog import facerec
import pyttsx3
import datetime




#wakeword API key
ACCESS_KEY = ""


wake_word_file = r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\wakeword\Jarvis_en_windows_v2_1_0.ppn"

detected_face = facerec()


engine = pyttsx3.init()
""" RATE"""

engine.setProperty('rate', 200)   # setting up new voice rate

#check the time of day 
now = datetime.datetime.now()
def time_of_day(current_time):
    if current_time.hour >= 6 and current_time.hour < 12:
        return "morning"
    elif current_time.hour >= 12 and current_time.hour < 18:
        return "afternoon"
    else:
        return "evening"


now = datetime.datetime.now()


engine.say(f"Good {time_of_day(now)},{detected_face}. The system is now fully operational and standing by.")
engine.runAndWait()

porcupine = pvporcupine.create(
  access_key=f'{ACCESS_KEY}',
  keyword_paths=[f'{wake_word_file}']
)


pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length)

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        subprocess.run(["python", fr"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\test2.py", detected_face])
        
        