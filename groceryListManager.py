# Import all the definitions from 'tkinter' library
import os.path as path
import json
from tkinter import *

"""
Note:
- Every window must be initialised with the following code.
"""
root = Tk() # Creates the main window
root.title("Grocery List Manager - Household Management Assistant App") # Sets the title of the window
root.geometry("800x600")    # Sets the size of the window
root.configure(bg='white')  # Changes the background colour using 'configure' function

"""
Note:
- The following code designs the user interface for the grocery list manager.
- Variables are also declared at this stage.
"""
if path.isfile("groceryList.json"):
    try:
        # Opens the 'JSON' file that contains the list of groceries
        f = open("groceryList.json", "r+")

        # Creates a list of groceries
        groceryList_json = f.read()

        # Closes 'groceryList.json' after reading the content
        f.close()

        # Loads the list of the groceries from 'JSON' string
        groceries = json.loads(groceryList_json)
    except:
        print("Something went wrong while opening 'groceryList.json' file. It seems that the file does not exist.")
else:
    # Warns the user that 'groceryList.json' does not exist
    print("WARNING: 'groceryList.json' file does not exist.")

    # Declares an empty list of groceries if the file does not exist
    groceries = []

categories = [] # Declares a list of options that will be displayed on the drop-down menu

# 'label_appTitle' greets the user
# Note: For labels in Tkinter, their inner text MUST be declared with StringVar() first.
label_appTitle_text = StringVar()
label_appTitle_text.set("Hi there!")
label_appTitle = Label(root,
                       textvariable=label_appTitle_text,
                       bg="white",
                       fg="black",
                       font=("Arial", 28, "bold")
                       )

# 'label_appDescription' explains users about the context of the current window
label_appDescription_text = StringVar()
label_appDescription_text.set("Let's manage your grocery list.")
label_appDescription = Label(root,
                             textvariable=label_appDescription_text,
                             bg="white",
                             fg="black",
                             font=("Arial", 12)
                             )

# This frame arranges the list boxes horizontally to make them look like a table
rowContainer = Frame(root, background="yellowgreen")

# Creates a drop-down menu that consists of the groceries
# 'Name' column
groceries_listView_name = Listbox(root,
                      bg="whitesmoke",
                      fg="black",
                      font=("Arial", 12),
                      )

# 'Category' column
groceries_listView_category = Listbox(root,
                                      bg="whitesmoke",
                                      fg="black",
                                      font=("Arial", 12)
                                      )

# 'Quantity' column
groceries_listView_quantity = Listbox(root,
                                      bg="whitesmoke",
                                      fg="black",
                                      font=("Arial", 12)
                                      )

# Note: In Python, 'def' defines functions.
def loadList(category):
    # Clears the list
    groceries_listView_name.delete(0, END)
    groceries_listView_category.delete(0, END)
    groceries_listView_quantity.delete(0, END)
    # Adds the item to the list based on the selected category
    for currIndex, grocery in enumerate(groceries):
        if grocery.get("category") == category:
            groceries_listView_name.insert(currIndex + 1, grocery.get("name"))  # Note: To get the value of a key in a dictionary, 'get()' function is used.
            groceries_listView_category.insert(currIndex + 1, category)
            groceries_listView_quantity.insert(currIndex + 1, grocery.get("quantity"))

def loadCategories():
    for grocery in groceries:
        category = grocery.get("category")
        if(category not in categories): # If the category does not exist in the list of categories
            categories.append(category) # Add the category into the list

category_opt = StringVar()   # Declares a variable for the selected category

# Shows the groceries based on the category chosen by the user
# Note: 'command' passes the arguments (like in this case, category) to the function that is being called.
def change_categoryView(category):
    print(category)
    loadList(category)    # Changes the category displayed on the option menu

# Initialises the window with initial values
def Init():
    if(len(categories) > 0):
        category_opt.set(categories[0])
        change_categoryView(category_opt.get())
    else:
        category_opt.set("No categories available")
        pass

loadCategories()    # Loads the categories from the list of groceries

Init()  # Loads the data onto the dynamic form controls for the first time

category = OptionMenu(root, category_opt, *categories, command=change_categoryView)  # Creates an option menu that lists out all the categories

# Note: Remember to show the control on the window with 'pack' function.
label_appTitle.pack(side="top")
label_appDescription.pack(side="top")
category.pack(side="top")
groceries_listView_name.pack(in_=rowContainer, side="left")
groceries_listView_category.pack(in_=rowContainer, side="left")
groceries_listView_quantity.pack(in_=rowContainer, side="left")
rowContainer.pack(side="top")

root.mainloop() # Runs the application with the window