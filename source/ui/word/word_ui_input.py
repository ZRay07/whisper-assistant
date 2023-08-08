import string
import time
import threading
import tkinter as tk


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
            "insert text": self.handle_insert_text,
            "make real time transcription": self.handle_real_time_transcription,#command_handler.real_time_text_input,
            "make real-time transcription": self.handle_real_time_transcription,#self.command_handler.real_time_text_input,

            "save and name file": self.command_handler.save_and_name_file,
            "save file": self.command_handler.save_file,

            "tab in": self.command_handler.tab_text, 
            "indent": self.command_handler.tab_text,
            "enter new line": self.command_handler.new_line,
            "make new page": self.command_handler.new_page,

            "change font": self.handle_change_font,
            "increase font size": self.command_handler.increase_font_size,      # Justification, lists (bullet and numbered)
            "decrease font size": self.command_handler.decrease_font_size,      # highlight, change font color
            "make my text bold": self.command_handler.make_font_bold,
            "make my text italicised": self.command_handler.make_font_italic,
            "make my text underlined": self.command_handler.make_font_underline,
            "change to title style": self.command_handler.make_title_style,
            "change to heading one style": self.command_handler.make_heading1_style,
            "change to heading two style": self.command_handler.make_heading2_style,
            "change to normal style": self.command_handler.make_normal_style,
            "make my text subscript": self.command_handler.make_subscript,
            "make my text superscript": self.command_handler.make_superscript,

            "delete a word": self.handle_delete_word,

            "mouse control": self.command_handler.mouse_control
                               }  # used in listenForCommands
        self.attributes("-topmost", True)
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

            # I've found the default if there is no sound is to predict "you"
            # In this case, I think it's best to interpret the input as silence and not update the user input history
            if self.userInput != "you":
                self.appendNewUserInputHistory(self.userInput)

            return self.userInput
        
        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False
        
    def confirmUserInput(self, user_input, long_text = False):
        #####
        # This function will specifically wait for the user to reply "yes" or "no"
        #####
        while True:
            if long_text:
                self.appendNewUserInputHistory(user_input)
                self.setLabel(self.user_inputs.user_instruction_label2, "Is above correct?")
            else:
                self.setLabel(self.user_inputs.user_instruction_label2, f"Is {user_input} correct?")

            time.sleep(self.instruction_sleep_time)
            confirmation = self.promptUser(2, True, True)

            if confirmation == "yes":  # User confirmed the input
                return True
            
            elif confirmation == "no":  # User did not confirm input
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
                    self.setLabel(self.user_inputs.user_instruction_label2, f"{invalid_input_message}: {user_input}")
                
                self.setLabel(self.user_inputs.user_instruction_label2, instruction)
                time.sleep(self.instruction_sleep_time)
                user_input = self.promptUser(5, True, True)

        except Exception as e:
            print(f"Error while validating/getting user input: {e}")

    def getUserAction(self):
        # This function will get the user input once they've entered the subgrid phase
        # They will choose a color -> choose a subgrid -> and then be prompted with these options
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

    def handleAction(self, userAction):
        # This function takes an input for what the user wants to do
        # and maps it to a function call
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

    def handle_insert_text(self):
        record_duration = self.getRecordDuration()
        text_input = self.getUserTextInput(record_duration)

        self.command_handler.insert_text(text_input)

    def handle_delete_word(self):
        try:
            while True:
                self.setLabel(self.user_inputs.user_instruction_label2, "What word would you like to delete?")
                time.sleep(self.instruction_sleep_time)

                delete_word = self.promptUser(3, True, True)

                confirmation = self.confirmUserInput(delete_word)

                if confirmation is True:
                    self.command_handler.delete_word(delete_word)
                else:
                    pass

        except Exception as e:
            print(f"Error while getting word to delete: {e}")


    def getRecordDuration(self):
        # This function will continuously prompt the user until they provide a number
        try:
            while True:
                self.setLabel(self.user_inputs.user_instruction_label2, "How long would you like to record for (in seconds)?")
                time.sleep(self.instruction_sleep_time)
                record_duration = self.promptUser(2, True, True)
                record_duration = Commands.convertToInt(record_duration)

                if isinstance(record_duration, int):
                    confirmation = self.confirmUserInput(record_duration)

                    if confirmation:
                        return record_duration

                else:
                    print(f"You must say a number. You said: {record_duration}")
                    self.setLabel(self.feedback_msg.error_label2, f"You must say a number. You said: {record_duration}")

        except Exception as e:
            print(f"Error while gathering record duration: {e}")

    def getUserTextInput(self, record_duration):
        # This function will prompt the user for text based off their record duration
        # It will then confirm the user's text with them
        try:
            while True:
                self.setLabel(self.user_inputs.user_instruction_label2, "What would you like to type?")
                time.sleep(self.instruction_sleep_time)
                text_input = self.promptUser(record_duration, True, True)

                if record_duration > 5:
                    confirmation = self.confirmUserInput(text_input, long_text = True)
                
                else:
                    confirmation = self.confirmUserInput(text_input)

                if confirmation:
                    return text_input

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

    def handle_change_font(self):
        print("get font name, check against valid inputs, run change font function")
        valid_fonts = ["times new roman", "calibri", "arial"]
        instruction = "What font would you like to set to?"
        invalid_input_message = "Invalid font"

        self.setLabel("What font would you like to set to?")
        font_input = self.promptUser(5, True, True)

        font_input = self.validate_general_input(self,
                                                instruction,
                                                invalid_input_message,
                                                valid_fonts,
                                                font_input)
        
        self.command_handler.change_font(font_input)

    def handle_real_time_transcription(self):

        self.setLabel(self.feedback_msg.listening_processing_label1, "Listening...")
        self.text_input = TextInputWindow(self)
        self.text_input.attributes('-topmost', 1)
        transcription = self.command_handler.real_time_text_input()
        self.text_input.destroy()

        time.sleep(2)
        for line in transcription:
            self.command_handler.insert_text(line)
        
        
    def listenForCommands(self):
        # This function should be called as soon as the word ui is launched
        # First, it updates the userInstruction label to let the users know we're first waiting for a command
        #   It will continuously listen until it hears a command
        #   When a command is heard:
        #       return command name
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

                time.sleep(0.25)

        except Exception as e:
            print(f"Error while listening for word commands: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the WordInputValidator class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForCommands)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

class TextInputWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Text Entry Box")
        self.width = 800
        self.height = 450
        self.center_window(self.width, self.height)
        
        

        self.grid_rowconfigure(0, weight = 10)
        self.grid_rowconfigure(1, weight = 1)

        self.grid_columnconfigure(0, weight = 1)

        self.background_color = tk.Label(self, background = "slate gray")
        self.background_color.grid(row = 0, rowspan = 2, column = 0, sticky = "nsew")
        
        self.text_entry = tk.Entry(self)
        self.text_entry["justify"] = "center"
        self.text_entry.grid(row = 0, column = 0, sticky = "nsew")

        
        self.exit_label = tk.Label(self, text = "Say 'exit' when you're done")
        self.exit_label.grid(row = 1, column = 0)


    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    word_window = WordInputValidator("Microsoft Word Menu", (300, 1000))
    word_window.mainloop()