# Source - https://stackoverflow.com/q
# Posted by user1340081
# Retrieved 2025-12-05, License - CC BY-SA 3.0

import tkinter
import ttkbootstrap as ttk
from tkinter.font import nametofont

class simpleapp_tk():
    def __init__(self, root):
        self.root = root

        #CHANGE FONT SIZE
        style.configure('custom.TButton', font = ('Times New Roman', 35, 'bold')) #changes font size to 25
        #---

        #SET DEFAULT WINDOW SIZE TO FULL SCREEN 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 

        width = int(screen_width * 1)
        height = int(screen_height * 1)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(600, 400)
        #---

        ttk.Label(self.root, text = "Styled Label", style = 'custom.TLabel').pack(pady=20)
        ttk.Button(self.root, text="Small Button", bootstyle="primary sm", style = 'custom.TButton').pack(pady=10)
        ttk.Button(self.root, text="Large Button", bootstyle="primary lg").pack(pady=10)
        ttk.Button(self.root, text="Default Button", bootstyle="info").pack(pady=10)
        ttk.Button(self.root, text="Big Button", width= 100, bootstyle="primary").pack(pady=10)

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    style = ttk.Style()
    app = simpleapp_tk(root)
    root.mainloop()
