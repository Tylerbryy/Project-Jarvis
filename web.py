from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyttsx3
import time
import pyaudio
import numpy as np

# Set up the audio processing parameters
CHUNK = 1024
RATE = 44100
THRESHOLD = 1500
CLAP_THRESHOLD = 15


# Create an instance of PyAudio
audio = pyaudio.PyAudio()
engine = pyttsx3.init()
def detect_claps(driver):
    
    # Open the microphone
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Record audio until a clap is detected
    clap_count = 0
    while True:
            
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-time-duration")))
        duration_element = driver.find_element(By.CLASS_NAME, "ytp-time-duration")
        duration = duration_element.get_attribute("innerText")
        current_time_element = driver.find_element(By.CLASS_NAME, "ytp-time-current")
        current_time = current_time_element.get_attribute("innerText")
        if duration <= current_time:
            print("Video finished playing")
            engine.say("Video stopped")
            engine.runAndWait()
            return True
        # Read the audio data
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

        # Check if the audio data exceeds the threshold
        if np.max(data) > THRESHOLD:
            clap_count += 1
            
            print(f"clap: {clap_count}")
            # Stop the video if the clap threshold is reached
            if clap_count == CLAP_THRESHOLD:
                print("clapped")
                engine.say("Video stopped")
                engine.runAndWait()
                return True

        # Reset the clap count if there is a long period of silence
        elif clap_count > 0:
            
            clap_count = 0

def play_youtube_video(query):
    driver = webdriver.Chrome()
    # Initialize the webdriver

    # Navigate to Google
    driver.get("https://www.google.com")

    # Find the search box and enter the search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'youtube.com')]")))

    # Find the first YouTube video link and click it
    youtube_link = driver.find_element(By.XPATH, "//a[contains(@href,'youtube.com')]")
    youtube_link.click()
    
    # Wait for the video to start playing
    time.sleep(5)
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button-text")))
        skip_button = driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-text")
        skip_button.click()
        engine.say(f"I skipped the ad for you")
        engine.runAndWait()
    except TimeoutException:
        engine.say(f"it appears that we have come across an unskippable advertisement.")
        engine.runAndWait()


    # Detect claps to stop the video
    if detect_claps(driver):
        print("Stopping video...")
        driver.execute_script("document.getElementsByClassName('ytp-play-button')[0].click()")



    # Close the webdriver
    driver.quit()



