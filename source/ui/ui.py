from tkinter import *
from tkinter import font
from source.core.command_module import *
from source.core.model_interface import *
from source.ui.mouse_grid_ui import MouseGridInputValidator
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
        self.root.config(bg = "AntiqueWhite3")     # set the background color

        # Set the starting size of the window and its location
        #self.root.geometry("1100x700+480+200")
        self.root.geometry("1900x1000+0+0")
        self.drawLeftFrame()
        self.drawCenterFrame()
        self.drawRightFrame()
        self.root.grid_rowconfigure(0, weight = 1)  # Allow the first row (all 3 frames) to expand vertically
        self.root.grid_columnconfigure(0, weight = 1)   # Allow the first column (left frame) to expand horizontally
        self.root.grid_columnconfigure(1, minsize = 550, weight = 1)   # Allow the second column (center frame) to expand horizontally
        self.root.grid_columnconfigure(2, weight = 1)   # Allow the third column (right frame) to expand horizontally
        self.root = mainloop()


    # This frame contains:
    # mountain climbing image
    # command list (clickable buttons)
    def drawLeftFrame(self):

        # Create left frame
        self.left_frame = Frame(self.root, width = 250, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ns")       # Places the frame onto the window

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
        self.openApp_button =       Button(self.cmd_bar, text = "Open Application",     font = self.buttonFont, command = lambda: [handleApplicationAction(self.validateAppInput("app", "open"), "open")],  bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.closeApp_button =      Button(self.cmd_bar, text = "Close Application",    font = self.buttonFont, command = lambda: [handleApplicationAction(self.validateAppInput("app", "close"), "close")],bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.scrollUp_button =      Button(self.cmd_bar, text = "Scroll Up",            font = self.buttonFont, command = lambda: [handleScrollAction(self.validateScrollInput("up"), "up")],               bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.scrollDown_button =    Button(self.cmd_bar, text = "Scroll Down",          font = self.buttonFont, command = lambda: [handleScrollAction(self.validateScrollInput("down"), "down")],           bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.setVol_button =        Button(self.cmd_bar, text = "Set Volume",           font = self.buttonFont, command = lambda: [setVolume(*self.validateVolumeInput("volume"))],                         bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.mouseControl_button =  Button(self.cmd_bar, text = "Mouse Control",        font = self.buttonFont, command = lambda: [MouseGridInputValidator()],                                                              bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.emailSignIn_button =   Button(self.cmd_bar, text = "Email sign-in",        font = self.buttonFont, command = lambda: [sign_in, self.bring_to_front],                                           bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.createAcc_button =     Button(self.cmd_bar, text = "Create Account",       font = self.buttonFont, command = lambda: [self.create_account],                                                    bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.addContact_button =    Button(self.cmd_bar, text = "Add Contact",          font = self.buttonFont, command = lambda: [addContact(*self.validateAllContactInputs("contact"))],                  bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)        
        self.docSearch_button =     Button(self.cmd_bar, text = "Open Document",        font = self.buttonFont, command = lambda: [searchForDocument(self.validateDocumentInput("document"))],              bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        self.exit_button =          Button(self.cmd_bar, text = "Exit",                 font = self.buttonFont, command = lambda: [self.root.quit],                                                         bg = "SlateGray3", activebackground = "green", relief = FLAT, width = 14)
        
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
        self.docSearch_button.grid(row = 9, column = 0, pady = 5)
        self.exit_button.grid(row = 10, column = 0, pady = 5)

    # This frame contains:
    # Record button
    # The user inputs
    # Directions for the user on how to call a command request
    # A label which shows the user when the system is either listening or processing
    # A label which displays error messages to the user
    def drawCenterFrame(self):
        # Create center frame
        self.center_frame = Frame(self.root, width = 750, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.center_frame.grid(row = 0, column = 1, padx = 20, pady = 10, sticky = "nsew")
        self.center_frame.grid_columnconfigure(0, weight = 1)   # Allow the widgets within the center frame to expand horizontally

        # Label the center frame
        self.commandDirection_label = Label(self.center_frame, text = "Say \"sherpa\" OR click \"Record\"", font = ("Franklin Gothic Medium", 24), bg = "slate gray")
        self.commandDirection_label.grid(row = 0, column = 0, padx = 250, pady = 10)

        # Add record button
        self.record_button = Button(self.center_frame, text = "Record", font = ("Franklin Gothic Medium", 24),
                                     bg = "SlateGray3", relief = FLAT, activebackground = "green", command = self.recordAndUseModel)
        self.record_button.grid(row = 1, column = 0, pady = 10)



       # Add area to show user input history
        self.userInputHistory_frame = Frame(self.center_frame, width = 340, height = 500,
                                     bg = "LightCyan4", borderwidth = 2, relief = "solid")
        self.userInputHistory_frame.grid(row = 2, column = 0, columnspan = 1, padx = 5, pady = 5)

        # Add label at the top of the frame to show what's in the box
        self.userInputHistoryTitle_label = Label(self.userInputHistory_frame, text = "User input history will appear here", font = ("Franklin Gothic Medium", 12), width = 45, height = 1, bg = "azure3")
        self.userInputHistoryTitle_label.grid(row = 0, column = 0, sticky = "ew")

        self.userInputHistory_label = Label(self.userInputHistory_frame, text = " ", font = ("Franklin Gothic Medium", 12), width = 45, height = 20, bg = "azure3", wraplength = 500, anchor = "s")
        self.userInputHistory_label.grid(row = 1, column = 0, sticky = "ew")

        self.userInstruction_label = Label(self.userInputHistory_frame, text = "Say \"sherpa\" and we'll listen for a command", font = ("Franklin Gothic Medium", 12), width = 60, height = 3, bg = "AntiqueWhite3", wraplength = 500)
        self.userInstruction_label.grid(row = 2, column = 0, sticky = "ew")

        self.listeningProcessing_label = Label(self.center_frame, text = "Getting ready...", font = ("Franklin Gothic Medium", 24), width = 16, height = 1, bg = "slate gray")
        self.listeningProcessing_label.grid(row = 3, column = 0, sticky = "ew")

        self.userInputError_label = Label(self.center_frame, text = " ", font = ("Franklin Gothic Medium", 12, "bold"), width = 45, height = 2, bg = "slate gray", wraplength = 500, fg = "#710505", anchor = "center")
        self.userInputError_label.grid(row = 4, column = 0)

        # Configure the 4th row of the center frame(which contains error messages), to stretch to the bottom of the frame
        self.center_frame.rowconfigure(4, weight = 1)

        #This is the create account button
       # self.create_account_bar = Frame(self.center_frame, width = 375, height = 250
                                  #      bg = "azure3", borderwidth = 2, relief = "solid")
      #  self.create_account_bar.grid(row = 4, column = 0, columnspan = 1, padx = 0, pady = 0 )
      #  self.create_account_label = Label(self.create_account_bar, height = 1, width = 40, bg = "azure3", textvariable = self.create_account_label, wraplength = 500)
      #  self.create_account_label.grid(row = 0, column = 1, padx = 0, pady = 10)

    def update_screen(self):
         self.root.update_idletasks()
         self.root.update()
    
    def recordAndUseModel(self):
        microphone.record(5)
        self.prediction = whisper.use_model(RECORD_PATH)
        self.predictionLabel.set(self.prediction)
        print("Prediction: " + self.prediction)
        engine.say("Prediction " + self.prediction) # check if works, should respond with what it predicted user said
        #A wait func might allow the above line to complete first
        self.commandExec(self.prediction)

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

    #These were needed for threading
    def setlabel(self, string):
        self.transcribedLabel.set("")
        self.transcribedLabel.set(string)
        engine.say(self.transcribedLabel) # test if transcribe function will read back predicted words
        
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
    #This fuction will return who the person wishes to contact and what they wish to say.
    def write_email(self):
        confirm = False
        #Loop to make sure the contact's name is correct
        while confirm == False:
            self.transcribedLabel.set("")
            self.setlabel("What is the first name of the person you would like to contact?\n")
                        #This should update the screen
            self.update_screen()
            self.pred_name = whisper.use_model(RECORD_PATH)
                        #display the name
                        #THIS IS WITH THREADING
                        #t_label1 = threading.thread(target = self.setlabel, args = "please give me your name.\n")
                        
                        #t_record = threading.thread(target = self.rec_3sec)
            self.transcribedLabel.set("")
            self.transcribedLabel.set("I heard " + self.pred_1st_name + "\nIs this correct?\nSay 'Yes', 'No' or 'Exit'.")
            self.update_screen()
            microphone.record(4)
            if_yes1 = whisper.use_model(RECORD_PATH)
            if (jellyfish.jaro_winkler_similarity(if_yes1, "Yes" or "Yeah") > 0.65):
                 confirm = True
            else:
                 comfirm = False
                 self.transcribedLabel.set("")
                 self.transcribedLabel.set("Sorry about that, please try again.")
                 


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
        self.right_frame = Frame(self.root, width = 350, height = 530,
                                 bg = "slate gray", borderwidth = 2, relief = FLAT)
        self.right_frame.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "ns")

        # Add area to show command message history
        self.cmdHistory_frame = Frame(self.right_frame, width = 250, height = 500,
                                     bg = "azure3", borderwidth = 2, relief = "solid")
        self.cmdHistory_frame.grid(row = 0, column = 0, columnspan = 1, padx = 20, pady = 5)

        # Add label at the top of the frame to show what's in the box
        self.cmdHistoryTitle_label = Label(self.cmdHistory_frame, text = "Command history will appear here", font = ("Franklin Gothic Medium", 12), width = 40, height = 1, bg = "azure3")
        self.cmdHistoryTitle_label.grid(row = 0, column = 0, sticky = "ew")

        self.cmdHistory_label = Label(self.cmdHistory_frame, text = " ", font = ("Franklin Gothic Medium", 12), width = 40, height = 20, bg = "azure3", wraplength = 400, anchor = "s")
        self.cmdHistory_label.grid(row = 1, column = 0, sticky = "ew")



        self.transcribedLabel = StringVar()
        self.transcribedLabel.set("Transcribed speech will appear here.\n\n\n\n")

        # Add a transcription box
        self.transcription_label = Label(self.right_frame, height = 10, width = 30, bg = "light cyan", relief = "solid", textvariable = self.transcribedLabel, wraplength = 200)
        self.transcription_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        # Add a transcribe button
        self.transcribe_button = Button(self.right_frame, text = "Transcribe", font = "Times 14",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.transcribeSpeech)
        self.transcribe_button.grid(row = 2, column = 0, padx = 10, pady = 5)

        self.predictionLabel = StringVar()
        self.predictionLabel.set("Predicted commands will appear here")

        self.prediction_label = Label(self.right_frame, textvariable = self.predictionLabel, font = ("Franklin Gothic Medium", 12), width = 40, height = 5,  bg = "azure3", wraplength = 500, anchor = "center")
        self.prediction_label.grid(row = 3, column = 0, padx = 0, pady = 10)

       # self.recordDurationLabel = StringVar()
        #self.recordDurationLabel.set("Record Duration")

       # self.recordDuration_label = Label(self.right_frame, height = 1, width = 30, bg = "light cyan", relief = "solid", textvariable = self.recordDurationLabel, wraplength = 200)
       # self.recordDuration_label.grid(row = 3, column = 1, padx = 10, pady = 10)

# This class is meant to store the various functions we'll use for validating a user's input
# Input validation should always occur before passing the argument to the function in command_module
class InputValidation(mainScreen):
    def __init__(self):
        # Call startListeningThread to start listening for keywords in a separate thread
        if not args.disable:
            self.startListeningThread()
            
        super().__init__()
        

    # This function takes in an input string
    # the string should be the predicted output from the ASR module
    def commandExec(self, userChoice):
        # make the string all lower case to help with similarity (want to focus solely on matching keywords)
        userChoice = userChoice.lower()
        self.userChoiceSplit = userChoice.split()

        for index, element in enumerate(self.userChoiceSplit):
            print(f"self.userChoiceSplit[{index}]: {element}")
        
        if (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "open") > 0.85):        # Open application
            print("\n***Open Application***")
            self.appName = self.userChoiceSplit[-1].rstrip(string.punctuation).lower()
            print(f"self.appName: {self.appName}")
            self.appName = self.validateAppInput(self.appName, "open")
            print(f"self.appName: {self.appName}")
            self.commandUpdate = handleApplicationAction(self.appName, "open")
            self.appendNewCommandHistory(str(self.commandUpdate))

        elif (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "close") > 0.85):      # Close application
            print("\n***Close Application***")
            self.appName = self.userChoiceSplit[-1].rstrip(string.punctuation).lower()
            self.appName = self.validateAppInput(self.appName, "close")
            self.commandUpdate = handleApplicationAction(self.appName, "close")
            self.appendNewCommandHistory(str(self.commandUpdate))

        # There was an index error being caused here. 
        # Sometimes, the user would only say one word. For example, "open"
        # In this case, the self.userChoiceSplit[1] was raising an index error.
        #   trying to check for a value that doesn't exist because self.userChoiceSplit was [0] indices long
        elif (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "scroll") > 0.9):   # Scroll up
            if len(self.userChoiceSplit) >= 1:
                if (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[1], "up") > 0.9):
                    print("\n***Scroll Up***")
                    self.scrollAmount = self.userChoiceSplit[-1]
                    self.scrollAmount = self.validateScrollInput(self.scrollAmount)
                    self.commandUpdate = handleScrollAction(self.scrollAmount, "up")
                    self.appendNewCommandHistory(str(self.commandUpdate))

                
                elif (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[1], "down") > 0.9):    # Scroll down
                    print("\n***Scroll Down***")
                    self.scrollAmount = self.userChoiceSplit[-1]
                    self.scrollAmount = self.validateScrollInput(self.scrollAmount)
                    self.commandUpdate = handleScrollAction(self.scrollAmount, "down")
                    self.appendNewCommandHistory(str(self.commandUpdate))


        elif (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "set") > 0.85):     # Set volume
            if len(self.userChoiceSplit) >= 1:
                if (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[1], "volume") > 0.85):   
                    print("\n***Set Volume***")
                    self.volChoice = self.userChoiceSplit[-1].rstrip(string.punctuation).lower()
                    self.volume, self.decibel = self.validateVolumeInput(self.volChoice)
                    self.commandUpdate = setVolume(self.volume, self.decibel)
                    self.appendNewCommandHistory(str(self.commandUpdate))


        elif (jellyfish.jaro_winkler_similarity(userChoice, "Navigate mouse and keyboard") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Mouse Control") > 0.85):
            print("\n***Navigate mouse + keyboard***")
            beepgood()
            # Minimize the main screen window first
            self.root.iconify()
            self.mouseGrid = MouseGridInputValidator()

        elif (jellyfish.jaro_winkler_similarity(userChoice, "Email sign in") > 0.85 or jellyfish.jaro_winkler_similarity(userChoice, "Send an email") > 0.85):    # Email sign in
            print("\n***Email sign-in***")
            beepgood()
            sign_in()

        elif(jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "add") > 0.85):     # Add contact
            if len(self.userChoiceSplit) >= 5:
                self.addContactKeywords = {"add", "to", "my", "list"}    # We use this array to check if the user really said "add ___ to my list"

                # self.userChoiceSplit will either be: "Add [fname lname] to my list" such as "Add Tyler Cohen to my list"
                #   or "add contact to my list"
                # The following line checks if all the words in self.addContactKeywords are present in self.userChoiceSplit
                if all(self.word in self.userChoiceSplit for self.word in self.addContactKeywords):
                    # All words present, start creating contact
                    print("\n***Add Contact***")

                    if "contact" in self.userChoiceSplit:
                        self.contactName = self.userChoiceSplit[1]  # If "contact" is in the string, then the user didn't specify a name
                    else:
                        self.contactName = self.userChoiceSplit[1] + " " + self.userChoiceSplit[2]  # If "contact" is not in the string, they the user specified a name

                    # The following three lines validate the inputs, call the command, and update command history
                    self.contactName, self.contactEmail, self.contactEmailDomain = self.validateAllContactInputs(self.contactName)
                    self.commandUpdate = addContact(self.contactName, self.contactEmail, self.contactEmailDomain)
                    self.appendNewCommandHistory(self.commandUpdate)

        elif (jellyfish.jaro_winkler_similarity(userChoice, "Google search") > 0.85):
            print("\nSearching now...\n")
            beepgood()
            google_search()


        elif(jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0], "search") > 0.85):
            if len(self.userChoiceSplit) >= 4:
                if (jellyfish.jaro_winkler_similarity(self.userChoiceSplit[0] + self.userChoiceSplit[1] + self.userChoiceSplit[2] + self.userChoiceSplit[3],
                                                    "search for a document") > 0.85):
                    print("\n***Search for a document***")
                    self.docChoice = userChoice
                    self.docChoice = self.validateDocumentInput(self.docChoice)
                    self.commandUpdate = searchForDocument(self.docChoice)
                    self.appendNewCommandHistory(str(self.commandUpdate))

        elif (jellyfish.jaro_winkler_similarity(userChoice, "Exit") > 0.85):    # Exit
            beepgood()
            print("***Exiting***")

        else:
            beepbad()
            print(f"Unrecognized command: {userChoice}")
            
            # GUI Update
            self.setLabel(self.userInputError_label, f"Unrecognized command: {userChoice}")

    # This function is used when we need to prompt the user for additional voice inputs
    # Used for getting application names, scroll amounts, volume levels, etc.
    # If removePunctuation is true when you call it, it removes trailing punctuation.
    # If makeLowerCase is true when you call it, it makes the output string lowercase
    def promptUser(self, recordDuration, removePunctuation, makeLowerCase):
        try:
            self.setLabel(self.listeningProcessing_label, "Listening...")
            microphone.record(recordDuration)
            self.setLabel(self.listeningProcessing_label, "Processing...")
            self.userInput = whisper.use_model(RECORD_PATH)
            self.setLabel(self.listeningProcessing_label, "Waiting...")

            # I've found the default if there is no sound is to predict "you"
            # In this case, I think it's best to interpret the input as silence and not update the user input history
            if self.userInput != "you":
                self.appendNewUserInputHistory(self.userInput)


            if removePunctuation:
                self.userInput = self.userInput.rstrip(string.punctuation)

            if makeLowerCase:
                self.userInput = self.userInput.lower()

            return self.userInput
        
        except Exception as e:
            print("Error occured during recording: ", str(e))
            return False
        
    # This function verifies the application name which the user intends to open
    # It also is used to update the GUI
    def validateAppInput(self, appName, action):
        if (appName not in VALID_APPS and appName not in {"application", "app"}):
            # Graphical UI Update
            self.setLabel(self.userInputError_label, f"Invalid application name \"{appName}\". Please try again")

        # Remove essential services from VALID_APPS list so they aren't accessible to close
        if action == "close":
            removeEssentialServices(ESSENTIAL_SERVICES)

        # Either an appname can be passed, or the user can simply say "open application"
        #   If the user specifies a specific app, the while true loop will be skipped 
        #   Otherwise, the function continuously prompts for a valid app name
        
        if (appName in {"application", "app"} or appName not in VALID_APPS):
            while True:  
                # Text UI update
                print(f"\nWhich application would you like to {action}?")
                print("\t- Word")
                print("\t- Edge")
                print("\t- Spotify")
                print("\t- Discord")

                # Graphical UI Update
                self.setLabel(self.userInstruction_label, f"Which application would you like to {action}?")
                time.sleep(2)

                appName = self.promptUser(3, True, True)

                if appName in VALID_APPS:
                    break   # Valid app name provided, exit the while loop
                else:
                    # Text UI update
                    print(f"Invalid application name \"{appName}\". Please try again")

                    # Graphical UI Update
                    self.setLabel(self.userInputError_label, f"Invalid application name \"{appName}\". Please try again")   

        return appName
    
    def validateScrollInput(self, scrollAmount):
        # Remove any trailing punctuation marks
        scrollAmount = scrollAmount.rstrip(string.punctuation)

        # Either a scroll amount can be passed, or the user can simply say "scroll up"
        #   If the user specifies a specific amount to scroll by, the while true loop will be skipped 
        #   Otherwise, the function automatically scrolls by 100 clicks
        while True:
            try:
                if scrollAmount in {"up", "down"}:
                    scrollAmount = 100  # Default scroll amount if user doesn't specify a number
                else:
                    scrollAmount = convertToInt(scrollAmount) # Convert string representation of number to integer
                    
                if scrollAmount is None  or scrollAmount < 0 or scrollAmount > 1000:
                    raise ValueError
                
                return scrollAmount

            except ValueError as ve:
                # Text UI Update
                print(f"Invalid scroll amount: {scrollAmount}. Valid scroll amounts are between 0 and 1000: {ve}")

                # Graphical UI Updates
                self.setLabel(self.userInputError_label, f"Invalid scroll amount: {scrollAmount}. Valid scroll amounts are between 0 and 1000.")
                self.setLabel(self.userInstruction_label, f"What amount would you like to scroll by (in clicks)?")
                time.sleep(2)

                scrollAmount = self.promptUser(2, removePunctuation = True, makeLowerCase = True)

        
    # The input to this function [volChoice] can be a number, or it can simply be volume
    #   The input comes from the output of the Whisper speech recognition module
    #   So a user may say "set volume" or "set volume to 80"
    #   if the user says "set volume", the function should prompt the user and record an audio clip to get the number they'd like to set their volume to
    #   if the user says "set volume to 80", the function should automatically set the volume to 80 without prompting again
    def validateVolumeInput(self, volChoice):
        # Actual volume levels and corresponding decibel levels
        volumeMapping = {
            0: -60.0,
            10: -33.0,
            20: -23.4,
            30: -17.8,
            40: -13.6,
            50: -10.2,
            60: -7.6,
            70: -5.3,
            80: -3.4,
            90: -1.6,
            100: 0
        }

        try:
            while True:
                if (volChoice == "volume"):
                    # If the input is only volume, prompt user for a desired volume level
                    print("\nWhat volume would you like to set to?")
                    print("*** MUST BE AN INCREMENT OF 10 ***")
                    # Graphical UI Update
                    self.setLabel(self.userInstruction_label, "What volume would you like to set to?")
                    
                    time.sleep(2)

                    volChoice = self.promptUser(3, True, True)

                volChoice = convertToInt(volChoice) # Convert string representation of number to integer
                
                if volChoice in volumeMapping:
                    return volChoice, volumeMapping[volChoice]

                # Prompt the user for a valid volume value if not "volume" or a valid level
                print(f"\nInvalid volume value: {volChoice}. Valid volume levels are increments of 10 between 0 and 100.")

                # Graphical UI Update
                self.setLabel(self.userInputError_label, f"Invalid volume value: {volChoice}. Valid volume levels are increments of 10 between 0 and 100.")
                self.setLabel(self.userInstruction_label, "What volume would you like to set to?")
                time.sleep(2)

                volChoice = self.promptUser(3, removePunctuation = True, makeLowerCase = True)

        except Exception as e:
            print(f"Error occured while getting valid volume: {e}")
            return False
        
    # This function confirms the name of the document with the user
    #   If the last word of the string was document:
    #       The user is prompted for a document name
    #   Otherwise:
    #       it waits for the user to say "yes" before searching
    def validateDocumentInput(self, docChoice):
        docChoice = docChoice.rstrip(string.punctuation)
        self.docChoiceSplit = docChoice.split()
        self.wordsAfterDocument = None

        while True:
            if (self.docChoiceSplit[-1] == "document") or (self.userConfirmation != "yes"):    # If the last word in the string is "document", we need to prompt user for a document name
                print("\nWhat document would you like to search for?")
                self.setLabel(self.userInstruction_label, "What document would you like to search for?")
                
            
                time.sleep(2)

                docChoice = self.promptUser(3, True, False)

            else:
                try:
                    # Grab the position of "document" from the array
                    self.indexDocument = self.docChoiceSplit.index("document")

                    # Pull every word after document
                    self.wordsAfterDocument = self.docChoiceSplit[self.indexDocument + 1:]

                    # Combine the words after document back into string
                    docChoice = " ".join(self.wordsAfterDocument)

                except ValueError:
                    print("'Document' not found in array.")

            try:
                self.setLabel(self.userInstruction_label, f"Search for {docChoice}?\nSay yes if correct.")
                time.sleep(2)

                self.userConfirmation = self.promptUser(2, True, True)

                if (self.userConfirmation == "yes"):
                    return docChoice
            
            except Exception as e:
                print(f"Error occured while getting document name: {e}")

    
    # This function confirms the name of the contact the user wishes to add
    #   If the second word of the string was contact:
    #       The user is prompted for a contact name
    #   Otherwise:
    #       it waits for the user to say "yes" before returning a name
    def validateContactNameInput(self, contactName):
        self.userConfirmation = " "
        while True:
            if (contactName == "contact") or (self.userConfirmation != "yes"):    # If the second word in the string is "contact", we need to prompt user for a name
                print("\nWho would you like to add?")
                self.setLabel(self.userInstruction_label, "Who would you like to add?")
                time.sleep(2)

                contactName = self.promptUser(3, True, False)

            # Whether or not the second word is "contact", we will check if the name is correct
            try:
                self.setLabel(self.userInstruction_label, f"Add {contactName} to your list?\nSay yes if correct.")
                time.sleep(2)

                self.userConfirmation = self.promptUser(2, True, True)

                if (self.userConfirmation == "yes"):
                    return contactName
            
            except Exception as e:
                print(f"Error occured while getting contact name: {e}")

    # This function confirms the email of the contact the user wishes to add
    # The user will be prompted for an email and asked if it's correct
    #   if they say "yes", the loop is exited and the email is returned
    #       otherwise, the loop will continue
    def validateContactEmailInput(self):
        self.userConfirmation = " "
        while True:
            if (self.userConfirmation != "yes"):    # If the second word in the string is "contact", we need to prompt user for a name
                print("\nWhat is their email? (do not include domain)")
                self.setLabel(self.userInstruction_label, "What is their email?")
                self.setLabel(self.userInputError_label, "DO NOT include domain")
                time.sleep(2)

                self.contactEmail = self.promptUser(3, True, True)
                self.contactEmail = self.contactEmail.replace(" ", "")
            try:
                self.setLabel(self.userInputError_label, "")
                self.setLabel(self.userInstruction_label, f"Is their email {self.contactEmail}?\nSay yes if correct.")
                time.sleep(2)

                self.userConfirmation = self.promptUser(2, True, True)

                if (self.userConfirmation == "yes"):
                    return self.contactEmail
            
            except Exception as e:
                print(f"Error occured while getting contact email: {e}")

    
    # This function confirms the email domain of the contact the user wishes to add
    # The user will be prompted for an email domain and asked if it's correct
    #   if they say "yes", the loop is exited and the email domain is returned
    #       otherwise, the loop will continue
    def validateContactEmailDomainInput(self):
        self.userConfirmation = " "
        while True:
            if (self.userConfirmation != "yes"):    # If the second word in the string is "contact", we need to prompt user for a name
                print("\nWhat is their email domain?")
                self.setLabel(self.userInstruction_label, "What domain does their email belong to?\ngmail, outlook, proton, etc.")
                time.sleep(2)

                self.contactEmailDomain = self.promptUser(3, True, False)

            try:
                self.setLabel(self.userInstruction_label, f"Is {self.contactEmailDomain} the correct domain?")
                time.sleep(2)

                self.userConfirmation = self.promptUser(2, True, True)

                if (self.userConfirmation == "yes"):
                    return self.contactEmailDomain
            
            except Exception as e:
                print(f"Error occured while getting contact email domain: {e}")

    def validateAllContactInputs(self, contactName):
        print("called")
        contactName = self.validateContactNameInput(contactName)
        self.appendNewCommandHistory(f"Got name: {contactName}")

        self.contactEmail = self.validateContactEmailInput()
        self.appendNewCommandHistory(f"Got email: {self.contactEmail}")

        self.contactEmailDomain = self.validateContactEmailDomainInput()
        self.appendNewCommandHistory(f"Got email domain: {self.contactEmailDomain}")

        return contactName, self.contactEmail, self.contactEmailDomain
        
    # This function is used to update GUI labels
    # Simply pass a label name such as:
    #   userInstruction_label, or
    #   listeningProcessing_label
    # and the message you'd like to update it with such as:
    #   "provide me a name"
    def setLabel(self, label, message):
        try:
            self.message = message
            self.label = label
            self.label.config(text = self.message)

        except Exception as e:
            print(f"Error updating {label} with \"{message}\": {e}")

    # This function updates the cmdHistory_label which is the center text box of the program
    # It's meant to be used after a function has been called, to notify the user of
    #  whether or not the command was successful
    def appendNewCommandHistory(self, message):
        try:
            self.newText = message
            self.currentText = self.cmdHistory_label.cget("text")
            self.updatedText = self.currentText + "\n" + self.newText
            self.cmdHistory_label.config(text = self.updatedText.capitalize())
        except Exception as e:
            print(f"Error updating command history with \"{message}\": {e}")

    # This function updates the userInputHistory_label which is the right side text box of the program
    # It's meant to be used after every recording, to display what the model has transcripted
    def appendNewUserInputHistory(self, message):
        try:
            self.newText = message
            self.currentText = self.userInputHistory_label.cget("text")
            self.updatedText = self.currentText + "\n" + self.newText
            self.userInputHistory_label.config(text = self.updatedText.capitalize())
        except Exception as e:
            print(f"Error updating user input history with \"{message}\": {e}")

    
        
    # This function should be called as soon as the UI is launched
    # First, it updates the userInstruction label to let the users know we're first waiting for the keyword
    #   It will continuously listen until it hears the keyword: "sherpa"
    #   When "sherpa" is heard:
    #       -run another function which listens for commands
    #       -based on what the record function captured and the transcripted output
    #       -run a command
    #       -start listening for keyword again
    def listenForKeywords(self):
        time.sleep(1)
        try:
            while True:
                self.setLabel(self.userInstruction_label, "say \"sherpa\" and we'll listen for a command")
                print("Testing where print from...")
                self.keywordCheck = self.promptUser(2, True, True)
                

                if (self.keywordCheck.rstrip(string.punctuation).lower() == "sherpa"):
                    self.setLabel(self.listeningProcessing_label, "Waiting...")
                    print("\nSpeak a command")

                    self.setLabel(self.userInstruction_label, "Speak a command")

                    time.sleep(1)
                    self.commandRequest = self.promptUser(5, True, True)
                    self.commandExec(self.commandRequest)

                elif (self.keywordCheck.rstrip(string.punctuation).lower() == "you"):   # I found the model defaults to you if there is no sound passed
                    pass                                                                # In this case, do nothing

                elif (self.keywordCheck.rstrip(string.punctuation).lower() == "exit"):
                    break

                # Check if the main window is minimized,
                #   if it is, we want to break out of keyword listening
                #self.minimized = self.root.wm_state() == "iconic"

                #if self.minimized:
                    #break
                
        except Exception as e:
            print(f"Error while listening for keyword: {e}")

    # Function to start the keyword listening thread
    # This function is called within the __init__ method of the mainScreen class, allowing it to run concurrently with the GUI.
    def startListeningThread(self):
        thread = threading.Thread(target = self.listenForKeywords)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

if __name__ == '__main__':
    inputValidator = InputValidation()