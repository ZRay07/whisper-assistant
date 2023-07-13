from tkinter import *
from source.core.command_module import *
from source.core.model_interface import *
import threading

# This function should be called as soon as the UI is launched
#   It will continuously listen until it hears the keyword: "sherpa"
#   When "sherpa" is heard:
#       -run another function which listens for commands
#       -based on what the record function captured and the transcripted output
#       -run a command
# TO-DO: update the GUI to show when we are listening or processing the audio
def listenForKeywords():
    try:
        while True:
            microphone.record(2)
            prediction = whisper.use_model(RECORD_PATH)

            if (prediction.rstrip(string.punctuation).lower() == "sherpa"):
                print("\nSpeak a command")
                time.sleep(1)
                prediction = promptUser(recordDuration = 5, removePunctuation = True, makeLowerCase = True)
                commandExec(prediction)
                break # Exit the loop after capturing the keyword and executing the action

    except Exception as e:
        print(f"Error while listening for keyword: {e}")

# Function to start the keyword listening thread
# This function is called within the __init__ method of the mainScreen class, allowing it to run concurrently with the GUI.
def startListeningThread():
    thread = threading.Thread(target = listenForKeywords)
    thread.daemon = True  # Set the thread as a daemon thread
    thread.start()

# The first screen to be displayed to users
class mainScreen:
    def __init__(self):
        # Create root window
        self.root = Tk()
        self.root.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.root.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.root.config(bg = "skyblue")     # set the background color

        # Call startListeningThread to start listening for keywords in a separate thread
        startListeningThread()

        # Set the starting size of the window and its location
        self.root.geometry("1100x700+480+200")
        self.drawRightFrame()
        self.drawLeftFrame()
        self.root = mainloop()

    def drawLeftFrame(self):
        # Create left frame
        def bring_to_front(root): 
            root.attributes('-topmost', 1)
            root.attributes('-topmost', 0)
        self.left_frame = Frame(self.root, width = 315, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady = 10)       # Places the frame onto the window

        # Adding image to the left hand frame
        self.mountainImage = PhotoImage(file = "source/ui/images/mountain3.gif")
        self.small_image = self.mountainImage.subsample(3 , 3)
        Label(self.left_frame, image = self.small_image).grid(row = 0, column = 0, padx = 10, pady = 10)

        # Label the left hand frame
        self.cmd_label = Label(self.left_frame, text = "Speech Commands", font = "times 18", bg = "white")
        self.cmd_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        # Add speech commands below label
        # Use buttons so we can use the GUI
        self.cmd_bar = Frame(self.left_frame, width = 315, height = 300, bg = "white")
        self.cmd_bar.grid(row = 2, column = 0)

        self.openApp_button = Button(self.cmd_bar, text = "Open Application", command = lambda: handleApplicationAction("app", "open"), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.closeApp_button = Button(self.cmd_bar, text = "Close Application", command = lambda: handleApplicationAction("app", "close"), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.scrollUp_button = Button(self.cmd_bar, text = "Scroll Up", command = lambda: handleScrollAction("up", "up"), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.scrollDown_button = Button(self.cmd_bar, text = "Scroll Down", command = lambda: handleScrollAction("down", "down"), bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.setVol_button = Button(self.cmd_bar, text = "Set Volume", command = setVolume, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.mouseControl_button = Button(self.cmd_bar, text = "Navigate Mouse and Keyboard", bg = "light grey", command = mouseGrid, activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.emailSignIn_button = Button(self.cmd_bar, text = "Email sign-in", command = lambda:[sign_in,bring_to_front], bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.exit_button = Button(self.cmd_bar, text = "Exit", command = self.root.quit, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        
        # Place the buttons in the frame
        self.openApp_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.closeApp_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.scrollUp_button.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.scrollDown_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.setVol_button.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.mouseControl_button.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.emailSignIn_button.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.exit_button.grid(row = 7, column = 0, padx = 10, pady = 10)

    def drawRightFrame(self):
        # Create right frame
        self.right_frame = Frame(self.root, width = 750, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.right_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Ensure the frame does not shrink to fit widget size
        self.right_frame.grid_propagate(False)

        # Label the right frame
        self.sherpa_label = Label(self.right_frame, text = "Welcome to S.H.E.R.P.A.", font = "Times 20", bg = "white")
        self.sherpa_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        # Add record button
        # *** in the future -> activate record by speaking a keyword
        self.record_button = Button(self.right_frame, text = "When ready to record, say [sherpa]", font = "Times 14",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.recordAndUseModel)
        self.record_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.create_account_butt = Button(self.right_frame, text = "Create Account", command = self.create_account, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.create_account_butt.grid(row = 4, column = 0, padx = 10, pady = 10 )

        self.Add_contact_butt = Button(self.right_frame, text = "Add Contact", command = self.add_contact, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.Add_contact_butt.grid(row = 5, column = 0, padx = 10, pady = 10 )
       
       
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

        # Add area to show predicted command
        self.prediction_bar = Frame(self.right_frame, width = 375, height = 500,
                                     bg = "light grey", borderwidth = 2, relief = "solid")
        self.prediction_bar.grid(row = 3, column = 0, columnspan = 1, padx = 5, pady = 5)

        self.weHeard_label = Label(self.prediction_bar, height = 1, width = 10, text = "We heard: ", bg = "light grey")
        self.weHeard_label.grid(row = 0, column = 0, padx = 0, pady = 10)

        self.predictionLabel = StringVar()
        self.predictionLabel.set("Predicted commands will appear here.")

        self.prediction_label = Label(self.prediction_bar, height = 1, width = 40, bg = "light grey", textvariable = self.predictionLabel, wraplength = 500)
        self.prediction_label.grid(row = 0, column = 1, padx = 0, pady = 10)

        engine = pyttsx3.init() # initialize
        engine.setProperty('rate', 100) # adjust settings
#        engine.say("We heard:" + self.predictionLabel) # what engine will say
        engine.runAndWait() # runs engine until 'sentence' is over

        #This is the create account button
       # self.create_account_bar = Frame(self.right_frame, width = 375, height = 250
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

if __name__ == '__main__':
    main = mainScreen()

