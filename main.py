from jarvis_config import Jarvis
from colorama import init, Fore, Style
import webbrowser
import sys

# Initialize colorama
init()

jarvis = Jarvis()

program_on = True

jarvis.say(jarvis.get_random_greeting())

while program_on:
    user_input = jarvis.get_user_input()

    if user_input != None:
        print(Fore.GREEN + 'User Input: ' + Style.RESET_ALL + user_input)
        jarvis.execute_methods()
        jarvis.web_search()
        jarvis.morning_protocol()
        jarvis.search_youtube()
        jarvis.art_mode()
        jarvis.check_stop()
        response = jarvis.process_input(user_input)
            
        print(Fore.BLUE + 'Jarvis: ' + Style.RESET_ALL + response)
    else:
        break

        

    jarvis.say(response)
    
    
    
    



