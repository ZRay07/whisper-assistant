from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from tkinter import*
from source.core.model_interface import*
#from model_interface import*
#This function is meant to make email sign in smoother 


def create_account():
  #Prompt user to give a name
       microphone.record(4)
       pred_name = whisper.use_model(RECORD_PATH)
      #display the name

      #if correct - > 
      #prompt user for email -> if correct write to a .txt
       microphone.record(4)
       pred_email = whisper.use_model(RECORD_PATH)
       account = {
           "name" : pred_name ,
           "email" : pred_email
         }
       #This one should overwrite any previous data
       return account

    

def add_to_contact_list():
      #Prompt user to give a name
       microphone.record(4)
       pred_name = whisper.use_model(RECORD_PATH)
      #display the name

      #if correct - > 
      #prompt user for email
       microphone.record(4)
       pred_email = whisper.use_model(RECORD_PATH)
     #potentially use a dict
      
       new_contact = {
           "name" : pred_name ,
           "email" : pred_email
         }
       # -> if correct write to a .txt append 
       return new_contact

def act_sub_level():
        sub = Toplevel()
        sub.title("Sub Window for web navigation")
        sub.minsize(200,200)
        sub.config(bg = "Skyblue")
        sub.geometry("1100x700+480+200")