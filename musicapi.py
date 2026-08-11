import requests


def search_music(term):
    url = "https://itunes.apple.com/search"

    params = {
        "term": term,
        "country": "KE",
        "media": "music",
        "limit": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    songs = []

    for item in data["results"]:
        song = {
            "title": item.get("trackName"),
            "artist": item.get("artistName"),
            "album": item.get("collectionName"),
            "artwork": item.get("artworkUrl100"),
            "preview": item.get("previewUrl"),
            "track_url": item.get("trackViewUrl")
        }

        songs.append(song)

    return songs