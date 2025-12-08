import os.path as path
import json
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("Light")


class Test:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def test_notebook(self):
        tabview = ctk.CTkTabview(self.root, 
                                 text_color="black",
                                 segmented_button_selected_color="#f7e7ce",
                                 segmented_button_selected_hover_color="white",
                                 fg_color="#c3b091")
        tabview.pack(expand = True, fill = "both")

        tabview.add("Archive") # add tab at the end
        tabview.add("Today's Chore List")
        tabview.add("Members")
        tabview.set("Archive") # set currently visible tab

        button = ctk.CTkButton(tabview.tab("Archive"), text = "Hello", command=self.hello)
        button.pack(padx=20, pady=20)
        
        ctk.CTkButton(self.root, text="Back", fg_color="#f7e7ce", text_color="black", command=self.back_callback).pack(side="bottom")

    def hello(self):
        print("hello")

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.test_notebook()