import pvporcupine
import pyaudio
import struct
import subprocess
from face_recog import facerec
import pyttsx3
import datetime
import random
from genderize import Genderize
import pygame
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from jarvis_config import Jarvis
from mail import get_num_unread_emails
import sys
from colorama import init, Fore, Style
from num2words import num2words
from keys import PICOVOICE_API_KEY

jarvis = Jarvis()

#wakeword API key
ACCESS_KEY = PICOVOICE_API_KEY

#if this model is outdated train a new one on https://picovoice.ai/ takes like 3 mins
wake_word_file = "D:\\OneDrive\\Desktop\\Jarvis\\wakeword\\jarvis_en_windows_v2_2_0.ppn"

detected_face = facerec()

pygame.init()
pygame.mixer.music.load(r'D:\OneDrive\Desktop\Jarvis\wakeword\0424.MP3')
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
with ThreadPoolExecutor(max_workers=1) as executor:
    future1 = executor.submit(get_num_unread_emails, email=jarvis.email, password=jarvis.email_password)

    # Wait for both functions to complete
    results = [future1.result()]
    unread_emails = num2words(results[0])

if results[0] > 0 :
    messages_dict = {
    "message1": f"Welcome back, {detected_face}! It's always a pleasure to see you. Rest assured that your system is fully optimized and secure. You have {unread_emails} unread emails waiting for you.",
    "message2": f"Welcome back, {detected_face}! Your system is fully optimized and secured, ready to assist you in any way possible. You have {unread_emails} unread emails to attend to.",
    "message3": f"Hello, {salutation}! I'm pleased to report that your system is running optimally and is secure. There are {unread_emails} unread emails that require your attention.",
    "message4": f"Greetings, {detected_face}! It's great to have you back. Your system is fully optimized and protected. You have {unread_emails} unread emails in your inbox.",
    "message5": f"Welcome back, {detected_face}. I'm happy to report that your system is running at peak performance and is fully secured. You have {unread_emails} unread emails to catch up on.",
    "message6" :f"Greetings, {detected_face}! Your system is optimized and protected from any unwanted visitors. It's always a joy to see you again. You have {unread_emails} unread emails to read."
   }
    
else:
    messages_dict = {
        "message1": f"Good {time_of_day(now)}, {detected_face}. The system is now fully operational and standing by.",
        "message2": f"Good day, {detected_face}. Jarvis at your service. All systems are online and ready for action.",
        "message3": f"System boot complete. Ready for your commands, {salutation}.",
        "message4": f"Good {time_of_day(now)}, {salutation}. Shall we begin?",
        "message5": f"Welcome back, {detected_face}! It's always a pleasure to see you. Rest assured that your system is fully optimized and secure.",
        "message6": f"Welcome back, {detected_face}. The facial recognition system has successfully identified you, and all systems are fully operational."
    }
    
 

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
        if keyword_index >= 0 and detected_face == jarvis.name:
            init()
            jarvis.say(jarvis.get_random_greeting())

            while True:
                user_input = jarvis.get_user_input()
                
                if user_input != None:
                    print(Fore.GREEN + f"{detected_face}'s Input: " + Style.RESET_ALL + user_input + '\n')
        
                    jarvis.web_search()
                    jarvis.get_weather()
                    jarvis.check_mood()
                    jarvis.check_stock_market()
                    jarvis.check_emails()
                    jarvis.read_subject_email()
                    jarvis.click_screen()
                    jarvis.morning_protocol()
                    jarvis.art_mode()
                    if not jarvis.search_youtube():
                        break                    
                    if not jarvis.stock_plotter():
                        break                    
                    if not jarvis.check_stop():
                        break
                    response = jarvis.process_input(user_input)
                    
                    print(Fore.BLUE + 'Jarvis: ' + Style.RESET_ALL + response + '\n')
                else:
                    break

                jarvis.say(response)

#security         
if detected_face.lower() != jarvis.name.lower():
    jarvis.say(f"sorry, you are not {jarvis.name}, you do not have access to jarvis permissions, shutting down Jarvis")
    sys.exit()        
else:
    bootup_message = random.choice(list(messages_dict.values()))
    jarvis.say(f"Facial recognition successful")
    jarvis.say(f"{bootup_message}")
    while True:
        listen_for_wake_word()



