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
import pyttsx3  # for text to speech

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def beepgood():
    winsound.Beep(1000, 1000)
    winsound.Beep(1250, 1000)

def beepbad():
    winsound.Beep(1000, 1000)
    winsound.Beep(750, 1000)

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):    
    print("userChoice: " + userChoice)

    userChoiceSplit = userChoice.split()

    if (userChoiceSplit[0] == "Open" or userChoiceSplit[0] == "open"):        # Open application
        print("\n***Open Application***")
        appName = userChoiceSplit[-1]
        openApplication(appName)

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Close application") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Close app") > 0.85):      # Close application
        print("\n***Close Application***")
        closeApplication()

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Scroll up") > 0.9):      # Scroll up
        print("\n***Scroll Up***")
        scrollUp(100)
            
    elif (jellyfish.jaro_winkler_similarity(userChoice, "Scroll down") > 0.9):    # Scroll down
        print("\n***Scroll Down***")
        scrollDown(100)

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Set volume") > 0.85):   # Set volume
        print("\n***Set Volume***")
        setVolume()           

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Navigate mouse and keyboard") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Mouse Control") > 0.85):
        print("\n***Navigate mouse + keyboard***")
        mouseGrid()

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Email sign in") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Send an email") > 0.85):    # Email sign in
        print("\n***Email sign-in***") 
        sign_in()       

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Exit") > 0.85):    # Exit
        print("***Exiting***")

    elif (jellyfish.jaro_winkler_similarity(userChoice, "Google search") > 0.85):
        print("\nSearching now...\n")
        google_search()

    else:
        print("Try again...")



def openApplication(appName):
    
    if (appName == "application." or appName == "application" or appName == "app." or appName == "app"):
        print("\nWhich application would you like to open?")
        print("\t*Word")
        print("\t*Edge")
        print("\t*Spotify")
        print("\t*Discord")

        microphone.record(3)
        appName = whisper.use_model(RECORD_PATH)

    try:
        AppOpener.open(appName, throw_error = True)
        return True
    except Exception as e:
        return False


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

def scrollUp(scrollAmount):
    pyautogui.scroll(scrollAmount)
    
def scrollDown(scrollAmount):
    pyautogui.scroll(-(scrollAmount))

def setVolume():
    numberFlag = False
    while (numberFlag == False):
        print("\nWhat volume would you like to set to?")
        print("*** MUST BE AN INCREMENT OF 10 ***")

        microphone.record(2)
        prediction = whisper.use_model(RECORD_PATH)

        if (prediction == "0" or prediction == "0." or prediction == "Zero" or prediction == "zero"):
            volume.SetMasterVolumeLevel(-60.0, None)
            print("Setting volume to 0")
            numberFlag = True

        elif (prediction == "10" or prediction == "10."):
            volume.SetMasterVolumeLevel(-33.0, None)
            print("Setting volume to 10")
            numberFlag = True

        elif (prediction == "20"):
            volume.SetMasterVolumeLevel(-23.4, None)
            print("Setting volume to 20")
            numberFlag = True

        elif (prediction == "30"):
            volume.SetMasterVolumeLevel(-17.8, None)
            print("Setting volume to 30")
            numberFlag = True

        elif (prediction == "40"):
            volume.SetMasterVolumeLevel(-13.6, None)
            print("Setting volume to 40")
            numberFlag = True

        elif (prediction == "50"):
            volume.SetMasterVolumeLevel(-10.2, None)
            print("Setting volume to 50")
            numberFlag = True

        elif (prediction == "60"):
            volume.SetMasterVolumeLevel(-7.6, None)
            print("Setting volume to 60")
            numberFlag = True

        elif (prediction == "70"):
            volume.SetMasterVolumeLevel(-5.3, None)
            print("Setting volume to 70")
            numberFlag = True

        elif (prediction == "80"):
            volume.SetMasterVolumeLevel(-3.4, None)
            print("Setting volume to 80")
            numberFlag = True

        elif (prediction == "90"):
            volume.SetMasterVolumeLevel(-1.6, None)
            print("Setting volume to 90")
            numberFlag = True

        elif (prediction == "100"):
            volume.SetMasterVolumeLevel(0, None)
            print("Setting volume to 100")
            numberFlag = True

        else:
            print("We heard: " + prediction)
            numberFlag = False

    return True

# end volume control loop 

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
            domain = extr_3[2]
            contact = {
                    'name' : first_name + " " + last_name,
                    'email' : email , 
                    'domain' : domain
                }
    return contact.get('name'), contact.get('email'), contact.get('domain')

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


if __name__ == "__main__":
    print("This should only run if called from cmd line")    