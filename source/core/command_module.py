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

# Initialize text to speech so that it can be used in all functions (if needed)
engine = pyttsx3.init() # initialize
engine.setProperty('rate', 100) # adjust settings (in this case speech rate)

# Below are what is needed for commands to say words
# engine.say("word") # -> what engine will say (feed prediction into this? so that it can read back what the program heard?)
# engine.runAndWait() # -> runs engine until 'sentence' is over


# Audio beep functions
def beepgood(): # used for successful recognition and execution of commands
    winsound.Beep(1000, 250)
    winsound.Beep(1500, 250)

def beepbad():  # used for unsuccessful recognition and execution of commands
    winsound.Beep(1000, 250)
    winsound.Beep(500, 250)

def beepcountdown(): # countdown sequence
    winsound.Beep(1200, 1000)
    winsound.Beep(1200, 1000)
    winsound.Beep(1250, 1000)

def beeprecord(): # used to indicate when recording starts
    winsound.Beep(1500, 250)

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


def convertToInt(stringValue):
    try:
        integerValue = int(stringValue)  # Attempt to convert the string to an integer
        return integerValue  # Return the converted integer value
    except ValueError:
        # Conversion failed, input is not a numeric value
        try:
            return convertWordToInt(stringValue)  # If input is a string representation, this function will handle it
        
        except Exception as e:
            print(f"Error: {e}")
            return None # Return None to indicate the failure to convert

def convertWordToInt(stringValue):
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
def addContact(name, email, domain):

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

def pull_contact(string):
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
            if (first_name + " " + last_name == string):
                contact = {
                    'name' : first_name + " " + last_name,
                    'email' : email , 
                    'domain' : domain
                }
            
            #copy string until second " " is found 
            #compare with user input
            #If same pull the info from the line and save as dict
    return contact.get('name'), contact.get('email'), contact.get('domain')


def account_info_in():
    with open("source/my_account.txt", "r") as f:
         contacts = f.readlines()
         for line in contacts:
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

def google_search():
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

def Full_send(url, session_id):
    #GOING TO USE INPUTS TO WORK IN SAME BROWSER THAT EMAIL SIGN IN MAKES
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 30)
    ele = wait.until(EC.element_to_be_clickable((By.LABEL, "New mail")))
    ele.click()
    #WRITING IN DUMMY CODE DO NOT USE FOR NOW

def sign_in():
    name, email, domain, password = account_info_in()
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
    passwerd = "Dummypassword"
    el2.send_keys(passwerd)
    el2.send_keys(Keys.RETURN)
    ele3 = wait.until(EC.presence_of_element_located((By.TYPE, "submit")))
    ele3.click()
    #THE BELOW CODE WAS TO BYPASS @ FACTOR AUTHENTICATION
    #el3 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button--link"))) 
    #el3.click()
    #time.sleep(2)
    #el4 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "method-select-chevron"))) 
    #el4.click()

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
    # IN ORDER TO CONTINUE WORKING ON THE SAME WINDOW WE NEED TO PASS THE NEXT FUNCTION THE SESSION ID AND URL
    url = driver.command_executor._url
    session_id = driver.session_id
    return url, session_id


class sub_window_int:
    def __init__(self):
        self.sub_window = Tk()
        self.sub_window.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.sub_window.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.sub_window.config(bg = "skyblue")     # set the background color
        self.sub_window.geometry("1100x700+480+200")
        self.command_frame()
        self.transcribe_frame()
        self.sub_window = mainloop()
    #There will be one frame for commands (left)
    def command_frame(self):
        self.command_frame = Frame(self.sub_window, width = 315, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.command_frame.grid(row = 0, column = 0, padx = 10, pady = 10)       # Places the frame onto the window
        self.mountainImage = PhotoImage(file = "source/core/images/mountain3.gif")
        self.small_image = self.mountainImage.subsample(3 , 3)
        Label(self.command_frame, image = self.small_image).grid(row = 0, column = 0, padx = 10, pady = 10)

        # Label the left hand frame
        self.cmd_label = Label(self.command_frame, text = "Speech Commands", font = "times 18", bg = "white")
        self.cmd_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        #Add the buttons
        self.add_contact_button = Button(self.cmd_bar, text = "Add Contact", command = self.add_contact, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)

        #Place the buttons
        self.add_contact_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        # Add speech commands below label
        # Use buttons so we can use the GUI
        self.cmd_bar = Frame(self.command_frame, width = 315, height = 300, bg = "white")
        self.cmd_bar.grid(row = 2, column = 0)
    #This frame is for the transcribe box
    def transcribe_frame(self): #(Right)
        self.transcribe_frame = Frame(self.sub_window, width = 750, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.transcribe_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
        #makes sure the frame doesn't change shape to fit the widget
        self.transcribe_frame.grid_propagate(False)
    def add_contact(self):
         confirm = False
         while confirm == False:
            self.setlabel("Please give me their name.")
            self.update_screen()
            microphone.record(3)
            self.pred_name = whisper.use_model(RECORD_PATH)
            self.setlabel("I heard " + self.pred_name + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
            self.update_screen()
            microphone.record(4)
            if_yes1 = whisper.use_model(RECORD_PATH)
            print(if_yes1)
            if (if_yes1 == "Yes" or if_yes1 == "Yes." or if_yes1 == "yes" or if_yes1 == "yes." or if_yes1 == "Yeah." or if_yes1 =="Yeah"):
                confirm = True
                #Stuff
            
                print(if_yes1)
            else: 
                 confirm = False
            while confirm == True:     
                self.setlabel("What is their email?")
                self.update_screen()
                microphone.record(3)
                self.pred_email = whisper.use_model(RECORD_PATH)
                self.pred_email = self.format_email(self.pred_email)
                self.setlabel("I heard " + self.pred_email + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
                self.update_screen()
                microphone.record(4)
                if_yes2 = whisper.use_model(RECORD_PATH)
            
                if(if_yes2 == "Yes" or if_yes2 == "Yes." or if_yes2 == "yes" or if_yes2 == "yes." or if_yes2 == "Yeah." or if_yes2 =="Yeah"):
                        #Have to toggle this to exit the loop
                        confirm = False
                else: 
                        confirm = True
            if(confirm == False):  
                while confirm == False:                                        
                    self.setlabel("What domain does the email belong to?\n (Gmail, outlook, proton, ect..)")
                    self.update_screen()
                    microphone.record(3)
                    self.pred_domain = whisper.use_model(RECORD_PATH)
                    self.setlabel("I heard " + self.pred_domain + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
                    self.update_screen()
                    microphone.record(4)
                    if_yes3 = whisper.use_model(RECORD_PATH)
                    if(if_yes3 == "Yes" or if_yes3 == "Yes." or if_yes3 == "yes" or if_yes3 == "yes." or if_yes3 == "Yeah." or if_yes3 =="Yeah"):
                        self.account = {
                                        "name" : self.pred_name ,
                                        "email" : self.pred_email ,
                                        "domain": self.pred_domain , 
                        }
                        with open("source/contact_list.txt", "a") as f:
                                        f.write(self.account.get("name") + " " + self.account.get("email") + " " + self.account.get("domain") + "\n")
                        confirm = True
                    else: 
                        self.setlabel("Please try again")
                        self.update_screen() 
                        confirm = False
            else:
                    self.setlabel("Please try again")
                    self.update_screen() 
                    confirm = True
    

# This function moves the mouse cursor down to the Windows search bar in bottom left and clicks
#   If the last word of the string was document:
#       The user is prompted for a document name
#   Otherwise:
#       it searches for a document with the document name being whatever comes after 'document' in the string
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


def recordAndUseModel():
    microphone.record(3)
    prediction = whisper.use_model(RECORD_PATH)

    print("We heard " + prediction)

    return prediction

# This if statement executes if apps are not already saved to a file
if os.path.exists("data/app_data.json"):
    VALID_APPS = loadValidApps()
else:
    AppOpener.mklist(path = "data")
    VALID_APPS = loadValidApps()
    
if __name__ == "__main__":

    print("This should only run if called from cmd line")
    