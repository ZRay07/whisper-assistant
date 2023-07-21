import time
import threading
import pyautogui


# This file stores functionality for commands in mouse grid
# These are things like: left click, double click, right click, etc.

def performClick(mouseGrid, clickType):
    # Minimize the mouse grid so we can click on the windows behind it
    mouseGrid.MouseGridWindow.iconify()
    time.sleep(0.1)

    if clickType == "left":
        pyautogui.leftClick()
        
    elif clickType == "right":
        pyautogui.rightClick()

    elif clickType == "double":
        pyautogui.doubleClick()

    # Bring back the window
    mouseGrid.MouseGridWindow.destroy()

    return f"Successfully {clickType} clicked"

def enterTextInput(mouseGrid, textInput):
    # Minimze the mouse grid
    mouseGrid.MouseGridWindow.iconify()
    time.sleep(0.2)

    # Type!
    pyautogui.leftClick()
    pyautogui.write(textInput, interval = 0.05)

    # Exit the mouse grid
    mouseGrid.MouseGridWindow.destroy()

    return f"Successfully typed: {textInput}"

def enterKeypressInput(mouseGrid, keyInput):
    # Minimize the mouse grid
    mouseGrid.MouseGridWindow.iconify()
    time.sleep(0.2)

    # Enter key pres
    pyautogui.leftClick()
    pyautogui.press(keyInput)

    # Exit the mouse grid
    mouseGrid.MouseGridWindow.iconify()

    return f"Successfully pressed {keyInput}"

def moveCursorSlightly(direction):
    if (direction == "left"):
        pyautogui.move(-15, 0, 0.2)

    elif (direction == "right"):
        pyautogui.move(15, 0, 0.2)

    elif (direction == "up"):
        pyautogui.move(0, -15, 0.2)

    elif (direction == "down"):
        pyautogui.move(0, 15, 0.2)
