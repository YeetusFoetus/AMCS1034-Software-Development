import os, sys
import customtkinter as ctk
import tkinter as tk
import ctypes
import tkinter.font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
from ChoreScheduler import ChoreScheduler
from GroceryListManager import groceryListManager
from BudgetTracker import BudgetTracker
from MealPlanner import MealPlanner

class main_menu():
    def __init__(self, root):
        self.root = root
        self.main_menu()   ## call to return to main menu

        self.chore_module = ChoreScheduler(self.root, back_callback = self.main_menu)
        self.grocery_module = groceryListManager(self.root, back_callback = self.main_menu)
        self.budget_module = BudgetTracker(self.root, back_callback = self.main_menu)
        self.meal_module = MealPlanner(self.root, back_callback = self.main_menu)

        ctk.set_appearance_mode("Light")

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(self.root, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()   # send it behind everything

        #WELCOME TITLE
        #load ttf file into Windows at runtime(running with 'file=' couldn't work)
        ctypes.windll.gdi32.AddFontResourceExW(
            r"Nunito/static/Nunito-SemiBold.ttf",
            16,
            0
        )
        label_frame = ctk.CTkFrame(self.root, width=497, height=47, corner_radius=0, border_width=2, border_color="black", fg_color="#c3b091")
        label_frame.pack(pady=20, side="top")
        label_frame.pack_propagate(False)
        
        label = ctk.CTkLabel(label_frame, 
                     text="HomeLife", 
                     font=("Nunito SemiBold", 40)
                    )
        label.pack(pady=5)
        label.pack_propagate(False)
        #-------------
        
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

        #SET DEFAULT WINDOW SIZE 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 

        width = int(screen_width * 1)
        height = int(screen_height * 1)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(400, 300)
        #------

        #FRAME FOR BUTTONS
        main_frame0 = ctk.CTkFrame(self.root, 
                                   width=950, 
                                   height=550, 
                                   corner_radius=0, 
                                   border_width=2, 
                                   border_color="black", 
                                   fg_color="#c3b091"
                                   )
        
        main_frame0.pack(pady=(40, 0), anchor='center')
        main_frame0.pack_propagate(False)

        #c3b091
        main_frame2 = ctk.CTkFrame(main_frame0, fg_color="#c3b091")
        main_frame2.pack(side='bottom', pady=35, anchor='center')

        main_frame1 = ctk.CTkFrame(main_frame0, fg_color="#c3b091")
        main_frame1.pack(side="bottom", pady=(15, 35), anchor='center')
        #------

        #BUTTONS
        #glm_frame = ctk.CTkFrame(main_frame1, fg_color="red")
        #glm_frame.pack(side="left", padx=75)
        #ctk.CTkLabel(glm_frame, text = "Grocery List ", font=("Nunito Semibold", 24)).pack()
        glm_button = ctk.CTkButton(main_frame1, 
                                   text="Grocery List\nManager", 
                                   width=5,  
                                   image=photo1, 
                                   fg_color="#f7e7ce",
                                   hover_color="#e6d5b8", 
                                   text_color="black",
                                   command=self.open_grocery)
        glm_button.image = photo1
        glm_button.pack(side="left", padx=75)
        #glm_button.pack(pady=10)
        
        #cs_frame = ctk.CTkFrame(main_frame1, fg_color="blue")
        #cs_frame.pack(side="left", padx=75) 
        #ctk.CTkLabel(cs_frame, text = "Chore Scheduler", font=("Nunito SemiBold", 24)).pack()
        cs_button = ctk.CTkButton(main_frame1, 
                                  text="   Chore\n   Scheduler", 
                                  width=5, image=photo2, 
                                  fg_color="#f7e7ce",
                                  hover_color="#e6d5b8", 
                                  text_color="black", 
                                  command=self.open_chore)
        cs_button.image = photo2
        cs_button.pack(side="left", padx=75)
        #cs_button.pack(pady=10)
        
        #bt_frame = ctk.CTkFrame(main_frame2, fg_color="#f7e7ce")
        #bt_frame.pack(anchor='n', side="left", padx=75)
        #ctk.CTkLabel(bt_frame, text = "Budget Tracker", font=("Nunito SemiBold", 24)).pack()
        bt_button = ctk.CTkButton(main_frame2, 
                                  text="        Budget\n        Tracker", 
                                  width=5,  image=photo3, 
                                  fg_color="#f7e7ce", 
                                  hover_color="#e6d5b8", 
                                  text_color="black", 
                                  command=self.open_budget)
        bt_button.image = photo3
        bt_button.pack(side="left", padx=75)
        #bt_button.pack(pady=10, fill="both", expand=True)
        
        #mp_frame = ctk.CTkFrame(main_frame2, fg_color="#f7e7ce")
        #mp_frame.pack(anchor='n', side='left', padx=75)
        #ctk.CTkLabel(mp_frame, text="Meal Planner", font=("Nunito SemiBold", 24)).pack()
        mp_button = ctk.CTkButton(main_frame2, 
                                  text="        Meal\n        Planner", 
                                  width=5,  image=photo4, 
                                  fg_color="#f7e7ce", 
                                  hover_color="#e6d5b8", 
                                  text_color="black", 
                                  command=self.open_meal)
        mp_button.image = photo4
        mp_button.pack(side="left", padx=75)
        #mp_button.pack(pady=10, fill="both", expand=True)

        exit = ctk.CTkButton(self.root, 
                             text = "Exit", 
                             text_color="red", 
                             fg_color="#f7e7ce", 
                             border_width=2,
                             border_color='red',
                             hover_color="#e6d5b8",
                             command=self.exit_program)
        exit.pack(pady=(0, 60), side="bottom")
        #------

    def open_grocery(self):
        self.grocery_module.menu()

    def open_chore(self):
        self.chore_module.menu()

    def open_budget(self):
        self.budget_module.menu()

    def open_meal(self):
        self.meal_module.menu()

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
