import time
import tkinter as tk
from tkinter import ttk

from source.core.model_interface import *


class WordWindow(tk.Tk):
    # This class creates the window, and creates objects which create the frames that store widgets
    def __init__(self, title, size):
        super().__init__()

        # Set the starting position so it always appears on furthest right point of screen
        self.start_x_position = self.winfo_screenwidth() - size[0] - 5
        self.start_y_position = 0

        # Main setup (title, geometry, minimum size)
        self.title(title)
        self.geometry(
            f"{size[0]}x{size[1]}+{self.start_x_position}+{self.start_y_position}"
        )
        self.minsize(150, 450)

        # TO-DO - Create an antiquewhite3 ring around the gray, similar to the landing page

        # Create the options labels
        self.user_options = UserOptions(self)

        # Create the user input box, user instruction label
        self.user_inputs = UserInput(self)
        self.user_inputs.lbl_input_history["wraplength"] = size[0] - 12
        self.user_inputs.lbl_user_instruction["wraplength"] = size[0] - 12

        # Create the listening label, and error message label
        self.feedback_msg = FeedbackMessages(self)

        # Create the window grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1, minsize=self.feedback_msg.winfo_height())
        self.grid_columnconfigure(0, weight=1)

    def set_label(self, label, message):
        try:
            label.config(text=message)

            # If the label is the error label, schedule a function to clear it after 10000 milliseconds (10 seconds)
            if label == self.feedback_msg.lbl_error:
                self.after(10000, lambda: self.clear_error_label())

            return True

        except Exception as e:
            print(f'Error updating {label} with "{message}": {e}')
            return False

    def clear_error_label(self):
        # Clear the error label text
        self.feedback_msg.lbl_error.config(text="")

    def append_user_input_history(self, message):
        # This function updates the user input history
        # It's meant to be used after every recording, to display what the model has transcripted
        def count_lines(label_text):
            lines = label_text.split("\n")
            return len(lines)

        try:
            self.new_text = message
            self.current_text = self.user_inputs.lbl_input_history.cget("text")
            self.updated_text = self.current_text + "\n" + self.new_text
            self.updated_text.capitalize()

            line_count = count_lines(self.updated_text)

            if line_count > 12:
                lines = self.updated_text.split("\n")
                new_lines = lines[1:]
                self.updated_text = "\n".join(new_lines)

            self.user_inputs.lbl_input_history.config(text=self.updated_text)

        except Exception as e:
            print(f'Error updating user input history with "{message}": {e}')


class UserOptions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background="slate gray").grid(
            row=0, rowspan=10, column=0, sticky="nsew"
        )

        # Places the frame onto the window
        self.grid(row=0, column=0, sticky="nsew")

        # Create the widgets
        self.create_text_options()
        self.layout_text_options()

    # This function will create the labels which store the command keywords
    def create_text_options(self):
        self.lbl_user_options = ttk.Label(
            self,
            text="Options",
            font=("Franklin Gothic Medium", 24),
            background="slate gray",
        )

        self.lbl_insert_text = ttk.Label(
            self,
            text="Insert text",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_save_file = ttk.Label(
            self,
            text="Save and name file / save file",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_tab = ttk.Label(
            self,
            text="Tab in / indent",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_new_line = ttk.Label(
            self,
            text="Make new line / new page",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_change_font = ttk.Label(
            self,
            text="Change font",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_change_font_size = ttk.Label(
            self,
            text="Increase / decrease font size",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_change_emphasis = ttk.Label(
            self,
            text="Make my text bold / italic / underlined",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_change_script = ttk.Label(
            self,
            text="Make my text subscript / superscript",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

        self.lbl_delete_word = ttk.Label(
            self,
            text="Delete a word",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
        )

    # This function will grid the text labels created above onto the frame
    def layout_text_options(self):
        # Create the grid
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure((2, 3, 4, 5, 6, 7, 8), weight=2)
        self.grid_columnconfigure(0, weight=1)

        self.lbl_user_options.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.lbl_insert_text.grid(row=1, column=0, pady=(10, 5))
        self.lbl_save_file.grid(row=2, column=0, pady=5)
        self.lbl_tab.grid(row=3, column=0, pady=5)
        self.lbl_new_line.grid(row=4, column=0, pady=5)
        self.lbl_change_font.grid(row=5, column=0, pady=5)
        self.lbl_change_font_size.grid(row=6, column=0, pady=5)
        self.lbl_change_emphasis.grid(row=7, column=0, pady=5)
        self.lbl_change_script.grid(row=8, column=0, pady=5)
        self.lbl_delete_word.grid(row=9, column=0, pady=5)


class UserInput(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background="slate gray").grid(
            row=0, rowspan=3, column=0, sticky="nsew"
        )

        self.grid(row=1, column=0, sticky="nsew")
        self.grid_propagate(False)

        # Create the widgets
        self.create_input_display()
        self.layout_user_input_display()

    def create_input_display(self):
        self.lbl_input_history = ttk.Label(
            self,
            text="Input history",
            font=("Franklin Gothic Medium", 12),
            background="azure3",
            anchor="s",
            justify="center",
        )

        self.lbl_user_instruction = ttk.Label(
            self,
            text="Say a command",
            font=("Franklin Gothic Medium", 12),
            background="AntiqueWhite3",
            anchor="center",
            justify="center",
        )

    def layout_user_input_display(self):
        # Create the grid
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(
            1, weight=1, minsize=self.lbl_user_instruction.winfo_height()
        )
        self.grid_columnconfigure(0, weight=1)

        self.lbl_input_history.grid(row=0, column=0, sticky="sew", padx=10)
        self.lbl_user_instruction.grid(row=1, column=0, sticky="nsew", padx=10)


class FeedbackMessages(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background="slate gray").grid(
            row=0, rowspan=2, column=0, sticky="nsew"
        )

        # Place the frame onnto the window
        self.grid(row=2, column=0, sticky="nsew")

        self.create_feedback_messages()
        self.layout_feedback_messages()

    def create_feedback_messages(self):
        self.lbl_listening_processing = ttk.Label(
            self,
            text="Waiting",
            font=("Franklin Gothic Medium", 24),
            background="slate gray",
        )

        self.lbl_error = ttk.Label(
            self,
            text="",
            font=("Franklin Gothic Medium", 12),
            background="slate gray",
            foreground="red",
        )

    def layout_feedback_messages(self):
        # Create the grid
        self.grid_rowconfigure(
            (0, 1), weight=1, minsize=self.lbl_listening_processing.winfo_height()
        )
        self.grid_columnconfigure(0, weight=1)

        self.lbl_listening_processing.grid(row=0, column=0)
        self.lbl_error.grid(row=1, column=0)
