from tkinter import * # Import Library
from tkinter import ttk # Import Other Parts of Library

# **Change buttons to labels to avoid inputting clicks with mouse** 

# Define New Confirmation Window
def openConfirmationWindow():
    newWindow = Toplevel(screen) # Record Window Will Open on Top of Previous 
    newWindow.title("Confirmation") # Titles New Window
    newWindow.geometry("1920x1080") # Set Window Size
    message = Label(newWindow, text = "Program detected the following command:", font=('Times 20')) # Create Label
    message.place(relx = 0.5, rely = 0.25, anchor = N) # Places Label
    #place detected word here
    yesno = Label(newWindow, text = "Is this the outcome you requested?\n Say 'Yes' or 'No'", font=('Times 20')) # Create Label
    yesno.place(relx = 0.5, rely = 0.50, anchor = N) # Places Label
    yes = Button(newWindow, text = "Yes", command=lambda: [Yes(),newWindow.destroy()], font=('Times 14'), width=50, height=5, bg="green", compound=LEFT, relief=RAISED)
    yes.place(relx = 0.25, rely = 0.75, anchor = S) # Places Speak Button
    no = Button(newWindow, text = "No",command=lambda: [No(), newWindow.destroy()], font=('Times 14'), width=50, height=5, bg="red", compound=LEFT, relief=RAISED)
    no.place(relx = 0.75, rely = 0.75, anchor = S)
    
def countdown(count):
    # change text in label        
    label['text'] = count
    if count > 0:
        # call countdown again after 1000ms (1s)
        screen.after(1000, countdown, count-1)

# Define Recording Function
def Record():
    #Start recording audio and runs through ASR, finds appropriate command
    print("User says command")
    openConfirmationWindow()
    
# Define Yes Function
def Yes():
    print("Executes program")
    ToggleLoop()
    
# Define No Function
def No():
    print("Loops back to recording section")
    ToggleLoop()
    
# Define Toggle Function
def ToggleRecord():
    speak_label.destroy()
    toggle = Button(screen, text = "Recording", font=('Times 14'), width=50, height=5, bg="yellow", compound=LEFT, relief=RAISED) # Create Start Button
    toggle.place(relx = 0.5, rely = 0.65, anchor = S) # Place Toggle Button

# Define Other Toggle Function
def ToggleLoop():
    speak_label = Button(screen, text = "To Begin Recording Say 'Yes'.", command=lambda: [Record(), ToggleRecord()], font=('Times 14'), width=50, height=5, bg="green", compound = LEFT, relief=RAISED) # Create Start Button
    speak_label.place(relx = 0.5, rely = 0.65, anchor = S) # Places Speak Button
        
# Creates Main Screen/window with Initial Buttons
screen = Tk()
screen.geometry("1920x1080") # Sets Window Size
screen.title("S.H.E.R.P.A (Super Helpful Enginer Recognizing People's Audio)") #Title of Window
screen.resizable(True, True) # Enable Resizeablity 
begin = Label(screen, text = "Recording will begin in", font=('Times 20'))
begin.place(relx=0.5, rely=0.375, anchor = S)
label = Label(screen, font=('Times 20'))
label.place(relx = 0.5, rely = 0.4)   
countdown(5)
welcome = Label(screen, text = "Welcome To S.H.E.R.P.A!", font=('Times 20')) # Creates Welcome Label
welcome.place(relx = 0.5, rely = 0.25, anchor = S) # Place Welcome Label at Set Location
quit_label = Button(screen, text = "To Quit Program Say 'No'.", command=screen.destroy, font=('Times 14'), width=50, height=5, bg="red", relief=RAISED) # Create Quit Button
quit_label.place(relx = 0.5, rely = 0.75, anchor = N) # Places Quit Button
speak_label = Button(screen, text = "To Begin Recording Say 'Yes'.", command=lambda: [Record(), ToggleRecord()], font=('Times 14'), width=50, height=5, bg="green", compound = LEFT, relief=RAISED) # Create Start Button
speak_label.place(relx = 0.5, rely = 0.65, anchor = S) # Places Speak Button
screen.mainloop() # Loops Code
