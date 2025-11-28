# Import all the definitions from 'tkinter' library
import os.path as path
import json
from tkinter import *
import tkinter.messagebox

class groceryListManager:
    def __init__(self, root = None, back_callback = None):
        # Define styles for 'tkinter' elements
        self.widgets_padx = 16
        self.widgets_pady = 8

        # Checks whether there is an instance of 'root' passes to that of this class
        if root == None:
            self.root = Tk()  # Creates a new instance of Tkinter window since the function is called by another Python module
        else:
            self.root = root
        
        # Checks whether the main menu of a window is defined and passed to this class
        """
        if back_callback == None:
            # Sets to customised styles
            self.widgets_bgColour = "white"
            self.widgets_fgColour = "black"
            self.widgets_header_font = ("Segoe UI Light", 18)
            self.widgets_anchor = "w"
        else:
            pass
        """
        if back_callback != None:
            self.back_callback = back_callback

        # Loads the groceries
        self.groceries = self.getList()
        self.categories = self.getCategories()

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
    
    def getCategories(self):
        # Declares an empty list of sets
        """
        Note:
        - Sets is used to avoid duplications of data.
        - Remember to use 'set()' function since curly braces {} also means dictionaries.
        """
        groceries = self.getList()
        categories = set()

        for grocery in groceries:
            category = grocery.get("category")
            categories.add(category) # Add the category into the set
        
        return categories   # Returns the set of categories to the calling function

    def isback_callbackExists(self):
        try:
            self.back_callback
        except AttributeError:
            print("INFO: 'back_callback' is not provided.")
            return False
        else:
            return True

    def Init_UI(self, root):
        # Checks whether 'back_callback()' function has been provided
        
        if self.isback_callbackExists()  == True:
        # if self.back_callback != None:
            # Clears all the widgets on the current window
            for widget in root.winfo_children():
                widget.destroy()
        else:
            # Sets the property of the window
            root.config()
    
    def UI_addBackButton(self, root):
        if self.isback_callbackExists() == True:
            # Adds a frame where the back button is located
            notch = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
            
            # Adds a back button
            Button(notch, text="Return to the main menu", command=self.back_callback).grid(row = 1, column = 1)

            notch.pack()

    def UI_closeWindow(self, root):
        if self.isback_callbackExists() == True:
            self.back_callback
        else:
            root.destroy()
    
    def UI_returnToHome(self, root):
        if self.isback_callbackExists() == True:
            self.App()
        else:
            root.destroy()

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
        elif quantity.isnumeric() == False:   # Validates the grocery's quantity
            tkinter.messagebox.showerror("showerror", f"'{quantity}' is an invalid quantity. It has to be an integer.")
            return False
        else:
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
    
    def addGrocery_UI(self, root = None):
        print("INFO: 'Grocery List Manager' window is opened in a new window.")

        # Sets the variable named 'root' to the current instance of the window
        if root == None:
            if self.isback_callbackExists() == True:
                root = self.root
            else:
                root = Toplevel()
                root.geometry("400x300")    # Sets the size of the window

        root.title("Add a grocery - Grocery List Manager (Household Management Assistant App)") # Sets the title of the window

        self.Init_UI(root)

        # Sets variables for certain form controls
        groceryName = StringVar()
        groceryCategory = StringVar()
        groceryQuantity = StringVar()

        def submitForm():
            result = self.addGrocery(groceryName.get(), groceryCategory.get(), groceryQuantity.get())
            if result == True:
                self.UI_returnToHome(root)  # Closes the window

        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        form = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        form_button = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)

        """
        Note:
        - Tkinter elements can be placed inside a frame by replacing 'root' with the frame's name.
        """
        Label(header, text="Add a grocery").grid(row = 1, column = 1)

        Label(form, text="Name: ").grid(row = 1, column = 1)
        Entry(form, textvariable=groceryName).grid(row = 1, column = 2)
        
        Label(form, text="Category: ").grid(row = 2, column = 1)
        Entry(form, textvariable=groceryCategory).grid(row = 2, column = 2)

        Label(form, text="Quantity: ").grid(row = 3, column = 1)
        Entry(form, textvariable=groceryQuantity).grid(row = 3, column = 2)

        Button(form_button, text="Add now", command=submitForm).grid(row = 1, column = 1)
        # Note: 'root.destroy()' closes the active window.
        Button(form_button, text="Cancel", command=lambda: self.UI_returnToHome(root)).grid(row = 1, column = 2)

        header.pack()
        form.pack()
        form_button.pack()

        # Displays the window
        root.mainloop()

    def App(self, root = None):
        """
        Note:
        - Every window must be initialised with the following code.

        - 'Tk()' function creates the main window.

        - Tkinter cannot have multiple main instances of 'Tk()' at the same time.
          Therefore, 'Toplevel()' function is utilised so multiple instances of Tkinter windows can be opened.
        """
        """
        if root is None:
            root = Toplevel()  # Creates a new instance of Tkinter window since the function is called by another Python module
            print("INFO: 'Grocery List Manager' window is opened in a new window.")
        """
        if root == None:
            if self.isback_callbackExists() == True:
                root = self.root
            else:
                root = self.root
                root.geometry("800x600")    # Sets the size of the window

        root.title("Grocery List Manager - Household Management Assistant App") # Sets the title of the window
        # root.configure(bg='white')  # Changes the background colour using 'configure' function
        
        self.Init_UI(root)

        """
        Note:
        - The following code designs the user interface for the grocery list manager.
        - Variables are also declared at this stage.
        """
        # Declaring variables
        groceries = self.getList() # Loads the list of groceries by calling 'loadList' function from the current 'groceryListManager' class' instance
        categories = self.getCategories() # Declares a list of options that will be displayed on the drop-down menu
        category_opt = StringVar()   # Declares a variable for the selected category
        
        # Calls UI
        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        actions = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        search = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        table = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)

        # 'label_appTitle' greets the user
        # Note: For labels in Tkinter, their inner text MUST be declared with StringVar() first.
        Label(header, text="Grocery List Manager").grid(row = 1, column = 1)
        
        # 'label_appDescription' explains users about the context of the current window
        # Label(root, text="Let's manage your grocery list.")
        
        # Defines the user actions
        userActions_wwyltd = LabelFrame(actions, text="What would you like to do?", padx=self.widgets_padx / 2, pady=self.widgets_pady)
        userActions_wwyltd.grid(row = 1, column = 1)
        Button(userActions_wwyltd, text="Add a grocery", command=self.addGrocery_UI).grid(row = 1, column = 1)

        # Designs the search bar
        container_category = LabelFrame(search, text="Category: ", padx=self.widgets_padx / 2, pady=self.widgets_pady)
        container_category.grid(row = 1, column = 1)

        # Defining the functions
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
        
        # Shows the groceries based on the category chosen by the user
        # Note: 'command' passes the arguments (like in this case, category) to the function that is being called.
        def change_categoryView(category):
            print(category)
            loadList(category)    # Changes the category displayed on the option menu
        
        # Initialises the window with initial values
        def Init():
            if(len(categories) > 0):
                change_categoryView(category_opt.get())
                pass
            else:
                category_opt.set("No categories available")
                pass

        OptionMenu(container_category, category_opt, *categories, command=change_categoryView).grid(row = 1, column = 1)  # Creates a drop-down menu that lists out all the groceries
        
        # Designs the table of groceries
        # This frame arranges the list boxes horizontally to make them look like a table
        Label(table, text="Name").grid(row = 1, column = 1)
        Label(table, text="Category").grid(row = 1, column = 2)
        Label(table, text="Quantity").grid(row = 1, column = 3)

        # 'Name' column
        groceries_listView_name = Listbox(table)
        groceries_listView_name.grid(row = 2, column = 1)
        
        # 'Category' column
        groceries_listView_category = Listbox(table)
        groceries_listView_category.grid(row = 2, column = 2)
        
        # 'Quantity' column
        groceries_listView_quantity = Listbox(table)
        groceries_listView_quantity.grid(row = 2, column = 3)
        
        Init()  # Loads the data onto the dynamic form controls for the first time

        # Note: Remember to show the control on the window with 'pack' function.
        header.pack()
        search.pack()
        table.pack()
        actions.pack()

        self.UI_addBackButton(root)
        
        root.mainloop() # Runs the application with the window
    
    def menu(self):
        self.App(self.root)

def Test():
    print("INFO: 'back_callback' function has been invoked.")

# Runs the grocery list manager application if no function from the class is being called
if __name__ == "__main__":
    print("Starting Grocery List Manager...")
    # Creates a new instance from 'groceryListManager' class
    root = Tk()
    instance = groceryListManager(root, Test)
    instance.App()
else:
    print("NOTE: 'groceryListManager' module has been imported.")
