import os.path as path
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter


class ChoreScheduler:
    def __init__(self, root, back_callback):
        self.root = root
        self.chore_list = []
        self.locations_list = []
        self.members_list = []
        self.back_callback = back_callback ## function to call to go back to main menu 
        self.status = 5

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

        #---------------------(SOME)FRAMES---------------------
        label_frame = ctk.CTkFrame(self.root, width=497, height=47, corner_radius=0, border_width=2, border_color="black", fg_color="#c3b091")
        label_frame.pack(pady=20)
        label_frame.pack_propagate(False)

        self.OverBG = ctk.CTkFrame(self.root, width=1000, height=500, corner_radius=0, border_width=2, border_color="black", fg_color="#c3b091")
        self.OverBG.pack(anchor='center', pady=100)
        self.OverBG.pack_propagate(False)

        self.tabframe = ctk.CTkFrame(self.OverBG, fg_color='#b09e83')
        self.tabframe.pack(side='top', anchor='center', padx=5, pady=10)
        #------------------------------------------------
        
        #--------------------TITLE-----------------------
        label = ctk.CTkLabel(label_frame, 
                     text="Chore Scheduler", 
                     font=("Nunito SemiBold", 40)
                    )
        label.pack(pady=5)
        label.pack_propagate(False)
        #------------------------------------------------ 

        #------------------------TABVIEW-----------------------------
        self.b_button = tk.Button(self.OverBG, 
                                      text='Back to main menu',
                                      font=('TkDefaultFont', 11),
                                      command=self.back_callback
                                      )
        self.b_button.pack(side='bottom', pady=20, anchor='center')

        self.tt_button = tk.Button(self.tabframe, text="Today's Tasks",
                                   font=('TkDefaultFont', 14),
                                       command=self.first_tab, 
                                        )
        self.tt_button.pack(side='left', padx=5, pady=10)

        self.l_button = tk.Button(self.tabframe, text="Locations",
                                  font=('TkDefaultFont', 14),
                                      command=self.second_tab
                                      )
        self.l_button.pack(side='left', padx=5, pady=10)

        self.m_button = tk.Button(self.tabframe, text="Members",
                                  font=('TkDefaultFont', 14),
                                      command=self.third_tab, 
                                      )
        self.m_button.pack(side='left', padx=5, pady=10)
       
        self.first_tab()
    #------------------------FIRST TAB-----------------------------
    def first_tab(self):
        for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()

        self.frametb1 = tk.Frame(self.OverBG, width=550, height=575, bg='#c3b091')
        self.frametb1.pack()
        self.frametb1.pack_propagate(False)

        if len(self.chore_list) == 0:
            nty_frame = ctk.CTkFrame(self.frametb1, fg_color="#c3b091")
            nty_frame.pack(anchor='center', pady=(50, 0))

            no_tasks = ctk.CTkLabel(nty_frame, text = "No tasks yet", font=('TkDefaultFont', 14))
            no_tasks.pack(anchor='center')
            
            add_task = tk.Button(nty_frame, text = "Add task", font=('TkDefaultFont', 12), command = self.add_chore_form)
            add_task.pack(pady=10)

            self.toplevel_window1 = None
        else:
            self.task_table()

    #---------------------------SECOND TAB---------------------------
    def second_tab(self):  
        for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()        

        if len(self.locations_list) == 0:    
            nly_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
            nly_frame.pack(anchor='center', pady=(50, 0))    

            ctk.CTkLabel(nly_frame, text="No locations yet? Add one now!", font=('TkDefaultFont', 14)).pack(anchor='center')

            tk.Button(nly_frame, text="Add", font=('TkDefaultFont', 12), command=self.add_locations).pack(pady=10)

            self.toplevel_window2 = None

        else:
            for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()

            self.frametb2 = tk.Frame(self.OverBG, width=550, height=300)
            self.frametb2.pack(pady=(40, 0))
            self.frametb2.pack_propagate(False)

            self.location_table = ttk.Treeview(self.frametb2,
                                          columns=("Locations",), 
                                          show="headings",
                                          height=10)
            self.location_table.heading("Locations", text="Locations")

            scrollbar = ttk.Scrollbar(self.frametb2, orient='vertical', command=self.location_table.yview)
            
            self.location_table.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            self.location_table.configure(yscrollcommand=scrollbar.set)

            for location in self.locations_list:
                self.location_table.insert("", "end", values=(location,))

            button_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
            button_frame.pack(side="bottom", pady=10)

            tk.Button(button_frame, text="Add", font=('TkDefaultFont', 12), command=self.add_locations).pack(padx=10)
            tk.Button(button_frame, text="Delete", font=('TkDefaultFont', 12), command=self.delete_location).pack(padx=10)


    #----------------------------THIRD TAB--------------------------
    def third_tab(self):
        for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()

        if len(self.members_list) == 0:         
            nmy_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
            nmy_frame.pack(anchor='center', pady=(50, 0))      

            ctk.CTkLabel(nmy_frame, text="No members yet? Add one now!", font=('TkDefaultFont', 14)).pack(anchor='center')
            self.toplevel_window3 = None

            tk.Button(nmy_frame, text="Add", font=('TkDefaultFont', 12), command=self.add_members).pack(pady=10)

        else:
            for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()
                
            self.frametb3 = tk.Frame(self.OverBG, width=550, height=300)
            self.frametb3.pack(pady=(40, 0))
            self.frametb3.pack_propagate(False)

            self.member_table = ttk.Treeview(self.frametb3,
                                          columns=("Members",), 
                                          show="headings",
                                          height=10)
            self.member_table.heading("Members", text="Members")

            scrollbar = ttk.Scrollbar(self.frametb3, orient='vertical', command=self.member_table.yview)

            self.member_table.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            self.member_table.configure(yscrollcommand=scrollbar.set)
            
            for member in self.members_list:
                self.member_table.insert("", "end", values=(member,))

            button_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
            button_frame.pack(side='bottom', pady=10)

            tk.Button(button_frame, text="Add", font=('TkDefaultFont', 12), command=self.add_members).pack(padx=10)
            tk.Button(button_frame, text='Delete', font=('TkDefaultFont', 12), command=self.delete_member).pack(padx=10)    

    #-------------------------TODAY'S TASKS---------------------------------------------
    def add_chore_form(self):
        if self.toplevel_window1 == None or not self.toplevel_window1.winfo_exists():
            self.toplevel_window1 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window1.after(10, lambda: self.toplevel_window1.focus_force())
            self.toplevel_window1.grab_set()
            self.toplevel_window1.title("Add a task")
            self.toplevel_window1.minsize(300, 300)

            frame_addchore1 = ctk.CTkFrame(self.toplevel_window1)
            frame_addchore1.pack(pady=5)
            frame_addchore2 = ctk.CTkFrame(self.toplevel_window1)
            frame_addchore2.pack(pady=5)
            frame_addchore3 = ctk.CTkFrame(self.toplevel_window1)
            frame_addchore3.pack(pady=5)
            frame_addchore4 = ctk.CTkFrame(self.toplevel_window1)
            frame_addchore4.pack(pady=5)
            frame_addchore5 = ctk.CTkFrame(self.toplevel_window1)
            frame_addchore5.pack(pady=5)

            ctk.CTkLabel(frame_addchore1, text='Chore: ').pack(side='left', padx=5, pady=5)
            self.task_entry = ctk.CTkEntry(frame_addchore1)
            self.task_entry.pack(side='left', pady=5)

            ctk.CTkLabel(frame_addchore2, text='Location: ').pack(side='left', padx=5, pady=5)
            self.location_menu = ctk.CTkOptionMenu(frame_addchore2, values=self.locations_list) 
            self.location_menu.pack(fill="x", padx=5, pady=5)   

            ctk.CTkLabel(frame_addchore3, text='Member: ').pack(side='left', padx=5, pady=5)
            self.member_menu = ctk.CTkOptionMenu(frame_addchore3, values=self.members_list)
            self.member_menu.pack(fill="x", padx=5, pady=5)  

            ctk.CTkLabel(frame_addchore4, text='Due By: ').pack(side='left', padx=5, pady=5)
            self.date_entry = ctk.CTkEntry(frame_addchore4)
            self.date_entry.pack(side='left', pady=5)

            ctk.CTkLabel(frame_addchore5, text='Repeat: ').pack(side='left', padx=5, pady=5)
            self.repeat_entry = ctk.CTkEntry(frame_addchore5)
            self.repeat_entry.pack(side='left', pady=5)    
            
            button = ctk.CTkButton(self.toplevel_window1, text='Add', command=self.save_chore)
            button.pack(side='bottom', anchor='center', pady=5)            
        else:
            self.toplevel_window1.focus()
        
    def task_table(self):
        for widget in self.OverBG.winfo_children():
                if widget not in (self.tabframe, self.b_button):
                    widget.destroy()

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

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree_archive.yview)

        self.tree_archive.pack(side='left', fill="both", expand=True)
        scrollbar.pack(side='right', fill='y')
        self.tree_archive.configure(yscrollcommand=scrollbar.set)
        
        for item in self.tree_archive.get_children():
            self.tree_archive.delete(item)

        for chore in self.chore_list:
            self.tree_archive.insert("", "end", values=chore)

        button_frame = ctk.CTkFrame(self.OverBG, fg_color="#c3b091")
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text = "Delete Task",
                  font=('TkDefaultFont', 12),
                  bg='pink',
                      command = self.delete_chore, 
                      ).pack(side="bottom", pady=(0, 3))
        
        tk.Button(button_frame, text = "Update Task",
                  font=('TkDefaultFont', 12),
                  bg='light blue',
                      command = self.update_chore, 
                      ).pack(side="bottom", pady=(0, 3))
        
        tk.Button(button_frame, text = "Add Task",
                  font=('TkDefaultFont', 12),
                  bg='light green',
                      command = self.add_chore_form, 
                      ).pack(side = "bottom", pady=(0, 3))
    
    def save_chore(self):
        task_name = self.task_entry.get().strip()
        location_name = self.location_menu.get()
        member_name = self.member_menu.get()
        due_date = self.date_entry.get()
        repetition = self.repeat_entry.get()

        if not task_name:
            self.toplevel_window_error1 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window_error1.after(10, lambda: self.toplevel_window_error1.focus_force())
            self.toplevel_window_error1.grab_set()
            self.toplevel_window_error1.title("Error")

            ctk.CTkLabel(self.toplevel_window_error1, text="Please enter a task name first").pack()

            return
        
        self.chore = [task_name, location_name, member_name, due_date, repetition, "Pending"]

        self.chore_list.append(self.chore)
        self.toplevel_window1.destroy()
        self.first_tab()

    def update_chore(self):
        selected = self.tree_archive.selection()
        if not selected:
            return

        for iid in selected:
            # Get current row values from Treeview
            values = list(self.tree_archive.item(iid)["values"])
            chore_name = values[0]
            current_status = values[5]

            # Toggle status
            new_status = "Done" if current_status == "Pending" else "Pending"
            values[5] = new_status

            # Update data list
            for chore in self.chore_list:
                if chore[0] == chore_name:
                    chore[5] = new_status
                    break

            # Update Treeview row
            self.tree_archive.item(iid, values=values)
        
    def delete_chore(self):
        selected = self.tree_archive.selection()
        if selected:
            for id in selected: 
                chore_name = self.tree_archive.item(id)["values"][0] 

                for chore in self.chore_list:
                    if chore[0] == chore_name:
                        self.chore_list.remove(chore)
                        self.tree_archive.delete(id)
                        break
                
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
        location = self.location_entry.get().strip()
        if not location:
            self.toplevel_window_error2 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window_error2.after(10, lambda: self.toplevel_window_error2.focus_force())
            self.toplevel_window_error2.grab_set()
            self.toplevel_window_error2.title("Error")

            ctk.CTkLabel(self.toplevel_window_error2, text="Please enter a location first").pack()

            return
        else:
            self.locations_list.append(location)
            #
            self.toplevel_window2.destroy()
            self.second_tab()

    def delete_location(self):
        selected = self.location_table.selection()
        if selected:
            for id in selected:
                location_name = self.location_table.item(id)["values"][0]
                location_name = str(location_name).strip()

                if location_name in self.locations_list:
                    self.locations_list.remove(location_name)
                    
                self.location_table.delete(id)

    #-------------------MEMBERS--------------------
    def add_members(self):
        if self.toplevel_window3 == None or not self.toplevel_window3.winfo_exists():
            self.toplevel_window3 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window3.after(10, lambda: self.toplevel_window3.focus_force())
            self.toplevel_window3.grab_set()
            self.toplevel_window3.title("Add a location")
            self.toplevel_window3.minsize(300, 300)
            self.member_entry = ctk.CTkEntry(self.toplevel_window3)
            self.member_entry.pack(pady=20)
            button = ctk.CTkButton(self.toplevel_window3, text='Add', command=self.get_member)
            button.pack(side='bottom', anchor='center')
        else:
            self.toplevel_window3.focus()

    def get_member(self):
        member = self.member_entry.get().strip()
        if not member:
            self.toplevel_window_error3 = ctk.CTkToplevel(self.OverBG)
            self.toplevel_window_error3.after(10, lambda: self.toplevel_window_error3.focus_force())
            self.toplevel_window_error3.grab_set()
            self.toplevel_window_error3.title("Error")

            ctk.CTkLabel(self.toplevel_window_error3, text="Please enter a member first").pack()

            return
        else:
            self.members_list.append(member)
            self.toplevel_window3.destroy()
            self.third_tab()


    def delete_member(self):
        selected = self.member_table.selection()
        if selected:
            for id in selected:
                member_name = self.member_table.item(id)["values"][0]
                member_name = str(member_name).strip()

                if member_name in self.members_list:
                    self.members_list.remove(member_name)
                    
                self.member_table.delete(id)
        
        

    
