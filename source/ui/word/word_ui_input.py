import string
import time
import threading

from source.ui.word.word_ui import WordWindow
from source.ui.word.word_ui_commands import WordCommandHandler

from source.core.model_interface import microphone, whisper, RECORD_PATH
from source.core.command_module import operations

Commands = operations()

class WordInputValidator(WordWindow):
    def __init__(self, title, size, document_name = "DefaultDocumentName"):
        super().__init__(title, size)
        
        self.document_name = document_name
        self.instruction_sleep_time = 2

        self.command_handler = WordCommandHandler(self)

        self.valid_commands = {
            "insert text": self.command_handler.real_time_text_input,

            "save and name file": self.command_handler.save_and_name_file,
            "save file": self.command_handler.save_file,

            "tab in": self.command_handler.tab_text, 
            "indent": self.command_handler.tab_text,
            "enter new line": self.command_handler.new_line,
            "make new page": self.command_handler.new_page,

            "change font": self.change_font,
            "increase font size": self.command_handler.increase_font_size,      # Justification, lists (bullet and numbered)
            "decrease font size": self.command_handler.decrease_font_size,      # highlight, change font color
            "turn on bold": self.command_handler.make_font_bold,
            "turn on italic": self.command_handler.make_font_italic,
            "turn on underline": self.command_handler.make_font_underline,
            "change to title style": self.command_handler.make_title_style,
            "change to heading one style": self.command_handler.make_heading1_style,
            "change to heading two style": self.command_handler.make_heading2_style,
            "change to normal style": self.command_handler.make_normal_style,
            "turn on subscript": self.command_handler.make_subscript,
            "turn on superscript": self.command_handler.make_superscript,

            "mouse control": self.command_handler.mouse_control
                               }  # used in listenForCommands
        
        self.startListeningThread()
  
    def promptUser(self, recordDuration, removePunctuation, makeLowerCase):
        #####
        # This function is used when we need to prompt the user for additional voice inputs
        # If removePunctuation is true when you call it, it removes trailing punctuation.
        # If makeLowerCase is true when you call it, it makes the output string lowercase
        #####
        try:
            self.setLabel(self.feedback_msg.listening_processing_label1, "Listening...")
            microphone.record(recordDuration)
            self.setLabel(self.feedback_msg.listening_processing_label1, "Processing...")
            self.userInput = whisper.use_model(RECORD_PATH)
            self.setLabel(self.feedback_msg.listening_processing_label1, "Waiting...")

            if removePunctuation:
                self.userInput = self.userInput.rstrip(string.punctuation)

            if makeLowerCase:
                self.userInput = self.userInput.lower()

            return self.userInput
        
        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False
        
    def confirmUserInput(self, userInput):
        #####
        # This function will specifically wait for the user to reply "yes" or "no"
        #####
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

    def validate_general_input(self, instruction, invalid_input_message, valid_input, user_input = None):
        #####
        # This function is a general input validator
        # Can be called with a user input, if no user input is passed, it moves directly to getting a user input
        # Pass an instruction to the user with 'instruction' for the input we're trying to gather
        # Pass a valid list to the function with 'valid_input', this list is what the input will be checked against
        #####
        try:
            while True:
                if user_input in valid_input:
                    return user_input
                
                elif user_input is not None:
                    self.setLabel(self.user_instruction_label2, f"{invalid_input_message}: {user_input}")
                
                self.setLabel(self.user_instruction_label2, instruction)
                time.sleep(self.instruction_sleep_time)
                user_input = self.promptUser(5, True, True)

        except Exception as e:
            print(f"Error while validating/getting user input: {e}")

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

    def change_font(self):
        print("get font name, check against valid inputs, run change font function")
        valid_fonts = ["times new roman", "calibri", "arial"]
        instruction = "What font would you like to set to?"
        invalid_input_message = "Invalid font"

        self.setLabel("What font would you like to set to?")
        font_name = self.promptUser(5, True, True)

        font_name = self.validate_general_input(self,
                                                instruction, invalid_input_message,
                                                valid_fonts, font_name)
        
        

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
                    selected_command = self.valid_commands[self.command_choice]

                    # Call the selected command
                    selected_command()

                elif (self.command_choice == "exit"):
                    self.destroy()
                    break

                elif self.command_choice != "you":
                    self.appendNewUserInputHistory(self.command_choice)

                time.sleep(0.25)

        except Exception as e:
            print(f"Error while listening for word commands: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the MouseGridInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForCommands)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

if __name__ == "__main__":
    word_window = WordInputValidator("Microsoft Word Menu", (300, 1000))
    word_window.mainloop()