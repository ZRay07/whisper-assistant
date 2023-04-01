import AppOpener        # used for opening / closing applications
import pyautogui        # used to control mouse cursor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    # used for audio
from ctypes import cast, POINTER                                # audio
from comtypes import CLSCTX_ALL                                 # audio
from Email_open import sign_in
from model_interface import *

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# This function takes in an input string
# the string should be the predicted output from the ASR module
def commandExec(userChoice):    
    if (userChoice == "go"):        # if user says go, open application
        print("\n***Open Application***")
        print("\nWhich application would you like to open?")
        print("\t*yes - Word")
        print("\t*go - Edge")
        print("\t*stop - Spotify")
        print("\t*down - Discord")
        print("\t*up - ...")
        print("\t*left - ...")
        print("\t*right - ...")
        print("\t*no - Exit")
        
        rCheck = checkReady()
        if (rCheck):
            Record()

            run_up, out = use_model(audio_path)
            print("out[3]: ", out[3])

            count, ans = veri_n_ind(out)
            print("count: ", count)
            print("ans: ", ans)

            ans = keywords[count]
            print("ans: ", ans)

        if (ans == "yes"):
            AppOpener.open("Word", match_closest=True)
        elif (ans == "go"):
            AppOpener.open("Edge", match_closest=True)
        elif (ans == "stop"):
            AppOpener.open("Spotify", match_closest=True)
        elif (ans == "down"):
            AppOpener.open("Discord", match_closest=True)
        elif (ans == "up"):
            print()


    elif (userChoice == "no"):      # no -> close application
        print("\n***Close Application***")
        print("\nWhich application would you like to close?")
        print("\t*yes - Word")
        print("\t*go - Edge")
        print("\t*stop - Spotify")
        print("\t*down - Discord")
        print("\t*up - ...")
        print("\t*left - ...")
        print("\t*right - ...")
        print("\t*no - Exit")
        
        rCheck = checkReady()
        if (rCheck):
            Record()

            run_up, out = use_model(audio_path)
            print("out[3]: ", out[3])

            count, ans = veri_n_ind(out)
            print("count: ", count)
            print("ans: ", ans)

            ans = keywords[count]
            print("ans: ", ans)

        if (ans == "yes"):
            AppOpener.open("Word", match_closest=True)
        elif (ans == "go"):
            AppOpener.open("Edge", match_closest=True)
        elif (ans == "stop"):
            AppOpener.open("Spotify", match_closest=True)
        elif (ans == "down"):
            AppOpener.open("Discord", match_closest=True)
        elif (ans == "up"):
            print()

    elif (userChoice == "up"):      # up -> scroll up
        print("\n***Scroll Up***")
        pyautogui.scroll(10)
            
    elif (userChoice == "down"):    # down -> scroll down
        print("\n***Scroll Down***")
        pyautogui.scroll(-10)

    elif (userChoice == "right"):   # right -> set volume
        print("\n***Set Volume***")
        print("\nWhat volume would you like to set to?")
        print("\t*no - 0")
        print("\t*yes - 10")
        print("\t*stop - 30")
        print("\t*down - 50")
        print("\t*up - 70")
        print("\t*left - 80")
        print("\t*right - 80")
        print("\t*go - 100")

        rCheck = checkReady()
        if (rCheck):
            Record()

            run_up, out = use_model(audio_path)
            print("out[3]: ", out[3])

            count, ans = veri_n_ind(out)
            print("count: ", count)
            print("ans: ", ans)

            ans = keywords[count]
            print("ans: ", ans)

        if (ans == "no"):
            print("Setting volume to 0")
            volume.SetMasterVolumeLevel(-60.0, None)

        elif (ans == "yes"):
            volume.SetMasterVolumeLevel(-33.0, None)
            print("Setting volume to 10")

#        elif (volChoice == 4):
#            volume.SetMasterVolumeLevel(-23.4, None)
#            print("Setting volume to 20")

        elif (ans == "stop"):
            volume.SetMasterVolumeLevel(-17.8, None)
            print("Setting volume to 30")

#        elif (volChoice == 4):
#            volume.SetMasterVolumeLevel(-13.6, None)
#            print("Setting volume to 40")

        elif (ans == "down"):
            volume.SetMasterVolumeLevel(-10.2, None)
            print("Setting volume to 50")

#        elif (volChoice == 6):
#            volume.SetMasterVolumeLevel(-7.6, None)
#            print("Setting volume to 60")

        elif (ans == "up"):
            volume.SetMasterVolumeLevel(-5.3, None)
            print("Setting volume to 70")

        elif (ans == "left"):
            volume.SetMasterVolumeLevel(-3.4, None)
            print("Setting volume to 80")

        elif (ans == "right"):
            volume.SetMasterVolumeLevel(-1.6, None)
            print("Setting volume to 90")

        elif (ans == "go"):
            volume.SetMasterVolumeLevel(0, None)
            print("Setting volume to 100")
# end volume control loop            

    elif (userChoice == "yes"):     # yes -> select file
        print("\n***Select File***")

    elif (userChoice == "left"):    # left -> email sign in
        print("\n***Email sign-in***") 
        sign_in()       

    elif (userChoice == "stop"):    # stop -> Exit
        print("***Exiting***")
# We only have 8 keywords at the moment

def checkReady():
    rCheck = " "
    print("\nAre you ready to record?")
    rCheck = input("Enter yes when ready: ")

    if (rCheck == "yes"):
        rCheck = 1
    else:
        rCheck = 0

    return rCheck
    
