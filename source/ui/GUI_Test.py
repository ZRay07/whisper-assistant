from tkinter import * # Import Library
from tkinter import ttk # Import Other Parts of Library
import time

from scipy.io.wavfile import write
from pydub import AudioSegment
from scipy.io.wavfile import read as read_wav
import numpy as np
import wave
import sys
import sounddevice as sd
import tensorflow as tf
import keras as k
from keras import layers
from keras import models
from scipy.io import wavfile
from scipy import signal
import librosa
# **Change buttons to labels to avoid inputting clicks with mouse** 
class_ids_list = (['down','go', 'left', 'no', 'right', 'stop', 'up', 'yes'])
class_id = ['d','g','l','n','r','s','u','y']
count = 5
model_model = tf.saved_model.load('C:/Users/cohent1/Anaconda3/SD/prometheus')
# Define New Confirmation Window

#Use the model
def use_model(path):
    fin = model_model(tf.constant(str(path)))
    run_up = fin['predictions'].numpy()
    out = np.array2string(fin['class_names'].numpy())
    return run_up, out

#Pull the answer and index from pred list
def veri_n_ind(out):
    for i in range(len(class_id)):
        if out[3] == class_id[i]:
            count = i
            ans = class_ids_list[i]
    return count, ans

#Pull the index of the second most likely option
#The input of this should be an array like the following:
#array = list(run_up[0])

def secd_lrg_num(arr):
    large = -10
    sec_large = -10
  
    for i in range(len(arr)):
        large = max(large, arr[i])
    
    for i in range(len(arr)):
        if (arr[i] != large):
            sec_large = max(sec_large, arr[i])
    for i in range(len(arr)):
        if sec_large == arr[i]:
            break
    return i
#Use like this:
#  ind = secd_lrg_num(array)
#Setting the prediction to a var that we can print an check for validity ect...
#sec_best_pred = class_ids_list[ind]

def openConfirmationWindow():
    newWindow = Toplevel(screen) # Record Window Will Open on Top of Previous 
    newWindow.title("Confirmation") # Titles New Window
    newWindow.geometry("1920x1080") # Set Window Size
    message = Label(newWindow, text = "Program detected the following command:", font=('Times 20')) # Create Label
    message.place(relx = 0.5, rely = 0.25, anchor = N) # Places Label
    #place detected word here
    #VERIFY LABEL AND SUCH

    yesno = Label(newWindow, text = "Is this the outcome you requested?\n Say 'Yes' or 'No'", font=('Times 20')) # Create Label
    yesno.place(relx = 0.5, rely = 0.50, anchor = N) # Places Label
    yes = Button(newWindow, text = "Yes", command=lambda: [Yes(),newWindow.destroy()], font=('Times 14'), width=50, height=5, bg="green", compound=LEFT, relief=RAISED)
    yes.place(relx = 0.25, rely = 0.75, anchor = S) # Places Speak Button
    no = Button(newWindow, text = "No",command=lambda: [No(), newWindow.destroy()], font=('Times 14'), width=50, height=5, bg="red", compound=LEFT, relief=RAISED)
    no.place(relx = 0.75, rely = 0.75, anchor = S)
    
# Define Recording Function
def Record():
    #Start recording audio and runs through ASR, finds appropriate command
     seconds = 1
     fs = 44100
     #Print into GUI SCREEN
     print('...Recording in 3\n')
     time.sleep(1)
     print('...Recording in 2\n')
     time.sleep(1)
     print('...Recording in 1\n')
     time.sleep(1)
     print('Go \n')
     time.sleep(0.5)
     myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = np.int16)
     sd.wait()  # Wait until recording is finished
#write(filename, sr, myrecording.astype(np.int16))
     write('output.wav', fs, myrecording) 
    #This opens the confirmation window
     openConfirmationWindow()
     return None
    
    
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
welcome = Label(screen, text = "Welcome To S.H.E.R.P.A!", font=('Times 20')) # Creates Welcome Label
welcome.place(relx = 0.5, rely = 0.25, anchor = S) # Place Welcome Label at Set Location
quit_label = Button(screen, text = "To Quit Program Say 'No'.", command=screen.destroy, font=('Times 14'), width=50, height=5, bg="red", relief=RAISED) # Create Quit Button
quit_label.place(relx = 0.5, rely = 0.75, anchor = N) # Places Quit Button
speak_label = Button(screen, text = "To Begin Recording Say 'Yes'.", command=lambda: [Record(), ToggleRecord()], font=('Times 14'), width=50, height=5, bg="green", compound = LEFT, relief=RAISED) # Create Start Button
speak_label.place(relx = 0.5, rely = 0.65, anchor = S) # Places Speak Button
screen.mainloop() # Loops Code

