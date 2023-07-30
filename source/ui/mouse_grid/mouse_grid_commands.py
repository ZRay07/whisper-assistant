import time
import pyautogui


# This file stores functionality for commands in mouse grid
# These are things like: left click, double click, right click, etc.
    # The input to this function comes from getInnerGridInput()
    # The validation function guarantees that the variable being passed will be an int from 1-9
def moveToInnerPosition(mouseGrid, innerGridChoice):
    try:
        movements = {
            1: (-(mouseGrid.screenWidth / 9), -(mouseGrid.screenHeight / 9)),
            2: (0, -(mouseGrid.screenHeight / 9)),
            3: ((mouseGrid.screenWidth / 9), -(mouseGrid.screenHeight / 9)),
            4: (-(mouseGrid.screenWidth / 9), 0),
            # 5 is the center position
            6: ((mouseGrid.screenWidth / 9), 0),
            7: (-(mouseGrid.screenWidth / 9), (mouseGrid.screenHeight / 9)),
            8: (0, (mouseGrid.screenHeight / 9)),
            9: ((mouseGrid.screenWidth / 9), (mouseGrid.screenHeight / 9))
        }

        # Check the dictionary for a matching number
        # If matching number found,
        #   then set "movement" to the two x and y positions stored in the grid
        if innerGridChoice in movements:
            movement = movements[innerGridChoice]
            print(f"Moving to {innerGridChoice}")
            pyautogui.move(*movement, 0.5)  # The * operator just unpacks the 2 x and y positions
        
        else:
            raise ValueError("Invalid inner grid choice")
    
    except ValueError as ve:
        print(ve)

    except Exception as e:
        print(f"Error occured while selecting inner grid: {e}")

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

    # Destroy the window
    mouseGrid.MouseGridWindow.destroy()

    return f"Successfully {clickType} clicked"

def enterTextInput(mouseGrid, textInput):
    # Minimze the mouse grid
    mouseGrid.MouseGridWindow.iconify()
    time.sleep(0.2)

    # Type!
    pyautogui.doubleClick()
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
