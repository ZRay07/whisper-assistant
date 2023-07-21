from source.core.model_interface import *
from source.core.command_module import operations
from source.core.mouse_grid_commands import *
import time
import string
import threading
from tkinter import *
import pyautogui

Commands = operations()
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

        self.userInteraction_frame = Frame(self.pinkFrame, height = 400, width = self.screenWidth / 3, bg = "lime green")
        self.userInteraction_frame.grid(row = 1, column = 1, sticky = "se")

        self.listeningProcessing_label = Label(self.userInteraction_frame, text = "Getting ready...", font = ("Franklin Gothic Medium", 24, "bold"), width = 16, height = 1, bg = "lime green")
        self.listeningProcessing_label.grid(row = 0, column = 0)

        self.userInstruction_label = Label(self.userInteraction_frame, text = "Say a color and we'll move the cursor there", font = ("Franklin Gothic Medium", 12, "bold"), width = 38, height = 5, bg = "lime green", wraplength = 500)
        self.userInstruction_label.grid(row = 1, column = 0)

        self.userInputError_label = Label(self.userInteraction_frame, text = " ", font = ("Franklin Gothic Medium", 12, "bold"), width = 45, height = 2, bg = "lime green", wraplength = 500, fg = "#710505", anchor = "center")
        self.userInputError_label.grid(row = 2, column = 0)

        self.SpaceHolder_frame = Frame(self.userInteraction_frame, height = 36, width = self.screenWidth / 3, bg = "lime green")
        self.SpaceHolder_frame.grid(row = 3, column = 0, sticky = "se")

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


    # The input to this function comes from listenForColors()
    # The validation function guarantees that the variable being passed will be a color in one of the if statements
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


    # The input to this function comes from getInnerGridInput()
    # The validation function guarantees that the variable being passed will be an int from 1-9
    def moveToInnerPosition(self, innerGridChoice):
        try:
            movements = {
                1: (-(self.screenWidth / 9), -(self.screenHeight / 9)),
                2: (0, -(self.screenHeight / 9)),
                3: ((self.screenWidth / 9), -(self.screenHeight / 9)),
                4: (-(self.screenWidth / 9), 0),
                # 5 is the center position
                6: ((self.screenWidth / 9), 0),
                7: (-(self.screenWidth / 9), (self.screenHeight / 9)),
                8: (0, (self.screenHeight / 9)),
                9: ((self.screenWidth / 9), (self.screenHeight / 9))
            }

            # Check the dictionary for a matching number
            # If matching number found,
            #   then set "movement" to the two x and y positions stored in the grid
            if innerGridChoice in movements:
                movement = movements[innerGridChoice]
                print(f"Moving to {innerGridChoice}")
                pyautogui.move(*movement, 0.5)  # The * operator just unpacks the 2 x and y positions
            
            else:
                raise ValueError("Invalid inner grid choice")
        
        except ValueError as ve:
            print(ve)

        except Exception as e:
            print(f"Error occured while selecting inner grid: {e}")

    # This function is used to update GUI labels
    # Simply pass a label name such as:
    #   userInstruction_label, or
    #   listeningProcessing_label
    # and the message you'd like to update it with such as:
    #   "provide me a color"
    def setLabel(self, label, message):
        try:
            label.config(text = message)
            return True

        except Exception as e:
            print(f"Error updating {label} with \"{message}\": {e}")
            return False
        


class MouseGridInputValidator(MouseGrid):
    def __init__(self):
        self.colors = {"red", "purple", "black", "green", "yellow", "orange", "blue", "white", "pink"}  # used in listenForColors
        self.validInnerGridPosition = {1, 2, 3, 4, 5, 6, 7, 8, 9}   # used in getInnerGridPosition
        self.validUserOptions = {"left click", "right click", "double click", "type something", "enter key press", "continue moving cursor"} # used in getUserAction
        self.validMovementDirections = {"right", "left", "up", "down", "i'm done"}
        
        # This array is from PyAutoGui (it's a list of available special keys), used in getUserKeyInput
        self.validKeyboardKeys = [
            'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
            'browserback', 'browserfavorites', 'browserforward', 'browserhome',
            'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
            'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
            'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
            'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
            'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
            'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
            'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
            'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
            'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
            'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
            'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
            'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
            'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
            'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
            'command', 'option', 'optionleft', 'optionright'
        ]

        self.typeSomething = None
        self.commandUpdate = None
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

            if removePunctuation:
                self.userInput = self.userInput.rstrip(string.punctuation)

            if makeLowerCase:
                self.userInput = self.userInput.lower()

            return self.userInput
        
        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False
        
    # This function will specifically wait for the user to reply "yes" or "no"
    def confirmUserInput(self, userInput):
        while True:
            self.setLabel(self.userInstruction_label, f"Is {userInput} correct?")
            time.sleep(2)
            self.confirmation = self.promptUser(2, True, True)

            if self.confirmation == "yes":  # User confirmed the input
                return True
            
            elif self.confirmation == "no":  # User did not confirm input
                return None
            
            else:
                pass
        
    # This function will continuously prompt the user until they provide a number between 1 and 9
    def getInnerGridInput(self):
        # Continuously prompt the user for an inner grid position (1-9)
        while True:
            try:
                # Graphical UI Updates
                self.setLabel(self.userInstruction_label, "Say an inner grid position (1-9)")
                time.sleep(2)

                # Get the input
                self.innerGridPosition = self.promptUser(2, True, True)
                self.innerGridPosition = Commands.convertToInt(self.innerGridPosition)

                if self.innerGridPosition in self.validInnerGridPosition:
                    return self.innerGridPosition
                
                else:
                    print(f"Invalid grid position: {self.innerGridPosition}")
                    self.setLabel(self.userInstruction_label, f"Invalid grid position: {self.innerGridPosition}")

            except Exception as e:
                print(f"Error while gathering inner grid postion: {e}")

    # This function will get the user input once they've entered the subgrid phase
    # They will choose a color -> choose a subgrid -> and then be prompted with these options
    def getUserAction(self):
        try:
            while True:
                self.setLabel(self.userInstruction_label, "What would you like to do now?")
                time.sleep(2)
                self.userChoice = self.promptUser(5, True, True)

                if self.userChoice in self.validUserOptions:
                    return self.userChoice

                else:
                    print(f"Invalid choice: {self.userChoice}")
                    self.setLabel(self.userInstruction_label, f"Invalid grid position: {self.innerGridPosition}")

        except Exception as e:
            print(f"Error while gathering user selection: {e}")

    # This function takes an input for what the user wants to do
    # and maps it to a function call
    def handleAction(self, userAction):
        # First, check if they want to click anything, as these are easier to deal with
        try:
            clickChoices = {
                "left click": ["left"],
                "right click": ["right"],
                "double click": ["double"]
            }

            if userAction in clickChoices:      # if user says "right click", the dictionary's values will be pulled by providing the "right click" key
                self.commandUpdate = performClick(self, clickChoices[userAction])    
                return self.commandUpdate

            elif (userAction == "type something"):                                    # User requests to type something
                self.recordDuration = self.getRecordDuration()                      # Get a record duration from the user
                self.userTextInput = self.getUserTextInput(self.recordDuration)     # Get a text input from the user
                self.commandUpdate = enterTextInput(self, self.userTextInput)       # Run the function and save return value
                self.typeSomething = True   # This changes how fast we re-open the main window
                return self.commandUpdate

            elif (userAction == "enter key press"):
                self.userKeyInput = self.getUserKeyInput()
                self.commandUpdate = enterKeypressInput(self, self.userKeyInput)
                return self.commandUpdate
                
            elif (userAction == "continue moving cursor"):
                while True:
                    self.moveCursorDirection = self.getUserCursorDirection()

                    if self.moveCursorDirection == "i'm done":
                        return None

                    moveCursorSlightly(self.moveCursorDirection)
            
            elif (userAction == "drag to"):
                print("drag to")

        except Exception as e:
            print(f"Error in handling action: {e}")

            

    # This function will continuously prompt the user until they provide a number
    def getRecordDuration(self):
        try:
            while True:
                self.setLabel(self.userInstruction_label, "How long would you like to record for (in seconds)?")
                time.sleep(2)
                self.recordDuration = self.promptUser(2, True, True)
                self.recordDuration = Commands.convertToInt(self.recordDuration)

                if isinstance(self.recordDuration, int):
                    self.confirmation = self.confirmUserInput(self.recordDuration)

                    if self.confirmation:
                        return self.recordDuration

                else:
                    print(f"You must say a number. You said: {self.recordDuration}")
                    self.setLabel(self.userInputError_label, f"You must say a number. You said: {self.innerGridPosition}")

        except Exception as e:
            print(f"Error while gathering record duration: {e}")

    # This function will prompt the user for text based off their record duration
    # It will then confirm the user's text with them
    def getUserTextInput(self, recordDuration):
        try:
            while True:
                self.setLabel(self.userInstruction_label, "What would you like to type?")
                time.sleep(2)
                self.userTextInput = self.promptUser(recordDuration, True, True)

                self.confirmation = self.confirmUserInput(self.userTextInput)

                if self.confirmation:
                    return self.userTextInput

        except Exception as e:
            print(f"Error while gathering text input: {e}")

    # This function will continuously prompt the user for a valid key to press
    #   Some valid keys are: "win" -> windows key, "enter", "f1-12", etc.
    # The user will then be prompted to confirm their desired key
    def getUserKeyInput(self):
        try:
            while True:
                self.setLabel(self.userInstruction_label, "What key-press would you like to simulate?")
                time.sleep(2)
                self.userKeyInput = self.promptUser(3, True, True)

                if self.userKeyInput in self.validKeyboardKeys:
                    self.confirmation = self.confirmUserInput(self.userKeyInput)

                elif self.userKeyInput == "you":
                    pass

                else:
                    self.setLabel(self.userInputError_label, f"Invalid key: {self.userKeyInput}")
                    continue    # return to top of loop

                if self.confirmation:
                    return self.userKeyInput

        except Exception as e:
            print(f"Error while getting key press input: {e}")

    # This function will continuously prompt the user for a valid direction to move the cursor
    #   The user can also say "I'm done"
    def getUserCursorDirection(self):
        try:
            while True:
                self.setLabel(self.userInstruction_label, "Which direction would you like to move the cursor?")
                time.sleep(2)
                self.movementDirection = self.promptUser(2, True, True)

                if self.movementDirection in self.validMovementDirections:
                    return self.movementDirection

                elif self.movementDirection == "you":
                    pass

                else:
                    self.setLabel(self.userInputError_label, f"Invalid direction: {self.movementDirection}")
                    continue    # return to top of loop

        except Exception as e:
            print(f"Error while getting cursor movement direction: {e}")

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
                    self.innerGridChoice = self.getInnerGridInput()

                    if self.innerGridChoice == 5:
                        pass
                    else:
                        self.moveToInnerPosition(self.innerGridChoice)

                    while self.commandUpdate is None:
                        self.userAction = self.getUserAction()
                        self.commandUpdate = self.handleAction(self.userAction)

                    break

                elif (self.colorChoice == "exit"):
                    self.MouseGridWindow.destroy()
                    break

        except Exception as e:
            print(f"Error while listening for colors: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the MouseGridInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForColors)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()