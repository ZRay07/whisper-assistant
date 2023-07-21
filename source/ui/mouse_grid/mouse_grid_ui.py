from source.core.model_interface import *

from tkinter import *
import pyautogui

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