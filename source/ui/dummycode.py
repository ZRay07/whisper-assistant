

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

format_email("T. Cohen West")
