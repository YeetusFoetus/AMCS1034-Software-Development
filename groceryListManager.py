# Import all the definitions from 'tkinter' library
import os.path as path
import json
from tkinter import *
import tkinter.messagebox

class groceryListManager:
    def __init__(self):
        self.widgets_bgColour = "white"
        self.widgets_fgColour = "black"
        self.widgets_padx = 16
        self.widgets_pady = 8

        # Loads the groceries
        self.groceries = self.getList()

        print("INFO: 'groceryListManager' class has been initialised successfully.")

    def getList(self):
        # Declares an empty list of groceries
        groceries = []

        if path.isfile("groceryList.json"):
            try:
                # Opens the 'JSON' file that contains the list of groceries
                f = open("groceryList.json", "r+")

                # Creates a list of groceries
                groceryList_json = f.read()

                # Loads the list of the groceries from 'JSON' string
                groceries = json.loads(groceryList_json)
            except:
                print("Something went wrong while opening 'groceryList.json' file. It seems that the file does not exist.")
            finally:
                # Closes 'groceryList.json' after reading the content
                f.close()
        else:
            # Warns the user that 'groceryList.json' does not exist
            print("WARNING: 'groceryList.json' file does not exist.")
        
        # Returns the 'groceries' list to the calling function
        return groceries
    
    def addGrocery_UI(self, root = None):
        if root is None:
            root = Toplevel()  # Creates a new instance of Tkinter window since the function is called by another Python module
            print("INFO: 'Grocery List Manager' window is opened in a new window.")

        root.title("Add a grocery - Grocery List Manager (Household Management Assistant App)") # Sets the title of the window
        root.geometry("400x300")    # Sets the size of the window
        root.config(bg="white")

        # Sets variables for certain form controls
        groceryName = StringVar()
        groceryCategory = StringVar()
        groceryQuantity = StringVar()

        def submitForm():
            result = self.addGrocery(groceryName.get(), groceryCategory.get(), groceryQuantity.get())
            if result == True:
                root.destroy()  # Closes the window

        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg=self.widgets_bgColour)
        form = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg=self.widgets_bgColour)
        form_button = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg=self.widgets_bgColour)

        """
        Note:
        - Tkinter elements can be placed inside a frame by replacing 'root' with the frame's name.
        """
        Label(header, text="Add a grocery", font=("Segoe UI Light", 18), bg=self.widgets_bgColour, fg=self.widgets_fgColour).grid(row = 1, column = 1)

        Label(form, text="Name: ", bg=self.widgets_bgColour, fg=self.widgets_fgColour).grid(row = 1, column = 1)
        Entry(form, textvariable=groceryName).grid(row = 1, column = 2)
        
        Label(form, text="Category: ", bg=self.widgets_bgColour, fg=self.widgets_fgColour).grid(row = 2, column = 1)
        Entry(form, textvariable=groceryCategory).grid(row = 2, column = 2)

        Label(form, text="Quantity: ", bg=self.widgets_bgColour, fg=self.widgets_fgColour).grid(row = 3, column = 1)
        Entry(form, textvariable=groceryQuantity).grid(row = 3, column = 2)

        Button(form_button, text="Add now", command=submitForm).grid(row = 1, column = 1)
        # Note: 'root.destroy()' closes the active window.
        Button(form_button, text="Cancel", command=root.destroy).grid(row = 1, column = 2)

        header.pack(anchor="w")
        form.pack(anchor="w")
        form_button.pack(anchor="w")

        # Displays the window
        root.mainloop()

    def addGrocery(self, name, category, quantity):
        # Validates the grocery's information entered by the user
        if name == "" or name == None:
            tkinter.messagebox.showwarning("showwarning", "Sorry, but the grocery's name cannot be empty.")
            return False    # Returns 'False' to the calling function
        elif category == "" or category == None:
            tkinter.messagebox.showwarning("showwarning", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        elif quantity == "" or quantity == None:
            tkinter.messagebox.showwarning("showwarning", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        else:
            try:    # Validates the grocery's quantity
                int(quantity)
            except ValueError:
                tkinter.messagebox.showerror("showerror", f"'{quantity}' is an invalid quantity. It has to be numerical.")
                return False
            else:
                pass
        
        # Creates a dictionary that contains the new grocery's information
        metadata = {"name": name, "category": category, "quantity": quantity}
        
        # Adds the dictionary to the end of the list
        self.groceries.append(metadata)
        
        # Writes the dictionary to 'groceryList.json'
        if path.isfile("groceryList.json"):
            try:
                # Opens the 'JSON' file that contains the list of groceries
                f = open("groceryList.json", "r+")

                # Converts the list of groceries which includes the new grocery into JSON string
                groceryList_json = json.dumps(self.groceries)

                # Writes 'JSON' string into 'JSON' file
                f.write(groceryList_json)

                # Reloads the list of the groceries from 'JSON' string
                self.groceries = self.getList()

                tkinter.messagebox.showinfo("showinfo", f"Your grocery which is '{name}' has been added successfully.")

                return True
            except:
                print("Something went wrong while opening 'groceryList.json' file. It seems that the file does not exist.")
            finally:
                # Closes 'groceryList.json' after reading the content
                f.close()
        else:
            # Warns the user that 'groceryList.json' does not exist
            print("WARNING: 'groceryList.json' file does not exist.")

    def App(self, root = None):
        """
        Note:
        - Every window must be initialised with the following code.

        - 'Tk()' function creates the main window.

        - Tkinter cannot have multiple main instances of 'Tk()' at the same time.
          Therefore, 'Toplevel()' function is utilised so multiple instances of Tkinter windows can be opened.
        """
        if root is None:
            root = Toplevel()  # Creates a new instance of Tkinter window since the function is called by another Python module
            print("INFO: 'Grocery List Manager' window is opened in a new window.")

        root.title("Grocery List Manager - Household Management Assistant App") # Sets the title of the window
        root.geometry("800x600")    # Sets the size of the window
        root.configure(bg='white')  # Changes the background colour using 'configure' function
        
        """
        Note:
        - The following code designs the user interface for the grocery list manager.
        - Variables are also declared at this stage.
        """
        groceries = self.getList() # Loads the list of groceries by calling 'loadList' function from the current 'groceryListManager' class' instance
        
        categories = [] # Declares a list of options that will be displayed on the drop-down menu
        
        # 'label_appTitle' greets the user
        # Note: For labels in Tkinter, their inner text MUST be declared with StringVar() first.
        label_appTitle = Label(root,
                               text="Hi there!",
                               bg=self.widgets_bgColour,
                               fg=self.widgets_fgColour)
        
        # 'label_appDescription' explains users about the context of the current window
        label_appDescription = Label(root,
                                     text="Let's manage your grocery list.",
                                     bg=self.widgets_bgColour,
                                     fg=self.widgets_fgColour)
        
        container_category = LabelFrame(root,
                                        text="Category: ",
                                        bg=self.widgets_bgColour,
                                        fg=self.widgets_fgColour)
        
        # This frame arranges the list boxes horizontally to make them look like a table
        groceries_table = LabelFrame(root,
                                     text="Your list of groceries",
                                     bg=self.widgets_bgColour,
                                     fg=self.widgets_fgColour)

        groceries_table_name = LabelFrame(root,
                                          text="Name",
                                          bg=self.widgets_bgColour,
                                          fg=self.widgets_fgColour,
                                          bd=0)
        
        groceries_table_category = LabelFrame(root,
                                          text="Category",
                                          bg=self.widgets_bgColour,
                                          fg=self.widgets_fgColour,
                                          bd=0)
        
        groceries_table_quantity = LabelFrame(root,
                                          text="Quantity",
                                          bg=self.widgets_bgColour,
                                          fg=self.widgets_fgColour,
                                          bd=0)
        
        # Creates a drop-down menu that consists of the groceries
        # 'Name' column
        groceries_listView_name = Listbox(root,
                              bg=self.widgets_bgColour,
                              fg=self.widgets_fgColour)
        
        # 'Category' column
        groceries_listView_category = Listbox(root,
                                              bg=self.widgets_bgColour,
                                              fg=self.widgets_fgColour)
        
        # 'Quantity' column
        groceries_listView_quantity = Listbox(root,
                                              bg=self.widgets_bgColour,
                                              fg=self.widgets_fgColour)
        
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
        
        category = OptionMenu(root,
                              category_opt,
                              *categories,
                              command=change_categoryView)  # Creates an option menu that lists out all the categories
        
        # Note: Remember to show the control on the window with 'pack' function.
        label_appTitle.pack()
        label_appDescription.pack()
        
        category.pack(in_=container_category)

        groceries_listView_name.pack(in_=groceries_table_name)
        groceries_listView_category.pack(in_=groceries_table_category)
        groceries_listView_quantity.pack(in_=groceries_table_quantity)
        
        # Containers
        container_category.pack()

        # The table that shows the list of groceries
        groceries_table_name.pack(in_=groceries_table, side="left")
        groceries_table_category.pack(in_=groceries_table, side="left")
        groceries_table_quantity.pack(in_=groceries_table, side="left")
        groceries_table.pack()
        
        root.mainloop() # Runs the application with the window

# Runs the grocery list manager application if no function from the class is being called
if __name__ == "__main__":
    print("Starting Grocery List Manager...")
    # Creates a new instance from 'groceryListManager' class
    root = Tk()
    instance = groceryListManager()
    instance.App(root)
else:
    print("NOTE: 'groceryListManager' module has been imported.")