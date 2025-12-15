# Import all the definitions from 'tkinter' library
import os.path as path
import json
from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter

class groceryListManager:
    def __init__(self, root = None, back_callback = None):
        # Prints a message regarding the debugging information
        print("DEBUGGING INFORMATION\n=====================")

        # Define styles for 'tkinter' elements
        self.widgets_padx = 16
        self.widgets_pady = 8
        self.LabelFrame_padx = self.widgets_padx / 2

        # Checks whether there is an instance of 'root' passes to that of this class
        if root is None:
            self.root = Tk()  # Creates a new instance of Tkinter window since the function is called by another Python module
        else:
            self.root = root
        
        # Checks whether the main menu of a window is defined and passed to this class
        """
        if back_callback is None:
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

        # Declares necessary variables for 'App()'
        self.selectCategory = ""
        self.selectIndex = None

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
    
    def isGroceryExists(self, name, category):    # Checks whether a grocery with the given name and category exists
        # Makes 'name' look like a title
        name = name.title()

        isExists = False if self.getGrocery(name, category) == {} else True
        
        return isExists
    
    def getGrocery(self, name, category):
        list_categoryBased = self.getListByCategory(category)

        result = {}

        for index, grocery in enumerate(list_categoryBased):
            if grocery.get("name") == name:
                grocery["index"] = index    # Adds the index of the grocery to the search result
                result = grocery

        return result
    
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
            notch = Frame(self.UI, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')
            
            # Adds a back button
            Button(notch, font=("Arial", 11), text="Return to the main menu", command=self.back_callback).grid(row = 1, column = 1)

            notch.pack(pady=20)

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
        if name == "" or name is None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's name cannot be empty.")
            return False    # Returns 'False' to the calling function
        elif category == "" or category is None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        elif quantity == "" or quantity is None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's quantity cannot be empty.")
            return False
        elif quantity.isnumeric() == False:   # Validates the grocery's quantity
            tkinter.messagebox.showerror("Error", f"Sorry, but '{quantity}' is an invalid quantity. It has to be a positive integer.")
            return False
        elif threshold == "" or threshold is None:
            tkinter.messagebox.showwarning("Error", "Sorry, but the grocery's threshold cannot be empty.")
            return False
        elif threshold.isnumeric() == False:   # Validates the grocery's quantity
            tkinter.messagebox.showerror("Error", f"Sorry, but '{threshold}' is an invalid threshold. It has to be a positive integer.")
            return False
        else:
            # Capitalises the first letter of the grocery's name and category and converts the rest of that to lower cases.
            name = name.title()
            category = category.title()
            
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
        if root is None and self.isback_callbackExists() == False:
            root = Toplevel()
            self.root = self.root    # Remembers the instance of the home page
            # root.geometry("400x300")    # Sets the size of the window
        elif root is not None and self.isback_callbackExists() == False:
            self.root = self.root
        else:   # self.isback_callbackExists() == True
            root = self.root    # 'self.root' is defined during the initialisation of this class

        root.title(("Add a grocery" if self.isEditing(index, oldCategory) == False else "Edit the grocery") + " - Grocery List Manager (Household Management Assistant App)") # Sets the title of the window

        self.Init_UI(root)

        # Configure background image
        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()   

        # Declares necessary flags (variables)
        self.gotoEdit = False

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
                self.refreshUI(self.root, self.App)
            else:
                self.UI_returnToHome(root)  # Closes the window

        def submitForm():
            result = False

            # Assigns the strings from StringVar() to variables
            name = groceryName.get().title()
            category = groceryCategory.get().title()
            quantity = groceryQuantity.get()
            threshold = groceryThreshold.get()

            existingGrocery = self.getGrocery(name, category)   # Checks for any existing groceries

            if self.isEditing(index, oldCategory) == False:
                if self.isGroceryExists(name, category) == True:
                    self.gotoEdit = tkinter.messagebox.askyesno("Grocery conflicted", f"The grocery named '{name}' which is categorised as '{category}', already exists within your list of groceries.\n\nWould you like to edit it instead?\n\nOtherwise, click 'No' to cancel and give the new grocery a new name.")
                else:
                    result = self.addEditGrocery(name, category, quantity, threshold)
            else:
                if existingGrocery != {}:   # If no groceries match the current edit
                    if existingGrocery["name"] == name and existingGrocery["category"] == category: # If the found grocery has the same information as the current edit
                        if existingGrocery["index"] == index:   # If the found grocery is actually the grocery that is being edited
                            result = self.addEditGrocery(name, category, quantity, threshold, index, oldCategory)
                        else:    
                            self.gotoEdit = tkinter.messagebox.askyesno("Grocery conflicted", f"The grocery named '{name}' is categorised as '{category}'.\n\nWould you like to edit it instead?\n\nOtherwise, click 'No' to cancel and give the grocery another category.")    
                    else:
                        result = self.addEditGrocery(name, category, quantity, threshold, index, oldCategory)
                else:
                    result = self.addEditGrocery(name, category, quantity, threshold, index, oldCategory)
                
            if self.gotoEdit == True:
                self.gotoEdit = False    # Sets 'self.gotoEdit' flag to 'false' to avoid duplicated windows

                # Edits the grocery that exists within the list
                self.clrScrn(root)
                self.addEditGrocery_UI(root, existingGrocery["index"], existingGrocery["category"])
            
            if result == True:
                closeWindow()

        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='orange')
        form = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='yellow')
        form_button = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='green')
        footer = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='blue')

        """
        Note:
        - Tkinter elements can be placed inside a frame by replacing 'root' with the frame's name.
        """
        Label(header, font=("Arial", 11), text="Add a grocery" if self.isEditing(index, oldCategory) == False else "Edit the grocery").grid(row = 1, column = 1)

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

        info4user = LabelFrame(footer, text="For your information", padx=self.LabelFrame_padx, pady=self.widgets_pady, bg='indigo')
        info4user.grid(row = 1, column = 1)

        Label(info4user, text="The first character of the name and category will be capitalised and the rest will be lower case.\n\ne.g.: 'cEreAl gRain' --> 'Cereal Grain'").grid(row = 1, column = 1)

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

        else:
            print("INFO: The deleting operation has been cancelled by the user.")
    
    def consumeGroceryByCategory(self, index, category):
        sortedList = (self.getListByCategory(category))

        print("Index selected: {}".format(index))
        print("Category selected: {}".format(category))

        name = sortedList[index].get("name")
        quantity = sortedList[index].get("quantity")

        if quantity == 0:
            tkinter.messagebox.showerror("Nothing to consume", f"Sorry, but the grocery named '{name}' is no more.")
        else:
            while True:
                consumeNum = tkinter.simpledialog.askinteger("Consuming a grocery", "Enter the number of '{}' you have consumed.".format(name))

                if consumeNum is None:
                    print("INFO: The consuming operation has been cancelled by the user.")
                    break
                elif consumeNum < 0:
                    tkinter.messagebox.showwarning("Invalid consumption", "Sorry, but the number of consumption should be positive.")
                elif consumeNum > quantity:
                    tkinter.messagebox.showwarning("Invalid consumption", f"Sorry, but the number of consumption should not exceed the quantity of the grocery which is {quantity}.")
                else:
                    self.groceries.remove(sortedList[index])
                    sortedList[index]["quantity"] -= consumeNum
                    self.groceries.append(sortedList[index])
                    print(self.groceries)

                    # Writing changes to the file
                    isSuccess = self.writeFile()

                    if isSuccess == True:
                        quantity = sortedList[index].get("quantity")    # Update the quantity with the new number
                        tkinter.messagebox.showinfo("Consumption successful", f"Now, you have {quantity} grocer{"y" if quantity == 1 else "ies"} named '{name}' left.")
                        break
                    else:
                        tkinter.messagebox.showerror("Grocery failed to be consumed", f"Sorry, but there is an error occurred while we're consuming '{name}' from the list. Please try again.")
                        break
    
    def refillGroceryByCategory(self, index, category):
        sortedList = (self.getListByCategory(category))

        print("Index selected: {}".format(index))
        print("Category selected: {}".format(category))

        name = sortedList[index].get("name")
        quantity = sortedList[index].get("quantity")

        while True:
            consumeNum = tkinter.simpledialog.askinteger("Refilling a grocery", "Enter the number of '{}' you have refilled.".format(name))

            if consumeNum is None:
                print("INFO: The refilling operation has been cancelled by the user.")
                break
            elif consumeNum < 0:
                tkinter.messagebox.showwarning("Invalid refill", f"Sorry, but the number of refilled grocery named '{name}' should be positive.")
            else:
                self.groceries.remove(sortedList[index])
                sortedList[index]["quantity"] += consumeNum
                self.groceries.append(sortedList[index])

                print(self.groceries)

                # Writing changes to the file
                isSuccess = self.writeFile()

                if isSuccess == True:
                    quantity = sortedList[index].get("quantity")    # Update the quantity with the new number
                    tkinter.messagebox.showinfo("Refill successful", f"Now, you have {quantity} grocer{"y" if quantity == 1 else "ies"} named '{name}' left.")
                    break
                else:
                    tkinter.messagebox.showerror("Grocery failed to be refilled", f"Sorry, but there is an error occurred while we're refilling '{name}' from the list. Please try again.")
                    break
        
    def refreshUI(self, root, function):
        #if self.isback_callbackExists() == False:
        self.clrScrn(root)
        function(root)  # Reinvoke the function to reinitialise the elements of 'tkinter' elements
    
    def refillList(self, root = None):
        root = Toplevel(self.root)
        # Sets the variable named 'root' to the current instance of the window
        '''if root is None:
            if self.isback_callbackExists() == True:
                root = self.root
            else:
                root = Toplevel()
                self.root = self.root'''    # Remembers the instance of the home page
                # root.geometry("400x300")    # Sets the size of the window

        root.title("Your refill list - Grocery List Manager (Household Management Assistant App)") # Sets the title of the window
        root.config(bg="#c3b091")

        self.Init_UI(root)

        header = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')
        table = Frame(root, width=200, height=200, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')
        footer = Frame(root, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')

        Label(header, font=("Arial", 12), text="My Refill List").grid(row = 1, column = 1)

        # Designs the table of grocer(ies) that need to be refilled
        Label(table, width=21, font=("Arial", 11), text="Name").grid(row = 1, column = 1)
        Label(table, width=21, font=("Arial", 11), text="Category").grid(row = 1, column = 2)
        Label(table, width=21, font=("Arial", 11), text="Quantity").grid(row = 1, column = 3)
        Label(table, width=21, font=("Arial", 11), text="Threshold").grid(row = 1, column = 4)
        Label(table, width=21, font=("Arial", 11), text="You need to refill…").grid(row = 1, column = 5)

        # 'Name' column
        groceries_listView_name = Listbox(table, font=("Arial", 11), width=24)
        groceries_listView_name.grid(row = 2, column = 1)

        # 'Category' column
        groceries_listView_category = Listbox(table, font=("Arial", 11), width=24)
        groceries_listView_category.grid(row = 2, column = 2)

        # 'Quantity' column
        groceries_listView_quantity = Listbox(table, font=("Arial", 11), width=24)
        groceries_listView_quantity.grid(row = 2, column = 3)

        # 'Threshold' column
        groceries_listView_threshold = Listbox(table, font=("Arial", 11), width=24)
        groceries_listView_threshold.grid(row = 2, column = 4)

        # 'You need to refill' column
        groceries_listView_refillAmt = Listbox(table, font=("Arial", 11), width=24)
        groceries_listView_refillAmt.grid(row = 2, column = 5)
        
        # Defining necessary functions
        def loadList():
            # Gets the list of groceries
            searchResult = self.groceries

            # Adds the item to the list based on the selected category
            for currIndex, grocery in enumerate(searchResult):
                quantity = grocery.get("quantity")
                threshold = grocery.get("threshold")

                if quantity < threshold:
                    # Calculates the number of the grocery that needs to be refilled
                    refillAmt = threshold - quantity

                    groceries_listView_name.insert(currIndex + 1, grocery.get("name"))  # Note: To get the value of a key in a dictionary, 'get()' function is used.
                    groceries_listView_category.insert(currIndex + 1, grocery.get("category"))
                    groceries_listView_quantity.insert(currIndex + 1, quantity)
                    groceries_listView_threshold.insert(currIndex + 1, threshold)
                    groceries_listView_refillAmt.insert(currIndex + 1, refillAmt)

        def closeWindow():
            if self.isback_callbackExists() == False:
                self.refreshUI(self.root, self.App)
            else:
                self.UI_returnToHome(root)  # Closes the window
        
        Button(footer, text="Close", command=closeWindow).grid(row = 1, column = 1)

        loadList()    # Changes the category displayed on the option menu

        header.pack(pady=10)
        table.pack(pady=10)
        footer.pack(pady=10)
        header.pack_propagate(False)
        table.pack_propagate(False)
        footer.pack_propagate(False)

        # Displays the window
        #root.mainloop()

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
        if root is None:
            if self.isback_callbackExists() == True:
                root = self.root
            else:
                root = self.root
                # root.geometry("800x600")    # Sets the size of the window

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

        # Configure background image
        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()   
        
        # Calls UI
        self.UI = ctk.CTkFrame(root, 
                               corner_radius=0,
                               width=700, height=550, 
                               border_width=2, border_color="black", 
                               fg_color='#c3b091'
                               )
        header = ctk.CTkFrame(root, width=497, height=50, corner_radius=0, border_width=2, border_color="black", fg_color="#c3b091")
        header.pack(pady=20, side="top")
        header.pack_propagate(False)
        empty = Frame(self.UI, padx=self.widgets_padx, pady=self.widgets_pady, bg='green')
        actions = Frame(self.UI, width=530, height=123, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')
        search = Frame(self.UI, width=200, height=100, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')
        table = Frame(self.UI, padx=self.widgets_padx, pady=self.widgets_pady, bg='#c3b091')

        ctk.CTkLabel(header, text="Grocery List Manager", text_color="black", font=("Nunito SemiBold", 35)).pack(padx=5, pady=5)
        Label(empty, text="Your list is empty. Let's add your first grocery to your first grocery list!").grid(row = 1, column = 1)
        
        # 'label_appDescription' explains users about the context of the current window
        # Label(root, text="Let's manage your grocery list.")
        
        # Defines the user actions
        userActions_wwyltd = LabelFrame(actions, font=("Arial", 11), text="What would you like to do?", padx=self.LabelFrame_padx, pady=self.widgets_pady, bg='#f7e7ce')
        userActions_wwyltd.pack(anchor='center', fill='both', expand=True)
        button_addGrocery = Button(userActions_wwyltd, font=("Arial", 11), text="Add a grocery", bg='light green')
        button_addGrocery.grid(row = 1, column = 1)

        def addEditGrocery():
            self.addEditGrocery_UI()
        
        button_addGrocery.config(command=addEditGrocery)

        # Note: Remember to show the control on the window with 'pack' function.
        header.pack()
        self.UI.pack(padx=self.widgets_padx, pady=75)
        self.UI.pack_propagate(False)

        if len(self.groceries) <= 0: # If the list is empty
            empty.pack()
        else:
            # Adds the button that deletes and edits the groceries within the list
            button_editGrocery = Button(userActions_wwyltd, font=("Arial", 11), text="Edit this grocery", bg='light blue')
            button_editGrocery.grid(row = 1, column = 2)

            button_delGrocery = Button(userActions_wwyltd, font=("Arial", 11), text="Delete this grocery", bg='pink')
            button_delGrocery.grid(row = 1, column = 3)

            button_consumeGrocery = Button(userActions_wwyltd, font=("Arial", 11), text="Consume this grocery")
            button_consumeGrocery.grid(pady=10, padx=3, row = 2, column = 1)

            button_refillGrocery = Button(userActions_wwyltd, font=("Arial", 11), text="Refill this grocery")
            button_refillGrocery.grid(padx=3, row = 2, column = 2)

            button_refillList = Button(userActions_wwyltd, font=("Arial", 11), text="Generate a refill list for me")
            button_refillList.grid(row = 2, column = 3)

            # Designs the search bar
            container_category = LabelFrame(search, text="Category: ", font=("Arial", 14), padx=self.LabelFrame_padx, pady=self.widgets_pady, bg='#f7e7ce')
            container_category.pack(anchor='center', fill='both', expand=True)

            # Designs the table of groceries
            # This frame arranges the list boxes horizontally to make them look like a table
            Label(table, width=21, font=("Arial", 11), text="Name").grid(row = 5, column = 1)
            Label(table, width=21, font=("Arial", 11), text="Category").grid(row = 5, column = 2)
            Label(table, width=21, font=("Arial", 11), text="Quantity").grid(row = 5, column = 3)
            Label(table, width=21, font=("Arial", 11), text="Threshold").grid(row = 5, column = 4)

            # 'Name' column
            groceries_listView_name = Listbox(table, font=("Fira Code", 11), width=24)
            groceries_listView_name.grid(row = 6, column = 1)
            groceries_listView_name.grid_propagate(False)

            # 'Category' column
            groceries_listView_category = Listbox(table, font=("Arial", 11), width=24)
            groceries_listView_category.grid(row = 6, column = 2)

            # 'Quantity' column
            groceries_listView_quantity = Listbox(table, font=("Arial", 11), width=24)
            groceries_listView_quantity.grid(row = 6, column = 3)

            # 'Threshold' column
            groceries_listView_threshold = Listbox(table, font=("Arial", 11), width=24)
            groceries_listView_threshold.grid(row = 6, column = 4)
        
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
                self.selectCategory = category  # Sets the selected category
                self.selectIndex = None
                
                print(self.selectCategory)
                loadList(self.selectCategory)    # Changes the category displayed on the option menu

            # Initialises the window with initial values
            def Init(): # category_opt.get()
                if(len(self.categories) > 0):   # If the list of groceries is not empty
                    if self.selectCategory == "" or (self.selectCategory != "" and self.selectCategory not in self.categories):   # If a category is not selected or if a category is selected but the selected category does not exist
                        self.selectCategory = self.groceries[0].get("category") # Choose the category of the first grocery item
                        
                    category_opt.set(self.selectCategory)
                    change_categoryView(category_opt.get())
                else:
                    # category_opt.set("No categories available")
                    pass

            option = OptionMenu(container_category, category_opt, *self.categories, command=change_categoryView)
            option.config(font=("Arial", 12))
            option["menu"].config(font=("Arial", 12))
            option.pack(anchor='center')  # Creates a drop-down menu that lists out all the groceries

            def editGrocery():
                if self.selectIndex is None:
                    tkinter.messagebox.showinfo("No selection", "In order to edit a grocery, you have to choose first.")
                else:
                    self.addEditGrocery_UI(index=self.selectIndex, oldCategory=category_opt.get())

            def delGrocery():
                if self.selectIndex is None:
                    # Shows an error message
                    tkinter.messagebox.showinfo("No selection", "In order to delete a grocery, you have to choose first.")
                    print("WARNING: Nothing has been selected yet.")
                else:
                    # status = self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    
                    # if status == True or status == False:
                        # Init()
                    self.refreshUI(root, self.App)
            
            def consumeGrocery():
                if self.selectIndex is None:
                    # Shows an error message
                    tkinter.messagebox.showinfo("No selection", "In order to consume a grocery, you have to choose first.")
                    print("WARNING: Nothing has been selected yet.")
                else:
                    # status = self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    self.consumeGroceryByCategory(self.selectIndex, category_opt.get())
                    
                    # if status == True or status == False:
                        # Init()
                    self.refreshUI(root, self.App)
            
            def refillGrocery():
                if self.selectIndex is None:
                    # Shows an error message
                    tkinter.messagebox.showinfo("No selection", "In order to refill a grocery, you have to choose first.")
                    print("WARNING: Nothing has been selected yet.")
                else:
                    # status = self.delGroceryByCategory(self.selectIndex, category_opt.get())
                    self.refillGroceryByCategory(self.selectIndex, category_opt.get())
                    
                    # if status == True or status == False:
                        # Init()
                    self.refreshUI(root, self.App)
            
            def refillList():
                self.refillList()

            button_editGrocery.config(command=editGrocery)
            button_delGrocery.config(command=delGrocery)
            button_consumeGrocery.config(command=consumeGrocery)
            button_refillGrocery.config(command=refillGrocery)
            button_refillList.config(command=refillList)

            Init()  # Loads the data onto the dynamic form controls for the first time

            search.pack(pady=(20, 10))
            search.pack_propagate(False)
            table.pack(pady=(30, 30))
        
        actions.pack(pady=(0, 10))
        actions.pack_propagate(False)

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