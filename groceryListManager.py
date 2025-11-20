# Import all the definitions from 'tkinter' library
import tkinter as tk
from tkinter import *

"""
PHASE 1
=======
Initialise the window

Note:
- Every window must be initialised with the following code.
"""
# Creates the main window
root = Tk()

# Sets the title of the window as 'Grocery List Manager - Household Management Assistant App'
root.title("Grocery List Manager - Household Management Assistant App")

# Sets the size of the window
root.geometry("800x600")

# Changes the background colour using 'configure' function
root.configure(bg='white')

"""
PHASE 2
=======
Designs form controls

Note:
- The following code designs the user interface for the grocery list manager.
"""
# Creates label
# Note: For labels in Tkinter, their inner text MUST be declared with StringVar() first.
label_appTitle_text = StringVar()
label_appTitle_text.set("Hi there!")
label_appTitle = Label(root,
                       textvariable = label_appTitle_text,
                       bg = "white",
                       fg = "black",
                       font = ("Arial", 28, "bold")
                       )

label_appDescription_text = StringVar()
label_appDescription_text.set("Let's manage your grocery list.")
label_appDescription = Label(root,
                             textvariable = label_appDescription_text,
                             bg = "white",
                             fg = "black",
                             font = ("Arial", 12)
                             )

"""
PHASE 3
=======
Setting up 'dynamic' form controls
(which involves their respective functions)
"""
# Creates a list of groceries
groceries = [
    {
        "name": "Cucumber",
        "category": "Vegetable",
        "quantity": 12
    },
    {
        "name": "Apple",
        "category": "Fruit",
        "quantity": 8
    },
    {
        "name": "Chicken meat",
        "category": "Raw meat",
        "quantity": 7
    },
    {
        "name": "Rice",
        "category": "Cereal grain",
        "quantity": 2
    },
    {
        "name": "Potato Chips",
        "category": "Snack",
        "quantity": 10
    },
    {
        "name": "Potato Tyre Chips",
        "category": "Snack",
        "quantity": 10
    },
    {
        "name": "Popcorn",
        "category": "Snack",
        "quantity": 10
    },
    {
        "name": "Muruku",
        "category": "Snack",
        "quantity": 10
    },
    {
        "name": "Pepsi",
        "category": "Beverage",
        "quantity": 5
    },
    {
        "name": "Pat Choi",
        "category": "Vegetable",
        "quantity": 8
    }
]

# Options on the drop-down menu
categories = ["Vegetable", "Fruit", "Raw meat", "Cereal grain", "Beverage", "Snack"]

# Declares a variable for the selected category
category_opt = StringVar(value = "Vegetable")

# Creates a drop-down menu that consists of categories
groceryList = Listbox(root,
                      bg = "whitesmoke",
                      fg = "black",
                      font = ("Arial", 12),
                      bd = 0
                      )

# Note: In Python, 'def' defines functions.
# Shows the groceries based on the category chosen by the user
def Init():
    change_categoryView()

def loadList(category):
    # Clears the list
    groceryList.delete(0, END)
    for currIndex, grocery in enumerate(groceries):
        if grocery.get("category") == category:
            # Note: To get the value of a key in a dictionary, 'get()' function is used.
            groceryList.insert(currIndex + 1, grocery.get("name"))

def change_categoryView():
    # Changes the category displayed on the option menu
    loadList(category_opt.get())

# Creates an option menu that lists out all the categories
category = OptionMenu(root, category_opt, *categories)

# Creates a button for manually searching the groceries based on the category given
categoryButton = Button(root, text="Search", command=change_categoryView)

"""
PHASE 4
=======
Finalising the graphical user interface
"""
# Note: Remember to show the control on the window with 'pack' function.
label_appTitle.pack(padx = 16, pady = 16)
label_appDescription.pack()
category.pack()
categoryButton.pack()
groceryList.pack()

"""
PHASE 5
=======
Shows the app's window
"""
# Loads the data onto the dynamic form controls for the first time
Init()

# Runs the application with the window
root.mainloop()