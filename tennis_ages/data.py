import requests
import re
import json

def _download_matches(player_name):
    # Remove spaces from the player's name
    name = "".join(word[0].upper() + word[1:] for word in player_name.split())

    # Create the URL for the player's career data
    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"

    # Download the data
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Return the JavaScript content
    return response.text


def _parse_matches(js_data):
    # Find the match data in the JavaScript file
    match = re.search(r"var\s+morematchmx\s*=", js_data)

    if match is None:
        raise ValueError("Could not find match data in JS file")

    # Find the beginning of the match array
    start = js_data.index("[", match.end())

    # Convert the JavaScript array into a Python list
    matches, _ = json.JSONDecoder().raw_decode(js_data[start:])

    return matches