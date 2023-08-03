import string
import time
import threading

from source.ui.mouse_grid.mouse_grid_ui import MouseGrid
from source.core.model_interface import microphone, whisper, RECORD_PATH
from source.core.command_module import operations
from source.ui.mouse_grid.mouse_grid_commands import *

Commands = operations()

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
                print(f"self.colorchoice {self.colorChoice}")
                
                if (self.colorChoice in self.colors):
                    self.setLabel(self.listeningProcessing_label, "Waiting...")
                    self.displaySubgrid(self.colorChoice)
                    self.innerGridChoice = self.getInnerGridInput()

                    if self.innerGridChoice == 5:
                        pass
                    else:
                        moveToInnerPosition(self, self.innerGridChoice)

                    while self.commandUpdate is None:
                        self.userAction = self.getUserAction()
                        self.commandUpdate = self.handleAction(self.userAction)

                    break

                elif (self.colorChoice == "exit"):
                    self.MouseGridWindow.destroy()
                    break

                time.sleep(0.25)

        except Exception as e:
            print(f"Error while listening for colors: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the MouseGridInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForColors)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()