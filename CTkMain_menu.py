import os, sys
import customtkinter as ctk
import tkinter as tk
import ctypes
import tkinter.font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk
from ChoreScheduler_test import ChoreScheduler
from GroceryListManager import groceryListManager
from BudgetTracker import BudgetTracker

class main_menu():
    def __init__(self, root):
        self.root = root
        self.main_menu()   ## call to return to main menu

        self.chore_module = ChoreScheduler(self.root, back_callback = self.main_menu)
        self.grocery_module = groceryListManager(self.root, back_callback = self.main_menu)
        self.budget_module = BudgetTracker(self.root, back_callback = self.main_menu)

        ctk.set_appearance_mode("Light")

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #WELCOME TITLE
        #load ttf file into Windows at runtime(running with 'file=' couldn't work)
        ctypes.windll.gdi32.AddFontResourceExW(
            r"Nunito/static/Nunito-SemiBold.ttf",
            16,
            0
        )
        ctk.CTkLabel(self.root, text="Welcome to HomeLife", font=("Nunito SemiBold", 40)).pack(pady=60, side="top")
        #------
        
        #IMAGES
        chore_img = Image.open("chore.png")
        chore_icon = chore_img.resize((240, 240), Image.Resampling.LANCZOS)
        grocery_img = Image.open("grocery.png")
        grocery_icon = grocery_img.resize((240, 240), Image.Resampling.LANCZOS)
        budget_img = Image.open("budget.png")
        budget_icon = budget_img.resize((240, 240), Image.Resampling.LANCZOS)
        meal_img = Image.open("meal.png")
        meal_icon = meal_img.resize((240, 240), Image.Resampling.LANCZOS)
        photo1 = ImageTk.PhotoImage(grocery_icon)
        photo2 = ImageTk.PhotoImage(chore_icon)
        photo3 = ImageTk.PhotoImage(budget_icon)
        photo4 = ImageTk.PhotoImage(meal_icon)
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
        main_frame1 = ctk.CTkFrame(self.root, fg_color="#c3b091")
        main_frame1.place(relx=0, rely=0.35, relwidth=1, relheight=0.3)
        ##main_frame2 = ctk.CTkFrame(self.root)
        ##main_frame2.place(relx=0.6, rely=0.25, relwidth=0.25, relheight=0.9)
        #------

        #BUTTONS
        glm_frame = ctk.CTkFrame(main_frame1, fg_color="#f7e7ce")
        glm_frame.pack(side="left", padx=75)
        ctk.CTkLabel(glm_frame, text = "Grocery List Manager", font=("Nunito Semibold", 24)).pack()
        glm_button = ctk.CTkButton(glm_frame, text="     ", width=5,  image=photo1, fg_color="#f7e7ce", command=self.open_grocery)
        glm_button.image = photo1
        glm_button.pack(pady=10)
        
        cs_frame = ctk.CTkFrame(main_frame1, fg_color="#f7e7ce")
        cs_frame.pack(side="left", padx=75) 
        ctk.CTkLabel(cs_frame, text = "Chore Scheduler", font=("Nunito SemiBold", 24)).pack()
        cs_button = ctk.CTkButton(cs_frame, text="     ", width=5, image=photo2, fg_color="#f7e7ce", command=self.open_chore)
        cs_button.image = photo2
        cs_button.pack(pady=10)
        
        bt_frame = ctk.CTkFrame(main_frame1, fg_color="#f7e7ce")
        bt_frame.pack(side="left", padx=75)
        ctk.CTkLabel(bt_frame, text = "Budget Tracker", font=("Nunito SemiBold", 24)).pack()
        bt_button = ctk.CTkButton(bt_frame, text="     ", width=5,  image=photo3, fg_color="#f7e7ce", command=self.open_budget)
        bt_button.image = photo3
        bt_button.pack(pady=10, fill="both", expand=True)
        
        mp_frame = ctk.CTkFrame(main_frame1, fg_color="#f7e7ce")
        mp_frame.pack(side="left", padx=75)
        ctk.CTkLabel(mp_frame, text="Meal Planner", font=("Nunito SemiBold", 24)).pack()
        mp_button = ctk.CTkButton(mp_frame, text="     ", width=5,  image=photo4, fg_color="#f7e7ce", command=self.open_meal)
        mp_button.image = photo4
        mp_button.pack(pady=10, fill="both", expand=True)

        exit = ctk.CTkButton(self.root, text = "Exit", command=self.exit_program)
        exit.pack(pady=60, side="bottom")
        #------

    def open_grocery(self):
        self.grocery_module.menu()

    def open_chore(self):
        self.chore_module.menu()

    def open_budget(self):
        self.budget_module.menu()

    def open_meal(self):
        print("Meal Planner clicked")

    def exit_program(self):
        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("HomeLife")
    
    #title bar icon
    icon_image = Image.open("house.png")
    icon_image = icon_image.resize((16, 16), Image.Resampling.LANCZOS)
    icon_image.save("house.ico", format="ICO")
    root.iconbitmap("house.ico")
    #------ 

    root.configure(fg_color="#c3b091")
    app = main_menu(root)
    root.mainloop()
