import os, sys
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
from PIL import Image, ImageTk

class main_menu():
    def __init__(self, root):
        self.root = root
        
        #IMAGES
        chore_img = Image.open("chore.png")
        chore_icon = chore_img.resize((300, 300), Image.Resampling.LANCZOS)
        grocery_img = Image.open("grocery.png")
        grocery_icon = grocery_img.resize((300, 300), Image.Resampling.LANCZOS)
        budget_img = Image.open("budget.png")
        budget_icon = budget_img.resize((300, 300), Image.Resampling.LANCZOS)
        meal_img = Image.open("meal.png")
        meal_icon = meal_img.resize((300, 300), Image.Resampling.LANCZOS)
        photo1 = ImageTk.PhotoImage(chore_icon)
        photo2 = ImageTk.PhotoImage(grocery_icon)
        photo3 = ImageTk.PhotoImage(budget_icon)
        photo4 = ImageTk.PhotoImage(meal_icon)
        #------

        #CHANGE FONT SIZE
        #style.configure('custom.TButton', font = ('Arial', 35, 'bold')) #changes font size to 25
        #------

        #SET DEFAULT WINDOW SIZE TO FULL SCREEN 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 

        width = int(screen_width * 1)
        height = int(screen_height * 1)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(600, 400)
        #------

        #FRAME FOR BUTTONS
        main_frame1 = ttk.Frame(self.root)
        main_frame1.place(relx=0.01, rely=0.25, relwidth=0.24, relheight=0.9)
        main_frame2 = ttk.Frame(self.root)
        main_frame2.place(relx=0.2, rely=0.25, relwidth=0.24, relheight=0.9)
        #------

        #BUTTONS
        glm_frame = ttk.Frame(main_frame1)
        glm_frame.pack()
        tk.Label(glm_frame, text = "Grocery List Manager").pack()
        glm_button = tk.Button(glm_frame, text="     ", width=5,  image=photo2)
        glm_button.image = photo2
        glm_button.pack(pady=10, fill="both", expand=True)
        
        cs_frame = ttk.Frame(main_frame1)
        cs_frame.pack() 
        tk.Label(cs_frame, text = "Chore Scheduler").pack()
        cs_button = tk.Button(cs_frame, text="     ", width=5,  image=photo1)
        cs_button.image = photo1
        cs_button.pack(pady=10, fill="both", expand=True)
        
        bt_frame = ttk.Frame(main_frame2)
        bt_frame.pack()
        tk.Label(bt_frame, text = "Budget Tracker").pack()
        bt_button = tk.Button(bt_frame, text="     ", width=5,  image=photo3)
        bt_button.image = photo3
        bt_button.pack(pady=10, fill="both", expand=True)
        
        mp_frame = ttk.Frame(main_frame2)
        mp_frame.pack()
        tk.Label(mp_frame, text="Meal Planner").pack()
        mp_button = tk.Button(mp_frame, text="     ", width=5,  image=photo4)
        mp_button.image = photo4
        mp_button.pack(pady=10, fill="both", expand=True)

        quit = ctk.CTkButton(self.root, text = "Exit")
        quit.pack(side="bottom")
        #------


if __name__ == "__main__":
    root = ctk.CTk()
    app = main_menu(root)
    root.mainloop()
