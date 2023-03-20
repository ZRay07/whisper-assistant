import AppOpener        # used for opening / closing applications
import pyautogui        # used to control mouse cursor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    # used for audio
from ctypes import cast, POINTER                                # audio
from comtypes import CLSCTX_ALL                                 # audio

# Set the device which we will change audio levels for
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

userChoice = " "

while(userChoice != "9"):
    print("What would you like to do?")
    print("1. Open application")
    print("2. Close application")
    print("3. Scroll up")
    print("4. Scroll down")
    print("5. Set volume")
    print("6. Select file")
    print("7. ")
    print("8. Make a Google search")
    print("9. Exit")

    userChoice = input("Enter your choice: ")

    if (userChoice == "1"):
        print("\n***Open Application***")
        appChoice = input("Enter the application you'd like to open: ")
        AppOpener.open(appChoice, match_closest=True)

    elif (userChoice == "2"):
        print("\n***Close Application***")
        appChoice = input("Enter the application you'd like to close: ")
        AppOpener.close(appChoice, match_closest=True)

    elif (userChoice == "3"):
        print("\n***Scroll Up***")
        pyautogui.scroll(10)
          
    elif (userChoice == "4"):
        print("\n***Scroll Down***")
        pyautogui.scroll(-10)

    elif (userChoice == "5"):
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

    elif (userChoice == "6"):
        print("\n***Select File***")
            
        

    elif (userChoice == "9"):
        print("\nExiting.")
        




