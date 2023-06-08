from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from tkinter import*
#from model_interface import*
#This function is meant to conduct a google search

search = "bugs on sticks"
def google_search():
   # microphone.record(10)
   # prediction = whisper.use_model(RECORD_PATH)
    driver = webdriver.Firefox()

    #so the pages have time to load 
    wait = WebDriverWait(driver, 30)
    #Go to google
    driver.get("https://www.google.com/")
    
    #Find the search bar and enter what the user wants to search
    ele = wait.until(EC.element_to_be_clickable((By.ID, "APjFqb")))
    ele.send_keys(search)
    ele.send_keys(Keys.RETURN)
    time.sleep(2)
    #ele.click()

#google_search()

def act_sub_level():
        sub = Toplevel()
        sub.title("Sub Window for web navigation")
        sub.minsize(200,200)
        sub.config(bg = "Skyblue")
        sub.geometry("1100x700+480+200")