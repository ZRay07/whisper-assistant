#####
# Text UI
#####

from source.core.command_module import commandExec
from source.core.model_interface import *

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

        run_up, out = use_model(audio_path)
#        print("out[3]: ", out[3])

        count, ans = veri_n_ind(out)
#        print("count: ", count)
#        print("ans: ", ans)

        ans = keywords[count]
        print("ans: ", ans)

        commandExec(ans)

    elif (userChoice == "no"):
        print("Exiting.")
        exitCheck = 1