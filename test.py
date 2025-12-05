import os.path as path
import json
import tkinter as tk
from tkinter import ttk

class Test:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def test_notebook(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand = True, fill = 'both')

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text='Tab 1')
        notebook.add(tab2, text='Tab 2')
        
        ttk.Button(tab1, text="Back", command=self.back_callback).pack(side="bottom")

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.test_notebook()