from tkinter import *
from source.core.command_module import *
from source.core.model_interface import *
import keyboard

# The first screen to be displayed to users
class mainScreen:
    def __init__(self):
        # Create root window
        self.root = Tk()
        self.root.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.root.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.root.config(bg = "skyblue")     # set the background color

        # Set the starting size of the window and its location
        self.root.geometry("1100x700+480+200")

        self.drawRightFrame()
        self.drawLeftFrame()
        self.root = mainloop()

    def drawLeftFrame(self):
        # Create left frame
        self.left_frame = Frame(self.root, width = 315, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady = 10)       # Places the frame onto the window

        # Adding image to the left hand frame
        self.mountainImage = PhotoImage(file = "mountain3.gif")
        self.small_image = self.mountainImage.subsample(3 , 3)
        Label(self.left_frame, image = self.small_image).grid(row = 0, column = 0, padx = 10, pady = 10)

        # Label the left hand frame
        self.cmd_label = Label(self.left_frame, text = "Speech Commands", font = "times 18", bg = "white")
        self.cmd_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        # Add speech commands below label
        # Use buttons so we can use the GUI
        self.cmd_bar = Frame(self.left_frame, width = 315, height = 300, bg = "white")
        self.cmd_bar.grid(row = 2, column = 0)

        self.openApp_button = Button(self.cmd_bar, text = "Open Application", command = openApplication, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.closeApp_button = Button(self.cmd_bar, text = "Close Application", command = closeApplication, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.scrollUp_button = Button(self.cmd_bar, text = "Scroll Up", command = pyautogui.scroll(10), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.scrollDown_button = Button(self.cmd_bar, text = "Scroll Down", command = pyautogui.scroll(-10), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.setVol_button = Button(self.cmd_bar, text = "Set Volume", command = setVolume, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.mouseControl_button = Button(self.cmd_bar, text = "Navigate Mouse and Keyboard", bg = "light grey", command = mouseControl, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.emailSignIn_button = Button(self.cmd_bar, text = "Email sign-in", command = sign_in, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.exit_button = Button(self.cmd_bar, text = "Exit", command = self.root.quit, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)

        # Place the buttons in the frame
        self.openApp_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.closeApp_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.scrollUp_button.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.scrollDown_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.setVol_button.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.mouseControl_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.emailSignIn_button.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.exit_button.grid(row = 7, column = 0, padx = 10, pady = 10)

    def drawRightFrame(self):
        # Create right frame
        self.right_frame = Frame(self.root, width = 750, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.right_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Ensure the frame does not shrink to fit widget size
        self.right_frame.grid_propagate(False)

        # Label the right frame
        self.sherpa_label = Label(self.right_frame, text = "Welcome to S.H.E.R.P.A.", font = "Times 20", bg = "white")
        self.sherpa_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        # Add record button
        # *** in the future -> activate record by speaking a keyword
        self.record_button = Button(self.right_frame, text = "When ready to record, say [keyword]", font = "Times 14",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.recordAndUseModel)
        self.record_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.transcribedLabel = StringVar()
        self.transcribedLabel.set("Transcribed speech will appear here.\n\n\n\n")

        # Add a transcription box
        self.transcription_label = Label(self.right_frame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.transcribedLabel, wraplength = 200)
        self.transcription_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Add a transcribe button
        self.transcribe_button = Button(self.right_frame, text = "Transcribe", font = "Times 14",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.transcribeSpeech)
        self.transcribe_button.grid(row = 1, column = 1, padx = 10, pady = 5)

        self.recordDurationLabel = StringVar()
        self.recordDurationLabel.set("Record Duration")

        self.recordDuration_label = Label(self.right_frame, height = 1, width = 30, bg = "light cyan", relief = "solid", textvariable = self.recordDurationLabel, wraplength = 200)
        self.recordDuration_label.grid(row = 2, column = 1, padx = 10, pady = 10)

    def recordAndUseModel(self):
        microphone.record(3)
        self.prediction = whisper.use_model(RECORD_PATH)

        print("Prediction: " + self.prediction)

        commandExec(self.prediction)

    def transcribeSpeech(self):
        # TO-DO: Figure out a way to ask how long the user would like to record for

        #self.recordDurationLabel.set("How long would you like to record for? (in seconds)")

        #microphone.record(3)
        #self.prediction = whisper.use_model(RECORD_PATH)
        #self.recordDurationLabel.set(self.prediction)

        microphone.record(15)   #int(self.prediction))
        self.prediction = whisper.use_model(RECORD_PATH)

        self.transcribedLabel.set(self.prediction)
         

if __name__ == '__main__':
    mainScreen()

