import requests

def _download_matches(player_name):
    # Remove spaces from the player's name
    name = player_name.replace(" ", "")

    # Create the URL for the player's career data
    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"

    # Download the data
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Return the JavaScript content
    return response.text