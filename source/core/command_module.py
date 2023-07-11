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
import keyboard
from tkinter import *
import jellyfish
import winsound # for creating beeps
import pyttsx3  # for text to speech if needed (ex: says begin recording)
import string
import json
import os
from word2number import w2n

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Initialize text to speech so that it can be used in all functions
engine = pyttsx3.init() # initialize
engine.setProperty('rate', 100) # adjust settings (in this case speech rate)

# Below are what is needed for commands to say words
# engine.say("word") # -> what engine will say (feed prediction into this?)
# engine.runAndWait() # -> runs engine until 'sentence' is over


# Audio beep functions
def beepgood():
    winsound.Beep(1000, 250)
    winsound.Beep(1500, 250)

def beepbad():
    winsound.Beep(1000, 250)
    winsound.Beep(500, 250)

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):
    # make the string all lower case to help with similarity (want to focus solely on matching keywords)
    userChoice = userChoice.lower()
    userChoiceSplit = userChoice.split()
    
    if (jellyfish.jaro_winkler_similarity(userChoiceSplit[0], "open") > 0.85):        # Open application
        beepgood()
        print("\n***Open Application***")
        engine.say("Open application") 
        engine.runAndWait()
        appName = userChoiceSplit[-1].rstrip(string.punctuation).lower()
        handleApplicationAction(appName, "open")


    elif (jellyfish.jaro_winkler_similarity(userChoiceSplit[0], "close") > 0.85):      # Close application
        beepgood()
        print("\n***Close Application***")
        engine.say("Close application") 
        engine.runAndWait()
        appName = userChoiceSplit[-1].rstrip(string.punctuation).lower()
        handleApplicationAction(appName, "close")


    elif (jellyfish.jaro_winkler_similarity(userChoiceSplit[0] + " " + userChoiceSplit[1], "scroll up") > 0.9):      # Scroll up
        beepgood()
        print("\n***Scroll Up***")
        engine.say("Scroll up") 
        engine.runAndWait()
        scrollAmount = userChoiceSplit[-1]
        handleScrollAction(scrollAmount, "up")

            
    elif (jellyfish.jaro_winkler_similarity(userChoiceSplit[0] + " " + userChoiceSplit[1], "Scroll down") > 0.9):    # Scroll down
        beepgood()
        print("\n***Scroll Down***")
        engine.say("Scroll down") 
        engine.runAndWait()
        scrollAmount = userChoiceSplit[-1]
        handleScrollAction(scrollAmount, "down")


    elif (jellyfish.jaro_winkler_similarity(userChoiceSplit[0] + " " + userChoiceSplit[1], "Set volume") > 0.85):   # Set volume
        beepgood()
        print("\n***Set Volume***")
        engine.say("Set volume") 
        engine.runAndWait()
        volChoice = userChoiceSplit[-1].rstrip(string.punctuation).lower()
        setVolume(volChoice)           


    elif (jellyfish.jaro_winkler_similarity(userChoice, "Navigate mouse and keyboard") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Mouse Control") > 0.85):
        beepgood()
        print("\n***Navigate mouse + keyboard***")
        engine.say("Navigate mouse and keyboard") 
        engine.runAndWait()
        mouseGrid()

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Email sign in") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Send an email") > 0.85):    # Email sign in
        beepgood()
        print("\n***Email sign-in***")
        engine.say("Email sign in") 
        engine.runAndWait()
        sign_in()       

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Exit") > 0.85):    # Exit
        beepgood()
        engine.say("Exiting") 
        engine.runAndWait()
        print("***Exiting***")

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Google search") > 0.85):
        beepgood()
        engine.say("Searching now") 
        engine.runAndWait()
        print("\nSearching now...\n")
        google_search()
   # elif(jellyfish.jaro_winkler_similarity(userChoice, "New email") > 0.85):
   #     write_email(url,session_id)
    elif(jellyfish.jaro_winkler_similarity(userChoice, "Email functions") > 0.85): 
        sub_window_int()
    else:
        beepbad()
        engine.say("Try again") 
        engine.runAndWait()
        print("Try again...")

# This function is used when we need to prompt the user for additional voice inputs
# Used for getting application names, scroll amounts, volume levels, etc.
# If removePunctuation is true when you call it, it removes trailing punctuation.
# If makeLowerCase is true when you call it, it makes the output string lowercase
def promptUser(recordDuration, removePunctuation, makeLowerCase):
    try:
        microphone.record(recordDuration)
        userInput = whisper.use_model(RECORD_PATH)

        if removePunctuation:
            userInput = userInput.rstrip(string.punctuation)

        if makeLowerCase:
            userInput = userInput.lower()

        return userInput
    
    except Exception as e:
        beepbad()
        print("Error occured during recording: ", str(e))
        engine.say("Error occured during recording.") 
        engine.runAndWait()
        return False

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
    if (appName in {"application", "app"}):
        while True:
            print(f"\nWhich application would you like to {action}?")
            print("\t- Word")
            print("\t- Edge")
            print("\t- Spotify")
            print("\t- Discord")
            time.sleep(2)

            appName = promptUser(3, True, True)

            if appName in VALID_APPS:
                break   # Valid app name provided, exit the while loop
            else:
                print("Invalid application name. Please try again")

    # Remove essential services from VALID_APPS list so they aren't accessible to close
    if action == "close":
        removeEssentialServices(ESSENTIAL_SERVICES)

    try:
        if appName in VALID_APPS:
            if action == "open":
                AppOpener.open(appName, throw_error = True)
            elif action == "close":
                AppOpener.close(appName, throw_error = True)
            else:
                print("Invalid action: ", action)
                return False
            return True
        else:
            print("Invalid application name: ", appName)
            return False
    except Exception as e:
        print(f"Error occured while {action}ing the application: ", str(e))
        return False


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
    # Remove any trailing punctuation marks
    scrollAmount = scrollAmount.rstrip(string.punctuation)

    while True:
        try:
            if scrollAmount in {"up", "down"}:
                scrollAmount = 100  # Default scroll amount if user doesn't specify a number
            else:
                scrollAmount = convertToInt(scrollAmount) # Convert string representation of number to integer
                
            if scrollAmount is None  or scrollAmount < 0 or scrollAmount > 1000:
                print(f"Invalid scroll amount: {scrollAmount}. Valid scroll amounts are between 0 and 1000.")
                time.sleep(2)
                scrollAmount = promptUser(3, True, True)   # Prompt the user again for input
                continue    # Restart the loop to revalidate the new input (if statement to check value in range)
            
            if direction == "up":
                print(f"Scrolling up by {scrollAmount} clicks")
                pyautogui.scroll(scrollAmount)
            elif direction == "down":
                print(f"Scrolling down by {scrollAmount} clicks")
                pyautogui.scroll(-scrollAmount)
            else:
                raise ValueError(f"Invalid scroll direction: {direction}")
            
            return True
        
        except ValueError as ve:
            print("Invalid scroll amount. Valid scroll amounts are between 0 and 1000.")
            time.sleep(2)
            scrollAmount = promptUser(2, True, True)

        except Exception as e:
            print(f"Error occured during scrolling: {e}")
            return False

# The input to this function [volChoice] can be a number, or it can simply be volume
#   The input comes from the output of the Whisper speech recognition module
#   So a user may say "set volume" or "set volume to 80"
#   if the user says "set volume", the function should prompt the user and record an audio clip to get the number they'd like to set their volume to
#   if the user says "set volume to 80", the function should automatically set the volume to 80 without prompting again
def setVolume(volChoice):
    # Actual volume levels and corresponding decibel levels
    volumeMapping = {
        0: -60.0,
        10: -33.0,
        20: -23.4,
        30: -17.8,
        40: -13.6,
        50: -10.2,
        60: -7.6,
        70: -5.3,
        80: -3.4,
        90: -1.6,
        100: 0
    }

    try:
        while True:
            if (volChoice == "volume"):
                # If the input is only volume, prompt user for a desired volume level
                print("\nWhat volume would you like to set to?")
                print("*** MUST BE AN INCREMENT OF 10 ***")
                time.sleep(2)

                volChoice = promptUser(3, True, True)

            volChoice = convertToInt(volChoice) # Convert string representation of number to integer
            
            if volChoice in volumeMapping:
                volume.SetMasterVolumeLevel(volumeMapping[volChoice], None) # Grabs the decibel value from volume mapping dict
                print(f"Setting volume to {volChoice}")
                return True

            # Prompt the user again for a valid volume value
            print(f"\nInvalid volume value: {volChoice}. Valid volume levels are increments of 10 between 0 and 100.")
            time.sleep(2)

            volChoice = promptUser(3, True, True)

    except Exception as e:
        print(f"Error occured while setting volume: {str(e)}")
        return False

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
    

class mouseGrid():
    def __init__(self):
        self.userChoiceFlag = 0

        # Open a new window
        self.mouseGrid = Tk()

        # Make this window transparent
        self.mouseGrid.attributes("-alpha", 0.3, "-fullscreen", TRUE)

        #mouseGrid.geometry("1919x1079")

        self.screenHeight = self.mouseGrid.winfo_screenheight()
        self.screenWidth = self.mouseGrid.winfo_screenwidth()

        # These variables store the center position's of the color grid
        self.redCenter = [self.screenWidth / 3 / 2, self.screenHeight / 3 / 2, 1]
        self.greenCenter = [self.screenWidth / 3 / 2, self.screenHeight / 3 / 2 + self.screenHeight / 3, 1]
        self.blueCenter = [self.screenWidth / 3 / 2, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3, 1]
        self.purpleCenter = [self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2, 1]
        self.yellowCenter = [self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2 + self.screenHeight / 3, 1]
        self.whiteCenter = [self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3, 1]
        self.blackCenter = [self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2, 1]
        self.orangeCenter = [self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2 + self.screenHeight / 3, 1]
        self.pinkCenter = [self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3, 1]

        self.drawColorGrid()

        self.mouseGrid.mainloop()

        # Make 9 frames (3 * 3 grid)
        # One for each portion of the grid
    def drawColorGrid(self):
        self.redFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "red")
        self.redFrame.grid(row = 0, column = 0)
        self.redFrame.grid_propagate(False)

        self.greenFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "green")
        self.greenFrame.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.greenFrame.grid_propagate(False)

        self.blueFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "blue")
        self.blueFrame.grid(row = 2, column = 0, padx = 0, pady = 0)
        self.blueFrame.grid_propagate(False)

        self.purpleFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "purple")
        self.purpleFrame.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.purpleFrame.grid_propagate(False)

        self.yellowFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "gold")
        self.yellowFrame.grid(row = 1, column = 1, padx = 0, pady = 0)
        self.yellowFrame.grid_propagate(False)

        self.whiteFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "white")
        self.whiteFrame.grid(row = 2, column = 1, padx = 0, pady = 0)
        self.whiteFrame.grid_propagate(False)

        self.blackFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "black")
        self.blackFrame.grid(row = 0, column = 2, padx = 0, pady = 0)
        self.blackFrame.grid_propagate(False)

        self.orangeFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "orange red")
        self.orangeFrame.grid(row = 1, column = 2, padx = 0, pady = 0)
        self.orangeFrame.grid_propagate(False)

        self.pinkFrame = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "deep pink")
        self.pinkFrame.grid(row = 2, column = 2, padx = 0, pady = 0)
        self.pinkFrame.grid_propagate(False)

        self.inputBox = Text(self.blackFrame, height = 1, width = 10, border = 2, relief = "solid")
        self.inputBox.grid(row = 0, column = 0,sticky = NE)

        self.submit_button = Button(self.blackFrame, text = "Submit", command = self.getUserChoice, border = 2, relief = "solid")
        self.submit_button.grid(row = 1, column = 0, sticky = NE)

    def deleteColorGrid(self):
        self.redFrame.destroy()
        self.greenFrame.destroy()
        self.blueFrame.destroy()
        self.purpleFrame.destroy()
        self.yellowFrame.destroy()
        self.whiteFrame.destroy()
        self.blackFrame.destroy()
        self.orangeFrame.destroy()
        self.pinkFrame.destroy()

    def getUserChoice(self):
        self.inputBoxChoice = self.inputBox.get(1.0, "end-1c")

        if (self.inputBoxChoice == "Record"):
            self.userChoice = recordAndUseModel()
            self.displaySubgrid()
            

        elif (self.inputBoxChoice == "Red" or self.inputBoxChoice == "Green" or self.inputBoxChoice == "Blue" or
              self.inputBoxChoice == "Purple" or self.inputBoxChoice == "Yellow" or self.inputBoxChoice == "White" or
              self.inputBoxChoice == "Black" or self.inputBoxChoice == "Orange" or self.inputBoxChoice == "Pink"):
            self.displaySubgrid()

        elif (self.inputBoxChoice == "Destroy"):
            self.deleteColorGrid()

            self.mouseGrid.update_idletasks()
            self.mouseGrid.update()

            time.sleep(5)

            self.drawColorGrid()

            self.mouseGrid.update_idletasks()
            self.mouseGrid.update()
        
        else:
            print("Enter a correct input")

    def displaySubgrid(self):
        self.displayFlag = 0

        if (jellyfish.jaro_winkler_similarity(self.userChoice, "Red") > 0.7):      # top left
            self.subgrid = Canvas(self.redFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.redCenter[0], self.redCenter[1], self.redCenter[2])
            self.displayFlag = 1
        
        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Green") > 0.85):  # middle left
            self.subgrid = Canvas(self.greenFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.greenCenter[0], self.greenCenter[1], self.greenCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Blue") > 0.85):   # bottom left
            self.subgrid = Canvas(self.blueFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.blueCenter[0], self.blueCenter[1], self.blueCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Purple") > 0.85): # top center
            self.subgrid = Canvas(self.purpleFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.purpleCenter[0], self.purpleCenter[1], self.purpleCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Yellow") > 0.85): # center
            self.subgrid = Canvas(self.yellowFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.yellowCenter[0], self.yellowCenter[1], self.yellowCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "White") > 0.85):  # bottom center
            self.subgrid = Canvas(self.whiteFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.whiteCenter[0], self.whiteCenter[1], self.whiteCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Black") > 0.85):  # top right
            self.subgrid = Canvas(self.blackFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.blackCenter[0], self.blackCenter[1], self.blackCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Orange") > 0.85):   # middle right
            self.subgrid = Canvas(self.orangeFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.orangeCenter[0], self.orangeCenter[1], self.orangeCenter[2])
            self.displayFlag = 1

        elif (jellyfish.jaro_winkler_similarity(self.userChoice, "Pink") > 0.7):   # bottom right
            self.subgrid = Canvas(self.pinkFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.pinkCenter[0], self.pinkCenter[1], self.pinkCenter[2])
            self.displayFlag = 1

        if (self.displayFlag):
            print("Displaying subgrid...")

            # Draw horizontal lines
            self.subgrid.create_line(0, self.screenHeight / 9, self.screenWidth / 3, self.screenHeight / 9, width = 5)  
            self.subgrid.create_line(0, self.screenHeight * 2 / 9, self.screenWidth / 3, self.screenHeight * 2 / 9, width = 5)

            # Draw vertical lines
            self.subgrid.create_line(self.screenWidth / 9, 0, self.screenWidth / 9, self.screenHeight / 3, width = 5)
            self.subgrid.create_line(self.screenWidth * 2 / 9, 0, self.screenWidth * 2 / 9, self.screenHeight / 3, width = 5)

            # Place the canvas onto user choice location
            self.subgrid.grid(padx = 0, pady = 0)

            self.mouseGrid.update_idletasks()
            self.mouseGrid.update()

            self.dynamicInstructionText = StringVar()
            

            if (self.userChoice == "Red." or self.userChoice == "Red" or self.userChoice == "red"):
                self.dynamicInstruction_label = Label(self.blackFrame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

            else:
                self.dynamicInstruction_label = Label(self.redFrame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

            self.dynamicInstructionText.set("If you'd like to get more specific, say yes. Otherwise, you can make an action where your cursor is.")
            
            self.mouseGrid.update_idletasks()
            self.mouseGrid.update()

            print("\nSay 'Get more specific' to specify a subgrid.")
            time.sleep(3)

            self.userChoice = recordAndUseModel()

            if (self.userChoice == "Get more specific." or self.userChoice == "Get more specific" or self.userChoice == "get more specific"):
                self.moveToInnerPosition()
                self.mouseOrKeyboardAction()

            else:
                self.mouseOrKeyboardAction()

        else:
            print("Incorrect input. Say the color which you'd like your cursor to be in...")



    def moveToInnerPosition(self):
        print("\nSay 1-9 to move to an inner grid position")
        print("OR say EXIT or CANCEL if the cursor is where you want it.")

        time.sleep(5)

        self.currentMouseX, self.currentMouseY = pyautogui.position()   # Get the XY position of the mouse.

        self.userChoice = recordAndUseModel()

        if (self.userChoice == "1"):
            print("Moving to 1...")
            pyautogui.move(-(self.screenWidth / 9), -(self.screenHeight / 9), 0.5)

        elif (self.userChoice == "2"):
            print("Moving to 2...")
            pyautogui.move(0, -(self.screenHeight / 9), 0.5)

        elif (self.userChoice == "3"):
            print("Moving to 3...")
            pyautogui.move((self.screenWidth / 9), -(self.screenHeight / 9), 0.5)

        elif (self.userChoice == "4"):
            print("Moving to 4...")
            pyautogui.move(-(self.screenWidth / 9), 0, 0.5)

        # 5 is the center

        elif (self.userChoice == "6"):
            print("Moving to 6...")
            pyautogui.move((self.screenWidth / 9), 0, 0.5)

        elif (self.userChoice == "7"):
            print("Moving to 7...")
            pyautogui.move(-(self.screenWidth / 9), (self.screenHeight / 9), 0.5)

        elif (self.userChoice == "8"):
            print("Moving to 8...")
            pyautogui.move(0, (self.screenHeight / 9), 0.5)

        elif (self.userChoice == "9"):
            print("Moving to 9...")
            pyautogui.move((self.screenWidth / 9), (self.screenHeight / 9), 0.5)

        elif (self.userChoice == "Exit." or self.userChoice == "exit" or self.userChoice == "Cancel." or self.userChoice == "cancel"):
            print("Cancelling...")

    def mouseOrKeyboardAction(self):
        self.mouseOrKeyboardFlag = 0

        while(self.mouseOrKeyboardFlag == 0):

            print("\n***Options***")
            print("* Left click, double click, right click")
            print("* Type something, key press")
            print("* Get more specific")
            print("* I'm done")

            time.sleep(5)

            self.userChoice = recordAndUseModel()

            if (self.userChoice == "Click." or self.userChoice == "click" or self.userChoice == "Left click." or self.userChoice == "left click"): # or self.userChoice == "you"):
                self.mouseGrid.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.leftClick()

            elif (self.userChoice == "Double click." or self.userChoice == "Double click" or self.userChoice == "double click"):
                self.mouseGrid.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.doubleClick()

            elif (self.userChoice == "Right click." or self.userChoice == "right click"):
                self.mouseGrid.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.rightClick()

            elif (self.userChoice == "Type something." or self.userChoice == "type something"): # or self.userChoice == "you"):
                self.mouseGrid.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.leftClick()

                print("Speak what you would like to type.")
                time.sleep(3)

                microphone.record(10)
                self.prediction = whisper.use_model(RECORD_PATH)

                pyautogui.write(self.prediction, interval=0.25)

            elif (self.userChoice == "Key press." or self.userChoice == "key press"):
                print("Which key would you like to press?")
                self.prediction = recordAndUseModel()

            elif (self.userChoice == "Get more specific." or self.userChoice == "get more specific"):
                print("Get more specific...")
                self.getMoreSpecific()

            elif (self.userChoice == "I'm done." or self.userChoice == "i'm done"):
                self.mouseOrKeyboardFlag = 1


    def getMoreSpecific(self):
        self.finalChoiceFlag = 0

        while (self.finalChoiceFlag == 0):
            print("Say left, right, up, or down.")
            print("If your cursor is at the position you want, say 'I'm done.'")

            time.sleep(5)

            self.userChoice = recordAndUseModel()

            if (self.userChoice == "Left." or self.userChoice == "left"):
                pyautogui.move(-15, 0, 0.2)

            elif (self.userChoice == "Right." or self.userChoice == "right"):
                pyautogui.move(15, 0, 0.2)

            elif (self.userChoice == "Up." or self.userChoice == "up"):
                pyautogui.move(0, -15, 0.2)

            elif (self.userChoice == "Down." or self.userChoice == "down" or self.userChoice == "Down!"):
                pyautogui.move(0, 15, 0.2)

            elif (self.userChoice == "I'm done." or self.userChoice == "i'm done"):
                self.finalChoiceFlag = 1




def recordAndUseModel():
    microphone.record(3)
    prediction = whisper.use_model(RECORD_PATH)

    print("We heard " + prediction)

    return prediction


    print("This should only run if called from cmd line")
    # This if statement executes if apps are not already saved to a file
    if os.path.exists("data/app_data.json"):
        VALID_APPS = loadValidApps()
    else:
        AppOpener.mklist(path = "data")
        VALID_APPS = loadValidApps()