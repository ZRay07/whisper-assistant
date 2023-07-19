import time
import threading
import pyautogui


# This file stores functionality for commands in mouse grid
# These are things like: left click, double click, right click, etc.

def performClick(mouseGrid, clickType):
    # Exit the mouse grid
    mouseGrid.MouseGridWindow.destroy()
    time.sleep(0.2)

    if clickType == "left":
        pyautogui.leftClick()
        
    elif clickType == "right":
        pyautogui.rightClick()

    elif clickType == "double":
        pyautogui.doubleClick()

    # Bring back the main window
    mouseGrid.mouseGridWindow.deiconify()

    return f"Successfully {clickType} clicked"

def enterTextInput(mouseGrid, textInput):
    # Exit the mouse grid
    mouseGrid.MouseGridWindow.destroy()
    time.sleep(1)

    # Type!
    pyautogui.leftClick()
    pyautogui.write(textInput, interval = 0.25)

# Function to start the typing thread
# This function is called to run the text input function
# I was having errors where the listening was taking over before the type function executed
#def enterTextInputThread(mouseGrid, textInput):
#    thread = threading.Thread(target = enterTextInput(mouseGrid, textInput))
#    thread.daemon = True  # Set the thread as a daemon thread
#    thread.start()







#            elif (self.userChoice == "Type something." or self.userChoice == "type something"): # or self.userChoice == "you"):
#                self.MouseGridWindow.wm_state("iconic")
#                time.sleep(0.2)
#                pyautogui.leftClick()
#
#                print("Speak what you would like to type.")
#                time.sleep(3)
#
#                microphone.record(10)
#                self.prediction = whisper.use_model(RECORD_PATH)
#
#                pyautogui.write(self.prediction, interval=0.25)
#
#            elif (self.userChoice == "Key press." or self.userChoice == "key press"):
#                print("Which key would you like to press?")
#                self.prediction = recordAndUseModel()
#
#            elif (self.userChoice == "Get more specific." or self.userChoice == "get more specific"):
#                print("Get more specific...")
#                self.getMoreSpecific()
