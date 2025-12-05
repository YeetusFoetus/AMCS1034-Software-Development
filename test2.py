import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from tkinter.font import nametofont

class main_menu():
    def __init__(self, root):
        self.root = root

        #CHANGE FONT SIZE
        style.configure('custom.TButton', font = ('Arial', 35, 'bold')) #changes font size to 25
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
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.05, rely=0.25, relwidth=0.5, relheight=0.5)
        
        glm_frame = ttk.Frame(main_frame)
        glm_frame.pack()
        tb.Label(glm_frame, text = "Placeholder").pack()
        tb.Button(glm_frame, text="Grocery List Manager", width=20, bootstyle="primary", style = 'custom.TButton').pack(pady=10, fill="both", expand=True)
        
        cs_frame = ttk.Frame(main_frame)
        cs_frame.pack() 
        tb.Label(cs_frame, text = "Placeholder")
        tb.Button(cs_frame, text="Chore Scheduler", width=20, bootstyle="primary", style = 'custom.TButton').pack(pady=10, fill="both", expand=True)
        
        bt_frame = ttk.Frame(main_frame)
        bt_frame.pack()
        tb.Label(bt_frame, text = "Placeholder")
        tb.Button(bt_frame, text="Budget Tracker", width=20, bootstyle="primary", style = 'custom.TButton').pack(pady=10, fill="both", expand=True)
        
        mp_frame = ttk.Frame(main_frame)
        mp_frame.pack()
        tb.Label(mp_frame, text="Placeholder")
        tb.Button(mp_frame, text="Meal Planner", width=20, bootstyle="primary", style = 'custom.TButton').pack(pady=10, fill="both", expand=True)
        #------

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    style = tb.Style()
    app = main_menu(root)
    root.mainloop()
