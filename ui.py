import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
import os
import webbrowser

from musicapi import search_music
from database import (
    add_song,
    get_all_songs,
    get_favorites,
    get_song,
    update_song,
    toggle_favorite,
    delete_song,
    song_exists
)


# COLORS

BG_COLOR = "#0D0D0D"
CARD_COLOR = "#181818"
SECONDARY_COLOR = "#242424"
TEXT_COLOR = "#FFFFFF"
MUTED_COLOR = "#A7A7A7"
ACCENT_COLOR = "#1DB954"


# LOAD SVG ICON

def load_icon(filename, size=(24, 24)):
    """
    Load a Font Awesome SVG icon and convert it
    into an image that Tkinter can display.
    """

    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    path = os.path.join(
        project_folder,
        "assets",
        "icons",
        filename
    )

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Icon not found: {path}"
        )

    drawing = svg2rlg(path)

    if drawing is None:
        raise ValueError(
            f"Could not read SVG file: {path}"
        )

    png_data = renderPM.drawToString(
        drawing,
        fmt="PNG"
    )

    image = Image.open(
        BytesIO(png_data)
    )

    image = image.resize(
        size,
        Image.Resampling.LANCZOS
    )

    return ImageTk.PhotoImage(image)


# MAIN HOME PAGE

def create_home_page(window):

    window.configure(bg=BG_COLOR)

    # LOAD ICONS

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


    # MAIN CONTENT CONTAINER

    content = tk.Frame(
        window,
        bg=BG_COLOR
    )

    content.pack(
        fill="both",
        expand=True
    )

    # Store reference
    window.main_content = content

    # NAVIGATION BAR

    navbar = tk.Frame(
        window,
        bg="#080808",
        height=70
    )

    navbar.pack(
        fill="x",
        side="top"
    )

    # Logo
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

    # Home
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
        cursor="hand2",
        command=lambda: show_home(window)
    )

    nav_home.pack(
        side="left",
        padx=15
    )

    # My Music
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
        cursor="hand2",
        command=lambda: show_my_music(window)
    )

    nav_music.pack(
        side="left",
        padx=15
    )

    # Favorites
    nav_favorites = tk.Button(
        navbar,
        text="  Favorites",
        font=("Arial", 11, "bold"),
        bg="#080808",
        fg=TEXT_COLOR,
        activebackground="#080808",
        activeforeground=ACCENT_COLOR,
        bd=0,
        cursor="hand2",
        command=lambda: show_favorites(window)
    )

    nav_favorites.pack(
        side="left",
        padx=15
    )


    # FOOTER

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

    window.footer = footer

    # Show home page
    show_home(window)


# CLEAR MAIN CONTENT

def clear_content(window):

    for widget in window.main_content.winfo_children():
        widget.destroy()


# HOME SCREEN

def show_home(window):

    clear_content(window)

    content = window.main_content

    # Hero
    hero = tk.Frame(
        content,
        bg=BG_COLOR
    )

    hero.pack(
        fill="both",
        expand=True
    )

    # Heading
    heading = tk.Label(
        hero,
        text="Your Music.\nYour World.",
        font=("Arial", 50, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="center"
    )

    heading.pack(
        pady=(70, 10)
    )

    # Description
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

    # SEARCH BAR

    search_container = tk.Frame(
        hero,
        bg=SECONDARY_COLOR,
        padx=10,
        pady=10
    )

    search_container.pack(
        pady=25
    )

    search_icon_label = tk.Label(
        search_container,
        image=window.search_icon,
        bg=SECONDARY_COLOR
    )

    search_icon_label.pack(
        side="left",
        padx=(5, 8)
    )

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
        cursor="hand2",
        command=lambda: perform_search(
            window,
            search_entry.get()
        )
    )

    search_button.pack(
        side="left",
        padx=(10, 0)
    )

    # Press Enter to search
    search_entry.bind(
        "<Return>",
        lambda event: perform_search(
            window,
            search_entry.get()
        )
    )


    # FEATURE CARDS

    features = tk.Frame(
        hero,
        bg=BG_COLOR
    )

    features.pack(
        pady=15
    )

    # Discover
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
        image=window.search_icon,
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

    # My Music
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
        image=window.music_icon,
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

    # Favorites
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
        text="favorites",
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


# SEARCH MUSIC

def perform_search(window, term):

    term = term.strip()

    if not term:
        messagebox.showwarning(
            "Search",
            "Please enter a song or artist."
        )
        return

    try:

        results = search_music(term)

        show_search_results(
            window,
            results,
            term
        )

    except Exception as error:

        messagebox.showerror(
            "Search Error",
            f"Could not search for music.\n\n{error}"
        )


# SEARCH RESULTS

def show_search_results(window, results, term):

    clear_content(window)

    content = window.main_content

    # Heading
    tk.Label(
        content,
        text=f"Search Results for \"{term}\"",
        font=("Arial", 28, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(25, 10)
    )

    if not results:

        tk.Label(
            content,
            text="No music found.",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(
            pady=40
        )

        return

    # Back button
    tk.Button(
        content,
        text=" Back Home",
        font=("Arial", 10, "bold"),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        activebackground="#333333",
        activeforeground=TEXT_COLOR,
        bd=0,
        padx=15,
        pady=7,
        cursor="hand2",
        command=lambda: show_home(window)
    ).pack(
        pady=5
    )

    # Scrollable area
    outer = tk.Frame(
        content,
        bg=BG_COLOR
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=15
    )

    canvas = tk.Canvas(
        outer,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )

    results_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    results_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=results_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Display results
    for song in results:

        create_api_song_card(
            results_frame,
            song
        )


# API SONG CARD

def create_api_song_card(parent, song):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        padx=15,
        pady=12
    )

    card.pack(
        fill="x",
        pady=7
    )

    # Song information
    info = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    info.pack(
        side="left",
        fill="x",
        expand=True
    )

    title = song.get(
        "trackName",
        "Unknown Song"
    )

    artist = song.get(
        "artistName",
        "Unknown Artist"
    )

    album = song.get(
        "collectionName",
        "Unknown Album"
    )

    tk.Label(
        info,
        text=title,
        font=("Arial", 13, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        anchor="w"
    ).pack(
        anchor="w"
    )

    tk.Label(
        info,
        text=f"{artist} • {album}",
        font=("Arial", 10),
        bg=CARD_COLOR,
        fg=MUTED_COLOR,
        anchor="w"
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    # Buttons
    buttons = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    buttons.pack(
        side="right"
    )

    preview_url = song.get(
        "previewUrl"
    )

    if preview_url:

        tk.Button(
            buttons,
            text=" Preview",
            font=("Arial", 9, "bold"),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR,
            activebackground="#333333",
            activeforeground=TEXT_COLOR,
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=lambda url=preview_url:
                play_preview(url)
        ).pack(
            side="left",
            padx=4
        )

    tk.Button(
        buttons,
        text="Favorite",
        font=("Arial", 9, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#1AA34A",
        activeforeground="white",
        bd=0,
        padx=10,
        pady=6,
        cursor="hand2",
        command=lambda s=song:
            save_api_favorite(s)
    ).pack(
        side="left",
        padx=4
    )


# SAVE API SONG AS FAVORITE

def save_api_favorite(song):

    track_id = song.get(
        "trackId"
    )

    if song_exists(track_id):

        messagebox.showinfo(
            "Favorites",
            "This song is already in your music collection."
        )

        return

    add_song(
        title=song.get(
            "trackName",
            "Unknown Song"
        ),
        artist=song.get(
            "artistName",
            "Unknown Artist"
        ),
        album=song.get(
            "collectionName",
            "Unknown Album"
        ),
        artwork=song.get(
            "artworkUrl100",
            ""
        ),
        preview_url=song.get(
            "previewUrl",
            ""
        ),
        track_id=track_id,
        favorite=True
    )

    messagebox.showinfo(
        "Favorites",
        "Song added to your favorites! ❤️"
    )


# PLAY PREVIEW

def play_preview(url):

    if not url:

        messagebox.showinfo(
            "Preview",
            "No preview is available for this song."
        )

        return

    try:

        webbrowser.open(url)

    except Exception as error:

        messagebox.showerror(
            "Preview Error",
            str(error)
        )

# MY MUSIC

def show_my_music(window):

    clear_content(window)

    content = window.main_content

    tk.Label(
        content,
        text="My Music",
        font=("Arial", 30, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        content,
        text="Your saved music collection",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(
        pady=(0, 15)
    )

    # Add button
    tk.Button(
        content,
        text="+ Add Song",
        font=("Arial", 10, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#1AA34A",
        activeforeground="white",
        bd=0,
        padx=18,
        pady=8,
        cursor="hand2",
        command=lambda: show_add_song(window)
    ).pack(
        pady=10
    )

    songs = get_all_songs()

    if not songs:

        tk.Label(
            content,
            text="Your music collection is empty.",
            font=("Arial", 13),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(
            pady=30
        )

        return

    # Scroll area
    outer = tk.Frame(
        content,
        bg=BG_COLOR
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=15
    )

    canvas = tk.Canvas(
        outer,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )

    songs_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    songs_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=songs_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for song in songs:

        create_database_song_card(
            songs_frame,
            song,
            window
        )


# DATABASE SONG CARD
def create_database_song_card(parent, song, window):

    song_id = song[0]
    title = song[1]
    artist = song[2]
    album = song[3]
    favorite = song[7]

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        padx=15,
        pady=12
    )

    card.pack(
        fill="x",
        pady=7
    )

    info = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    info.pack(
        side="left",
        fill="x",
        expand=True
    )

    tk.Label(
        info,
        text=title,
        font=("Arial", 13, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    tk.Label(
        info,
        text=f"{artist} • {album}",
        font=("Arial", 10),
        bg=CARD_COLOR,
        fg=MUTED_COLOR
    ).pack(
        anchor="w"
    )

    buttons = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    buttons.pack(
        side="right"
    )

    # Favorite
    favorite_text = "♥" if favorite else "♡"

    tk.Button(
        buttons,
        text=favorite_text,
        font=("Arial", 15),
        bg=CARD_COLOR,
        fg=ACCENT_COLOR,
        activebackground=CARD_COLOR,
        activeforeground=ACCENT_COLOR,
        bd=0,
        cursor="hand2",
        command=lambda sid=song_id:
            favorite_database_song(window, sid)
    ).pack(
        side="left",
        padx=4
    )

    # Preview
    preview_url = song[5]

    if preview_url:

        tk.Button(
            buttons,
            text="▶",
            font=("Arial", 10, "bold"),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=lambda url=preview_url:
                play_preview(url)
        ).pack(
            side="left",
            padx=4
        )

    # Edit
    tk.Button(
        buttons,
        text="Edit",
        font=("Arial", 9, "bold"),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        activebackground="#333333",
        activeforeground=TEXT_COLOR,
        bd=0,
        padx=10,
        pady=6,
        cursor="hand2",
        command=lambda sid=song_id:
            show_edit_song(window, sid)
    ).pack(
        side="left",
        padx=4
    )

    # Delete
    tk.Button(
        buttons,
        text="Delete",
        font=("Arial", 9, "bold"),
        bg="#8B0000",
        fg="white",
        activebackground="#AA0000",
        activeforeground="white",
        bd=0,
        padx=10,
        pady=6,
        cursor="hand2",
        command=lambda sid=song_id:
            confirm_delete(window, sid)
    ).pack(
        side="left",
        padx=4
    )


# FAVORITE DATABASE SONG

def favorite_database_song(window, song_id):

    toggle_favorite(song_id)

    show_my_music(window)


# FAVORITES PAGE

def show_favorites(window):

    clear_content(window)

    content = window.main_content

    tk.Label(
        content,
        text="Favorites ♥",
        font=("Arial", 30, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        content,
        text="Your favorite songs",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(
        pady=(0, 20)
    )

    favorites = get_favorites()

    if not favorites:

        tk.Label(
            content,
            text="You haven't added any favorites yet.",
            font=("Arial", 13),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(
            pady=40
        )

        return

    outer = tk.Frame(
        content,
        bg=BG_COLOR
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=40
    )

    for song in favorites:

        create_database_song_card(
            outer,
            song,
            window
        )


# ADD SONG PAGE

def show_add_song(window):

    clear_content(window)

    content = window.main_content

    tk.Label(
        content,
        text="Add Your Own Song",
        font=("Arial", 28, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(30, 25)
    )

    form = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=30,
        pady=25
    )

    form.pack()

    title_entry = create_form_field(
        form,
        "Song Title"
    )

    artist_entry = create_form_field(
        form,
        "Artist"
    )

    album_entry = create_form_field(
        form,
        "Album"
    )

    # Buttons
    buttons = tk.Frame(
        form,
        bg=CARD_COLOR
    )

    buttons.pack(
        pady=20
    )

    tk.Button(
        buttons,
        text="Save Song",
        font=("Arial", 10, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#1AA34A",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2",
        command=lambda: save_manual_song(
            window,
            title_entry,
            artist_entry,
            album_entry
        )
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        buttons,
        text="Cancel",
        font=("Arial", 10, "bold"),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2",
        command=lambda: show_my_music(window)
    ).pack(
        side="left",
        padx=5
    )


# FORM FIELD

def create_form_field(parent, label_text):

    tk.Label(
        parent,
        text=label_text,
        font=("Arial", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        anchor="w"
    )

    entry = tk.Entry(
        parent,
        width=40,
        font=("Arial", 11),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        bd=0
    )

    entry.pack(
        pady=(5, 15),
        ipady=7
    )

    return entry


# SAVE MANUAL SONG

def save_manual_song(
    window,
    title_entry,
    artist_entry,
    album_entry
):

    title = title_entry.get().strip()
    artist = artist_entry.get().strip()
    album = album_entry.get().strip()

    if not title or not artist:

        messagebox.showwarning(
            "Add Song",
            "Song title and artist are required."
        )

        return

    add_song(
        title=title,
        artist=artist,
        album=album,
        artwork="",
        preview_url="",
        track_id=None,
        favorite=False
    )

    messagebox.showinfo(
        "Success",
        "Song added to My Music! 🎵"
    )

    show_my_music(window)


# EDIT SONG

def show_edit_song(window, song_id):

    song = get_song(song_id)

    if not song:

        messagebox.showerror(
            "Error",
            "Song could not be found."
        )

        return

    clear_content(window)

    content = window.main_content

    tk.Label(
        content,
        text="Edit Song",
        font=("Arial", 28, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(30, 25)
    )

    form = tk.Frame(
        content,
        bg=CARD_COLOR,
        padx=30,
        pady=25
    )

    form.pack()

    title_entry = create_form_field(
        form,
        "Song Title"
    )

    artist_entry = create_form_field(
        form,
        "Artist"
    )

    album_entry = create_form_field(
        form,
        "Album"
    )

    # Put old values into fields
    title_entry.insert(
        0,
        song[1]
    )

    artist_entry.insert(
        0,
        song[2]
    )

    album_entry.insert(
        0,
        song[3] or ""
    )

    buttons = tk.Frame(
        form,
        bg=CARD_COLOR
    )

    buttons.pack(
        pady=20
    )

    tk.Button(
        buttons,
        text="Update Song",
        font=("Arial", 10, "bold"),
        bg=ACCENT_COLOR,
        fg="white",
        activebackground="#1AA34A",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2",
        command=lambda: save_edit(
            window,
            song_id,
            title_entry,
            artist_entry,
            album_entry
        )
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        buttons,
        text="Cancel",
        font=("Arial", 10, "bold"),
        bg=SECONDARY_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2",
        command=lambda: show_my_music(window)
    ).pack(
        side="left",
        padx=5
    )


# SAVE EDIT

def save_edit(
    window,
    song_id,
    title_entry,
    artist_entry,
    album_entry
):

    title = title_entry.get().strip()
    artist = artist_entry.get().strip()
    album = album_entry.get().strip()

    if not title or not artist:

        messagebox.showwarning(
            "Edit Song",
            "Song title and artist are required."
        )

        return

    old_song = get_song(song_id)

    if not old_song:
        return

    update_song(
        song_id=song_id,
        title=title,
        artist=artist,
        album=album,
        artwork=old_song[4],
        preview_url=old_song[5],
        track_id=old_song[6]
    )

    messagebox.showinfo(
        "Success",
        "Song updated successfully! ✏️"
    )

    show_my_music(window)


# DELETE CONFIRMATION

def confirm_delete(window, song_id):

    answer = messagebox.askyesno(
        "Delete Song",
        "Are you sure you want to delete this song?"
    )

    if answer:

        delete_song(song_id)

        messagebox.showinfo(
            "Deleted",
            "Song deleted successfully."
        )

        show_my_music(window)