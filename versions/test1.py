import speech_recognition as sr
import openai
import os
import pyttsx3
import requests
from datetime import datetime
# Set up the OpenAI API credentials
openai.api_key = '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'
weather_api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

weather_api_key = "1e54c7d6c61aa00ad5e7ca0068cb5c7f"
city_name = "Blanchard"
lat =35.138901
lon = -97.654617

engine = pyttsx3.init()

# Define a dictionary to store previous interactions
previous_interactions = {}

messages = []
jarvis_personality = "You are a personal assistant named Jarvis. Your task is to respond to your user's requests as if you were an assistant. You have witty sense of humor but also very informative, and should sound natural and conversational."
messages.append({"role": "assistant", "content": f"{jarvis_personality}"})

# Define a function to process user input
def process_input(input_text):
    
   
    messages.append({f"role": "user", "content": f"{input_text}"})
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    return reply

# Define a function to save previous interactions to a text file
def save_interactions():
    with open(r'Jarvis\interactions.txt', 'w') as f:
        for i, interaction in previous_interactions.items():
            f.write(f'Interaction {i}:\nUser input: {interaction["user_input"]}\nJarvis response: {interaction["jarvis_response"]}\n\n')

# Use SpeechRecognition to recognize audio input
r = sr.Recognizer()
engine.say("Jarvis is listening")
           
engine.runAndWait()

while True:
    with sr.Microphone() as source:
        
        try:
            audio = r.listen(source, timeout=10) # wait for 10 seconds for input
        except sr.WaitTimeoutError:
            engine.say("Goodbye!")
            print("Goodbye")
            engine.runAndWait()
            break

    # Convert audio to text using SpeechRecognition
    try:
        user_input = r.recognize_google(audio)
    except sr.UnknownValueError:
        engine.say("Goodbye!")
        print("Goodbye")
        engine.runAndWait()
        break

    print(user_input)
    #real time weather data 
    if user_input.lower() == "what is the weather like today":
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
        response = requests.get(url)
        weather_data = response.json()
        town = weather_data["name"]
        temp = float(weather_data["main"]["temp"])
        converted_temp = (temp - 273.15) * 1.8 + 32
        weather_description = weather_data["weather"][0]["description"]
        engine.say(f"The weather in {town}, is {int(converted_temp)} °F with {weather_description}")
        engine.runAndWait()
    
    
    # Check if the user has said "stop"
    if user_input.lower() == "stop":
        engine.say("Okay, Goodbye")
        print("Okay, Goodbye!")
        engine.runAndWait()
        break
    if user_input.lower() == "no":
        engine.say("Okay, Goodbye!")
        print("Okay, Goodbye!")
        engine.runAndWait()
        break
    
    # Check if the user has said "save interactions"
    if user_input.lower() == "save interactions":
        save_interactions()
        engine.say("Your interactions have been saved to a text file.")
        print("Your interactions have been saved to a text file.")
        engine.runAndWait()
        continue

    # Send user input to OpenAI GPT-3 API for processing
    response_text = process_input(user_input)
    print("Jarvis: " + response_text)
    
    # Store the user input and Jarvis response in previous interactions
    previous_interactions[len(previous_interactions) + 1] = {'user_input': user_input, 'jarvis_response': response_text}
    
    engine.say(response_text)
    engine.runAndWait()

    # Speak "Is there anything else?"

    engine.runAndWait()