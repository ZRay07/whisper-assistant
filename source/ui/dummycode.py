from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import pyautogui
from tkinter import*
from source.core.model_interface import microphone, whisper, RECORD_PATH

driver = webdriver.Firefox()
def sign_in():
        name, email, domain, password = account_info_in()
        #driver = webdriver.Firefox()

        #so the pages have time to load 
        wait = WebDriverWait(driver, 30)

        driver.get("https://outlook.live.com/owa/")
        
        #SPECIFY WINDOW OPENS AT MAX SIZE
        driver.maximize_window()
        #This is an alternative method
        # Wait for the Sign in link to become available
        ele = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
        ele.click()

        # Wait for the email input field to become available
        el1 = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))


        #email = driver.find_element(By.XPATH, "//form[input/@name='email']")
        #email = driver.find_element(By.XPATH, "//form[@id='loginForm']/input[1]")
        #email = driver.find_element(By.XPATH, "//input[@name='email']")
        #time.sleep(2)
        #el1 = ( driver.find_element(By.NAME, "loginfmt"))
        #user = "sherpaemail361@gmail.com"
        el1.send_keys(email + "@" + domain + ".com" )

        el1.send_keys(Keys.RETURN)
        time.sleep(2)
        #keyword = "geeksforgeeks"
        el2 = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
        el2.send_keys(password)
        el2.send_keys(Keys.RETURN)
        time.sleep(2)
        
        pyautogui.click(x=1080, y=675)

      #  el3 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "splitPrimaryButton")))
      #  print("\n Found it or nah?")
      #  el3.click()
        #el4 = wait.until(driver.find_element(By.ID,("idSIButton9"))) 
        #el4.click()
       #//*[@id="idSIButton9"]
       #//*[@id="idSIButton9"]
        #elements = driver.find_elements(By.CLASS_NAME, "method-select-chevron")
        #This for loop helped identify which element to click
        #for e in elements:
        #    print(e)
        #elements[3].click()
        #time.sleep(15)

        #el5 = wait.until(EC.presence_of_element_located((By.ID,"trust-browser-button")))
        #el5.click()

        #Find the yes button
        #elements2 = wait.until(EC.presence_of_element_located((By.ID,"idSIButton9")))
        #elements2.click()

        #The lines below are meant to start a new email but the id is incorrect - fix later
        #el4 = wait.until(EC.presence_of_element_located((By.ID, "id__248")))
        #el4.click()

    # This function moves the mouse cursor down to the Windows search bar in bottom left and clicks
    #   If the last word of the string was document:
    #       The user is prompted for a document name
    #   Otherwise:
    #       it searches for a document with the document name being whatever comes after 'document' in the string
        current_window = driver.current_window_handle
        print(current_window)
        return current_window


def new_email(current_window, contact, subject, body):
     # driver = webdriver.Firefox()
      driver.switch_to.window(current_window)
      wait = WebDriverWait(driver, 30)
      wait1 = WebDriverWait(driver, 1)
      #element 1 is the 'New email' button
     # //*[@id="id__130"]
      try:
              #  id_num = 99 + i 
               # print(id_num)
                print("You're in here")
                el1 = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, "splitPrimaryButton")))
                el1.click()
                print("\n Found the 1st one")
                ele2 = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, "Z4n09")))
                ele2.send_keys(contact)
                ele3 = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, "ms-TextField-field")))
                ele3.send_keys(subject)
                ele4 = wait1.until(EC.presence_of_element_located((By.CLASS_NAME, "dFCbN")))
                ele4.send_keys(body)
                #print(id_num+"\n")
      except Exception as e:
                 print(f"Error during clicking. \nError: {e}")
          #for i in range(50): 
          ##      id_num = 149 + i 
            #    el1 = wait1.until(EC.presence_of_element_located((By.ID, f"id__{id_num}")))
            #    el1.click()
                
      #element 2 is the text box where you input the email of the person in question
     #THIS IS THE XPATH USED //*[@id="docking_InitVisiblePart_1"]/div/div[3]/div[1]/div/div[4]/div/div/div[1]
      #ele2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@Class="VbY1P T6Va1 Z4n09 EditorClass g7toD]"')))
      #ele2.send_keys(contact)
      #Element 3 is the subject line xpath
    #  ele3 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='docking_InitVisiblePart_1']")))
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

#sub_window_int()


#name, email, domain, password = account_info_in()
#print(password)
current_window = sign_in()
time.sleep(2)
new_email(current_window, "tcohenwest@gmail.com", "Work please", "If you see me then you have won.")
