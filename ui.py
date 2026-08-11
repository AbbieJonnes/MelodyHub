import tkinter as tk
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
import os


# ---------- COLORS ----------

BG_COLOR = "#0D0D0D"
CARD_COLOR = "#181818"
SECONDARY_COLOR = "#242424"
TEXT_COLOR = "#FFFFFF"
MUTED_COLOR = "#A7A7A7"
ACCENT_COLOR = "#1DB954"


# ---------- LOAD SVG ICON ----------

def load_icon(filename, size=(24, 24)):
    # Get the folder where this ui.py file is located
    project_folder = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to the icon
    path = os.path.join(
        project_folder,
        "assets",
        "icons",
        filename
    )

    # Check that the icon exists
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Icon not found: {path}"
        )

    # Read the SVG file
    drawing = svg2rlg(path)

    if drawing is None:
        raise ValueError(
            f"Could not read SVG file: {path}"
        )

    # Convert SVG to PNG
    png_data = renderPM.drawToString(
        drawing,
        fmt="PNG"
    )

    # Open the PNG with Pillow
    image = Image.open(
        BytesIO(png_data)
    )

    # Resize the icon
    image = image.resize(
        size,
        Image.Resampling.LANCZOS
    )

    # Convert it to a Tkinter-compatible image
    return ImageTk.PhotoImage(image)


# ---------- HOME PAGE ----------

def create_home_page(window):

    # Window background
    window.configure(
        bg=BG_COLOR
    )

    # Load Font Awesome icons
    home_icon = load_icon(
        "home.svg",
        (22, 22)
    )

    music_icon = load_icon(
        "music.svg",
        (22, 22)
    )

    search_icon = load_icon(
        "search-dollar.svg",
        (22, 22)
    )

    # Keep icons alive
    window.home_icon = home_icon
    window.music_icon = music_icon
    window.search_icon = search_icon


    # ==================================================
    # NAVIGATION BAR
    # ==================================================

    navbar = tk.Frame(
        window,
        bg="#080808",
        height=70
    )

    navbar.pack(
        fill="x",
        side="top"
    )


    # ---------- LOGO ----------

    logo = tk.Label(
        navbar,
        text="MelodyHub",
        font=("Arial", 22, "bold"),
        bg="#080808",
        fg=ACCENT_COLOR
    )

    logo.pack(
        side="left",
        padx=30
    )


    # ---------- HOME BUTTON ----------

    nav_home = tk.Button(
        navbar,
        image=home_icon,
        text="  Home",
        compound="left",
        font=("Arial", 11, "bold"),
        bg="#080808",
        fg=TEXT_COLOR,
        activebackground="#080808",
        activeforeground=ACCENT_COLOR,
        bd=0,
        cursor="hand2"
    )

    nav_home.pack(
        side="left",
        padx=15
    )


    # ---------- MY MUSIC BUTTON ----------

    nav_music = tk.Button(
        navbar,
        image=music_icon,
        text="  My Music",
        compound="left",
        font=("Arial", 11, "bold"),
        bg="#080808",
        fg=TEXT_COLOR,
        activebackground="#080808",
        activeforeground=ACCENT_COLOR,
        bd=0,
        cursor="hand2"
    )

    nav_music.pack(
        side="left",
        padx=15
    )


    # ==================================================
    # HERO SECTION
    # ==================================================

    hero = tk.Frame(
        window,
        bg=BG_COLOR
    )

    hero.pack(
        fill="both",
        expand=True
    )


    # ---------- MAIN HEADING ----------

    heading = tk.Label(
        hero,
        text="Your Music.\nYour World.",
        font=("Arial", 50, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="center"
    )

    heading.pack(
        pady=(80, 10)
    )


    # ---------- DESCRIPTION ----------

    description = tk.Label(
        hero,
        text=(
            "Discover music, save your favorites,\n"
            "and build your own personal music collection."
        ),
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=MUTED_COLOR,
        justify="center"
    )

    description.pack(
        pady=10
    )


    # ==================================================
    # SEARCH SECTION
    # ==================================================

    search_container = tk.Frame(
        hero,
        bg=SECONDARY_COLOR,
        padx=10,
        pady=10
    )

    search_container.pack(
        pady=30
    )


    # ---------- SEARCH ICON ----------

    search_icon_label = tk.Label(
        search_container,
        image=search_icon,
        bg=SECONDARY_COLOR
    )

    search_icon_label.pack(
        side="left",
        padx=(5, 8)
    )


    # ---------- SEARCH BOX ----------

    search_entry = tk.Entry(
        search_container,
        width=35,
        font=("Arial", 14),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        bd=0
    )

    search_entry.pack(
        side="left",
        ipady=8
    )


    # ---------- SEARCH BUTTON ----------

    search_button = tk.Button(
        search_container,
        text="Search",
        font=("Arial", 11, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#1AA34A",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=9,
        cursor="hand2"
    )

    search_button.pack(
        side="left",
        padx=(10, 0)
    )


    # ==================================================
    # FEATURE CARDS
    # ==================================================

    features = tk.Frame(
        hero,
        bg=BG_COLOR
    )

    features.pack(
        pady=20
    )


    # ---------- DISCOVER MUSIC CARD ----------

    search_card = tk.Frame(
        features,
        bg=CARD_COLOR,
        width=220,
        height=110
    )

    search_card.pack(
        side="left",
        padx=10
    )

    search_card.pack_propagate(False)

    tk.Label(
        search_card,
        image=search_icon,
        bg=CARD_COLOR
    ).pack(
        pady=(15, 5)
    )

    tk.Label(
        search_card,
        text="Discover Music",
        font=("Arial", 11, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack()


    # ---------- MY MUSIC CARD ----------

    music_card = tk.Frame(
        features,
        bg=CARD_COLOR,
        width=220,
        height=110
    )

    music_card.pack(
        side="left",
        padx=10
    )

    music_card.pack_propagate(False)

    tk.Label(
        music_card,
        image=music_icon,
        bg=CARD_COLOR
    ).pack(
        pady=(15, 5)
    )

    tk.Label(
        music_card,
        text="My Music",
        font=("Arial", 11, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack()


    # ---------- FAVORITES CARD ----------

    favorites_card = tk.Frame(
        features,
        bg=CARD_COLOR,
        width=220,
        height=110
    )

    favorites_card.pack(
        side="left",
        padx=10
    )

    favorites_card.pack_propagate(False)

    tk.Label(
        favorites_card,
        text="♡",
        font=("Arial", 25),
        bg=CARD_COLOR,
        fg=ACCENT_COLOR
    ).pack(
        pady=(8, 0)
    )

    tk.Label(
        favorites_card,
        text="Favorites",
        font=("Arial", 11, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack()


    # ==================================================
    # FOOTER
    # ==================================================

    footer = tk.Label(
        window,
        text="MelodyHub • Discover. Save. Enjoy.",
        font=("Arial", 9),
        bg="#080808",
        fg=MUTED_COLOR
    )

    footer.pack(
        fill="x",
        side="bottom",
        pady=10
    )