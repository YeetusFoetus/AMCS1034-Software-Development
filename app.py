import tkinter as tk
from tkinter import ttk


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management System")
        self.root.geometry("500x400")

        self.build_main_menu()

    # ----------------------------------------------------
    # MAIN MENU
    # ----------------------------------------------------
    def build_main_menu(self):
        title = ttk.Label(self.root, text="Household Management", font=("Arial", 20))
        title.pack(pady=20)

        # Each button opens a different module window
        ttk.Button(self.root, text="Grocery List Manager", width=30,
                   command=self.open_grocery).pack(pady=8)

        ttk.Button(self.root, text="Meal Planner", width=30,
                   command=self.open_meal).pack(pady=8)

        ttk.Button(self.root, text="Budget Tracker", width=30,
                   command=self.open_budget).pack(pady=8)

        ttk.Button(self.root, text="Chore Scheduler", width=30,
                   command=self.open_chore).pack(pady=8)

    # ----------------------------------------------------
    # SUBMODULE WINDOWS
    # ----------------------------------------------------

    # --- Grocery List Module ---
    def open_grocery(self):
        win = tk.Toplevel(self.root)
        win.title("Grocery List Manager")
        win.geometry("450x350")

        ttk.Label(win, text="Grocery List Module", font=("Arial", 16)).pack(pady=10)

        # TODO: Add your grocery module widgets here
        ttk.Label(win, text="[TODO: Grocery UI here]").pack(pady=10)

    # --- Meal Planner Module ---
    def open_meal(self):
        win = tk.Toplevel(self.root)
        win.title("Meal Planner")
        win.geometry("450x350")

        ttk.Label(win, text="Meal Planner Module", font=("Arial", 16)).pack(pady=10)

        # TODO: Add your meal planner widgets here
        ttk.Label(win, text="[TODO: Meal Planner UI here]").pack(pady=10)

    # --- Budget Tracker Module ---
    def open_budget(self):
        win = tk.Toplevel(self.root)
        win.title("Budget Tracker")
        win.geometry("450x350")

        ttk.Label(win, text="Budget Tracker Module", font=("Arial", 16)).pack(pady=10)

        # TODO: Add your budget UI here
        ttk.Label(win, text="[TODO: Budget UI here]").pack(pady=10)

    # --- Chore Scheduler Module ---
    def open_chore(self):
        win = tk.Toplevel(self.root)
        win.title("Chore Scheduler")
        win.geometry("450x350")

        ttk.Label(win, text="Chore Scheduler Module", font=("Arial", 16)).pack(pady=10)

        # TODO: Add your chore scheduler UI here
        ttk.Label(win, text="[TODO: Chore Scheduler UI here]").pack(pady=10)


# ----------------------------------------------------
# RUN APP
# ----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
