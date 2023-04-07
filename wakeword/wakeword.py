import pvporcupine
import pyaudio
import struct
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()


ACCESS_KEY = os.getenv('PICO_ACCESS_KEY')
wake_word_file = r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\wakeword\Jarvis_en_windows_v2_1_0.ppn"

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
        subprocess.run(["python", r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\test2.py"])
