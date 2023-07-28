import time

from source.core.model_interface import *

import tkinter as tk
from tkinter import ttk

import pyautogui

# This class creates the window, and creates objects which create the frames that store widgets
class WordWindow(tk.Tk):
    def __init__(self, title, size):
        super().__init__()

        # Set the starting position so it always appears on furthest right point of screen
        self.start_x_position = self.winfo_screenwidth() - size[0] - 5
        self.start_y_position = 0

        # Main setup (title, geometry, minimum size)
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}+{self.start_x_position}+{self.start_y_position}")
        self.minsize(size[0], size[1])

        self.configure(background = "black")

        # TO-DO - Create an antiquewhite3 ring around the gray, similar to the landing page


        # Create the options labels
        self.user_options = UserOptions(self)

        # Create the user input box, user instruction label
        self.user_inputs = UserInput(self)
        self.user_inputs.input_history_label1["width"] = size[0]
        self.user_inputs.input_history_label1["wraplength"] = size[0] - 5

        # Create the listening label, and error message label
        self.feedback_msg = FeedbackMessages(self)

        # Create the window grid 
        self.grid_rowconfigure((0, 4), weight = 1)

        # Ensure expansion of user history is greater than options labels
        self.grid_rowconfigure(2, weight = 2)



        self.grid_columnconfigure(0, weight = 1)

    def setLabel(self, label, message):
        try:
            label.config(text = message)
            return True

        except Exception as e:
            print(f"Error updating {label} with \"{message}\": {e}")
            return False
        
    def appendNewUserInputHistory(self, message):
        # This function updates the user input history
        # It's meant to be used after every recording, to display what the model has transcripted
        try:
            self.newText = message
            self.currentText = self.user_inputs.input_history_label1.cget("text")
            self.updatedText = self.currentText + "\n" + self.newText
            self.updatedText.capitalize()
            self.user_inputs.input_history_label1.config(text = self.updatedText)
        except Exception as e:
            print(f"Error updating user input history with \"{message}\": {e}")


class UserOptions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background = "slate gray").grid(row = 0, rowspan = 7, column = 0, sticky = "nsew")

        # Places the frame onto the window
        self.grid(row = 0, column = 0, sticky = "nsew")

        # Create the widgets
        self.create_text_options()
        self.layout_text_options()

    # This function will create the labels which store the command keywords
    def create_text_options(self):
        self.user_options_label1 = ttk.Label(self, text = "Options",
                                            font = ("Franklin Gothic Medium", 24),
                                            background = "slate gray")
        
        self.save_file_label2 = ttk.Label(self, text = "Save file",
                                            font = ("Franklin Gothic Medium", 12),
                                            background = "slate gray")
        
        self.tab_label3 = ttk.Label(self, text = "Tab in / indent",
                                        font = ("Franklin Gothic Medium", 12),
                                        background = "slate gray")
        
        self.new_line_label4 = ttk.Label(self, text = "Make new line / new page",
                                            font = ("Franklin Gothic Medium", 12),
                                            background = "slate gray")
        
        self.change_font_label5 = ttk.Label(self, text = "Change font",
                                                font = ("Franklin Gothic Medium", 12),
                                                background = "slate gray")

        self.change_font_size_label6 = ttk.Label(self, text = "Increase / decrease font size",
                                                    font = ("Franklin Gothic Medium", 12),
                                                    background = "slate gray")
        
        self.change_emphasis_label7 = ttk.Label(self, 
                                                    text = "Make my text bold / italic / underlined",
                                                    font = ("Franklin Gothic Medium", 12),
                                                    background = "slate gray")
        
    # This function will grid the text labels created above onto the frame
    def layout_text_options(self):

        # Create the grid
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight = 2)
        self.grid_columnconfigure(0, weight = 1)

        #self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight = 1)
        #self.grid_columnconfigure((0, 1), weight = 1)
        
        self.user_options_label1.grid(row = 0, column = 0, pady = (10, 0))
        self.save_file_label2.grid(row = 1, column = 0, pady = (20, 5))
        self.tab_label3.grid(row = 2, column = 0, pady = 5)
        self.new_line_label4.grid(row = 3, column = 0, pady = 5)
        self.change_font_label5.grid(row = 4, column = 0, pady = 5)
        self.change_font_size_label6.grid(row = 5, column = 0, pady = 5)
        self.change_emphasis_label7.grid(row = 6, column = 0, pady = 5)


class UserInput(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background = "red").grid(row = 0, rowspan = 2, column = 0, sticky = "nsew")

        # Places the frame onto the window
        ttk.Separator(orient = "horizontal").grid(row = 1, column = 0)
        self.grid(row = 2, column = 0, sticky = "nsew")
        ttk.Separator(orient = "horizontal").grid(row = 3, column = 0)

        # Create the widgets
        self.create_input_display()
        self.layout_user_input_display()

    def create_input_display(self):
        self.input_history_label1 = ttk.Label(self, text = "user input history",
                                            font = ("Franklin Gothic Medium", 12),
                                            background = "slate gray",
                                            anchor = "s",
                                            justify = "center"
                                            )

        #self.input_history_label1.configure(padding = "60 60")
        print(self.input_history_label1.configure())
        
        self.user_instruction_label2 = ttk.Label(self, 
                                                    text = "Say 'input text' or a command",
                                                    font = ("Franklin Gothic Medium", 12),
                                                    background = "antiquewhite3",
                                                    anchor = "n",
                                                    justify = "center")
        #self.user_instruction_label2.configure(padding = "20 60")
        
    def layout_user_input_display(self):

        # Create the grid
        self.grid_rowconfigure((0, 1), weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.input_history_label1.grid(row = 0, column = 0, sticky = "ew")
        self.user_instruction_label2.grid(row = 1, column = 0, sticky = "ew")


class FeedbackMessages(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # This label stores no text, simply the background color
        ttk.Label(self, background = "white").grid(row = 0, rowspan = 2, column = 0, sticky = "nsew")

        # Place the frame onnto the window
        self.grid(row = 4, column = 0, sticky = "nsew")

        self.create_feedback_messages()
        self.layout_feedback_messages()


    def create_feedback_messages(self):
        self.listening_processing_label1 = ttk.Label(self, text = "Waiting",
                                                        font = ("Franklin Gothic Medium", 24),
                                                        background = "slate gray")
        
        self.error_label2 = ttk.Label(self, text = "",
                                        font = ("Franklin Gothic Medium", 12),
                                        background = "slate gray",
                                        foreground = "red")
        
    def layout_feedback_messages(self):
        
        # Create the grid
        self.grid_rowconfigure((0, 1), weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.listening_processing_label1.grid(row = 0, column = 0)
        self.error_label2.grid(row = 1, column = 0)
