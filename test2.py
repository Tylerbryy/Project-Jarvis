import speech_recognition as sr
import openai
import sys
import os
import pyttsx3
import requests
from datetime import datetime
from weatherconfig import get_weather_info
from facial_expression import detect_expression
from keys import *
from bs4 import BeautifulSoup
import random
from mail import get_num_unread_emails, get_subject_lines_unread_emails

your_name = "Tyler"
# Set up the OpenAI API credentials
openai.api_key = OPEN_AI_APIKEY
weather_api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

weather_api_key = WEATHER_API_KEY
city_name = CITY_NAME
lat = YOUR_LATITUDE
lon = YOUR_LONGITUDE

engine = pyttsx3.init()
engine.setProperty('rate', 190) 

try:
    name = sys.argv[1]
except IndexError:
    name = your_name
    

# Define a dictionary to store previous interactions
previous_interactions = {}
messages = []
jarvis_personality = f"You are a personal assistant named Jarvis. Your task is to respond to {name}'s requests as if you were an his personal assistant. Your personality is modeled after the helpful and efficient Jarvis from the Iron Man movies, but you are also capable of adapting your tone to match your user's preferences and needs and should sound natural and conversational."



# Define a function to process user input
def process_input(input_text):
        
    
    #app creation logic
    define_gpt = "You are a Senior Software Engineer that can build python apps on command. Your responses should only be python code nothing more nothing less and do not explain the code"
    if "create" in input_text and "app" in input_text:
        # Gather information about the app
        messages.append({"role": "assistant", "content": f"{define_gpt}"})
        messages.append({f"role": "user", "content": f"{input_text}"})
        
        # Generate the code using OpenAI API
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
        
        
        # Get the generated code from the response
        generated_code = response.choices[0].message.content
        #getting rid of '''
        
        if "```" in generated_code:
           generated_code = generated_code.replace("```", "")
        if "python" in generated_code:
            generated_code = generated_code.replace("python", "")
        if "```" and "python" in generated_code:
            generated_code = generated_code.replace("```", "").replace("python", "")
            
           
           
        
        #generate a custom title for the app
        title_list = []
        response_param = "Give me a title for this app don't include any spaces in the title. Your response should only be the title nothing else"
        title_list.append({"role": "assistant", "content": f"{response_param}"})
        title_list.append({f"role": "user", "content": f"{input_text}"})
    
        title_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=title_list
        )
        title = title_response.choices[0].message.content
        
        
        # Save the code to a file
        with open(f"{title}.py", "w") as f:
            f.write(generated_code)
            engine.say("The app you requested is done")
            print("Jarvis: " + "The app you requested is done")
            engine.runAndWait()
        
        # Run the code to create the app
        try:
            os.system(f"python {title}.py")
        except:
            engine.say("There was an error running the app.")
            engine.runAndWait()
    else:
        
        messages.append({"role": "assistant", "content": f"{jarvis_personality}"})
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
    with open(r'misc', 'w') as f:
        for i, interaction in previous_interactions.items():
            f.write(f'Interaction {i}:\nUser input: {interaction["user_input"]}\nJarvis response: {interaction["jarvis_response"]}\n\n')

# Use SpeechRecognition to recognize audio input
greeting_messages = {
    "message1": f"Yes, {name}?",
    "message2": f"How can I be of service, {name}?",
    "message3": f"At your service, {name}.",
    "message4": f"JARVIS here, {name}. How may I be of assistance?",
    "message5": f"JARVIS online, {name}.",
    "message6": f"Ready and waiting, {name}."
    }

def get_random_message(message_dict):
    
    random_key = random.choice(list(message_dict.keys()))
    random_value = message_dict[random_key]
    return random_value

r = sr.Recognizer()
engine.say(get_random_message(message_dict=greeting_messages))
           
engine.runAndWait()

while True:
    with sr.Microphone() as source:
        
        try:
            audio = r.listen(source, timeout=10) # wait for 10 seconds for input
        except sr.WaitTimeoutError:
            engine.say("Goodbye, just call my name if you need anything else")
            engine.runAndWait()
            break

    # Convert audio to text using SpeechRecognition
    try:
        user_input = r.recognize_google(audio)
    except sr.UnknownValueError:
        
        break

    print(user_input)
    
    #real time weather data 
    if "weather" in user_input:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
        response = requests.get(url)
        weather_data = response.json()
        messages.append({"role": "assistant", "content": f"Here is the all the relevant current weather data you need to fulfill the request only give what is requested. Current Weather Data: {get_weather_info(weather_data)}"})
        
    
    #check if user said mood or feeling
    if "mood" in user_input or "feeling" in user_input:
        emotion = detect_expression()
        messages.append({"role": "assistant", "content": f"{jarvis_personality} now that you know who you are. {name} asked {user_input}. here is {name}'s current mood is {emotion}. Start by saying 'I can tell you're {emotion}"})
        
        
    #check if user said stock market today
    if "stock market" in user_input:
        url = "https://finance.yahoo.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = [headline.text.strip() for headline in soup.find_all("h3")]
        messages.append({"role": "assistant", "content": f"{jarvis_personality} now that you know who you are. {name} asked {user_input}. using these financial headlines aggregate them and answer {name}'s request accordingly and your answers should be somewhat short. : {headlines}"})
    
    if "do"in user_input and "emails" in user_input:
        unread = get_num_unread_emails()
        messages.append({"role": "assistant", "content": f"{jarvis_personality} now that you know who you are. {name} asked {user_input}. answer {name}'s request using this info: {name} has {unread} unread emails"})
    
    if "read"in user_input and "emails" in user_input: 
        read = get_subject_lines_unread_emails()
        messages.append({"role": "assistant", "content": f"{jarvis_personality} now that you know who you are. {name} asked {user_input}. answer the request using this info: in {name}'s inbox here are the subject lines of the emails {read}"})
        
    
    
    # Check if the user has said "stop"
    if user_input.lower() == "stop":
        engine.say("Okay, Goodbye")
        print("Okay, Goodbye!")
        engine.runAndWait()
        break
    if user_input.lower() == "bye":
        engine.say("Okay, Goodbye!")
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
    try:
     print("Jarvis: " + response_text)
    except TypeError:
        engine.say("Would you like anything else?")
        engine.runAndWait()
        
    
    # Store the user input and Jarvis response in previous interactions
    previous_interactions[len(previous_interactions) + 1] = {'user_input': user_input, 'jarvis_response': response_text}
    
    engine.say(response_text)
    engine.runAndWait()
