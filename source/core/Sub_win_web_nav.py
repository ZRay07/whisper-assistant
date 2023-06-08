from tkinter import *
#from source.core.search_bar_fire_fox import*

class main_screen:
    def __init__(self):
        # Create root window
        self.root = Tk()
        self.root.title("Super Helpful Engine Recognizing Peoples Audio")    # title of the window
        self.root.minsize(200, 200)          # set a min size of 200 x 200 pixels
        self.root.config(bg = "skyblue")     # set the background color

        # Set the starting size of the window and its location
        self.root.geometry("1100x700+480+200")
       
        #Create a  sub window
 
        
        #make frames within the window
        self.drawRightFrame()
        self.drawLeftFrame()
        self.root = mainloop() 
    def drawLeftFrame(self):
        # Create left frame
        self.left_frame = Frame(self.root, width = 500, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.left_frame.grid(row = 0, column = 0, padx = 10, pady = 10) 
    def act_sub_level(self):
        self.sub = Toplevel()
        self.sub.title("Sub Window for web navigation")
        self.sub.minsize(200,200)
        self.sub.config(bg = "Skyblue")
        self.sub.geometry("1100x700+480+200")
    def drawRightFrame(self):
        # Create right frame
        self.right_frame = Frame(self.root, width = 500, height = 530,
                                 bg = "white", borderwidth = 2, relief = "raised")
        self.right_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.cmd_bar = Frame(self.right_frame, width = 100, height = 200, bg = "white")
        self.cmd_bar.grid(row = 2, column = 0)
        # Ensure the frame does not shrink to fit widget size
        self.right_frame.grid_propagate(False)
        self.beginwebnav = Button(self.cmd_bar, text = "Begin Website Navigation", command = self.act_sub_level, bg = "light grey", activebackground = "green", activeforeground = "skyblue", relief = RAISED)
        self.beginwebnav.grid(row = 0, column = 0, padx = 10, pady = 10)


if __name__ == '__main__':
    main_screen()


       