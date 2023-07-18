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

#audio beep functions
def beepgood():
    winsound.Beep(1000, 250)
    winsound.Beep(1500, 250)

def beepbad():
    winsound.Beep(1000, 250)
    winsound.Beep(500, 250)

#example text to speech function
def tts():
    engine = pyttsx3.init() # initialize
    engine.setProperty('rate', 100) # adjust settings (in this case speech rate)
    engine.say("Begin recording") # what engine will say (feed prediction into this?)
    engine.runAndWait() # runs engine until 'sentence' is over

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


def sign_in():
    name, email, domain = account_info_in()
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

class MouseGrid():
    def __init__(self):
        self.userChoiceFlag = 0

        # Open a new window
        self.MouseGridWindow = Tk()

        # Make this window transparent
        self.MouseGridWindow.attributes("-alpha", 0.3, "-fullscreen", TRUE)

        # Grab the screen height and screen width from window (should be 1920 X 1080 in most cases)
        self.screenHeight = self.MouseGridWindow.winfo_screenheight()
        self.screenWidth = self.MouseGridWindow.winfo_screenwidth()

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
        self.MouseGridWindow.mainloop()

        
    def drawColorGrid(self):
        # Make 9 frames (3 * 3 grid)
        # One for each portion of the grid
        self.redFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "red")
        self.redFrame.grid(row = 0, column = 0)
        self.redFrame.grid_propagate(False)

        self.greenFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "green")
        self.greenFrame.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.greenFrame.grid_propagate(False)

        self.blueFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "blue")
        self.blueFrame.grid(row = 2, column = 0, padx = 0, pady = 0)
        self.blueFrame.grid_propagate(False)

        self.purpleFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "purple")
        self.purpleFrame.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.purpleFrame.grid_propagate(False)

        self.yellowFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "gold")
        self.yellowFrame.grid(row = 1, column = 1, padx = 0, pady = 0)
        self.yellowFrame.grid_propagate(False)

        self.whiteFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "white")
        self.whiteFrame.grid(row = 2, column = 1, padx = 0, pady = 0)
        self.whiteFrame.grid_propagate(False)

        self.blackFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "black")
        self.blackFrame.grid(row = 0, column = 2, padx = 0, pady = 0)
        self.blackFrame.grid_propagate(False)

        self.orangeFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "orange red")
        self.orangeFrame.grid(row = 1, column = 2, padx = 0, pady = 0)
        self.orangeFrame.grid_propagate(False)

        self.pinkFrame = Frame(self.MouseGridWindow, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "deep pink")
        self.pinkFrame.grid(row = 2, column = 2, padx = 0, pady = 0)
        self.pinkFrame.grid_propagate(False)

        self.inputBox = Text(self.blackFrame, height = 1, width = 10, border = 2, relief = "solid")
        self.inputBox.grid(row = 0, column = 0,sticky = NE)

        self.submit_button = Button(self.blackFrame, text = "Submit", command = self.getUserChoice, border = 2, relief = "solid")
        self.submit_button.grid(row = 1, column = 0, sticky = NE)

    # This function will be used when we need to re-draw the grid
    #   It simply deletes all of the frames, and we can re-draw them by calling: drawColorGrid()
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

    # This function grabs the text inside of the box next to the submit button
    def getUserChoice(self):
        self.inputBoxChoice = self.inputBox.get(1.0, "end-1c")

        # If the user specifies they wish to record, we call our prompt user function which records and uses the speech recognition model
        #   The output of the model is formatted to have no trailing punctuation and to be all lowercase
        if (self.inputBoxChoice == "Record"):
            self.userChoice = promptUser(3, removePunctuation = True, makeLowerCase = True)
            self.displaySubgrid(self.userChoice)
            
        elif (self.inputBoxChoice == "Destroy"):
            self.deleteColorGrid()
            self.MouseGridWindow.update_idletasks()
            self.MouseGridWindow.update()

            time.sleep(5)

            self.drawColorGrid()
            self.MouseGridWindow.update_idletasks()
            self.MouseGridWindow.update()
        
        else:
            print("Enter a correct input")

    def displaySubgrid(self, colorChoice):
    
        self.displayFlag = 0
        while True:
            try:
                if (jellyfish.jaro_winkler_similarity(colorChoice, "red") > 0.7):      # top left
                    self.subgrid = Canvas(self.redFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.redCenter[0], self.redCenter[1], self.redCenter[2])
                    self.displayFlag = 1
                
                elif (jellyfish.jaro_winkler_similarity(colorChoice, "green") > 0.85):  # middle left
                    self.subgrid = Canvas(self.greenFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.greenCenter[0], self.greenCenter[1], self.greenCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "blue") > 0.85):   # bottom left
                    self.subgrid = Canvas(self.blueFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.blueCenter[0], self.blueCenter[1], self.blueCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "purple") > 0.85): # top center
                    self.subgrid = Canvas(self.purpleFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.purpleCenter[0], self.purpleCenter[1], self.purpleCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "yellow") > 0.85): # center
                    self.subgrid = Canvas(self.yellowFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.yellowCenter[0], self.yellowCenter[1], self.yellowCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "white") > 0.85):  # bottom center
                    self.subgrid = Canvas(self.whiteFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.whiteCenter[0], self.whiteCenter[1], self.whiteCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "black") > 0.85):  # top right
                    self.subgrid = Canvas(self.blackFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.blackCenter[0], self.blackCenter[1], self.blackCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "orange") > 0.85):   # middle right
                    self.subgrid = Canvas(self.orangeFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.orangeCenter[0], self.orangeCenter[1], self.orangeCenter[2])
                    self.displayFlag = 1

                elif (jellyfish.jaro_winkler_similarity(colorChoice, "pink") > 0.7):   # bottom right
                    self.subgrid = Canvas(self.pinkFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                    print(f"Moving to {colorChoice} center")
                    pyautogui.moveTo(self.pinkCenter[0], self.pinkCenter[1], self.pinkCenter[2])
                    self.displayFlag = 1

                else:
                    raise ValueError(print(f"Error: {e}"))
                
                # return True
            

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

                    self.MouseGridWindow.update_idletasks()
                    self.MouseGridWindow.update()

                    self.dynamicInstructionText = StringVar()
                    

                    if (self.userChoice == "Red." or self.userChoice == "Red" or self.userChoice == "red"):
                        self.dynamicInstruction_label = Label(self.blackFrame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                        self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

                    else:
                        self.dynamicInstruction_label = Label(self.redFrame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                        self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

                    self.dynamicInstructionText.set("If you'd like to get more specific, say yes. Otherwise, you can make an action where your cursor is.")
                    
                    self.MouseGridWindow.update_idletasks()
                    self.MouseGridWindow.update()

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
            
            except ValueError as ve:
                print(f"Invalid color: {colorChoice}")
                time.sleep(2)
                colorChoice = promptUser(3, removePunctuation = True, makeLowerCase = True)
                    
            except Exception as e:
                print(f"Error displaying subgrid: {e}")



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
                self.MouseGridWindow.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.leftClick()

            elif (self.userChoice == "Double click." or self.userChoice == "Double click" or self.userChoice == "double click"):
                self.MouseGridWindow.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.doubleClick()

            elif (self.userChoice == "Right click." or self.userChoice == "right click"):
                self.MouseGridWindow.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.rightClick()

            elif (self.userChoice == "Type something." or self.userChoice == "type something"): # or self.userChoice == "you"):
                self.MouseGridWindow.wm_state("iconic")
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

# This if statement executes if apps are not already saved to a file
if os.path.exists("data/app_data.json"):
    VALID_APPS = loadValidApps()
else:
    AppOpener.mklist(path = "data")
    VALID_APPS = loadValidApps()
    
if __name__ == "__main__":
    print("This should only run if called from cmd line")
    