Welcome to my first project shared with the world! As an ongoing effort to provide you with the best virtual assistant experience, I will continue to update this repository with new features, bug fixes, and improvements.

Your feedback is important to me, and I encourage you to share any ideas or suggestions you have for future features. Together, we can make this project even better and more useful to our community.

![Iron Man](ironman.png)
__________________________________________________

# Installation

### A Virtual Environment is NOT recommended for this project
insert relevant API Keys and Info into keys.py file

### Sign up for the weather api and get your longitude and latitude
sign up here https://api.openweathermap.org

find your lat and long here https://www.latlong.net
put them in the relevant place in the keys.py file

### For the wake word to work
Sign up for the picoai api at https://picovoice.ai/

then train your own model using this link https://console.picovoice.ai/ppn (By default i have the Windows (x86_64) version already trained in the wakeword folder)

then copy and paste it in the relevant position in the wakeword.py file

This file will be the one you set to start on bootup 

look in the wakeword.py file and replace my local paths with your locals paths to the same file

## Setting up to run on startup

### For Mac:

1. Open the "Automator" application, which can be found in the "Applications" folder.

2. Choose "Application" as the document type and click "Choose".

3. In the search bar, type "Run Shell Script" and drag the resulting action into the workflow area.

4. In the shell script, type the following command to run the wakeword.py script:

``/usr/bin/python /path/to/wakeword.py``

Replace **/path/to/wakeword.py** with the actual path to the **wakeword.py** script on your computer.

5. Save the workflow as an application by selecting "File" > "Save" and choosing a name and location for the application.

6. Open "System Preferences" > "Users & Groups" > "Login Items" and click the "+" button.

7. Select the application you just created and click "Add".

### For Windows:

1. Press "Windows key + R" to open the "Run" dialog box.

2. Type "shell:startup" and press "Enter" to open the startup folder.

3. Right-click in the folder and select "New" > "Shortcut".

4. In the "Type the location of the item" field, type the following command to run the **wakeword.py** script:

``python C:\path\to\wakeword.py``

Replace **C:\path\to\wakeword.py** with the actual path to the **wakeword.py** script on your computer.

5. Click "Next" and give the shortcut a name, then click "Finish".

### For Linux:

1. Open a terminal window.

2. Type the following command to edit the **rc.local** file:

``sudo nano /etc/rc.local``

Add the following command to the file before the "exit 0" line to run the **wakeword.py** script:

``/usr/bin/python /path/to/wakeword.py &``

Replace **/path/to/wakeword.py** with the actual path to the **wakeword.py** script on your computer.

4. Save the file and exit the editor.

5. Make the rc.local file executable by typing the following command:

``sudo chmod +x /etc/rc.local``

6. Reboot your computer to test if the wakeword.py script runs on startup.

#### All setup!
Just run the wakeword.py file
__________________________________________________

# Project Jarvis

## Features

### Version 1:

- speech recognition
- Davinci model

### Version 2: 

- Ability to reference and keep context from past queries
- Chat-GPT-Turbo model
- Save interactions
- Fetch live weather data

### Version 3: 

- Autonomously create simple apps on command
- Added the abilty to listen to the keyword Jarvis then use Jarvis (can be ran on startup)

### Version 4: 

- Improved the Weather Functionality.
- Implemented Face Detection upon Bootup to personalize user experience.
- Integrated a Mood Detection Feature for more personalized.interactions. Jarvis now listens for keywords such as "mood" and "feeling" to provide relevant responses based on the user's emotional state.
- More message options for greetings upon bootup will randomly choose one.
- Has the ability to give you sentiment on the stock market. By aggregating all of them. Then able to answer any question about the market.

### Version 5:
- Added the Jarvis class to the project, providing a streamlined interface for users to interact with the virtual assistant.
- Improved the functionality of Jarvis, allowing it to perform a variety of tasks, including website lookups, playing YouTube videos, retrieving stock market information, creating art, and executing a morning protocol.
- The morning protocol feature has been implemented, allowing users to customize the website that Jarvis opens upon activation. Simply say "activate morning protocol" to launch the site of your choice.
- Overall, version 5 of the Jarvis project provides a more robust and powerful virtual assistant, capable of performing many tasks to simplify and enhance the user's life. We encourage you to try it out and see how it can help you with your daily tasks.

If you have any ideas on some cool stuff to add i would love the feedback!
- Implement feature to generate stock charts instantly on command and optimize Jarvis to achieve 11x faster performance, enhancing user experience and enabling more efficient analysis of financial data.
__________________________________________________

**Oh, don't forget to follow me on my socials.**

**Instagram**
https://www.instagram.com/tylergbss

**Tiktok**
https://www.tiktok.com/@tylergbbs

**Twitter**
https://twitter.com/tylerbryy 



