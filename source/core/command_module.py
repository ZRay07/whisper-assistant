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
from tkinter import *
import jellyfish
import winsound # for creating beeps
import pyttsx3  # for text to speech if needed (ex: says begin recording)
import string
import json
import os
from word2number import w2n
import threading

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#1080 675
class operations:   #audio beep functions
    def __init__(self):
        self.current_window =" "
        self.session_id = " "
        self.driver = webdriver.Firefox()
    def beepgood(self):
        winsound.Beep(1000, 250)
        winsound.Beep(1500, 250)

    def beepbad(self):
        winsound.Beep(1000, 250)
        winsound.Beep(500, 250)

    #example text to speech function
    def tts():
        engine = pyttsx3.init() # initialize
        engine.setProperty('rate', 100) # adjust settings (in this case speech rate)
        engine.say("Begin recording") # what engine will say (feed prediction into this?)
        engine.runAndWait() # runs engine until 'sentence' is over

    # User voice input has been split by word
    # If user says "open application" -> the if statement will be entered which will prompt for an app name
    #   else if user says "open application spotify" or "open spotify" -> the command will run with appName being last word spoken
    def handleApplicationAction(appName, action):
        try:
            if appName in VALID_APPS:
                if action == "open":
                    AppOpener.open(appName, throw_error = True)
                elif action == "close":
                    AppOpener.close(appName, throw_error = True)
                else:
                    print("Invalid action: ", action)
                    return False
                return f"{action} {appName} successful."
            
            else:
                print("Invalid application name: ", appName)
                return f"{action} {appName} NOT successful"
            
        except Exception as e:
            print(f"Error occured while {action}ing the application: ", str(e))
            return f"{action} {appName} NOT successful"


    def convertToInt(self,stringValue):
        try:
            integerValue = int(stringValue)  # Attempt to convert the string to an integer
            return integerValue  # Return the converted integer value
        except ValueError:
            # Conversion failed, input is not a numeric value
            try:
                return self.convertWordToInt(stringValue)  # If input is a string representation, this function will handle it
            
            except Exception as e:
                print(f"Error: {e}")
                return None # Return None to indicate the failure to convert

    def convertWordToInt(self, stringValue):
        try:
            if isinstance(stringValue, int):
                return stringValue
            elif isinstance(stringValue, str):
                # Convert word representation of number to integer
                # For example: "Ten" becomes 10
                try:
                    return w2n.word_to_num(stringValue)
                except ValueError:
                    print(f"Invalid number word: {stringValue}")
                    return None
            else:
                raise TypeError
        except TypeError as e:
            print("Only integers or number strings are allowed", str(e))
            return None

    def handleScrollAction(scrollAmount, direction):
        try:        
            if direction == "up":
                print(f"Scrolling up by {scrollAmount} clicks")
                pyautogui.scroll(scrollAmount)
            elif direction == "down":
                print(f"Scrolling down by {scrollAmount} clicks")
                pyautogui.scroll(-scrollAmount)
            else:
                raise ValueError(f"Invalid scroll direction: {direction}")
            
            return f"Scrolled {direction} by {scrollAmount} click(s)"

        except Exception as e:
            print(f"Error occured during scrolling: {e}")
            return False

    # The input to this function [volChoice] can be a number, or it can simply be volume
    #   The input comes from the output of the Whisper speech recognition module
    #   So a user may say "set volume" or "set volume to 80"
    #   if the user says "set volume", the function should prompt the user and record an audio clip to get the number they'd like to set their volume to
    #   if the user says "set volume to 80", the function should automatically set the volume to 80 without prompting again
    def setVolume(volChoice, decibel):
        try:
            volume.SetMasterVolumeLevel(decibel, None)
            print(f"Setting volume to {volChoice}")
            return f"Successfully set volume to {volChoice}"

        except Exception as e:
            print(f"Error occured while setting volume: {str(e)}")
            return False


    # The inputs to this function are: [fname lname], [email], and [domain]
    def addContact(self,name, email, domain):

        # TO-DO: Create error handling to ensure a proper domain name is passed (gmail, outlook, etc.)
        try:
            account = {
                "name" : name,
                "email" : email,
                "domain": domain, 
            }
            with open("source/contact_list.txt", "a") as f:
                f.write(account.get("name") + " " + account.get("email") + " " + account.get("domain") + "\n")

            return f"Successfully added {name} {email}@{domain} to contact list"

        except Exception as e:
            print(f"Error adding {name} to contact list: {e}")

    def pull_contact(self, string):
        found = True
        with open("source/my_account.txt", "r") as f:
            contacts = f.readlines()

            for line in contacts:
                extr = line.partition(" ")
                first_name = extr[0]
                extr_2 = extr[2].partition(" ")
                last_name = extr_2[0]
                extr_3 = extr_2[2].partition(" ")
                email = extr_3[0]
                domain = extr_3[2]
                try:
                    if (first_name + " " + last_name == string):
                        contact = {
                            'name' : first_name + " " + last_name,
                            'email' : email , 
                            'domain' : domain
                        }
                    else: 
                        found = False
                except Exception as e:
                    print((f"Unable to locate contact in list: {e}"))
                #copy string until second " " is found 
                #compare with user input
                #If same pull the info from the line and save as dict
        return found, contact.get('email'), contact.get('domain')


    def account_info_in(self):
        with open("source/my_account.txt", "r") as f:
            contacts = f.readlines()
            for line in contacts:
                #extr is a tuple that contains the 1st word, a space, then the rest
                extr = line.partition(" ")
                first_name = extr[0]
                extr_2 = extr[2].partition(" ")
                last_name = extr_2[0]
                extr_3 = extr_2[2].partition(" ")
                email = extr_3[0]
                extr_4 = extr_3[2].partition(" ")
                domain = extr_4[0]
                extr_5 = extr_4[2]
                password = extr_5
                contact = {
                        'name' : first_name + " " + last_name,
                        'email' : email , 
                        'domain' : domain,
                        'password' : password
                    }
        return contact.get('name'), contact.get('email'), contact.get('domain'), contact.get('password')

    def google_search(self):
        microphone.record(10)
        prediction = whisper.use_model(RECORD_PATH)
        driver = webdriver.Firefox()

        #so the pages have time to load 
        wait = WebDriverWait(driver, 30)
        #Go to google
        driver.get("https://www.google.com/")
        
        #Find the search bar and enter what the user wants to search
        ele = wait.until(EC.element_to_be_clickable((By.ID, "APjFqb")))
        ele.send_keys(prediction)
        ele.send_keys(Keys.RETURN)
        time.sleep(2)
        #ele.click()


    def sign_in(self):
        name, email, domain, password = self.account_info_in()
       

        #so the pages have time to load 
        wait = WebDriverWait(self.driver, 30)

        self.driver.get("https://outlook.live.com/owa/")
        
        #SPECIFY WINDOW OPENS AT MAX SIZE
        self.driver.maximize_window()
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
        #user = "sherpaemail361@gmail.com"
        el1.send_keys(email + "@" + domain + ".com" )

        el1.send_keys(Keys.RETURN)
        time.sleep(2)
        #keyword = "geeksforgeeks"
        el2 = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
        el2.send_keys(password)
        el2.send_keys(Keys.RETURN)
        time.sleep(2)
        el4 = wait.until(self.driver.find_element(By.ID,("idSIButton9"))) 
        el4.click()
       #//*[@id="idSIButton9"]
       #//*[@id="idSIButton9"]
        #elements = driver.find_elements(By.CLASS_NAME, "method-select-chevron")
        #This for loop helped identify which element to click
        #for e in elements:
        #    print(e)
        #elements[3].click()
        #time.sleep(15)

        #el5 = wait.until(EC.presence_of_element_located((By.ID,"trust-browser-button")))
        #el5.click()

        #Find the yes button
        #elements2 = wait.until(EC.presence_of_element_located((By.ID,"idSIButton9")))
        #elements2.click()

        #The lines below are meant to start a new email but the id is incorrect - fix later
        #el4 = wait.until(EC.presence_of_element_located((By.ID, "id__248")))
        #el4.click()

    # This function moves the mouse cursor down to the Windows search bar in bottom left and clicks
    #   If the last word of the string was document:
    #       The user is prompted for a document name
    #   Otherwise:
    #       it searches for a document with the document name being whatever comes after 'document' in the string
        self.current_window = self.driver.current_window_handle
        print(self.current_window)
        return self.current_window
    

    def searchForDocument(docChoice):
        try:
            docChoice = "Document: " + docChoice

            # Move cursor to search bar
            pyautogui.click(120, 1065, duration = 1)
            time.sleep(0.2)

            # Type in document name and press enter
            pyautogui.typewrite(docChoice, interval = 0.2)
            pyautogui.press('enter')
            return f"Successful search for {docChoice}"
        
        except Exception as e:
            print(f"Error occured while searching for document: {e}")
            return False
# end class definition        



# For closing applications, we want to remove some essential windows services 
#   to ensure the user does not close programs essential for their OS to function correctly
ESSENTIAL_SERVICES = ["event viewer", "task scheduler", "windows powershell ise", "system configuration",
                        "run", "task manager", "windows memory diagnostic", "windows administrative tools",
                        "control panel", "windows memory diagnostic", "system information", "file explorer",
                        "windows powershell ise x", "iscsi initiator", "component services", "services", "this pc"]

def removeEssentialServices(essentialServices):
    removedApps = []
    for essentialService in essentialServices:
        try:
            VALID_APPS.remove(essentialService)
            removedApps.append(essentialService)
        except KeyError:
            print(f"App '{essentialService}' does not exist in the valid apps list.")

    if removedApps:
        print("Successfully removed the following apps: ")
        for appName in removedApps:
            print(f"- {appName}")  


# This function will generate a list of all the apps on users pc and store it in a json file
# Its used to check for errors in open/close application methods
def loadValidApps():
    try:
        with open("data/app_data.json") as json_file:
            data = json.load(json_file)
            return set(data.keys())
    except Exception as e:
        print("Error occured while loading valid app names: ", str(e))
        return False
    

# This if statement executes if apps are not already saved to a file
if os.path.exists("data/app_data.json"):
    VALID_APPS = loadValidApps()
else:
    AppOpener.mklist(path = "data")
    VALID_APPS = loadValidApps()
    
if __name__ == "__main__":
    print("This should only run if called from cmd line")
    