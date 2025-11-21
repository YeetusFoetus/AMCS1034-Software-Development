import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management System")
        self.root.geometry("600x500")

        # Use a modern theme
        style = ttk.Style(theme="flatly")

        self.build_main_menu()

    # ----------------------------------------------------
    # MAIN MENU
    # ----------------------------------------------------
    def build_main_menu(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=True)

        title = ttk.Label(frame, text="Household Management", 
                          font=("Segoe UI", 24, "bold"))
        title.pack(pady=20)

        # Icon images (optional)
        try:
            self.grocery_img = tk.PhotoImage(file="icons/grocery.png").subsample(6)
            self.meal_img = tk.PhotoImage(file="icons/meal.png").subsample(6)
            self.budget_img = tk.PhotoImage(file="icons/budget.png").subsample(6)
            self.chore_img = tk.PhotoImage(file="icons/chore.png").subsample(6)
        except:
            self.grocery_img = self.meal_img = self.budget_img = self.chore_img = None

        # Modern rounded buttons
        ttk.Button(frame, text="  Grocery List Manager", image=self.grocery_img,
                   compound="left", bootstyle=PRIMARY, width=30,
                   command=self.open_grocery).pack(pady=12)

        ttk.Button(frame, text="  Meal Planner", image=self.meal_img,
                   compound="left", bootstyle=INFO, width=30,
                   command=self.open_meal).pack(pady=12)

        ttk.Button(frame, text="  Budget Tracker", image=self.budget_img,
                   compound="left", bootstyle=SUCCESS, width=30,
                   command=self.open_budget).pack(pady=12)

        ttk.Button(frame, text="  Chore Scheduler", image=self.chore_img,
                   compound="left", bootstyle=DANGER, width=30,
                   command=self.open_chore).pack(pady=12)

    # ----------------------------------------------------
    # SUBMODULE WINDOWS (Modern Styled)
    # ----------------------------------------------------
    def base_window(self, title):
        win = ttk.Toplevel(self.root)
        win.title(title)
        win.geometry("500x400")
        ttk.Label(win, text=title, font=("Segoe UI", 20, "bold")).pack(pady=20)
        return win

    def open_grocery(self):
        win = self.base_window("Grocery List Manager")
        ttk.Label(win, text="[TODO: Grocery UI Here]").pack(pady=20)

    def open_meal(self):
        win = self.base_window("Meal Planner")
        ttk.Label(win, text="[TODO: Meal Planner UI Here]").pack(pady=20)

    def open_budget(self):
        win = self.base_window("Budget Tracker")
        ttk.Label(win, text="[TODO: Budget UI Here]").pack(pady=20)

    def open_chore(self):
        win = self.base_window("Chore Scheduler")
        ttk.Label(win, text="[TODO: Chore Scheduler UI Here]").pack(pady=20)


# ----------------------------------------------------
# RUN APP
# ----------------------------------------------------
if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = MainApp(root)
    root.mainloop()
