from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyttsx3
import time


engine = pyttsx3.init()
engine.setProperty('rate', 195) 


def play_youtube_video(query, wait_time=300):
    
    # initialize the webdriver
    driver = webdriver.Chrome()

    # navigate to Google
    driver.get("https://www.google.com")

    # find the search box and enter the search query
    search_box = driver.find_element(By.NAME,"q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # wait for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'youtube.com')]")))

    # find the first YouTube video link and click it
    youtube_link = driver.find_element(By.XPATH,"//a[contains(@href,'youtube.com')]")
    youtube_link.click()

    # wait for the "Skip Ad" button to appear and click it, or print a message if it can't be skipped
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button-text")))
        skip_button = driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-text")
        skip_button.click()
        engine.say(f"I skipped the ad for you")
        engine.runAndWait()
    except TimeoutException:
        engine.say(f"it appears that we have come across an unskippable advertisement. Unfortunately, our attempts to bypass it have been unsuccessful at this time.")
        engine.runAndWait()
        

    # wait for the video to finish playing
    time.sleep(wait_time)

    # close the webdriver
    driver.quit()


