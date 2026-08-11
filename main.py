import tkinter as tk
from ui import create_home_page


# Create the main application window
window = tk.Tk()

# Window settings
window.title("MelodyHub")
window.geometry("1200x800")
window.minsize(1000, 700)

# Create the landing page
create_home_page(window)

# Keep the application running
window.mainloop()