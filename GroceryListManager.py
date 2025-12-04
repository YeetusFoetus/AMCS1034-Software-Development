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
        self.LabelFrame_padx = self.widgets_padx / 2

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

        self.loadData()

        print("INFO: 'groceryListManager' class has been initialised successfully.")

    def getList(self):
        # Declares an empty list of groceries
        groceries = []

        if path.isfile("groceryList.json"):
            try:
                # Opens the 'JSON' file that contains the list of groceries
                """
                Note:
                - For file operations in Python, there are three flags that serve different functions.
                  - 'r' --> Read operation only
                  - 'w' --> Write operation only
                  - 'r+' --> Read and write operations
                """
                f = open("groceryList.json", "r")

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
    
    def loadData(self):
        # Loads the groceries
        self.groceries = self.getList()
        self.categories = self.getCategories()
    
    def writeFile(self):
        global isSuccess
        isSuccess = False   # 'isSuccess' variable is used to indicate the status of the file's writing operation

        # Writes the dictionary to 'groceryList.json'
        try:
            # Opens the 'JSON' file that contains the list of groceries
            # Note: 'w' flag will create the file with the name if it does not exist.
            f = open("groceryList.json", "w")

            # Converts the list of groceries which includes the new grocery into JSON string
            groceryList_json = json.dumps(self.groceries)

            # Writes 'JSON' string into 'JSON' file
            f.write(groceryList_json)

            # Closes 'groceryList.json' after reading the content
            f.close()

            isSuccess = True

            # Reloads the list of the groceries from 'JSON' string
            self.loadData()
        except:
            print("Something went wrong while writing data to 'groceryList.json' file.")
            isSuccess = False
        finally:
            f.close()

        return isSuccess

    def isback_callbackExists(self):
        try:
            self.back_callback
        except AttributeError:
            print("INFO: 'back_callback' is not provided.")
            return False
        else:
            return True

    def clrScrn(self, root):
        # Clears all the widgets on the current window
        for widget in root.winfo_children():
            widget.destroy()

    def Init_UI(self, root):
        # Checks whether 'back_callback()' function has been provided
        
        if self.isback_callbackExists()  == True:
        # if self.back_callback != None:
            self.clrScrn(root)
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
        self.loadData() # Refreshes the list of groceery and categories saved within the class

        if self.isback_callbackExists() == True:
            self.back_callback
        else:
            root.destroy()
    
    def UI_returnToHome(self, root):
        self.loadData()

        if self.isback_callbackExists() == True:
            self.App()
        else:
            root.destroy()

    def isEditing(self, index = None, oldCategory = None):
        result = True if index != None and oldCategory != None else False
        return result
    
    def addEditGrocery(self, name, category, quantity, threshold, index = None, oldCategory = None):
        # Validates the grocery's information entered by the user
        if name == "" or name == None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's name cannot be empty.")
            return False    # Returns 'False' to the calling function
        elif category == "" or category == None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        elif quantity == "" or quantity == None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        elif quantity.isnumeric() == False:   # Validates the grocery's quantity
            tkinter.messagebox.showerror("Error", f"Sorry, but '{quantity}' is an invalid quantity. It has to be a positive integer.")
            return False
        elif threshold == "" or threshold == None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's threshold cannot be empty.")
            return False
        elif threshold.isnumeric() == False:   # Validates the grocery's quantity
            tkinter.messagebox.showerror("Error", f"Sorry, but '{threshold}' is an invalid threshold. It has to be a positive integer.")
            return False
        else:
            # Converts the quantity and threshold to integer-type variables
            quantity = int(quantity)
            threshold = int(threshold)

            if self.isEditing(index, oldCategory) == False:   # If the user is adding a grocery to the list
                # Creates a dictionary that contains the new grocery's information
                metadata = {"name": name, "category": category, "quantity": quantity, "threshold": threshold}

                # Adds the dictionary to the end of the list
                self.groceries.append(metadata)
            else:
                searchResult = self.getListByCategory(oldCategory)
                oldInfo = searchResult[index]
                newInfo = {"name": name, "category": category, "quantity": quantity, "threshold": threshold}   # Duplicates the old information from the list

                print(oldInfo)
                print(newInfo)

                self.groceries.remove(oldInfo)  # Removes the old information from the list of groceries
                self.groceries.append(newInfo)  # Adds the old information to the list
                

            # Saves the changes to a file named 'groceryList.json'
            isSuccess = self.writeFile()

            if isSuccess == True:
                tkinter.messagebox.showinfo("Grocery added" if self.isEditing(index, oldCategory) == False else "Grocery edited", "Your grocery which is '{}' has been {} successfully.".format(name, "added" if self.isEditing(index, oldCategory) == False else "edited"))
            else:
                tkinter.messagebox.showerror("Grocery failed to be added", f"Sorry, but there is an error occurred while we're adding '{name}' to the list. Please try again.")
            
            return isSuccess
    
    def addEditGrocery_UI(self, root = None, index = None, oldCategory = None):
        print("INFO: 'Grocery List Manager' window is opened in a new window.")

        # Sets the variable named 'root' to the current instance of the window
        if root == None:
            if self.isback_callbackExists() == True:
                root = self.root
            else:
                root = Toplevel()
                homeRoot = self.root    # Remembers the instance of the home page
                root.geometry("400x300")    # Sets the size of the window

        root.title(("Add a grocery" if self.isEditing(index, oldCategory) == False else "Edit the grocery") + " - Grocery List Manager (Household Management Assistant App)") # Sets the title of the window

        self.Init_UI(root)

        # Sets variables for certain form controls
        groceryName = StringVar()
        groceryCategory = StringVar()
        groceryQuantity = StringVar()
        groceryThreshold = StringVar()

        # Note: 'index' is True if the user is editing an grocery
        if self.isEditing(index, oldCategory) == True:
            # Search the list of categories based on the category given
            searchResult = self.getListByCategory(oldCategory)

            # Gets the current information about the grocery
            oldName = searchResult[index].get("name")
            oldCategory = searchResult[index].get("category")
            oldQuantity = searchResult[index].get("quantity")
            oldThreshold = searchResult[index].get("threshold")

            # Displays the information of the grocery if the user is making some edits
            groceryName.set(oldName)
            groceryCategory.set(oldCategory)
            groceryQuantity.set(oldQuantity)
            groceryThreshold.set(oldThreshold)

        def closeWindow():
            if self.isback_callbackExists() == False:
                self.refreshUI(homeRoot, self.App)
            else:
                self.UI_returnToHome(root)  # Closes the window

        def submitForm():
            if self.isEditing(index, oldCategory) == False:
                result = self.addEditGrocery(groceryName.get(), groceryCategory.get().title(), groceryQuantity.get(), groceryThreshold.get())
            else:
                result = self.addEditGrocery(groceryName.get(), groceryCategory.get().title(), groceryQuantity.get(), groceryThreshold.get(), index, oldCategory)
            
            if result == True:
                closeWindow()

        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        form = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        form_button = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        footer = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)

        """
        Note:
        - Tkinter elements can be placed inside a frame by replacing 'root' with the frame's name.
        """
        Label(header, text="Add a grocery" if self.isEditing(index, oldCategory) == False else "Edit the grocery").grid(row = 1, column = 1)

        Label(form, text="Name: ").grid(row = 1, column = 1)
        Entry(form, textvariable=groceryName).grid(row = 1, column = 2)
        
        Label(form, text="Category: ").grid(row = 2, column = 1)
        Entry(form, textvariable=groceryCategory).grid(row = 2, column = 2)

        Label(form, text="Quantity: ").grid(row = 3, column = 1)
        Entry(form, textvariable=groceryQuantity).grid(row = 3, column = 2)

        Label(form, text="Threshold: ").grid(row = 5, column = 1)
        Entry(form, textvariable=groceryThreshold).grid(row = 5, column = 2)

        Button(form_button, text="Add now" if self.isEditing(index, oldCategory) == False else "Save now", command=submitForm).grid(row = 1, column = 1)
        # Note: 'root.destroy()' closes the active window.
        Button(form_button, text="Cancel", command=closeWindow).grid(row = 1, column = 2)

        info4user = LabelFrame(footer, text="For your information", padx=self.LabelFrame_padx, pady=self.widgets_pady)
        info4user.grid(row = 1, column = 1)

        Label(info4user, text="The first character of the category will be capitalised and the rest will be lower case.\n\ne.g.: 'frUit' --> 'Fruit'").grid(row = 1, column = 1)

        header.pack()
        form.pack()
        form_button.pack()
        footer.pack()

        # Displays the window
        root.mainloop()

    def getListByCategory(self, category):
        groceries = (self.getList())
        result = []

        for grocery in groceries:            
            if(grocery.get("category") == category):
                result.append(grocery)

        return result
        
    def delGroceryByCategory(self, index, category):
        sortedList = (self.getListByCategory(category))

        print("Index selected: {}".format(index))
        print("Category selected: {}".format(category))

        name = sortedList[index].get("name")
        quantity = sortedList[index].get("quantity")
        
        isYes = tkinter.messagebox.askyesno("Confirming deletion", "Are you sure you would like to delete {} grocer{} named '{}'?".format(quantity, "y" if quantity == 1 else "ies", name))

        if(isYes == True):
            self.groceries.remove(sortedList[index])
            print(self.groceries)

            # Writing changes to the file
            isSuccess = self.writeFile()

            if isSuccess == True:
                tkinter.messagebox.showinfo("Deletion successful", f"The grocery which is '{name}' has been deleted successfully.")
            else:
                tkinter.messagebox.showerror("Grocery failed to be added", f"Sorry, but there is an error occurred while we're deleting '{name}' from the list. Please try again.")

            return isSuccess

        else:
            print("INFO: The deleting operation has been cancelled by the user.")
            return False
    
    def refreshUI(self, root, function):
        #if self.isback_callbackExists() == False:
        self.clrScrn(root)
        function(root)  # Reinvoke the function to reinitialise the elements of 'tkinter' elements

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
        """
        groceryList = self.getList() # Loads the list of groceries by calling 'loadList' function from the current 'groceryListManager' class' instance
        groceries = (groceryList) # Note: Tuples are used to avoid any changes to the data / list.
        categories = self.getCategories() # Declares a list of options that will be displayed on the drop-down menu
        """
        category_opt = StringVar()   # Declares a variable for the selected category
        
        # Calls UI
        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        empty = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        actions = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        search = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)
        table = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady)

        Label(header, text="Grocery List Manager").grid(row = 1, column = 1)
        Label(empty, text="Your list is empty. Let's add your first grocery to your first grocery list!").grid(row = 1, column = 1)
        
        # 'label_appDescription' explains users about the context of the current window
        # Label(root, text="Let's manage your grocery list.")
        
        # Defines the user actions
        userActions_wwyltd = LabelFrame(actions, text="What would you like to do?", padx=self.LabelFrame_padx, pady=self.widgets_pady)
        userActions_wwyltd.grid(row = 1, column = 1)
        button_addGrocery = Button(userActions_wwyltd, text="Add a grocery")
        button_addGrocery.grid(row = 1, column = 1)

        def addEditGrocery():
            self.addEditGrocery_UI()
        
        button_addGrocery.config(command=addEditGrocery)

        # Note: Remember to show the control on the window with 'pack' function.
        header.pack()

        if len(self.groceries) <= 0: # If the list is empty
            empty.pack()
        else:
            # Adds the button that deletes and edits the groceries within the list
            button_editGrocery = Button(userActions_wwyltd, text="Edit this grocery")
            button_editGrocery.grid(row = 1, column = 2)

            button_delGrocery = Button(userActions_wwyltd, text="Delete this grocery")
            button_delGrocery.grid(row = 1, column = 3)

            # Designs the search bar
            container_category = LabelFrame(search, text="Category: ", padx=self.LabelFrame_padx, pady=self.widgets_pady)
            container_category.grid(row = 1, column = 1)

            # Designs the table of groceries
            # This frame arranges the list boxes horizontally to make them look like a table
            Label(table, text="Name").grid(row = 1, column = 1)
            Label(table, text="Category").grid(row = 1, column = 2)
            Label(table, text="Quantity").grid(row = 1, column = 3)
            Label(table, text="Threshold").grid(row = 1, column = 4)

            # 'Name' column
            groceries_listView_name = Listbox(table)
            groceries_listView_name.grid(row = 2, column = 1)

            # 'Category' column
            groceries_listView_category = Listbox(table)
            groceries_listView_category.grid(row = 2, column = 2)

            # 'Quantity' column
            groceries_listView_quantity = Listbox(table)
            groceries_listView_quantity.grid(row = 2, column = 3)

            # 'Threshold' column
            groceries_listView_threshold = Listbox(table)
            groceries_listView_threshold.grid(row = 2, column = 4)

            self.selectIndex = None
        
            def getSelectedGrocery_name(event):
                print(event)
                selections = groceries_listView_name.curselection()
                for selected in selections:
                    self.selectIndex = selected
                    print("INFO: The user has chosen the following index(es) from 'name' column.")
                    print(selected)
            
            def getSelectedGrocery_category(event):
                print(event)
                selections = groceries_listView_category.curselection()
                for selected in selections:
                    self.selectIndex = selected
                    print("INFO: The user has chosen the following index(es) from 'category' column.")
                    print(selected)
            
            def getSelectedGrocery_quantity(event):
                print(event)
                selections = groceries_listView_quantity.curselection()
                for selected in selections:
                    self.selectIndex = selected
                    print("INFO: The user has chosen the following index(es) from 'quantity' column.")
                    print(selected)
            
            def getSelectedGrocery_threshold(event):
                print(event)
                selections = groceries_listView_threshold.curselection()
                for selected in selections:
                    self.selectIndex = selected
                    print("INFO: The user has chosen the following index(es) from 'threshold' column.")
                    print(selected)
            
            # Note: The function in '.bind("<<ListboxSelect>>", <function>)' function will be trigerred when the user chooses anything on the list box.
            groceries_listView_name.bind("<<ListboxSelect>>", getSelectedGrocery_name)
            groceries_listView_category.bind("<<ListboxSelect>>", getSelectedGrocery_category)
            groceries_listView_quantity.bind("<<ListboxSelect>>", getSelectedGrocery_quantity)
            groceries_listView_threshold.bind("<<ListboxSelect>>", getSelectedGrocery_threshold)

            # Defining the functions
            # Note: In Python, 'def' defines functions.
            def loadList(category):
                # Gets the groceries based on the category given
                searchResult = self.getListByCategory(category)

                # Clears the list
                groceries_listView_name.delete(0, END)
                groceries_listView_category.delete(0, END)
                groceries_listView_quantity.delete(0, END)
                groceries_listView_threshold.delete(0, END)

                # Adds the item to the list based on the selected category
                for currIndex, grocery in enumerate(searchResult):
                    groceries_listView_name.insert(currIndex + 1, grocery.get("name"))  # Note: To get the value of a key in a dictionary, 'get()' function is used.
                    groceries_listView_category.insert(currIndex + 1, category)
                    groceries_listView_quantity.insert(currIndex + 1, grocery.get("quantity"))
                    groceries_listView_threshold.insert(currIndex + 1, grocery.get("threshold"))

            # Shows the groceries based on the category chosen by the user
            # Note: 'command' passes the arguments (like in this case, category) to the function that is being called.
            def change_categoryView(category):
                self.selectIndex = None
                
                print(category)
                loadList(category)    # Changes the category displayed on the option menu

            # Initialises the window with initial values
            def Init():
                if(len(self.categories) > 0):   # If the list of groceries is not empty
                    if category_opt.get() not in self.categories: # If the selected category does not exist
                        category_opt.set(self.groceries[0].get("category"))  # Choose the category of the first grocery item

                    change_categoryView(category_opt.get())
                else:
                    # category_opt.set("No categories available")
                    pass

            OptionMenu(container_category, category_opt, *self.categories, command=change_categoryView).grid(row = 1, column = 1)  # Creates a drop-down menu that lists out all the groceries

            def editGrocery():
                if self.selectIndex == None:
                    tkinter.messagebox.showinfo("No selection", "In order to delete a grocery, you have to choose first.")
                else:
                    self.addEditGrocery_UI(index=self.selectIndex, oldCategory=category_opt.get())

            def delGrocery():
                if self.selectIndex == None:
                    # Shows an error message
                    tkinter.messagebox.showinfo("No selection", "In order to delete a grocery, you have to choose first.")
                    print("WARNING: Nothing has been selected yet.")
                else:
                    # status = self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    
                    # if status == True or status == False:
                        # Init()
                    self.refreshUI(root, self.App)

            button_editGrocery.config(command=editGrocery)
            button_delGrocery.config(command=delGrocery)

            Init()  # Loads the data onto the dynamic form controls for the first time

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
    instance = groceryListManager(root)
    instance.App()
else:
    print("NOTE: 'groceryListManager' module has been imported.")
