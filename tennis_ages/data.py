import requests
import re
import json
import pandas as pd

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


def _extract_columns(matches):
    # Columns we want to keep
    columns = [
        "date",
        "tournament",
        "surface",
        "result",
        "opponent",
        "opponent_info"
    ]

    rows = []

    # Extract the relevant information from each match
    for match in matches:
        rows.append([
            match[0],   # Match date
            match[1],   # Tournament
            match[2],   # Surface
            match[4],   # Win or loss
            match[11],  # Opponent's name
            match[16]   # Opponent's DOB (female) or age (male)
        ])

    return pd.DataFrame(rows, columns=columns)