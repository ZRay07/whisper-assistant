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
        self.root.geometry("1100x620+480+200")

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

        self.go_button = Button(self.cmd_bar, text = "GO - Open Application", command = openApplication, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.no_button = Button(self.cmd_bar, text = "NO - Close Application", command = closeApplication, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.up_button = Button(self.cmd_bar, text = "UP - Scroll Up", command = pyautogui.scroll(10), activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.down_button = Button(self.cmd_bar, text = "DOWN - Scroll Down", command = pyautogui.scroll(-10), activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.right_button = Button(self.cmd_bar, text = "RIGHT - Set Volume", command = setVolume, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.yes_button = Button(self.cmd_bar, text = "YES - Navigate Mouse + Keyboard", command = mouseControl, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.left_button = Button(self.cmd_bar, text = "LEFT - Email sign-in", command = sign_in, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.stop_button = Button(self.cmd_bar, text = "STOP - Exit", command = self.root.quit, activebackground = "green", activeforeground = "skyblue", relief = RAISED)

        # Place the buttons in the frame
        self.go_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.no_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.up_button.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.down_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.right_button.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.yes_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.left_button.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.stop_button.grid(row = 7, column = 0, padx = 10, pady = 10)

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
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = recordAndUseModel)
        self.record_button.grid(row = 1, column = 0, padx = 10, pady = 10)


def recordAndUseModel():
    Record()

    confidenceValues, greatestPrediction = use_model(audio_path)

    commandExec(greatestPrediction)

class mouseControl():
    def __init__(self):
        print("***Mouse Control***")

        self.userChoiceFlag = 0

        # Open a new window
        self.mouseGrid = Tk()

        # Make this window transparent
        self.mouseGrid.attributes("-alpha", 0.5, "-fullscreen", TRUE)

        #mouseGrid.geometry("1919x1079")

        self.screenHeight = self.mouseGrid.winfo_screenheight()
        self.screenWidth = self.mouseGrid.winfo_screenwidth()

        # Make 9 frames (3 * 3 grid)
        # One for each portion of the grid
        self.a1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "red")
        self.a1.grid(row = 0, column = 0)
        self.a1.grid_propagate(False)

        self.a2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "green")
        self.a2.grid(row = 1, column = 0, padx = 0, pady = 0)
        self.a2.grid_propagate(False)

        self.a3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "blue")
        self.a3.grid(row = 2, column = 0, padx = 0, pady = 0)
        self.a3.grid_propagate(False)

        self.b1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "purple")
        self.b1.grid(row = 0, column = 1, padx = 0, pady = 0)
        self.b1.grid_propagate(False)

        self.b2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "orange")
        self.b2.grid(row = 1, column = 1, padx = 0, pady = 0)
        self.b2.grid_propagate(False)

        self.b3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "white")
        self.b3.grid(row = 2, column = 1, padx = 0, pady = 0)
        self.b3.grid_propagate(False)

        self.c1 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "black")
        self.c1.grid(row = 0, column = 2, padx = 0, pady = 0)
        self.c1.grid_propagate(False)

        self.c2 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "cyan")
        self.c2.grid(row = 1, column = 2, padx = 0, pady = 0)
        self.c2.grid_propagate(False)

        self.c3 = Frame(self.mouseGrid, width = self.screenWidth / 3, height = self.screenHeight / 3, borderwidth = 5, relief = "raised", bg = "grey")
        self.c3.grid(row = 2, column = 2, padx = 0, pady = 0)
        self.c3.grid_propagate(False)

        self.inputBox = Text(self.c1, height = 1, width = 5, border = 2, relief = "solid")
        self.inputBox.grid(row = 0, column = 0,sticky = NE)

        self.submit_button = Button(self.c1, text = "Submit", command = self.getUserChoice, border = 2, relief = "solid")
        self.submit_button.grid(row = 1, column = 0, sticky = NE)

        self.mouseGrid.mainloop()

    def getUserChoice(self):
        self.userChoice = self.inputBox.get(1.0, "end-1c")
        self.displaySubgrid()

    def displaySubgrid(self):
        print("Displaying subgrid")

        if (self.userChoice == "A1"):
            self.subgrid = Canvas(self.a1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2, self.screenHeight / 3 / 2)
            #self.moveCursorWithArrowKeys()
        
        elif (self.userChoice == "A2"):
            self.subgrid = Canvas(self.a2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2, self.screenHeight / 3 / 2 + self.screenHeight / 3)
            #self.moveCursorWithArrowKeys()

        elif (self.userChoice == "A3"):
            self.subgrid = Canvas(self.a3, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3)
            #self.moveCursorWithArrowKeys()

        elif (self.userChoice == "B1"):
            self.subgrid = Canvas(self.b1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2)
            self.moveCursorWithArrowKeys()

        elif (self.userChoice == "B2"):
            self.subgrid = Canvas(self.b2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2 + self.screenHeight / 3)
            self.moveCursorWithArrowKeys()

        elif (self.userChoice == "B3"):
            self.subgrid = Canvas(self.b3, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + self.screenWidth / 3, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3)
            self.moveCursorWithArrowKeys()

        elif (self.userChoice == "C1"):
            self.subgrid = Canvas(self.c1, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2)
            self.moveCursorWithArrowKeys()

        elif (self.userChoice == "C2"):
            self.subgrid = Canvas(self.c2, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2 + self.screenHeight / 3)
            self.moveCursorWithArrowKeys()

        elif (self.userChoice == "C3"):
            self.subgrid = Canvas(self.c3, width = self.screenWidth / 3, height = self.screenHeight / 3)
            pyautogui.moveTo(self.screenWidth / 3 / 2 + 2 * self.screenWidth / 3, self.screenHeight / 3 / 2 + 2 * self.screenHeight / 3)
            self.moveCursorWithArrowKeys()

        # Place the canvas onto user choice location
        self.subgrid.grid(padx = 0, pady = 0)

        # Draw horizontal lines
        self.subgrid.create_line(0, self.screenHeight / 9, self.screenWidth / 3, self.screenHeight / 9, width = 5)  
        self.subgrid.create_line(0, self.screenHeight * 2 / 9, self.screenWidth / 3, self.screenHeight * 2 / 9, width = 5)

        # Draw vertical lines
        self.subgrid.create_line(self.screenWidth / 9, 0, self.screenWidth / 9, self.screenHeight / 3, width = 5)
        self.subgrid.create_line(self.screenWidth * 2 / 9, 0, self.screenWidth * 2 / 9, self.screenHeight / 3, width = 5)

    def moveToInnerPosition(self):
        print("***Type 1-9 to move to an inner grid position***")

    def moveCursorWithArrowKeys(self):
        while True:
            try: 
                if keyboard.is_pressed('w'):
                    print("moving cursor up...")
                    pyautogui.moveRel(x = 0, y = -10)

                elif keyboard.is_pressed('a'):
                    print("moving cursor left...")
                    pyautogui.moveRel(x = -10, y = 0)

                elif keyboard.is_pressed('s'):
                    print("moving cursor down...")
                    pyautogui.moveRel(x = 0, y = 10)

                elif keyboard.is_pressed('d'):
                    print("moving cursor right...")
                    pyautogui.moveRel(x = 10, y = 0)
            except:
                break       # anything other than wasd will break out the loop
    

if __name__ == '__main__':
    mainScreen()

