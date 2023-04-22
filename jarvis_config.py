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
import pygame
import time
from genderize import Genderize
import webbrowser
from web import play_youtube_video
from image_creation import generate_image
import speech_recognition as sr
import threading



class Jarvis:
    """
    A personal assistant modeled after Jarvis from Iron Man.

    Attributes:
    - openai: The OpenAI library for creating chat responses.
    - name: The name of the user.
    - previous_interactions: A dictionary of the user's previous interactions.
    - messages: A list of the user's messages.
    - personality: The personality of Jarvis.
    - salutation: The salutation to address the user.
    - engine: The text-to-speech engine.
    - greeting_messages: A dictionary of greeting messages.
    - weather_api_endpoint: The API endpoint for the weather.
    - weather_api_key: The API key for the weather.
    - city_name: The name of the city for the weather.
    - latitude: The latitude of the user's location.
    - longitude: The longitude of the user's location.
    - openai_api_key: The API key for OpenAI.
    - genderize: The Genderize library for determining the user's gender.
    """
    
    def __init__(self):
        self.openai = openai
        self.name = "Tyler"
        self.previous_interactions = {}
        self.messages = []
        self.jarvis_personality = f"You are a personal assistant named Jarvis. Your task is to respond to {self.name}'s requests as if you were his personal assistant. Your personality is modeled after the helpful and efficient Jarvis from the Iron Man movies, but you are also capable of adapting your tone to match your user's preferences and needs and should sound natural and conversational."
        self.genderize = Genderize()
        self.gen_info = self.genderize.get([self.name])[0]
        if self.gen_info['gender'] == 'male':
            self.salutation = 'Sir'
        else:
            self.salutation = 'ma\'am'
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 190)
        self.greeting_messages = {
            "message1": f"Yes, {self.name}?",
            "message2": f"How can I be of service, {self.salutation}?",
            "message3": f"At your service, {self.salutation}.",
            "message4": f"JARVIS here, {self.name}. How may I be of assistance?",
            "message5": f"JARVIS online, {self.name}.",
            "message6": f"Ready and waiting, {self.salutation}."
            }
        self.weather_api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
        self.weather_api_key = WEATHER_API_KEY
        self.city_name = CITY_NAME
        self.lat = YOUR_LATITUDE
        self.lon = YOUR_LONGITUDE
        self.openai.api_key = OPEN_AI_APIKEY
        
    def execute_methods(self):
        """Executes several methods in separate threads and waits for them to finish.

    This method creates five threads, each running a different method in the current
    object instance. The methods that are executed are `get_weather`, `check_mood`,
    `check_stock_market`, `check_emails`, and `read_subject_email`. The threads are
    started and allowed to run concurrently. The method then waits for all threads to
    complete before returning.
        """
    # create threads for both methods
        t1 = threading.Thread(target=self.get_weather)
        t2 = threading.Thread(target=self.check_mood)
        t3 = threading.Thread(target=self.check_stock_market)
        t4 = threading.Thread(target=self.check_emails)
        t5 = threading.Thread(target=self.read_subject_email)
        # start both threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        # wait for all threads to finish
        t1.join()
        t2.join()
        t3.join() 
        t4.join()
        t5.join()         
        

    def process_input(self, input_text):
        """Process user input and return an AI-generated response.

        Args:
            input_text (str): The user input to be processed.

        Returns:
            str: The AI-generated response to the user input.

        This method adds the user input to a list of previous messages and uses OpenAI's
        GPT-3.5 Turbo model to generate a response based on the entire conversation history.
        The response is then added to the message list and returned.
        """

        try:
            if self.messages[-1]['role'] != "assistant":
                
                self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality}"})
        except IndexError:
            self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality}"})
        
        self.messages.append({f"role": "user", "content": f"{input_text}"})
        
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        
        reply = response.choices[0].message.content
        
        
        self.messages.append({"role": "assistant", "content": reply})
        
        return reply
    
    def get_random_greeting(self):
        """
        Select a random greeting message from the dictionary of greeting messages.

        The method chooses a random key from the `greeting_messages` attribute,
        which is assumed to be a dictionary mapping strings to strings. It then
        returns the corresponding value associated with the selected key.

        Returns:
            A string representing a randomly selected greeting message.
        """
        self.random_key = random.choice(list(self.greeting_messages.keys()))
        self.random_value = self.greeting_messages[self.random_key]
        return self.random_value
    
    def say(self, text):
        """
        Uses the text-to-speech engine to speak the provided text.

        Args:
            text (str): The text to be spoken.

        Returns:
            None
        """        
        self.engine.say(text)
        self.engine.runAndWait()
        
    def get_user_input(self):
        """
        Captures audio input from the user's microphone and returns the recognized text.

        Returns:
        --------
        str or None:
            Returns the recognized text if successful, otherwise None.

        Raises:
        -------
        None.

        Example:
        --------
        To capture user input and get the recognized text, call the method as follows:
            recognized_text = get_user_input()
        """

        self.r = sr.Recognizer()
        
        with sr.Microphone() as source:

            try:
                self.user_choice_audio = self.r.listen(source, timeout=10)
            except sr.WaitTimeoutError:
                self.say(f"Goodbye, just call my name if you need anything else")
                return None
            except sr.RequestError:
                self.say(f"Sorry {self.salutation}, I'm having trouble accessing the microphone.")
                return None

        try:
            self.user_choice = self.r.recognize_google(self.user_choice_audio).lower()
            return self.user_choice
        except sr.UnknownValueError:
            self.say("Goodbye, just call my name if you need anything else")
            return None
        except sr.RequestError:
            self.say("Sorry, I'm having trouble accessing the internet right now.")
            return None
                
                
    def get_weather(self):
        """
        Retrieves current weather data from OpenWeatherMap API based on the latitude and longitude provided by the user.

        If "weather" is included in the user's choice, the function constructs a URL for the OpenWeatherMap API and sends a GET request
        to retrieve the weather data. The data is stored in self.weather_data and a message containing the data is appended to self.messages.

        Args:
            None

        Returns:
            None
        """

        if "weather" in self.user_choice:
            self.weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.weather_api_key}"
            response = requests.get(self.weather_url)
            self.weather_data = response.json()
            self.messages.append({"role": "assistant", "content": f"Here is the all the relevant current weather data. i am going to ask you questions about it and you respond accordingly. Current Weather Data: {get_weather_info(self.weather_data)}."})
            
    def check_mood(self):
        """
        Check the user's mood and prompt a conversation about it.

        This method first checks whether the user has mentioned their mood or feeling
        in their input, by looking for the words "mood" or "feeling" in `self.user_choice`.
        If so, it calls the `detect_expression` function to detect the user's facial
        expression and stores the result in `self.emotion`. Then it adds a message to the
        `self.messages` list, with the assistant's role and a prompt to start a conversation
        about the user's mood.

        Returns:
            None
        """
        if "mood" in self.user_choice or "feeling" in self.user_choice:
            self.emotion = detect_expression()
            self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality} now that you know who you are. here is {self.name}'s current mood is {self.emotion}. i am going to ask you questions about it and you respond accordingly"})
        

    def check_stock_market(self):
        """
        Check if the user has requested information about the stock market today.
        If so, fetch the latest financial headlines from Yahoo Finance and add a message to the
        conversation with the headlines, asking the assistant to summarize the information in a short response.

        Returns:
            None
        """
        #check if user said stock market today
        if "stock market" in self.user_choice:
            url = "https://finance.yahoo.com/"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            headlines = [headline.text.strip() for headline in soup.find_all("h3")]
            self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality} now that you know who you are. using these financial headlines aggregate them and answer {self.name}'s request accordingly and your answers should be somewhat short and don't speak of the headlines. Headlines: {headlines}"})  
        
    def check_emails(self):
        """
        Check the user's email account for unread messages, and append a message to the `messages` list
        with the number of unread emails.

        Args:
            self (Jarvis): The current Jarvis instance.

        Returns:
            None
        """
        if "do"in self.user_choice and "emails" in self.user_choice:
            unread = get_num_unread_emails()
            self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality} now that you know who you are. answer {self.name}'s request using this info: {self.name} has {unread} unread emails"})
    
    def read_subject_email(self):
        """
        Reads the subject lines of unread emails in the user's inbox and adds them to the `messages` list.

        If the user's choice includes the phrase "read emails", this function calls the `get_subject_lines_unread_emails()`
        function to retrieve the subject lines of all unread emails in the user's inbox. It then creates a message object
        and adds it to the `messages` list with the `role` field set to "assistant" and the `content` field set to a string
        containing the Jarvis personality and the subject lines of the unread emails.

        Returns:
            None.
        """
        if "read"in self.user_choice and "emails" in self.user_choice: 
            read = get_subject_lines_unread_emails()
            self.messages.append({"role": "assistant", "content": f"{self.jarvis_personality} now that you know who you are. answer the request using this info: in {self.name}'s inbox here are the subject lines of the emails {read}"})

    
    def web_search(self):
        """Searches for a website specified by the user and opens it in a new browser tab.

        If the user's input contains the phrases "pull," "up," and "website," the function prompts the user to provide the URL of the website they want to open. It then uses the OpenAI GPT-3 API to generate a response to the user and extract the URL from the response. Finally, it opens the website in a new browser tab using the `webbrowser` module.

        Returns:
            None
        """
        if "pull" in self.user_choice and "up" in self.user_choice and "website" in self.user_choice:
            define_gpt_web = "Your task is to give me the whole url of the website i am talking about. Don't explain anything i just want the url that is it. nothing before or after it"
            self.say(f"Pulling it up now")
    
            web_list = []
            web_list.append({"role": "assistant", "content": f"{define_gpt_web}"})
            web_list.append({f"role": "user", "content": f"{self.user_choice}"})
        
            title_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=web_list
            )
            web_url = title_response.choices[0].message.content
            
            
            def open_website(url):
             webbrowser.open_new_tab(url)
            open_website(web_url)
            sys.exit()
        
    def morning_protocol(self):
        """
        Initiates the morning protocol by opening several URLs in the user's web browser.

        If the user's choice includes the strings "initiate," "morning," and "protocol," this method
        will initiate the morning protocol by opening several URLs in the user's web browser.

        The URLs that are opened are stored in the `morning_protocol_urls` list. This list can be
        modified to include additional or different URLs as needed.

        This method calls the `morning_web_protocol` function, which accepts a list of URLs as an argument
        and opens each URL in a new tab in the user's default web browser.

        After all the URLs have been opened, the script will exit.

        Note: This method requires the `webbrowser` and `sys` modules to be imported.
        """
        if "initiate" in self.user_choice and "morning" in self.user_choice and "protocol" in self.user_choice:
        
            self.say(f"Initiating morning protocol, {self.salutation}")
            
            
            morning_protocol_urls = ["https://www.linkedin.com", "https://app.beehiiv.com", "https://twitter.com/home", "https://chat.openai.com/"]
            def morning_web_protocol(urls):
                for url in urls:
                  webbrowser.open_new_tab(url)
            
            morning_web_protocol(morning_protocol_urls)
            sys.exit()
            
    def search_youtube(self): 
        """
        This method searches for a YouTube video based on user input and plays it.

        If the user has selected the 'youtube' and 'mode' options, the method prompts the user for a video to play
        and then searches YouTube for the video using the `play_youtube_video` function. The method then exits the program.

        Args:
            None

        Returns:
            None
        """
        if "youtube" in self.user_choice and "mode" in self.user_choice:
            self.say("What youtube video would you like to play?")
            video_choice = self.get_user_input()
            self.say("pulling it up now")
            play_youtube_video(query=video_choice)
            sys.exit()
        
    
    def art_mode(self):
        """Initiates an art mode and generates an image based on user input.

        Prompts the user for an image prompt and generates an image using the 
        generate_image() function. The program terminates after the image is generated.

        Raises:
            No exceptions are explicitly raised, but the generate_image() function 
            called within this method may raise exceptions if there are issues with 
            the image generation process.

        Returns:
            None
        """
        if "initiate" in self.user_choice and "art" in self.user_choice and "mode" in self.user_choice:
            self.say(f"Art mode initiated")
            self.say(f"what is it you would like me to make?")
            image_prompt = self.get_user_input()
            if image_prompt is not None:
                self.say(f"Generating a masterpiece for you")
                generate_image(prompt=image_prompt)       
                sys.exit()
                
         
    def check_stop(self):
        """
        Check if the user has requested to stop the conversation.

        If the user's choice is 'stop', 'bye', or 'no' (case-insensitive),
        this method prints a goodbye message and terminates the program using
        sys.exit().

        Returns: None
        """
        if self.user_choice.lower() == "stop":
            self.say("Okay, Goodbye")
            sys.exit()
        if self.user_choice.lower() == "bye":
            self.say("Okay, Goodbye")
            sys.exit()
        if self.user_choice.lower() == "no":
            self.say("Okay, Goodbye")
            sys.exit()
            
            
            








        



