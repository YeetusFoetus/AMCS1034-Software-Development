import os.path as path
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter


class ChoreScheduler:
    def __init__(self, root, back_callback):
        self.root = root
        self.toplevel_window3 = None
        self.chore_list = []
        self.locations_list = []
        self.members_list = []
        self.back_callback = back_callback ## function to call to go back to main menu 

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()  

        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(self.root, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()   # send it behind everything

        #---------------------FRAMES---------------------
        self.OverBG = ctk.CTkFrame(self.root, width=700, height=765, fg_color="#c3b091")
        self.OverBG.pack(side='top', anchor='center', pady=10)
        self.OverBG.pack_propagate(False)
        self.tabframe = ctk.CTkFrame(self.OverBG, fg_color='red')
        self.tabframe.pack(side='top', anchor='center', padx=5, pady=10)
        #------------------------BUTTONS-----------------------------
        '''self.menu_tabview = ctk.CTkTabview(frame,
                                           #width=700,
                                           #height=850,
                                           corner_radius=0,
                                           text_color="black",
                                           segmented_button_selected_color="#f7e7ce",
                                           segmented_button_selected_hover_color="white",
                                           fg_color="#c3b091")
        self.menu_tabview.pack(padx=20, pady=20)
        self.menu_tabview.pack_propagate(False)
        self.menu_tabview.add("Today's Tasks")
        self.menu_tabview.add("Locations")
        self.menu_tabview.add("Members")'''

        self.b_button = ctk.CTkButton(self.OverBG, text='Back', command=self.back_callback)
        self.b_button.pack(side='bottom', pady=20, anchor='center')

        self.tt_button = ctk.CTkButton(self.tabframe, text="Today's Tasks", command=self.first_tab)
        self.tt_button.pack(side='left', padx=5, pady=10)

        self.l_button = ctk.CTkButton(self.tabframe, text="Locations", command=self.second_tab)
        self.l_button.pack(side='left', padx=5, pady=10)

        self.m_button = ctk.CTkButton(self.tabframe, text="Members", command=self.third_tab)
        self.m_button.pack(side='left', padx=5, pady=10)
       
    #------------------------FIRST TAB-----------------------------
    def first_tab(self):
        self.frametb1 = ctk.CTkFrame(self.OverBG).grid(sticky='nsew')
        if len(self.chore_list) == 0:
            no_tasks = ctk.CTkLabel(self.frametb1, text = "No tasks yet")
            no_tasks.grid(row=0, column=5, padx=20, pady=20)
            
            add_task = ctk.CTkButton(self.frametb1, text = "Add task", command = self.add_chore_form)
            add_task.grid(row=1, column=5, padx=20, pady=20)

            back = ctk.CTkButton(self.frametb1, text = "Back", command = self.back_callback)
            back.grid(row=2, column=5, padx=20, pady=20)
        else:
            self.store_archive()

    #---------------------------SECOND TAB---------------------------
    def second_tab(self):  
        for widget in self.OverBG.winfo_children():
                if widget is not self.tabframe:
                    widget.destroy()

        if len(self.locations_list) == 0:                        
            self.frametb2 = tk.Frame(self.OverBG, width=200, height=200)
            self.frametb2.pack()
            self.frametb2.pack_propagate(False)
            ctk.CTkLabel(self.frametb2, text="No locations yet? Add one now!").pack()
            ctk.CTkButton(self.frametb2, text="Add location", command=self.add_locations).pack()
            self.toplevel_window2 = None

        else:
            location_table = ttk.Treeview(self.frametb2,
                                          columns=("Locations"), 
                                          show="headings",
                                          height=10)
            location_table.heading("Locations", text="Locations")
            
            for location in self.locations_list:
                location_table.insert("", "end", values=location)

            location_table.pack(anchor='center')

        ctk.CTkButton(self.frametb2, text='Back', command=self.back_callback).pack(side='bottom', pady=10)
        ctk.CTkButton(self.frametb2, text='Delete').pack(side='bottom', pady=10)
        ctk.CTkButton(self.frametb2, text='Add').pack(side='bottom', pady=10)

    #----------------------------THIRD TAB--------------------------
    def third_tab(self):
        if len(self.members_list) == 0:
            for widget in self.OverBG.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.OverBG, text="No members yet? Add one now!").pack()
            ctk.CTkButton(self.OverBG, text="Add member").pack()
    

    #-------------------------TODAY'S TASKS---------------------------------------------
    def store_archive(self):
        table_frame = ctk.CTkFrame(self.OverBG)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_archive = ttk.Treeview(table_frame, 
                                         columns=("Chore", "Location", "Member", "Due By", "Repeat", "Status"), 
                                         show="headings", 
                                         height=10)
        
        self.tree_archive.heading("Chore", text = "Chore")
        self.tree_archive.heading("Location", text = "Location")
        self.tree_archive.heading("Member", text="Member")
        self.tree_archive.heading("Due By", text = "Due By")
        self.tree_archive.heading("Repeat", text="Repeat")
        self.tree_archive.heading("Status", text = "Status")

        for item in self.tree_archive.get_children():
            self.tree_archive.delete(item)

        for chore in self.chore_list:
            self.tree_archive.insert("", "end", values=chore)
        
        self.tree_archive.pack(fill="both", expand=True)

        button_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
        button_frame.pack(fill="x", pady=5)

        ctk.CTkButton(button_frame, text = "Back", command = self.back_callback).pack(side = "bottom")
        ctk.CTkButton(button_frame, text = "Delete All Tasks", command = self.delete_chore).pack(side="bottom")
        ctk.CTkButton(button_frame, text = "Add Task", command = self.add_chore_form).pack(side = "bottom")
    
    def save_chore(self):
        new_chore = self.entry.get().strip()
        if new_chore:
            self.chore_list.append(new_chore)
        self.menu()

    def delete_chore(self):
        selected = self.tree_archive.selection()
        if selected:
            for iid in selected:
                chore_name = self.tree_archive.item(iid)["values"][0]
                del self.chore_list[chore_name]
                self.tree_archive.delete(iid)

    def add_chore_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text = "Enter new task: ").pack(pady = 10)
        
        self.entry = ttk.Entry(self.root, width=25)
        self.entry.pack(pady=5)

        tk.Button(self.root, text = "Save", command = self.save_chore).pack(pady=5)
        tk.Button(self.root, text = "Back", command = self.menu).pack(pady = 10)

    #--------------------LOCATIONS--------------------------        
    def add_locations(self):
        if self.toplevel_window2 == None or not self.toplevel_window2.winfo_exists():
            self.toplevel_window2 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window2.after(10, lambda: self.toplevel_window2.focus_force())
            self.toplevel_window2.grab_set()
            self.toplevel_window2.title("Add a location")
            self.toplevel_window2.minsize(300, 300)
            self.location_entry = ctk.CTkEntry(self.toplevel_window2)
            self.location_entry.pack(pady=20)
            button = ctk.CTkButton(self.toplevel_window2, text='Add', command=self.get_location)
            button.pack(side='bottom', anchor='center')
        else:
            self.toplevel_window2.focus()

    def get_location(self):
        location = self.location_entry.get()
        self.locations_list.append(location)
        self.toplevel_window2.destroy()
        print(location)



    
