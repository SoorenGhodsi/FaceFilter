# This is the program for the main user interface. It will be in control of what the user sees.

from tkinter import *


class RecognitionInterface:
    
    def __init__(self):
       self.root = Tk()
       self.root.title('Harmonizer')
       self.root.minsize(480, 270)
       self.root.geometry(str(int(round(self.root.winfo_screenwidth() * 0.7))) + 'x' +
                          str(int(round(self.root.winfo_screenheight()) * 0.7)))
       self.root.mainloop()   # makes sure window does not close immediately after initially running the program
