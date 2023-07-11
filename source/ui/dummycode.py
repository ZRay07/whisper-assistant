import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import*
from source.core.command_module import*
#Def create_account:
    #part 1 prompt for name    

    #Prompt user for name
    #call record function from class obj
    #call use_model() and set = to variable Pred_name
    #Clear transcription box
    #INPUT new text into box with OUTPUT from use_model
    #Prompt for correctness 
    #Put time buffer here
    #Call record for verification -  SAVE TO IF_YES
    #If IF_YES = yes
        #continue 
        #Part 2 prompt for email

        #If output = yes
        #clear transcribe label
        #Input text to box and prompt for email
        #Call record


        #part 3 prompt for for password
    #else 
        #print("Please try again")
def format_email(string):
    punc_list = '''!()-[]{};*:'"\,<>./?_~'''
    for i in string:
        if i in punc_list:
            string = string.replace(i,"")
    
    string = string.replace(" ", "")
    print(string)

def exp_contact_list():
    with open("source/contact_list.txt", "w") as f:
        f.write("Tyler Cohen tcohenwest gobblety154\n" + "Devin Chen Dchen1 furryornah\n" + "Zach Ray zray1 beastmode\n")
        f.close()
    with open("source/contact_list.txt", "r") as f:
        contacts = f.readlines()
        for line in contacts:
            print(line)

#exp_contact_list()
#format_email("T. Cohen West")
def pull_contact(string):
    with open("source/my_account.txt", "r") as f:
         contacts = f.readlines()

         for line in contacts:
            extr = line.partition(" ")
            first_name = extr[0]
            extr_2 = extr[2].partition(" ")
            last_name = extr_2[0]
            extr_3 = extr_2[2].partition(" ")
            email = extr_3[0]
            domain = extr_3[2]
            if (first_name + " " + last_name == string):
                contact = {
                    'name' : first_name + " " + last_name,
                    'email' : email , 
                    'domain' : domain
                }
            
            #copy string until second " " is found 
            #compare with user input
            #If same pull the info from the line and save as dict
    return contact.get('name'), contact.get('email'), contact.get('domain')
    
    
    #return output
#name, email, domain = pull_contact("Chris Perlowin")
#print(name, email, domain)

def account_info_in():
    with open("source/my_account.txt", "r") as f:
         contacts = f.readlines()
         for line in contacts:
            extr = line.partition(" ")
            first_name = extr[0]
            extr_2 = extr[2].partition(" ")
            last_name = extr_2[0]
            extr_3 = extr_2[2].partition(" ")
            email = extr_3[0]
            extr_4 = extr_3[2].partition(" ")
            domain = extr_4[0]
            extr_5 = extr_4[2]
            password = extr_5
            contact = {
                    'name' : first_name + " " + last_name,
                    'email' : email , 
                    'domain' : domain,
                    'password' : password
                }
    return contact.get('name'), contact.get('email'), contact.get('domain'), contact.get('password')
#Make two functions 'write email' will take contact info and dictation
#'Full Send' will send the info gathered from write email if user confirms
def Full_send():

    name, email, domain, password = account_info_in()
    driver = webdriver.Firefox()

    #so the pages have time to load 
    wait = WebDriverWait(driver, 30)

    #driver.get("https://outlook.live.com/owa/")


    ele4 = wait.until(EC.element_to_be_clickable((By.LABEL, "New mail")))
    ele4.click()


class sub_window_int:
    def __init__(self):
        self.sub_window = Tk()
        self.sub_window.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.sub_window.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.sub_window.config(bg = "skyblue")     # set the background color
        self.sub_window.geometry("1100x700+240+50")
        self.command_frame()
        self.transcribe_frame()
        self.sub_window.mainloop()
    #There will be one frame for commands (left)
    def command_frame(self):
        self.command_frame = Frame(self.sub_window, width = 315, height = 600,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.command_frame.grid(row = 0, column = 0, padx = 10, pady = 10)       # Places the frame onto the window
        self.mountainImage = PhotoImage(file = "source/ui/images/mountain3.gif")
        self.small_image = self.mountainImage.subsample(3 , 3)
        Label(self.command_frame, image = self.small_image).grid(row = 0, column = 0, padx = 10, pady = 10)

        # Label the left hand frame
        self.cmd_label = Label(self.command_frame, text = "Speech Commands", font = "times 18", bg = "white")
        self.cmd_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        # Add speech commands below label
        # Use buttons so we can use the GUI
        self.cmd_bar = Frame(self.command_frame, width = 315, height = 300, bg = "white")
        self.cmd_bar.grid(row = 2, column = 0)
    #This frame is for the transcribe box
    def transcribe_frame(self): #(Right)
        self.transcribe_frame = Frame(self.sub_window, width = 750, height = 600,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.transcribe_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
        #makes sure the frame doesn't change shape to fit the widget
        self.transcribe_frame.grid_propagate(False)
        self.transcribedLabel = StringVar()
        self.transcribedLabel.set("Transcribed speech will appear here.\n\n\n\n")

        # Add a transcription box
        self.transcription_label = Label(self.transcribe_frame, height = 20, width = 80, bg = "light cyan", relief = "solid", textvariable = self.transcribedLabel, wraplength = 200)
        self.transcription_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Add a transcribe button
        self.transcribe_button = Button(self.transcribe_frame, text = "Transcribe", font = "Times 26",
                                     bg = "#ADD8E6", relief = "solid", activebackground = "green", activeforeground = "skyblue", command = self.transcribeSpeech)
        self.transcribe_button.grid(row = 1, column = 1, padx = 10, pady = 5)
    
    def transcribeSpeech(self):
        # TO-DO: Figure out a way to ask how long the user would like to record for

        #self.recordDurationLabel.set("How long would you like to record for? (in seconds)")

        #microphone.record(3)
        #self.prediction = whisper.use_model(RECORD_PATH)
        #self.recordDurationLabel.set(self.prediction)

        microphone.record(5)   #int(self.prediction))
        self.prediction = whisper.use_model(RECORD_PATH)
        self.transcribedLabel.set(self.prediction)

sub_window_int()


