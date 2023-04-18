import pvporcupine
import pyaudio
import struct
import subprocess
import os
from dotenv import load_dotenv
from face_recog import facerec
import pyttsx3
import datetime
import random
from genderize import Genderize
import pygame
import time
from mail import get_num_unread_emails,get_subject_lines_unread_emails
import threading
from concurrent.futures import ThreadPoolExecutor

#wakeword API key
ACCESS_KEY = ""

wake_word_file = r"D:\OneDrive\Desktop\Jarvis\wakeword\Jarvis_en_windows_v2_1_0.ppn"

detected_face = facerec()

pygame.init()
pygame.mixer.music.load('D:\OneDrive\Desktop\Jarvis\Project-Jarvis\wakeword\sound-1_cBqZb05.mp3')
pygame.mixer.music.play()
time.sleep(1)

engine = pyttsx3.init()
engine.setProperty('rate', 190)   # setting up new voice rate

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

def gender_of_user(name):
    gen_info = Genderize().get([f'{name}'])
    gender = gen_info[0]["gender"]
    return gender
    
if gender_of_user(detected_face) == "male":
    salutation = "Sir"
else:
    salutation = "ma'am"

#email section
with ThreadPoolExecutor(max_workers=2) as executor:
    future1 = executor.submit(get_num_unread_emails)
    future2 = executor.submit(get_subject_lines_unread_emails)

    # Wait for both functions to complete
    results = [future1.result(), future2.result()]
    

if results[0] > 0 :
    unread_emails = f'you have {results[0]} new emails'
    
else:
    unread_emails = ""
    
    

def listen_for_wake_word():
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
            subprocess.run(["python", fr"D:\OneDrive\Desktop\Jarvis\test2.py", detected_face])
            
thread = threading.Thread(target=listen_for_wake_word)
thread.start()

#random message upon bootup
messages_dict = {
    "message1": f"Good {time_of_day(now)},{detected_face}. The system is now fully operational and standing by.{unread_emails}",
    "message2": f"Good day, {detected_face}. Jarvis at your service. All systems are online and ready for action.{unread_emails}",
    "message3": f"System boot complete. Ready for your commands, {salutation}.{unread_emails}",
    "message4": f"Good {time_of_day(now)}, {salutation}. Shall we begin?{unread_emails}",
    "message5": f"Greetings, {detected_face}. It’s a pleasure to see you again. Your system is fully optimized and secure.{unread_emails}"
}

bootup_message = random.choice(list(messages_dict.values()))
engine.say(f"{bootup_message}")
engine.runAndWait()
