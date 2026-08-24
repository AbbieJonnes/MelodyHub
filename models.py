class Song:
    def __init__(  #init runs automatically when you add a new song
        self,
        title,
        artist,
        album="Unknown",
        artwork="",
        preview_url="",
        track_id=None,
        favorite=False
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.artwork = artwork
        self.preview_url = preview_url
        self.track_id = track_id
        self.favorite = favorite   