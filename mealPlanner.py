# get like an input prompt asking the user like what typa diet they going for
# like they tryna lose weight or bulk or whatever right
# then output a list of what they should eat for breakfast lunch and dinner based on the prompt
#tf do i do again
from tkinter import *

class mealPlanner:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.categories = ["something"]
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
        Label(self.root, text="Welcome to Budget Tracker").pack(pady=10)
        self.budget_page = Frame(self.root)
        self.budget_page.pack(pady = 20)
        Button(self.root, text = "Placeholder1", width = 25, height = 2, command = self.back_callback).pack(pady = 20)
        Button(self.root, text = "2", width = 25, height = 2, command = print("hi")).pack(pady = 20)
        Button(self.root, text = "3", width = 25, height = 2, command = print("print")).pack(pady = 20)
        Button(self.root, text = "Back", command = self.back_callback).pack(pady = 20)


        