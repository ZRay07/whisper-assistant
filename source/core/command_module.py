import AppOpener        # used for opening / closing applications
import pyautogui        # used to control mouse cursor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    # used for audio
from ctypes import cast, POINTER                                # audio
from comtypes import CLSCTX_ALL                                 # audio
from asr_module import *

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):    
    if (userChoice == "go"):        # if user says go, open microsoft word
        print("\n***Open Word***")
        appChoice = 'Microsoft Word'
        AppOpener.open(appChoice, match_closest=True)

    elif (userChoice == "no"):      # no -> close word
        print("\n***Close Word***")
        appChoice = 'Microsoft Word'
        AppOpener.close(appChoice)

    elif (userChoice == "up"):      # up -> scroll up
        print("\n***Scroll Up***")
        pyautogui.scroll(10)
            
    elif (userChoice == "down"):    # down -> scroll down
        print("\n***Scroll Down***")
        pyautogui.scroll(-10)

    elif (userChoice == "right"):   # right -> set volume
        print("\n***Set Volume***")
        volChoice = input("(0-10) Enter desired volume level: ")
        volChoice = int(volChoice)

        if (volChoice == 0):
            print("Setting volume to 0")
            volume.SetMasterVolumeLevel(-60.0, None)

        elif (volChoice == 1):
            volume.SetMasterVolumeLevel(-33.0, None)
            print("Setting volume to 10")

        elif (volChoice == 2):
            volume.SetMasterVolumeLevel(-23.4, None)
            print("Setting volume to 20")

        elif (volChoice == 3):
            volume.SetMasterVolumeLevel(-17.8, None)
            print("Setting volume to 30")

        elif (volChoice == 4):
            volume.SetMasterVolumeLevel(-13.6, None)
            print("Setting volume to 40")

        elif (volChoice == 5):
            volume.SetMasterVolumeLevel(-10.2, None)
            print("Setting volume to 50")

        elif (volChoice == 6):
            volume.SetMasterVolumeLevel(-7.6, None)
            print("Setting volume to 60")

        elif (volChoice == 7):
            volume.SetMasterVolumeLevel(-5.3, None)
            print("Setting volume to 70")

        elif (volChoice == 8):
            volume.SetMasterVolumeLevel(-3.4, None)
            print("Setting volume to 80")

        elif (volChoice == 9):
            volume.SetMasterVolumeLevel(-1.6, None)
            print("Setting volume to 90")

        elif (volChoice == 10):
            volume.SetMasterVolumeLevel(0, None)
            print("Setting volume to 100")
# end volume control loop            

    elif (userChoice == "yes"):     # yes -> select file
        print("\n***Select File***")

    elif (userChoice == "left"):    # left -> 
        print()        

    elif (userChoice == "stop"):    # stop ->
        print()
# We only have 8 keywords at the moment

