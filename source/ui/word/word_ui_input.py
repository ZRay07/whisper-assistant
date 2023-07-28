import string
import time
import threading

from source.ui.word.word_ui import WordWindow
from source.core.model_interface import microphone, whisper, RECORD_PATH
from source.core.command_module import operations

Commands = operations()

class WordInputValidator(WordWindow):
    def __init__(self, title, size, start_position):
        super().__init__(title, size, start_position)

        self.valid_commands = {
            "save file": "save_file", 
            "tab in": "tab_text", 
            "indent": "tab_text",
            "enter new line": "new_line",
            "make new page": "new_page",
            "change font": self.validate_font_name,
            "increase font size": "increase_font_size",
            "decrease font size": "decrease_font_size",
            "turn on bold": "change_emphasis('bold')",
            "turn on italic": "change_emphasis('italic')",
            "turn on underline": "change_emphasis('underline')"
                               }  # used in listenForCommands
        
        self.startListeningThread()
  

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

    # This function should be called as soon as the word ui is launched
    # First, it updates the userInstruction label to let the users know we're first waiting for a command
    #   It will continuously listen until it hears a command
    #   When a command is heard:
    #       return command name
    def listenForCommands(self):
        time.sleep(1)
        try:
            while True:
                self.setLabel(self.user_inputs.user_instruction_label2, "Say 'insert text' or a command")

                self.command_choice = self.promptUser(5, True, True)
                
                if (self.command_choice in self.valid_commands):
                    # Get the corresponding function from the dictionary
                    selected_command = getattr(self, "valid_commands")[self.command_choice]

                    # Call the selected command
                    selected_command()


                elif (self.command_choice == "exit"):
                    self.destroy()
                    break

        except Exception as e:
            print(f"Error while listening for word commands: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the MouseGridInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForColors)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

word_window = WordInputValidator("Microsoft Word Menu", (300, 600), (300 , 300))
word_window.mainloop()