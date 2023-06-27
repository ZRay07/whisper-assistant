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


# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):    

    print("userChoice: " + userChoice)

    if (userChoice == "Open application." or userChoice == "open application" or userChoice == "Open app."):        # Open application
        print("\n***Open Application***")
        openApplication()

    elif (userChoice == "Close application." or userChoice == "close application" or userChoice == "Close app" or userChoice == "Close application." or userChoice == "Close app."):      # Close application
        print("\n***Close Application***")
        closeApplication()

    elif (userChoice == "Scroll up" or userChoice == "Scroll up."):      # Scroll up
        print("\n***Scroll Up***")
        pyautogui.scroll(100)
            
    elif (userChoice == "Scroll down" or userChoice == "Scroll down."):    # Scroll down
        print("\n***Scroll Down***")
        pyautogui.scroll(-100)

    elif (userChoice == "Set volume" or userChoice == "Set volume."):   # Set volume
        print("\n***Set Volume***")
        setVolume()           

    elif (userChoice == "Navigate mouse and keyboard" or userChoice == "Navigate mouse and keyboard." or userChoice == "Mouse control." or userChoice == "mouse control"):
        print("\n***Navigate mouse + keyboard***")
        mouseGrid()

    elif (userChoice == "Sign into email." or userChoice == "Email sign in." or userChoice == "Send an email." or userChoice == "Email Sign In" or userChoice == "Email sign it" or userChoice == "Email Sign In."):    # Email sign in
        print("\n***Email sign-in***") 
        sign_in()       

    elif (userChoice == "Exit" or userChoice == "Exit."):    # Exit
        print("***Exiting***")

    elif (userChoice == "Google search" or userChoice == "google search" or userChoice == "Google search." or userChoice == "google search."  ):
        print("\nSearching now...\n")
        google_search()
    else:
        print("Try again...")



def openApplication():
    print("\nWhich application would you like to open?")
    print("\t*Word")
    print("\t*Edge")
    print("\t*Spotify")
    print("\t*Discord")

    microphone.record(3)
    prediction = whisper.use_model(RECORD_PATH)

    print("Opening " + prediction)
    AppOpener.open(prediction)

def closeApplication():
    print("\nWhich application would you like to close?")
    print("\t*Word")
    print("\t*Edge")
    print("\t*Spotify")
    print("\t*Discord")

    microphone.record(3)
    prediction = whisper.use_model(RECORD_PATH)

    print("Closing " + prediction)
    AppOpener.close(prediction)


def setVolume():
    userConfirmation = False
    while (userConfirmation == False):
        print("\nWhat volume would you like to set to?")
        print("*** MUST BE AN INCREMENT OF 10 ***")

        microphone.record(2)
        prediction = whisper.use_model(RECORD_PATH)

        if (prediction == "0" or prediction == "0." or prediction == "Zero" or prediction == "zero"):
            volume.SetMasterVolumeLevel(-60.0, None)
            print("Setting volume to 0")
            userConfirmation = True

        elif (prediction == "10" or prediction == "10."):
            volume.SetMasterVolumeLevel(-33.0, None)
            print("Setting volume to 10")
            userConfirmation = True

        elif (prediction == "20"):
            volume.SetMasterVolumeLevel(-23.4, None)
            print("Setting volume to 20")
            userConfirmation = True

        elif (prediction == "30"):
            volume.SetMasterVolumeLevel(-17.8, None)
            print("Setting volume to 30")
            userConfirmation = True

        elif (prediction == "40"):
            volume.SetMasterVolumeLevel(-13.6, None)
            print("Setting volume to 40")
            userConfirmation = True

        elif (prediction == "50"):
            volume.SetMasterVolumeLevel(-10.2, None)
            print("Setting volume to 50")
            userConfirmation = True

        elif (prediction == "60"):
            volume.SetMasterVolumeLevel(-7.6, None)
            print("Setting volume to 60")
            userConfirmation = True

        elif (prediction == "70"):
            volume.SetMasterVolumeLevel(-5.3, None)
            print("Setting volume to 70")
            userConfirmation = True

        elif (prediction == "80"):
            volume.SetMasterVolumeLevel(-3.4, None)
            print("Setting volume to 80")
            userConfirmation = True

        elif (prediction == "90"):
            volume.SetMasterVolumeLevel(-1.6, None)
            print("Setting volume to 90")
            userConfirmation = True

        elif (prediction == "100"):
            volume.SetMasterVolumeLevel(0, None)
            print("Setting volume to 100")
            userConfirmation = True

        else:
            print("We heard: " + prediction)
            userConfirmation = False

# end volume control loop 

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

class mouseGrid():
    def __init__(self):
        print("***Mouse Control***")
        self.userChoiceFlag = 0

        # Open a new window
        self.mouseGrid = Tk()

        # Make this window transparent
        self.mouseGrid.attributes("-alpha", 0.5, "-fullscreen", TRUE)

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

        # Make 9 frames (3 * 3 grid)
        # One for each portion of the grid
        self.a1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "red")
        self.a1.grid(row = 0, column = 0)
        self.a1.grid_propagate(False)

        self.a2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "green")
        self.a2.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.a2.grid_propagate(False)

        self.a3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "blue")
        self.a3.grid(row = 2, column = 0, padx = 0, pady = 0)
        self.a3.grid_propagate(False)

        self.b1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "purple")
        self.b1.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.b1.grid_propagate(False)

        self.b2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "gold")
        self.b2.grid(row = 1, column = 1, padx = 0, pady = 0)
        self.b2.grid_propagate(False)

        self.b3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "white")
        self.b3.grid(row = 2, column = 1, padx = 0, pady = 0)
        self.b3.grid_propagate(False)

        self.c1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "black")
        self.c1.grid(row = 0, column = 2, padx = 0, pady = 0)
        self.c1.grid_propagate(False)

        self.c2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "orange red")
        self.c2.grid(row = 1, column = 2, padx = 0, pady = 0)
        self.c2.grid_propagate(False)

        self.c3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "deep pink")
        self.c3.grid(row = 2, column = 2, padx = 0, pady = 0)
        self.c3.grid_propagate(False)

        self.inputBox = Text(self.c1, height = 1, width = 10, border = 2, relief = "solid")
        self.inputBox.grid(row = 0, column = 0,sticky = NE)

        self.submit_button = Button(self.c1, text = "Submit", command = self.getUserChoice, border = 2, relief = "solid")
        self.submit_button.grid(row = 1, column = 0, sticky = NE)

        self.mouseGrid.mainloop()

    def getUserChoice(self):
        self.inputBoxChoice = self.inputBox.get(1.0, "end-1c")

        if (self.inputBoxChoice == "Record"):
            self.userChoice = recordAndUseModel()
            self.displaySubgrid()
            

        elif (self.inputBoxChoice == "Red" or self.inputBoxChoice == "Green" or self.inputBoxChoice == "Blue" or
              self.inputBoxChoice == "Purple" or self.inputBoxChoice == "Yellow" or self.inputBoxChoice == "White" or
              self.inputBoxChoice == "Black" or self.inputBoxChoice == "Orange" or self.inputBoxChoice == "Pink"):
            self.displaySubgrid()
        
        else:
            print("Enter a correct input")

    def displaySubgrid(self):
        self.displayFlag = 0

        if (self.userChoice == "Red." or self.userChoice == "Red" or self.userChoice == "red"):      # top left
            self.subgrid = Canvas(self.a1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.redCenter[0], self.redCenter[1], self.redCenter[2])
            self.displayFlag = 1
        
        elif (self.userChoice == "Green." or self.userChoice == "Green" or self.userChoice == "green"):  # middle left
            self.subgrid = Canvas(self.a2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.greenCenter[0], self.greenCenter[1], self.greenCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Blue." or self.userChoice == "Blue" or self.userChoice == "blue"):   # bottom left
            self.subgrid = Canvas(self.a3, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.blueCenter[0], self.blueCenter[1], self.blueCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Purple." or self.userChoice == "Purple" or self.userChoice == "purple"): # top center
            self.subgrid = Canvas(self.b1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.purpleCenter[0], self.purpleCenter[1], self.purpleCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Yellow." or self.userChoice == "Yellow" or self.userChoice == "yellow"): # center
            self.subgrid = Canvas(self.b2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.yellowCenter[0], self.yellowCenter[1], self.yellowCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "White." or self.userChoice == "White" or self.userChoice == "white"):  # bottom center
            self.subgrid = Canvas(self.b3, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.whiteCenter[0], self.whiteCenter[1], self.whiteCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Black." or self.userChoice == "Black" or self.userChoice == "black"):  # top right
            self.subgrid = Canvas(self.c1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.blackCenter[0], self.blackCenter[1], self.blackCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Orange." or self.userChoice == "Orange" or self.userChoice == "orange"):   # middle right
            self.subgrid = Canvas(self.c2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.orangeCenter[0], self.orangeCenter[1], self.orangeCenter[2])
            self.displayFlag = 1

        elif (self.userChoice == "Pink." or self.userChoice == "Pink" or self.userChoice == "pink"):   # bottom right
            self.subgrid = Canvas(self.c3, width = self.screenWidth / 3, height = self.screenHeight / 3)
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
            self.dynamicInstructionText.set("If you'd like to get more specific, say yes. Otherwise, you can make an action where your cursor is.")

            if (self.userChoice == "Red." or self.userChoice == "red"):
                self.dynamicInstruction_label = Label(self.c1, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

            else:
                self.dynamicInstruction_label = Label(self.a1, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.dynamicInstructionText, wraplength = 200)
                self.dynamicInstruction_label.grid(row = 0, column = 1, sticky = NE)

            self.mouseGrid.update_idletasks()
            self.mouseGrid.update()

            print("Say 'yes' to specify a subgrid.")
            time.sleep(3)

            self.userChoice = recordAndUseModel()

            if (self.userChoice == "Yes." or self.userChoice == "yes"):
                self.moveToInnerPosition()
                self.mouseOrKeyboardAction()

            else:
                self.mouseOrKeyboardAction()

        else:
            print("Incorrect input. Say the color which you'd like your cursor to be in...")



    def moveToInnerPosition(self):
        print("Say 1-9 to move to an inner grid position")
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

            print("***Options***")
            print("* Left click, right click")
            print("* Type something, key press")
            print("* Get more specific")
            print("* I'm done")

            time.sleep(5)

            self.userChoice = recordAndUseModel()

            if (self.userChoice == "Click." or self.userChoice == "click" or self.userChoice == "Left click." or self.userChoice == "left click"): # or self.userChoice == "you"):
                self.mouseGrid.wm_state("iconic")
                time.sleep(0.2)
                pyautogui.leftClick()

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
    