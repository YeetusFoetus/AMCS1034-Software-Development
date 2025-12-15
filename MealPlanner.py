import tkinter as tk
from tkinter import messagebox

class MealPlanner:
    def __init__(self, window, back_callback):
        self.window = window
        self.back_callback = back_callback
        self.current_goal = ""
        
        self.GOAL_DATA = {
            "Weight Loss": {
                "desc": "Focus: High Fiber, Moderate Protein, Low Carbs.",
                "shopping_tips": [
                    "Produce: Leafy greens (Spinach, Kale), Cucumber, Tomato (High Volume, Low Cal).",
                    "Protein: Chicken Breast, White Fish, Tofu, Egg Whites.",
                    "Carbs: Minimize. Stick to Pumpkin or small amounts of Brown Rice."
                ],
                "targets": {
                    "Vegetables (Vitamins)": 600,
                    "Protein (Meat/Egg)": 140,
                    "Carbs (Rice/Noodle)": 120
                }
            },
            "Muscle Gain": {
                "desc": "Focus: High Protein, High Carbs, Caloric Surplus.",
                "shopping_tips": [
                    "Produce: Banana, Avocado, Broccoli (Calorie dense fruits).",
                    "Protein: Lean Beef, Salmon, Whole Eggs, Chicken Thigh.",
                    "Carbs: White Rice, Pasta, Potatoes, Oats (Energy source)."
                ],
                "targets": {
                    "Vegetables (Vitamins)": 350,
                    "Protein (Meat/Egg)": 200,
                    "Carbs (Rice/Noodle)": 400
                }
            }
        }
        
        self.user_entries = {}

    def open_planner_page(self):
        
        for widget in self.window.winfo_children():
            widget.destroy()
            
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(self.main_frame, text="Meal Planner & Tracker", font=("Arial", 20, "bold")).pack(pady=20)
        
        # --- Part 1: Goal Selection ---
        self.frame_part1 = tk.Frame(self.main_frame)
        self.frame_part1.pack(pady=20)
        
        tk.Label(self.frame_part1, text="Choose Your Goal", font=("Arial", 14)).pack(pady=10)
        
        btn_frame = tk.Frame(self.frame_part1)
        btn_frame.pack()
        
        # Weight Loss
        tk.Button(btn_frame, text="Weight Loss (Cut)", bg="#FFB6C1", width=20, height=3, command=lambda: self.setup_goal("Weight Loss")).grid(row=0, column=0, padx=20)
        
        # Muscle
        tk.Button(btn_frame, text="Muscle Gain (Bulk)", bg="#ADD8E6", width=20, height=3, command=lambda: self.setup_goal("Muscle Gain")).grid(row=0, column=1, padx=20)

        # Back to Menu
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_callback).pack(side=tk.BOTTOM, pady=10)

    def setup_goal(self, goal):
        self.current_goal = goal
        self.frame_part1.pack_forget()
        self.show_shopping_and_planning()

    def show_shopping_and_planning(self):
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        data = self.GOAL_DATA[self.current_goal]
        
        # --- Part 2: Shopping Guide ---
        frame_shopping = tk.LabelFrame(self.content_frame, text=f"Shopping Guide for {self.current_goal} (Weekly Target)", font=("Arial", 12, "bold"), fg="blue", padx=10, pady=10)
        frame_shopping.pack(fill="x", pady=10)
        
        tk.Label(frame_shopping, text=data["desc"], font=("Arial", 10, "italic")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))
        
        # --- Shopping List Table Header (Row 1) ---
        header_row = 1
        tk.Label(frame_shopping, text="Category", font=("Arial", 10, "bold")).grid(row=header_row, column=0, padx=10, pady=5, sticky="w")
        tk.Label(frame_shopping, text="Weekly Amount (kg)", font=("Arial", 10, "bold")).grid(row=header_row, column=1, padx=10, pady=5)
        tk.Label(frame_shopping, text="Example Items", font=("Arial", 10, "bold")).grid(row=header_row, column=2, padx=10, pady=5, sticky="w")
        
        # --- Shopping List Table Content (week target) ---
        row_idx = 2 
        for category, daily_target in data["targets"].items():
            weekly_kg = round((daily_target * 7) / 1000, 1)
            
            if "Vegetables" in category or "Vitamins" in category:
                example = "Broccoli, Spinach, Apples, Berries"
            elif "Protein" in category:
                example = "Chicken Breast/Thigh, Fish, Tofu, Eggs"
            elif "Carbs" in category:
                example = "Rice, Oats, Potatoes, Whole Wheat Bread"
            else:
                example = "N/A"
                
            tk.Label(frame_shopping, text=category, anchor="w").grid(row=row_idx, column=0, padx=10, sticky="w")
            tk.Label(frame_shopping, text=f"{weekly_kg} kg").grid(row=row_idx, column=1, padx=10)
            tk.Label(frame_shopping, text=example, anchor="w").grid(row=row_idx, column=2, padx=10, sticky="w")
            row_idx += 1

        # --- Daily Planner (System Show vs User Input) ---
        frame_planning = tk.LabelFrame(self.content_frame, text="Part 3: Daily Intake Tracker", font=("Arial", 12, "bold"), fg="green", padx=10, pady=10)
        frame_planning.pack(fill="both", expand=True, pady=10)
        
        tk.Label(frame_planning, text="Category", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame_planning, text="Target Goal (g)", font=("Arial", 10, "bold"), fg="black").grid(row=0, column=1, padx=10, pady=5, columnspan=2)
        tk.Label(frame_planning, text="Your Input (g)", font=("Arial", 10, "bold"), fg="black").grid(row=0, column=3, padx=10, pady=5, columnspan=2)
        
        row_idx = 1
        self.user_entries = {}
        
        for category, target_val in data["targets"].items():
            tk.Label(frame_planning, text=category).grid(row=row_idx, column=0, sticky="e", padx=10, pady=5)
            
            # System Show
            lbl_target = tk.Label(frame_planning, text=f"{target_val}", bg="#ffffff", width=8, relief="sunken")
            lbl_target.grid(row=row_idx, column=1, padx=(10, 0))
            tk.Label(frame_planning, text="g").grid(row=row_idx, column=2, sticky="w", padx=(0, 10))
            
            # User Input
            entry_user = tk.Entry(frame_planning, width=8, justify="center")
            entry_user.grid(row=row_idx, column=3, padx=(10, 0))
            tk.Label(frame_planning, text="g").grid(row=row_idx, column=4, sticky="w", padx=(0, 10))
            
            #Save and link to Part 4
            self.user_entries[category] = entry_user 
            row_idx += 1
            
        # Go to Part 4
        tk.Button(frame_planning, text="Generate Daily Report", bg="orange", 
                  command=lambda: self.generate_report(data["targets"])).grid(row=row_idx, column=0, columnspan=5, pady=20)
        
        tk.Button(self.content_frame, 
                  text="← Back to Goal Selection (Part 1)", 
                  command=lambda: self.content_frame.destroy() or self.open_planner_page()).pack(pady=10)
        
    def show_report_page(self, report_details, final_msg, all_good):
        """ Display Report Page (Transition to new content)"""
        if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
            self.content_frame.destroy() 
            
        self.report_frame = tk.Frame(self.main_frame)
        self.report_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(self.report_frame, text=f"--- Daily Performance Report for {self.current_goal} ---", 
                 font=("Arial", 16, "bold")).pack(pady=15)
        details_frame = tk.LabelFrame(self.report_frame, text="Category Breakdown (Target vs Actual)", padx=10, pady=10)
        details_frame.pack(padx=20, fill="x")
        
        tk.Label(details_frame, text="Category", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        tk.Label(details_frame, text="Status", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, sticky="w")
        
        row_idx = 1
        for category, status in report_details.items():
            tk.Label(details_frame, text=f"{category}:", width=20, anchor="w").grid(row=row_idx, column=0, padx=10, sticky="w")
            fg_color = "green" if status == "✅ Perfect!" else "red"
            tk.Label(details_frame, text=status, anchor="w", fg=fg_color).grid(row=row_idx, column=1, padx=10, sticky="w")
            row_idx += 1
            
        tk.Label(self.report_frame, text="----------------", pady=10).pack()
        fg_color = "green" if all_good else "red"
        
        tk.Label(self.report_frame, text=final_msg, font=("Arial", 14, "bold"), fg=fg_color, wraplength=500).pack(pady=15)
        
        # Back to Part2/3
        tk.Button(self.report_frame, text="Back to Planner", 
                  command=lambda: self.report_frame.destroy() or self.show_shopping_and_planning()).pack(pady=20)
            
    def generate_report(self, targets):
        """Calculates the logic for Part 4 and passes the result to show_report_page"""
        
        all_good = True
        report_details = {} 
        
        for category, target_val in targets.items():
            user_input_str = self.user_entries[category].get().strip()
            
            if not user_input_str:
                user_val = 0.0
            else:
                try:
                    user_val = float(user_input_str)
                except ValueError:
                    messagebox.showerror("Error", "Please enter numbers only in the input fields.")
                    return 

            # (System show - User input)
            diff = target_val - user_val
            
            # status more than or less than 15% also ok
            tolerance = target_val * 0.15 
            
            status = ""
            if abs(diff) <= tolerance:
                status = "✅ Perfect!"
            elif diff > tolerance:
                status = "⚠️ Eat More!"
                all_good = False
            else:
                status = "❌ Too Much!"
                all_good = False
                
            report_details[category] = status 

        # Final
        if all_good:
            final_msg = "Excellent Work! You hit your goals!"
        else:
            final_msg = "Don't give up! Try to stick to the plan tomorrow."
            
        self.show_report_page(report_details, final_msg, all_good)

# --- for testing ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Meal Planner Test")
    root.geometry("600x600")
    
    def back():
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text="Back to Main Menu placeholder").pack(pady=50)
        
    app = MealPlanner(root, back)
    app.open_planner_page()
    
    root.mainloop()