import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup

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


def _convert_dates(df):
    # Make a copy so we don't change the original DataFrame
    df = df.copy()

    # Convert the match date into datetime
    df["date"] = pd.to_datetime(
        df["date"], format="%Y%m%d", errors="coerce"
    )

    return df


def _calculate_player_age(df, player_dob):
    # Make a copy of the DataFrame
    df = df.copy()

    # Convert the player's birthday to datetime
    birthday = pd.to_datetime(player_dob)

    # Calculate the player's age at each match
    df["player_age"] = (df["date"] - birthday).dt.days / 365.25

    return df


def _calculate_opponent_age(df, gender):
    df = df.copy()

    if gender == "female":
        # Convert opponent birthdays to dates
        opponent_dob = pd.to_datetime(
            df["opponent_info"], format="%Y%m%d", errors="coerce"
        )

        # Calculate age at each match
        df["opponent_age"] = (
            (df["date"] - opponent_dob).dt.days / 365.25
        )

    elif gender == "male":
        # Age is already provided
        df["opponent_age"] = pd.to_numeric(
            df["opponent_info"], errors="coerce"
        )

    else:
        raise ValueError("Gender must be 'female' or 'male'")

    return df


def _calculate_age_difference(df):
    # Make a copy of the DataFrame
    df = df.copy()

    # Calculate the age difference
    df["age_diff"] = df["player_age"] - df["opponent_age"]

    return df


def _clean_data(df):
    # Make a copy of the DataFrame
    df = df.copy()

    # Remove rows with missing age or date information
    df = df.dropna(
        subset=["date", "player_age", "opponent_age"]
    )

    # Keep only wins and losses
    df = df[df["result"].isin(["W", "L"])]

    return df


def _get_player_info(player_name):
    # Temporary player information for testing
    players = {
        "SerenaWilliams": ("1981-09-26", "female"),
        "RafaelNadal": ("1986-06-03", "male")
    }

    name = "".join(word[0].upper() + word[1:]
                   for word in player_name.split())

    if name not in players:
        raise ValueError(f"Player '{player_name}' not found")

    return players[name]


def get_player_matches(player_name):
    # Get the player's birthday and gender
    player_dob, gender = _get_player_info(player_name)

    # Download and extract the matches
    js_data = _download_matches(player_name)
    matches = _parse_matches(js_data)

    # Create the DataFrame and convert dates
    df = _extract_columns(matches)
    df = _convert_dates(df)

    # Calculate player and opponent ages
    df = _calculate_player_age(df, player_dob)
    df = _calculate_opponent_age(df, gender)

    # Calculate age difference and clean the data
    df = _calculate_age_difference(df)
    df = _clean_data(df)

    return df