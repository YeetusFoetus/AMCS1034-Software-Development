# get like an input prompt asking the user like what typa diet they going for
# like they tryna lose weight or bulk or whatever right
# then output a list of what they should eat for breakfast lunch and dinner based on the prompt
#tf do i do again
from tkinter import *

class mealPlanner:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        print("INFO: 'mealPlanner' initialised successfully.")

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.App()

    def App(self):
        style_widgets_bgColour = "white"
        style_widgets_fgColour = "black"
        style_widgets_font = "Arial 12"

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Meal Planner - Household Management Assistant App") # Sets the title of the window
        self.root.geometry("800x600")    # Sets the size of the window
        self.root.configure(bg='white')  # Changes the background colour using 'configure' function

        categories = []

        