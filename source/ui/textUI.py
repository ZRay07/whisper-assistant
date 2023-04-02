#####
# Text UI
#####

from source.core.command_module import commandExec
from source.core.model_interface import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Run until user chooses to exit
exitCheck = 0
while (exitCheck == 0):
    print("\n***COMMANDS***")
    print("\t* Go - Open Application")
    print("\t* No - Close Application")
    print("\t* Up - Scroll Up")
    print("\t* Down - Scroll Down")
    print("\t* Right - Set Volume")
    print("\t* Yes - Select File")
    print("\t* Left - Email sign in")
    print("\t* Stop - Exit")

    print("\nWould you like to run a command?")
    userChoice = input("Enter yes or no: ")
    if (userChoice == "yes"):
        
        Record()
        confidenceValues, greatestPrediction = use_model(audio_path)

        # Check with user to make sure we heard the correct command
        predictionCheck = 0
        predictionCheck = checkPredictionWithUser(greatestPrediction)

        if (predictionCheck == 0):
            print()
        elif (predictionCheck == 1):
            print("Executing command.")
            commandExec(greatestPrediction)
        else:
            print("Say either 'yes' or 'no'")

    elif (userChoice == "no"):
        print("Exiting.")
        exitCheck = 1

    else:
        print(f"{bcolors.FAIL}Invalid input. Enter 'yes' or 'no'.{bcolors.ENDC}")