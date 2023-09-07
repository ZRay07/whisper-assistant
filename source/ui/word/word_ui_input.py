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
    def __init__(self, title, size, document_name="DefaultDocumentName"):
        super().__init__(title, size)

        self.document_name = document_name
        self.instruction_sleep_time = 2

        self.command_handler = WordCommandHandler(self)

        self.valid_commands = {
            "insert text": self.handle_insert_text,
            "make real time transcription": self.handle_real_time_transcription,
            "make real-time transcription": self.handle_real_time_transcription,
            "save and name file": self.command_handler.save_and_name_file,
            "save file": self.command_handler.save_file,
            "tab in": self.command_handler.tab_text,
            "indent": self.command_handler.tab_text,
            "make new line": self.command_handler.new_line,
            "make new page": self.command_handler.new_page,
            "change font": self.handle_change_font,  # TO-DO: add commands for below
            "increase font size": self.command_handler.increase_font_size,  # Justification, lists (bullet and numbered)
            "decrease font size": self.command_handler.decrease_font_size,  # highlight, change font color
            "make my text bold": self.command_handler.make_font_bold,
            "make my text italic": self.command_handler.make_font_italic,
            "make my text underlined": self.command_handler.make_font_underline,
            "change to title style": self.command_handler.make_title_style,
            "change to heading one style": self.command_handler.make_heading1_style,
            "change to heading two style": self.command_handler.make_heading2_style,
            "change to normal style": self.command_handler.make_normal_style,
            "make my text subscript": self.command_handler.make_subscript,
            "make my text superscript": self.command_handler.make_superscript,
            "delete a word": self.handle_delete_word,
            "mouse control": self.command_handler.mouse_control,
        }  # used in listen_for_commands
        self.attributes("-topmost", True)
        self.start_listening_thread()

    def prompt_user(self, recordDuration, removePunctuation, makeLowerCase):
        #####
        # This function is used when we need to prompt the user for additional voice inputs
        # If removePunctuation is true when you call it, it removes trailing punctuation.
        # If makeLowerCase is true when you call it, it makes the output string lowercase
        #####
        try:
            self.set_label(self.feedback_msg.lbl_listening_processing, "Listening...")
            microphone.record(recordDuration)
            self.set_label(self.feedback_msg.lbl_listening_processing, "Processing...")
            self.user_input = whisper.use_model(RECORD_PATH)
            self.set_label(self.feedback_msg.lbl_listening_processing, "Waiting...")

            if removePunctuation:
                self.user_input = self.user_input.rstrip(string.punctuation)

            if makeLowerCase:
                self.user_input = self.user_input.lower()

            # I've found the default if there is no sound is to predict "you"
            # In this case, I think it's best to interpret the input as silence and not update the user input history
            if self.user_input != "you":
                self.append_user_input_history(self.user_input)

            return self.user_input

        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False

    def confirm_user_input(self, user_input, long_text=False):
        #####
        # This function will specifically wait for the user to reply "yes" or "no"
        #####
        while True:
            if long_text:
                self.set_label(
                    self.user_inputs.lbl_user_instruction, "Is above correct?"
                )
            else:
                self.set_label(
                    self.user_inputs.lbl_user_instruction, f"Is {user_input} correct?"
                )

            time.sleep(self.instruction_sleep_time)
            confirmation = self.prompt_user(2, True, True)

            if confirmation == "yes":  # User confirmed the input
                return True

            elif confirmation == "no":  # User did not confirm input
                return None

            else:
                pass

    def validate_general_input(
        self, instruction, invalid_input_message, valid_input, user_input=None
    ):
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
                    self.set_label(
                        self.user_inputs.lbl_user_instruction,
                        f"{invalid_input_message}: {user_input}",
                    )

                self.set_label(self.user_inputs.lbl_user_instruction, instruction)
                time.sleep(self.instruction_sleep_time)
                user_input = self.prompt_user(5, True, True)

        except Exception as e:
            print(f"Error while validating/getting user input: {e}")

    def handle_insert_text(self):
        record_duration = self.get_record_duration()
        text_input = self.get_user_text_input(record_duration)

        if text_input[:-1] == ".":
            text_input = text_input + " "

        else:
            text_input = text_input + ". "

        self.command_handler.insert_text(text_input)

    def handle_delete_word(self):
        try:
            while True:
                self.set_label(
                    self.user_inputs.lbl_user_instruction,
                    "What word would you like to delete?",
                )
                time.sleep(self.instruction_sleep_time)

                delete_word = self.prompt_user(3, True, True)

                confirmation = self.confirm_user_input(delete_word)

                if confirmation is True:
                    self.command_handler.delete_word(delete_word)
                else:
                    pass

        except Exception as e:
            print(f"Error while getting word to delete: {e}")

    def get_record_duration(self):
        # This function will continuously prompt the user until they provide a number
        try:
            while True:
                self.set_label(
                    self.user_inputs.lbl_user_instruction,
                    "How long would you like to record for (in seconds)?",
                )
                time.sleep(self.instruction_sleep_time)
                record_duration = self.prompt_user(2, True, True)
                record_duration = Commands.convertToInt(record_duration)

                if isinstance(record_duration, int):
                    confirmation = self.confirm_user_input(record_duration)

                    if confirmation:
                        return record_duration

                else:
                    print(f"You must say a number. You said: {record_duration}")
                    self.set_label(
                        self.feedback_msg.lbl_error,
                        f"You must say a number. You said: {record_duration}",
                    )

        except Exception as e:
            print(f"Error while gathering record duration: {e}")

    def get_user_text_input(self, record_duration):
        # This function will prompt the user for text based off their record duration
        # It will then confirm the user's text with them
        try:
            while True:
                self.set_label(
                    self.user_inputs.lbl_user_instruction,
                    "What would you like to type?",
                )
                time.sleep(self.instruction_sleep_time)
                text_input = self.prompt_user(record_duration, True, False)

                if record_duration > 5:
                    confirmation = self.confirm_user_input(text_input, long_text=True)

                else:
                    confirmation = self.confirm_user_input(text_input)

                if confirmation:
                    return text_input

        except Exception as e:
            print(f"Error while gathering text input: {e}")

    def handle_change_font(self):
        print("get font name, check against valid inputs, run change font function")
        valid_fonts = ["times new roman", "calibri", "arial"]
        instruction = "What font would you like to set to?"
        invalid_input_message = "Invalid font"

        self.set_label(
            self.user_inputs.lbl_user_instruction, "What font would you like?"
        )
        font_input = self.prompt_user(5, True, True)

        font_input = self.validate_general_input(
            instruction, invalid_input_message, valid_fonts, font_input
        )

        self.command_handler.change_font(font_input)

    def handle_real_time_transcription(self):
        self.set_label(self.feedback_msg.lbl_listening_processing, "Listening...")

        self.text_input = TextInputWindow(self)
        self.text_input.attributes("-topmost", 1)
        transcription = self.command_handler.real_time_text_input()
        self.text_input.destroy()

        time.sleep(2)

        input_text = ". ".join(transcription).rstrip(".") + ". "
        self.command_handler.insert_text(input_text)

    def listen_for_commands(self):
        # This function should be called as soon as the word ui is launched
        # First, it updates the userInstruction label to let the users know we're first waiting for a command
        #   It will continuously listen until it hears a command
        #   When a command is heard:
        #       return command name
        time.sleep(1)
        try:
            while True:
                self.set_label(
                    self.user_inputs.lbl_user_instruction,
                    "Say 'insert text' or a command",
                )

                self.command_choice = self.prompt_user(5, True, True)

                if self.command_choice in self.valid_commands:
                    # Get the corresponding function from the dictionary
                    selected_command = self.valid_commands[self.command_choice]

                    # Call the selected command
                    selected_command()

                elif self.command_choice == "exit":
                    self.destroy()
                    break

                time.sleep(0.25)

        except Exception as e:
            print(f"Error while listening for word commands: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the WordInputValidator class, allowing it to run concurrently with the GUI.
    def start_listening_thread(self):
        thread = threading.Thread(target=self.listen_for_commands)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()


class TextInputWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Text Entry Box")
        self.width = 800
        self.height = 450
        self.center_window(self.width, self.height)

        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.background_color = tk.Label(self, bg="slate gray")
        self.background_color.grid(row=0, rowspan=2, column=0, sticky="nsew")

        self.user_text = tk.Label(self, bg="slate gray", text="")
        self.user_text.grid(row=0, column=0, sticky="nsew")
        self.user_text["justify"] = "center"
        self.user_text.config(wraplength=self.width - 20)

        self.lbl_exit = tk.Label(
            self,
            text="Say 'exit' when you're done",
            font=("Franklin Gothic Medium", 24),
            bg="AntiqueWhite3",
        )
        self.lbl_exit.grid(row=1, column=0, sticky="sew")

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    word_window = WordInputValidator("Microsoft Word Menu", (300, 1000))
    word_window.mainloop()
