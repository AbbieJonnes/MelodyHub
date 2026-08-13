import sqlite3


# Database file
DATABASE_NAME = "melodyhub.db"

# DATABASE CONNECTION
def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_NAME)



# CREATE TABLE

def initialize_database():
    """
    Create the songs table if it does not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT,
            artwork TEXT,
            preview_url TEXT,
            track_id INTEGER,
            favorite INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# ADD SONG

def add_song(
    title,
    artist,
    album="",
    artwork="",
    preview_url="",
    track_id=None,
    favorite=False
):
    """
    Add a song to the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO songs
        (title, artist, album, artwork, preview_url, track_id, favorite)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        artist,
        album,
        artwork,
        preview_url,
        track_id,
        int(favorite)
    ))

    connection.commit()
    connection.close()


# GET ALL SONGS

def get_all_songs():
    """
    Return all songs stored in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM songs
        ORDER BY id DESC
    """)

    songs = cursor.fetchall()

    connection.close()

    return songs


# GET FAVORITES

def get_favorites():
    """
    Return only songs marked as favorites.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM songs
        WHERE favorite = 1
        ORDER BY id DESC
    """)

    favorites = cursor.fetchall()

    connection.close()

    return favorites


# GET ONE SONG

def get_song(song_id):
    """
    Find a song using its database ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM songs
        WHERE id = ?
    """, (song_id,))

    song = cursor.fetchone()

    connection.close()

    return song


# UPDATE SONG

def update_song(
    song_id,
    title,
    artist,
    album="",
    artwork="",
    preview_url="",
    track_id=None
):
    """
    Edit an existing song.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE songs
        SET
            title = ?,
            artist = ?,
            album = ?,
            artwork = ?,
            preview_url = ?,
            track_id = ?
        WHERE id = ?
    """, (
        title,
        artist,
        album,
        artwork,
        preview_url,
        track_id,
        song_id
    ))

    connection.commit()
    connection.close()


# TOGGLE FAVORITE

def toggle_favorite(song_id):
    """
    Change a song between favorite and not favorite.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE songs
        SET favorite =
            CASE
                WHEN favorite = 0 THEN 1
                ELSE 0
            END
        WHERE id = ?
    """, (song_id,))

    connection.commit()
    connection.close()


# DELETE SONG

def delete_song(song_id):
    """
    Delete a song from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM songs
        WHERE id = ?
    """, (song_id,))

    connection.commit()
    connection.close()


# CHECK IF SONG EXISTS

def song_exists(track_id):
    """
    Check whether an API song is already saved.
    """

    if track_id is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM songs
        WHERE track_id = ?
    """, (track_id,))

    result = cursor.fetchone()

    connection.close()

    return result is not None