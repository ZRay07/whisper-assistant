#from AppOpener import open
#from PIL import Image
#open("matlab r b")
#im = Image.open('C:/Users/cohent1/Pictures/Camera Roll/glass.jfif')
#im.show()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

import AppOpener        # used for opening / closing applications
import pyautogui        # used to control mouse cursor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    # used for audio
from ctypes import cast, POINTER                                # audio
from comtypes import CLSCTX_ALL                                 # audio
from source.core.model_interface import *

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):    

    print("userChoice: " + userChoice)
    print(type(userChoice))

    if (userChoice == "Open application" or "Open app" or "Open application." or "Open app."):        # Open application
        print("\n***Open Application***")
        openApplication()

    elif (userChoice == "Close application" or "close application" or "Close app" or "Close application." or "Close app."):      # Close application
        print("\n***Close Application***")
        closeApplication()

    elif (userChoice == "Scroll up" or "Scroll up."):      # Scroll up
        print("\n***Scroll Up***")
        pyautogui.scroll(10)
            
    elif (userChoice == "Scroll down" or "Scroll down."):    # Scroll down
        print("\n***Scroll Down***")
        pyautogui.scroll(-10)

    elif (userChoice == "Set volume" or "Set volume."):   # Set volume
        print("\n***Set Volume***")
        setVolume()           

    elif (userChoice == "Navigate mouse and keyboard" or "Navigate mouse and keyboard."):
        print("\n***Navigate mouse + keyboard***")

    elif (userChoice == "Sign into email." or "Email sign in." or "Send an email."):    # Email sign in
        print("\n***Email sign-in***") 
        sign_in()       

    elif (userChoice == "Exit"):    # Exit
        print("***Exiting***")

    else:
        print("Try again...")



def openApplication():
    print("\nWhich application would you like to open?")
    print("\t*Word")
    print("\t*Edge")
    print("\t*Spotify")
    print("\t*Discord")

    microphone.record()
    prediction = whisper.use_model(RECORD_PATH)

    print("Opening " + prediction)
    AppOpener.open(prediction)

def closeApplication():
    print("\nWhich application would you like to close?")
    print("\t*Word")
    print("\t*Edge")
    print("\t*Spotify")
    print("\t*Discord")

    microphone.record()
    prediction = whisper.use_model(RECORD_PATH)

    print("Closing " + prediction)
    AppOpener.close(prediction)


def setVolume():
    print("\nWhat volume would you like to set to?")
    print("*** MUST BE AN INCREMENT OF 10 ***")

    microphone.record()
    prediction = whisper.use_model(RECORD_PATH)

    if (prediction == "0"):
        print("Setting volume to 0")
        volume.SetMasterVolumeLevel(-60.0, None)

    elif (prediction == "10"):
        volume.SetMasterVolumeLevel(-33.0, None)
        print("Setting volume to 10")

    elif (prediction == "20"):
        volume.SetMasterVolumeLevel(-23.4, None)
        print("Setting volume to 20")

    elif (prediction == "30"):
        volume.SetMasterVolumeLevel(-17.8, None)
        print("Setting volume to 30")

    elif (prediction == "40"):
        volume.SetMasterVolumeLevel(-13.6, None)
        print("Setting volume to 40")

    elif (prediction == "50"):
        volume.SetMasterVolumeLevel(-10.2, None)
        print("Setting volume to 50")

    elif (prediction == "60"):
        volume.SetMasterVolumeLevel(-7.6, None)
        print("Setting volume to 60")

    elif (prediction == "70"):
        volume.SetMasterVolumeLevel(-5.3, None)
        print("Setting volume to 70")

    elif (prediction == "80"):
        volume.SetMasterVolumeLevel(-3.4, None)
        print("Setting volume to 80")

    elif (prediction == "90"):
        volume.SetMasterVolumeLevel(-1.6, None)
        print("Setting volume to 90")

    elif (prediction == "100"):
        volume.SetMasterVolumeLevel(0, None)
        print("Setting volume to 100")
# end volume control loop 


def sign_in():
    driver = webdriver.Firefox()

    #so the pages have time to load 
    wait = WebDriverWait(driver, 30)

    driver.get("https://outlook.live.com/owa/")
    #time.sleep(3)
    #ele = (driver.find_element(By.LINK_TEXT,"Sign in"))

    #ele.click()
        
    #This is an alternative method
    # Wait for the Sign in link to become available
    ele = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
    ele.click()

    # Wait for the email input field to become available
    el1 = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))


    #email = driver.find_element(By.XPATH, "//form[input/@name='email']")
    #email = driver.find_element(By.XPATH, "//form[@id='loginForm']/input[1]")
    #email = driver.find_element(By.XPATH, "//input[@name='email']")
    #time.sleep(2)
    #el1 = ( driver.find_element(By.NAME, "loginfmt"))
    user = "sherpaemail361@gmail.com"
    el1.send_keys(user)

    el1.send_keys(Keys.RETURN)
    time.sleep(2)
    #keyword = "geeksforgeeks"
    el2 = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
    passwerd = "dummypassword"
    el2.send_keys(passwerd)
    el2.send_keys(Keys.RETURN)
    el3 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button--link"))) 
    el3.click()
    time.sleep(2)
    #el4 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "method-select-chevron"))) 
    #el4.click()

    elements = driver.find_elements(By.CLASS_NAME, "method-select-chevron")
    #This for loop helped identify which element to click
    #for e in elements:
    #    print(e)
    elements[3].click()
    time.sleep(15)

    el5 = wait.until(EC.presence_of_element_located((By.ID,"trust-browser-button")))
    el5.click()

    #Find the yes button
    elements2 = wait.until(EC.presence_of_element_located((By.ID,"idSIButton9")))
    elements2.click()

    #The lines below are meant to start a new email but the id is incorrect - fix later
    #el4 = wait.until(EC.presence_of_element_located((By.ID, "id__248")))
    #el4.click()

