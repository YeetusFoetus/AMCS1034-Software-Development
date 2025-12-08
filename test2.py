import customtkinter as ctk

root = ctk.CTk()

fruit_list = {
    "apple":"Ripe",
    "orange":"Rotten",
    "banana":"Unripe"
}

scroll_frame = ctk.CTkScrollableFrame(root, width=400, height=300)
scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

header = ctk.CTkFrame(scroll_frame, fg_color="white")
header.pack(fill="x")

ctk.CTkLabel(header, text="Chore", width=150, anchor="w").grid(row=0, column=0)
ctk.CTkLabel(header, text="Status", width=100, anchor="w").grid(row=0, column=1)
ctk.CTkLabel(header, text="Action", width=100, anchor="w").grid(row=0, column=2)

for fruit, status in fruit_list.items():
    row = ctk.CTkFrame(scroll_frame)
    row.pack(fill="x", pady=2)
    
    ctk.CTkLabel(row, text=fruit, width=150, anchor="w").grid(row=0, column=0)
    ctk.CTkLabel(row, text=status, width=100, anchor="w").grid(row=0, column=1)
    
    # Example: delete button per row
    ctk.CTkOptionMenu(row, width=80,).grid(row=0, column=2)




root.mainloop()
