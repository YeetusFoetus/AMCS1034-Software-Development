import customtkinter as ctk
from PIL import ImageTk, Image

root = ctk.CTk()

# Open the png
img = Image.open("house.png")

# Resize to 16x16 (or 32x32)
img = img.resize((16, 16), Image.Resampling.LANCZOS)

# Convert to PhotoImage
photo = ImageTk.PhotoImage(img)

# Set window icon
root.iconphoto(True, photo)

# Keep a reference to prevent garbage collection
root.icon_image = photo

root.mainloop()