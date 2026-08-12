import requests


# iTunes Music API
API_URL = "https://itunes.apple.com/search"


def search_music(term):
    """
    Search for music using the iTunes Search API.

    Args:
        term: The song, artist, or music keyword to search for.

    Returns:
        A list of music results.
    """

    # Don't search if nothing was entered
    if not term or not term.strip():
        return []

    params = {
        "term": term.strip(),
        "country": "KE",
        "media": "music",
        "limit": 10
    }

    # Send request to the real API
    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )

    # Raise an error if the API request failed
    response.raise_for_status()

    # Convert API response from JSON to Python dictionary
    data = response.json()

    # Return only the songs
    return data.get("results", [])