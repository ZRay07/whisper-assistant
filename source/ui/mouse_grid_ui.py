import time
import string
import threading
from source.core.model_interface import *
from source.core.command_module import convertToInt
from tkinter import *
import pyautogui

class MouseGrid():
    def __init__(self):
        
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
        self.pinkFrame.grid(row=2, column=2, padx=0, pady=0)
        self.pinkFrame.grid_propagate(False)

        self.userInteraction_frame = Frame(self.pinkFrame, height = 300, width = 400, bg = "lime green")
        self.userInteraction_frame.grid(row = 1, column = 1, sticky = "se")

        self.listeningProcessing_label = Label(self.userInteraction_frame, text = "Getting ready...", font = ("Franklin Gothic Medium", 24, "bold"), width = 16, height = 1, bg = "lime green")
        self.listeningProcessing_label.grid(row = 0, column = 0)

        self.userInstruction_label = Label(self.userInteraction_frame, text = "Say a color and we'll move the cursor there", font = ("Franklin Gothic Medium", 12, "bold"), width = 38, height = 3, bg = "lime green", wraplength = 350)
        self.userInstruction_label.grid(row = 1, column = 0)

        self.SpaceHolder_frame = Frame(self.userInteraction_frame, height = 36, width = 400, bg = "yellow")
        self.SpaceHolder_frame.grid(row = 2, column = 0, sticky = "se")

        # Configure the row and column weights of the pinkFrame
        self.pinkFrame.grid_rowconfigure(1, weight = 1)
        self.pinkFrame.grid_columnconfigure(1, weight = 1)

        
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
        try:
            if (colorChoice == "red"):      # top left
                self.subgrid = Canvas(self.redFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.redCenter[0], self.redCenter[1], self.redCenter[2])
                self.displayFlag = 1
            
            elif (colorChoice == "green"):  # middle left
                self.subgrid = Canvas(self.greenFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.greenCenter[0], self.greenCenter[1], self.greenCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "blue"):   # bottom left
                self.subgrid = Canvas(self.blueFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.blueCenter[0], self.blueCenter[1], self.blueCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "purple"): # top center
                self.subgrid = Canvas(self.purpleFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.purpleCenter[0], self.purpleCenter[1], self.purpleCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "yellow"): # center
                self.subgrid = Canvas(self.yellowFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.yellowCenter[0], self.yellowCenter[1], self.yellowCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "white"):  # bottom center
                self.subgrid = Canvas(self.whiteFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.whiteCenter[0], self.whiteCenter[1], self.whiteCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "black"):  # top right
                self.subgrid = Canvas(self.blackFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.blackCenter[0], self.blackCenter[1], self.blackCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "orange"):   # middle right
                self.subgrid = Canvas(self.orangeFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.orangeCenter[0], self.orangeCenter[1], self.orangeCenter[2])
                self.displayFlag = 1

            elif (colorChoice == "pink"):   # bottom right
                self.subgrid = Canvas(self.pinkFrame, width = self.screenWidth / 3, height = self.screenHeight / 3)
                print(f"Moving to {colorChoice} center")
                pyautogui.moveTo(self.pinkCenter[0], self.pinkCenter[1], self.pinkCenter[2])
                self.displayFlag = 1

            else:
                raise ValueError(print(f"Color error: {e}"))
            
            # Draw horizontal lines
            self.subgrid.create_line(0, self.screenHeight / 9, self.screenWidth / 3, self.screenHeight / 9, width = 5)  
            self.subgrid.create_line(0, self.screenHeight * 2 / 9, self.screenWidth / 3, self.screenHeight * 2 / 9, width = 5)

            # Draw vertical lines
            self.subgrid.create_line(self.screenWidth / 9, 0, self.screenWidth / 9, self.screenHeight / 3, width = 5)
            self.subgrid.create_line(self.screenWidth * 2 / 9, 0, self.screenWidth * 2 / 9, self.screenHeight / 3, width = 5)

            # Place the canvas onto user choice location
            self.subgrid.grid(padx = 0, pady = 0)

            return f"Successfully displayed {colorChoice} subgrid"
        
        except Exception as e:
            print(f"Error displaying subgrid: {e}")



    def moveToInnerPosition(self, innerGridChoice):
        try:
            if (innerGridChoice == 1):
                print("Moving to 1...")
                pyautogui.move(-(self.screenWidth / 9), -(self.screenHeight / 9), 0.5)

            elif (innerGridChoice == 2):
                print("Moving to 2...")
                pyautogui.move(0, -(self.screenHeight / 9), 0.5)

            elif (innerGridChoice == "3"):
                print("Moving to 3...")
                pyautogui.move((self.screenWidth / 9), -(self.screenHeight / 9), 0.5)

            elif (innerGridChoice == "4"):
                print("Moving to 4...")
                pyautogui.move(-(self.screenWidth / 9), 0, 0.5)

            # 5 is the center

            elif (innerGridChoice == "6"):
                print("Moving to 6...")
                pyautogui.move((self.screenWidth / 9), 0, 0.5)

            elif (innerGridChoice == "7"):
                print("Moving to 7...")
                pyautogui.move(-(self.screenWidth / 9), (self.screenHeight / 9), 0.5)

            elif (innerGridChoice == "8"):
                print("Moving to 8...")
                pyautogui.move(0, (self.screenHeight / 9), 0.5)

            elif (innerGridChoice == "9"):
                print("Moving to 9...")
                pyautogui.move((self.screenWidth / 9), (self.screenHeight / 9), 0.5)

            else:
                raise ValueError
        
        except ValueError as ve:
            print(f"Invalid inner grid choice: {ve}")

        except Exception as e:
            print(f"Error occured while selecting inner grid: {e}")

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

            self.userChoice = self.promptUser(3, True, True)

            if (self.userChoice == "left"):
                pyautogui.move(-15, 0, 0.2)

            elif (self.userChoice == "right"):
                pyautogui.move(15, 0, 0.2)

            elif (self.userChoice == "up"):
                pyautogui.move(0, -15, 0.2)

            elif (self.userChoice == "down"):
                pyautogui.move(0, 15, 0.2)

            elif (self.userChoice == "I'm done." or self.userChoice == "i'm done"):
                self.finalChoiceFlag = 1

class MouseGridInputValidator(MouseGrid):
    def __init__(self):
        self.colors = {"red", "purple", "black", "green", "yellow", "orange", "blue", "white", "pink"}
        self.startListeningThread()

        super().__init__()

    # This function is used when we need to prompt the user for additional voice inputs
    # If removePunctuation is true when you call it, it removes trailing punctuation.
    # If makeLowerCase is true when you call it, it makes the output string lowercase
    def promptUser(self, recordDuration, removePunctuation, makeLowerCase):
        try:
            self.setLabel(self.listeningProcessing_label, "Listening...")
            microphone.record(recordDuration)
            self.setLabel(self.listeningProcessing_label, "Processing...")
            self.userInput = whisper.use_model(RECORD_PATH)
            self.setLabel(self.listeningProcessing_label, "Waiting...")

            # I've found the default if there is no sound is to predict "you"
            # In this case, I think it's best to interpret the input as silence and not update the user input history
#            if self.userInput != "you":
#                self.appendNewUserInputHistory(self.userInput)


            if removePunctuation:
                self.userInput = self.userInput.rstrip(string.punctuation)

            if makeLowerCase:
                self.userInput = self.userInput.lower()

            return self.userInput
        
        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False
        
    # This function is used to update GUI labels
    # Simply pass a label name such as:
    #   userInstruction_label, or
    #   listeningProcessing_label
    # and the message you'd like to update it with such as:
    #   "provide me a color"
    def setLabel(self, label, message):
        try:
            self.message = message
            self.label = label
            self.label.config(text = self.message)

        except Exception as e:
            print(f"Error updating {label} with \"{message}\": {e}")
        

    def validateInnerGridInput(self):
        self.validInnerGridPosition = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Continuously prompt the user for an inner grid position (1-9)
        while True:
            try:
                # Graphical UI Updates
                self.setLabel(self.userInstruction_label, "Say an inner grid position (1-9)")
                time.sleep(2)

                self.innerGridPosition = self.promptUser(2, True, True)
                self.innerGridPosition = convertToInt(self.innerGridPosition)

                if self.innerGridPosition in self.validInnerGridPosition:
                    return self.innerGridPosition
                
                else:
                    print(f"Invalid grid position: {self.innerGridPosition}")
                    self.setLabel(self.userInstruction_label, f"Invalid grid position: {self.innerGridPosition}")

            except Exception as e:
                print(f"Error while gathering inner grid postion: {e}")

    # This function should be called as soon as the mouse window is launched
    # First, it updates the userInstruction label to let the users know we're first waiting for a color
    #   It will continuously listen until it hears a color
    #   When a color is heard:
    #       return color choice
    def listenForColors(self):
        time.sleep(1)
        try:
            while True:
                self.setLabel(self.userInstruction_label, "Say a color and we'll move the cursor there")

                self.colorChoice = self.promptUser(2, True, True)
                

                if (self.colorChoice in self.colors):
                    self.setLabel(self.listeningProcessing_label, "Waiting...")
                    self.displaySubgrid(self.colorChoice)
                    self.innerGridChoice = self.validateInnerGridInput()
                    self.moveToInnerPosition(self.innerGridChoice)
                    break

                elif (self.colorChoice == "you"):   # I found the model defaults to you if there is no sound passed
                    pass                                                                # In this case, do nothing

                elif (self.colorChoice == "exit"):
                    break

        except Exception as e:
            print(f"Error while listening for colors: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the MouseGridInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForColors)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

mouseGrid = MouseGridInputValidator()