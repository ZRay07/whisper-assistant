from tkinter import *
from tkinter import font
from source.core.command_module import *
from source.core.model_interface import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--disable', help = 'Disable keyword listening', action = 'store_true')
args = parser.parse_args()

# The first screen to be displayed to users
class mainScreen:
    def __init__(self):
        # Create root window
        self.root = Tk()
        self.root.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.root.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.root.config(bg = "dark slate gray")     # set the background color

        # Call startListeningThread to start listening for keywords in a separate thread
        if not args.disable:
            startListeningThread()

        # Set the starting size of the window and its location
        #self.root.geometry("1100x700+480+200")
        self.root.geometry("1919x1000+0+0")
        self.drawLeftFrame()
        self.drawCenterFrame()
        self.drawRightFrame()
        self.root = mainloop()


    # This frame contains:
    # mountain climbing image
    # command list (clickable buttons)
    def drawLeftFrame(self):

        # Create left frame
        self.left_frame = Frame(self.root, width = 250, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ns")       # Places the frame onto the window

        self.root.grid_rowconfigure(0, weight = 1)  # Allow the first row (left_frame) to expand vertically

        # Adding image to the left hand frame
#        self.mountainImage = PhotoImage(file = "source/ui/images/mountain3.gif")
#        self.small_image = self.mountainImage.subsample(3 , 3)
#        Label(self.left_frame, image = self.small_image).grid(row = 0, column = 0, padx = 10, pady = 10)

        self.title_frame = Frame(self.left_frame, width = 315, height = 100, bg = "slate gray")
        self.title_frame.grid(row = 0, column = 0)

        # Adding little icon next to SHERPA title   (<a href="https://www.flaticon.com/free-icons/altitude" title="altitude icons">Altitude icons created by Graficon - Flaticon</a>)
        # simple mountain: <a href="https://www.flaticon.com/free-icons/mountain" title="mountain icons">Mountain icons created by Freepik - Flaticon</a>
        # all black tour guide: <a href="https://www.flaticon.com/free-icons/tour" title="tour icons">Tour icons created by Leremy - Flaticon</a>
        # color tour guide: <a href="https://www.flaticon.com/free-icons/tourism" title="tourism icons">Tourism icons created by denimao - Flaticon</a>
        self.mountainLogo = PhotoImage(file = "source/ui/images/tour-guide.png")
        self.downsizedMountainLogo = self.mountainLogo.subsample(10, 10)
        self.mountainLogo_label = Label(self.title_frame, image = self.downsizedMountainLogo, bg = "slate gray")
        self.mountainLogo_label.grid(row = 0, column = 0, sticky = 'e')

        # Create S.H.E.R.P.A. title in top left hand corner of window
        self.sherpa_label = Label(self.title_frame, text = "SHERPA", font = ("Bauhaus 93", 36), bg = "slate gray")
        self.sherpa_label.grid(row = 0, column = 1, sticky = 'w')

        # Write out acronym below title
        self.sherpaFull_label = Label(self.title_frame, text = "Super Helpful Engine Recognizing People's Audio", font = ("Franklin Gothic Medium", 12, "italic"), bg = "slate gray")
        self.sherpaFull_label.grid(row = 1, rowspan = 3, columnspan = 2)

        # Below acronym, display "Speech commands"
        self.cmd_label = Label(self.left_frame, text = "Speech Commands",    font = ("Franklin Gothic Medium", 24), bg = "slate gray")
        self.cmd_label.grid(row = 1, column = 0, padx = 10)

        # Add actual speech commands below label
        self.cmd_bar = Frame(self.left_frame, width = 315, height = 300, bg = "slate gray")
        self.cmd_bar.grid(row = 2, column = 0)

        self.buttonFont = font.Font(family = "Franklin Gothic Medium", size = 12)
        self.openApp_button =  Button(self.cmd_bar, text = "Open Application",  font = self.buttonFont, command = lambda: handleApplicationAction("app", "open"),   bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.closeApp_button = Button(self.cmd_bar, text = "Close Application", font = self.buttonFont, command = lambda: handleApplicationAction("app", "close"),  bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.scrollUp_button = Button(self.cmd_bar, text = "Scroll Up",         font = self.buttonFont, command = lambda: handleScrollAction("up", "up"),           bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.scrollDown_button = Button(self.cmd_bar, text = "Scroll Down",     font = self.buttonFont, command = lambda: handleScrollAction("down", "down"),       bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.setVol_button = Button(self.cmd_bar, text = "Set Volume",          font = self.buttonFont, command = lambda: setVolume,                                bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.mouseControl_button = Button(self.cmd_bar, text = "Mouse Control", font = self.buttonFont, command = mouseGrid,                                        bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.emailSignIn_button = Button(self.cmd_bar, text = "Email sign-in",  font = self.buttonFont, command = lambda:[sign_in, self.bring_to_front],            bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.createAcc_button = Button(self.cmd_bar, text = "Create Account",   font = self.buttonFont, command = self.create_account,                              bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.addContact_button = Button(self.cmd_bar, text = "Add Contact",     font = self.buttonFont, command = self.add_contact,                                 bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)        
        self.exit_button = Button(self.cmd_bar, text = "Exit",                  font = self.buttonFont, command = self.root.quit,                                   bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        
        # Place the buttons in the frame
        self.openApp_button.grid(row = 0, column = 0, pady = 5)
        self.closeApp_button.grid(row = 1, column = 0, pady = 5)
        self.scrollUp_button.grid(row = 2, column = 0, pady = 5)
        self.scrollDown_button.grid(row = 3, column = 0, pady = 5)
        self.setVol_button.grid(row = 4, column = 0, pady = 5)
        self.mouseControl_button.grid(row = 5, column = 0, pady = 5)
        self.emailSignIn_button.grid(row = 6, column = 0, pady = 5)
        self.createAcc_button.grid(row = 7, column = 0, pady = 5)
        self.addContact_button.grid(row = 8, column = 0, pady = 5)
        self.exit_button.grid(row = 9, column = 0, pady = 5)

    # This frame contains:
    # Directions for the user on how to call a command request
    # Prediction outputs
    # Command outputs
    def drawCenterFrame(self):
        # Create center frame
        self.center_frame = Frame(self.root, width = 750, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.center_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ns")

        self.root.grid_rowconfigure(0, weight = 1)  # Allow the (center_frame) to expand vertically

        # Ensure the frame does not shrink to fit widget size
        #self.center_frame.grid_propagate(False)

        # Label the center frame
        self.commandDirection_label = Label(self.center_frame, text = "Say \"sherpa\" OR click \"Record\"", font = ("Franklin Gothic Medium", 24), bg = "slate gray")
        self.commandDirection_label.grid(row = 0, column = 0, padx = 5, pady = 10)

        # Add record button
        # *** in the future -> activate record by speaking a keyword
        self.record_button = Button(self.center_frame, text = "Record", font = ("Franklin Gothic Medium", 24),
                                     bg = "SlateGray3", relief = FLAT, activebackground = "green", command = self.recordAndUseModel)
        self.record_button.grid(row = 1, column = 0, padx = 10, pady = 10)
       

        # Add area to show predicted command
        self.cmdHistory_frame = Frame(self.center_frame, width = 350, height = 500,
                                     bg = "light grey", borderwidth = 2, relief = "solid")
        self.cmdHistory_frame.grid(row = 2, column = 0, columnspan = 1, padx = 5, pady = 5)

        # Add label at the top of the frame to show what's in the box
        self.cmdHistory_label = Label(self.cmdHistory_frame, text = "Command history will appear here", font = ("Franklin Gothic Medium", 12), width = 60, height = 1, bg = "light grey")
        self.cmdHistory_label.grid(row = 0, column = 0, sticky = "n")

        self.predictionLabel = StringVar()
        self.predictionLabel.set("Command history")

        self.prediction_label = Label(self.cmdHistory_frame, textvariable = self.predictionLabel, font = ("Franklin Gothic Medium", 12), width = 60, height = 30,  bg = "light grey", wraplength = 500, anchor = "s")
        self.prediction_label.grid(row = 1, column = 0, padx = 0, pady = 10)

        self.recordDisplay_label = Label(self.cmdHistory_frame, text = "Listening...", font = ("Franklin Gothic Medium", 12), width = 60, height = 1, bg = "light grey", )
        self.recordDisplay_label.grid(row = 2, column = 0, sticky = "s")

        engine = pyttsx3.init() # initialize
        engine.setProperty('rate', 100) # adjust settings
#        engine.say("We heard:" + self.predictionLabel) # what engine will say
        engine.runAndWait() # runs engine until 'sentence' is over

        #This is the create account button
       # self.create_account_bar = Frame(self.center_frame, width = 375, height = 250
                                  #      bg = "light grey", borderwidth = 2, relief = "solid")
      #  self.create_account_bar.grid(row = 4, column = 0, columnspan = 1, padx = 0, pady = 0 )
      #  self.create_account_label = Label(self.create_account_bar, height = 1, width = 40, bg = "light grey", textvariable = self.create_account_label, wraplength = 500)
      #  self.create_account_label.grid(row = 0, column = 1, padx = 0, pady = 10)

    def update_screen(self):
         self.root.update_idletasks()
         self.root.update()
    
    def recordAndUseModel(self):
        microphone.record(5)
        self.prediction = whisper.use_model(RECORD_PATH)
        self.predictionLabel.set(self.prediction)
        print("Prediction: " + self.prediction)
        #A wait func might allow the above line to complete first
        commandExec(self.prediction)

    def transcribeSpeech(self):
        # TO-DO: Figure out a way to ask how long the user would like to record for

        #self.recordDurationLabel.set("How long would you like to record for? (in seconds)")

        #microphone.record(3)
        #self.prediction = whisper.use_model(RECORD_PATH)
        #self.recordDurationLabel.set(self.prediction)

        microphone.record(15)   #int(self.prediction))
        self.prediction = whisper.use_model(RECORD_PATH)

        self.transcribedLabel.set(self.prediction)

    def bring_to_front(root): 
        root.attributes('-topmost', 1)
        root.attributes('-topmost', 0)

    def handleUserNameValidation():
         print("Handling user name validation")

    #These were needed for threading
    def setlabel(self, string):
        self.transcribedLabel.set("")
        self.transcribedLabel.set(string)
    #These were needed for threading
    def rec_3sec(self):
        microphone.record(3)
        self.pred_word = whisper.use_model(RECORD_PATH)
        return self.pred_word
    
    def format_email(self, string):
        punc_list = '''!()-[]{};*:'"\,<>./?_~'''
        for i in string:
            if i in punc_list:
                string = string.replace(i,"")
        
        string = string.replace(" ", "")
        return string

    def add_contact(self):
         confirm = False
         while confirm == False:
            self.setlabel("Please give me their name.")
            self.update_screen()
            microphone.record(3)
            self.pred_name = whisper.use_model(RECORD_PATH)
            self.setlabel("I heard " + self.pred_name + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
            self.update_screen()
            microphone.record(4)
            if_yes1 = whisper.use_model(RECORD_PATH)
            print(if_yes1)
            if (if_yes1 == "Yes" or if_yes1 == "Yes." or if_yes1 == "yes" or if_yes1 == "yes." or if_yes1 == "Yeah." or if_yes1 =="Yeah"):
                confirm = True
                #Stuff
            
                print(if_yes1)
            else: 
                 confirm = False
            while confirm == True:     
                self.setlabel("What is their email?")
                self.update_screen()
                microphone.record(3)
                self.pred_email = whisper.use_model(RECORD_PATH)
                self.pred_email = self.format_email(self.pred_email)
                self.setlabel("I heard " + self.pred_email + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
                self.update_screen()
                microphone.record(4)
                if_yes2 = whisper.use_model(RECORD_PATH)
            
                if(if_yes2 == "Yes" or if_yes2 == "Yes." or if_yes2 == "yes" or if_yes2 == "yes." or if_yes2 == "Yeah." or if_yes2 =="Yeah"):
                        #Have to toggle this to exit the loop
                        confirm = False
                else: 
                        confirm = True
            if(confirm == False):  
                while confirm == False:                                        
                    self.setlabel("What domain does the email belong to?\n (Gmail, outlook, proton, ect..)")
                    self.update_screen()
                    microphone.record(3)
                    self.pred_domain = whisper.use_model(RECORD_PATH)
                    self.setlabel("I heard " + self.pred_domain + "\nIs this correct?\nSay 'Yes', 'Exit', or anything else.")
                    self.update_screen()
                    microphone.record(4)
                    if_yes3 = whisper.use_model(RECORD_PATH)
                    if(if_yes3 == "Yes" or if_yes3 == "Yes." or if_yes3 == "yes" or if_yes3 == "yes." or if_yes3 == "Yeah." or if_yes3 =="Yeah"):
                        self.account = {
                                        "name" : self.pred_name ,
                                        "email" : self.pred_email ,
                                        "domain": self.pred_domain , 
                        }
                        with open("source/contact_list.txt", "a") as f:
                                        f.write(self.account.get("name") + " " + self.account.get("email") + " " + self.account.get("domain") + "\n")
                        confirm = True
                    else: 
                        self.setlabel("Please try again")
                        beepbad()
                        self.update_screen() 
                        confirm = False
            else:
                    self.setlabel("Please try again")
                    beepbad()
                    self.update_screen() 
                    confirm = True
           


    #Call this and use root as the input. Brings window to the foreground.
    def bring_to_front(root): 
         root.attributes('-topmost', 1)
         root.attributes('-topmost', 0)



    def create_account(self):
           #THIS IS THE OLD METHOD
           #Prompt user to give a name
            confirm = False
            correct = False
            while confirm == False or  correct == False:
                    self.transcribedLabel.set("")
                    self.transcribedLabel.set("Please give me your name.")
                    self.setlabel("please give me your name.\n")
                    #This should update the screen
                    self.update_screen()
                    microphone.record(3)
                    self.pred_name = whisper.use_model(RECORD_PATH)
                    #display the name
                    #THIS IS WITH THREADING
                    #t_label1 = threading.thread(target = self.setlabel, args = "please give me your name.\n")
                    
                    #t_record = threading.thread(target = self.rec_3sec)
                    self.transcribedLabel.set("")
                    self.transcribedLabel.set("I heard " + self.pred_name + "\nIs this correct?\nSay 'Yes', 'No' or 'Exit'.")
                    #This should update the screen
                    self.update_screen()
                    microphone.record(4)
                    if_yes1 = whisper.use_model(RECORD_PATH)
                    #if correct - > 
                    print(if_yes1)
                    if(if_yes1 == "Yes" or if_yes1 == "Yes." or if_yes1 == "yes" or if_yes1 == "yes." or if_yes1 == "Yeah." or if_yes1 =="Yeah"):
                        confirm = True 
                        correct = True
                    else:
                        confirm = False
                        correct = False
                    
                    if (confirm == True): 
                        #We have to toggle correct or it makes an inf loop
                        while (correct == True):
                    #   print(if_yes1)
                    #prompt user for email -> 
                            self.transcribedLabel.set("")
                            self.transcribedLabel.set("What is your email?")
                            #This should update the screen
                            self.root.update_idletasks()
                            self.root.update()
                            microphone.record(4)
                            self.pred_email = whisper.use_model(RECORD_PATH)
                            #This removes spaces and punctuation from the email
                            self.pred_email = self.format_email(self.pred_email)
                            self.transcribedLabel.set("")
                            self.transcribedLabel.set("I heard: " + self.pred_email + "\n Is this correct?\nSay 'Yes', 'Exit', or anything else.\n I'm listening.")
                            #This should update the screen
                            self.update_screen()
                            #time.sleep(2)
                            #Verify
                            microphone.record(3)
                            if_yes2 = whisper.use_model(RECORD_PATH)
                            print(if_yes2)
                            #time.sleep(5)
                            if (if_yes2 == "Yes" or if_yes2 == "Yes." or if_yes2 == "yes" or if_yes2 == "yes."or if_yes2 == "Yeah." or if_yes2 =="Yeah"):
                                 correct = False
                                 print(if_yes2)
                            else:
                                 correct = True
                        if (correct == False):   
                            
                            while(correct == False):
                                self.setlabel("What domain does the email belong to?\n (Gmail, outlook, proton, ect..)")
                                #This should update the screen
                                self.update_screen()
                                self.pred_domain = self.rec_3sec()
                                self.setlabel("I heard: " + self.pred_domain + "\n Is this correct?\nSay 'Yes', 'Exit', or anything else.\n I'm listening.")
                                #This should update the screen
                                self.update_screen()
                                #time.sleep(2)
                                #Verify
                                microphone.record(3)
                                if_yes3 = whisper.use_model(RECORD_PATH)
                                #Add a password if you like
                                print(if_yes3)
                                if  (if_yes3 == "Yes" or if_yes3 == "Yes." or if_yes3 == "yes" or if_yes3 == "yes." or if_yes3 == "Yeah." or if_yes3 =="Yeah"):
                                    correct = True
                                else:
                                     correct = False
                                    
                            if(confirm == True):        
                                
                                while confirm == True:
                                    self.setlabel("Would you like to add a password? Yes or No.")
                                    self.update_screen()

                                    if_yes4 = self.rec_3sec()
                                    if (if_yes4 == "Yes" or if_yes4 == "Yes." or if_yes4 == "yes" or if_yes4 == "yes."): 
                                        print(if_yes4)
                                        self.setlabel("What would you like your password to be?")
                                        self.update_screen()
                                    # time.sleep(1)
                                        self.pred_password = self.rec_3sec()
                                        self.setlabel("I heard: " + self.pred_password + "\n Is this correct?\nSay 'Yes', or anything else.\n")
                                #This should update the screen
                                        self.update_screen()
                                        if_yes5 = self.rec_3sec()
                                        if (if_yes5 == "Yes" or if_yes5 == "Yes." or if_yes5 == "yes" or if_yes5 == "yes."):
                                            confirm = False
                                
                                    
                                            if (confirm == False):    
                                                    self.account = {
                                                        "name" : self.pred_name ,
                                                        "email" : self.pred_email ,
                                                        "domain": self.pred_domain , 
                                                        "password" : self.pred_password 
                                                        }
                                                    with open("source/my_account.txt", "w") as f:
                                                        f.write(self.account.get("name") + " " + self.account.get("email") + " " + self.account.get("domain") + " " + self.account.get("password") )
                                    else:
                                        self.account = {
                                                "name" : self.pred_name ,
                                                "email" : self.pred_email ,
                                                "domain": self.pred_domain , 
                                                "password" : self.pred_password 
                                                }
                                        with open("source/my_account.txt", "w") as f:
                                                f.write(self.account.get("name") + " " + self.account.get("email") + " " + self.account.get("domain"))
                            
                    
            

            
        #This one should overwrite any previous data

    # This frame contains:
    # Transcription Box
    # The button to change transcription record duration
    def drawRightFrame(self):

        # Create right frame
        self.right_frame = Frame(self.root, width = 750, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.right_frame.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "ns")

        self.root.grid_rowconfigure(0, weight = 1)  # Allow the (right_frame) to expand vertically

        # Ensure the frame does not shrink to fit widget size
        #self.right_frame.grid_propagate(False)


        self.transcribedLabel = StringVar()
        self.transcribedLabel.set("Transcribed speech will appear here.\n\n\n\n")

        # Add a transcription box
        self.transcription_label = Label(self.right_frame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.transcribedLabel, wraplength = 200)
        self.transcription_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Add a transcribe button
        self.transcribe_button = Button(self.right_frame, text = "Transcribe", font = "Times 14",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.transcribeSpeech)
        self.transcribe_button.grid(row = 1, column = 1, padx = 10, pady = 5)

       # self.recordDurationLabel = StringVar()
        #self.recordDurationLabel.set("Record Duration")

       # self.recordDuration_label = Label(self.right_frame, height = 1, width = 30, bg = "light cyan", relief = "solid", textvariable = self.recordDurationLabel, wraplength = 200)
       # self.recordDuration_label.grid(row = 3, column = 1, padx = 10, pady = 10)

if __name__ == '__main__':
    main = mainScreen()

