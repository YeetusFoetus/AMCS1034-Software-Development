import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter

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

    def menu(self):
        
        for widget in self.window.winfo_children():
            widget.destroy()

        bg_image = Image.open("house_interior.png")
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = ctk.CTkLabel(self.window, image=bg_photo, text="")
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

        label_frame = ctk.CTkFrame(self.window, border_width=2, border_color="black", corner_radius=0, fg_color="#c3b091")
        ctk.CTkLabel(label_frame, 
                     text="Meal Planner", text_color="black", font=("Microsoft HaYei",35), 
                     fg_color="#c3b091"
                     ).pack(pady=5, padx=5)
        label_frame.pack(padx=5, pady=10, anchor='center')
            
        self.main_frame = ctk.CTkFrame(self.window, width=700, height=600, border_width=2, border_color="black", corner_radius=0, fg_color='#c3b091')
        self.main_frame.pack(padx=20, pady=20)
        self.main_frame.pack_propagate(False)
        
        #tk.Label(self.main_frame, text="Meal Planner & Tracker", font=("Arial", 20, "bold")).pack(pady=20)
        
        # --- Part 1: Goal Selection ---
        self.frame_part1 = tk.Frame(self.main_frame, width=600, height=300, bg='#c3b091')
        self.frame_part1.pack(anchor='center', pady=(150, 0))
        self.frame_part1.pack_propagate(False)

        
        tk.Label(self.frame_part1, text="Choose Your Goal", bg="#c3b091", font=("Arial", 22)).pack(pady=15)
        
        btn_frame = tk.Frame(self.frame_part1, bg='#c3b091')
        btn_frame.pack(pady=(50, 0))
        
        # Weight Loss
        tk.Button(btn_frame, text="Weight Loss (Cut)", bg="#FFB6C1", width=20, height=3, font=("Arial", 13), command=lambda: self.setup_goal("Weight Loss")).grid(row=50, column=0, padx=20)
        
        # Muscle
        tk.Button(btn_frame, text="Muscle Gain (Bulk)", bg="#ADD8E6", width=20, height=3, font=("Arial", 13), command=lambda: self.setup_goal("Muscle Gain")).grid(row=50, column=1, padx=20)

        # Back to Menu
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.back_callback).pack(side=tk.BOTTOM, pady=10)

    def setup_goal(self, goal):
        self.current_goal = goal
        self.frame_part1.pack_forget()
        self.show_shopping_and_planning()

    def show_shopping_and_planning(self):
        self.content_frame = ctk.CTkFrame(self.main_frame, width=600, height=450, border_width=2, border_color='black', corner_radius=0, fg_color='#b09e83')
        self.content_frame.pack(anchor='center', pady=(40, 10))
        self.content_frame.pack_propagate(False)
        
        data = self.GOAL_DATA[self.current_goal]

        if self.current_goal == "Weight Loss":
            color = "red"#FFB6C1
        elif self.current_goal == "Muscle Gain":
            color = "blue"#ADD8E6
        else:
            color = "black"
        
        # --- Part 2: Shopping Guide ---
        frame_shopping = tk.LabelFrame(self.content_frame, text=f"Shopping Guide for {self.current_goal} (Weekly Target)", font=("Arial", 12, "bold"), fg=color, padx=10, pady=10)
        frame_shopping.pack(fill="x", padx=10, pady=20)
        
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

        # --- Part 3: Daily Planner (System Show vs User Input) ---
        frame_planning = tk.LabelFrame(self.content_frame, height=200, text="Daily Intake Tracker", font=("Arial", 12, "bold"), fg="green", padx=10, pady=10)
        frame_planning.pack(fill="x", expand=True, padx=10, pady=(0, 25))
        frame_planning.pack_propagate(False)

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
                  text="← Back to Goal Selection", 
                  command=lambda: self.content_frame.destroy() or self.menu()).pack(pady=10)
        
    def show_report_page(self, report_details, final_msg, all_good):
        """ Display Report Page (Transition to new content)"""
        if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
            self.content_frame.destroy() 
            
        self.report_frame = tk.Frame(self.main_frame, width=550, height=300, bg='#c3b091')
        self.report_frame.pack(pady=(200, 0))
        self.report_frame.pack_propagate(False)
        
        label_frame = ctk.CTkFrame(self.report_frame, fg_color='#c3b091', border_color='black', border_width=2, corner_radius=0)
        label_frame.pack(pady=15, fill='x')

        ctk.CTkLabel(label_frame, text=f"Daily Performance Report for {self.current_goal}", 
                 font=("Arial", 21, "bold"),
                 text_color='black',
                 fg_color='#c3b091').pack(pady=5)
        
        details_frame = tk.LabelFrame(self.report_frame, width=300, height=225, text="Category Breakdown (Target vs Actual)", font=("Arial", 13), padx=10, pady=10)
        details_frame.pack(padx=5, fill='x')
        details_frame.pack_propagate(False)
        
        tk.Label(details_frame, text="Category", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        tk.Label(details_frame, text="Status", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, sticky="w")
        
        row_idx = 1
        for category, status in report_details.items():
            tk.Label(details_frame, text=f"{category}:", font=("Arial", 11), width=20, anchor="w").grid(row=row_idx, column=0, padx=10, sticky="w")
            fg_color = "green" if status == "✅ Perfect!" else "red"
            tk.Label(details_frame, text=status, font=("Arial", 11), anchor="w", fg=fg_color).grid(row=row_idx, column=1, padx=10, sticky="w")
            row_idx += 1
            
        fg_color = "green" if all_good else "red"
        
        tk.Label(self.report_frame, text=final_msg, font=("Arial", 14, "bold"), bg='#c3b091', fg=fg_color, wraplength=500).pack(pady=15, fill='x')
        
        # Back to Part2/3
        tk.Button(self.report_frame, text="Back to Planner", 
                  command=lambda: self.report_frame.destroy() or self.show_shopping_and_planning()).pack()
            
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
    app.menu()
    
    root.mainloop()