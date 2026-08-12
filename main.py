import tkinter as tk

from database import initialize_database
from ui import create_home_page


# Initialize the database
initialize_database()


# Create the main application window
window = tk.Tk()

window.title("MelodyHub")
window.geometry("1000x700")
window.minsize(900, 600)

# Create the home page
create_home_page(window)


# Start the Tkinter application
window.mainloop()