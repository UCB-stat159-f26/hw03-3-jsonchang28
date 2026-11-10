from pathlib import Path
import requests

# URL containing Serena Williams's career match data
url = "https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js"

# Create the data folder if it doesn't exist
data = Path("data")
data.mkdir(exist_ok=True)

# Download the JavaScript file
response = requests.get(url, timeout=30)
response.raise_for_status()

# Save the file in the data folder
file_path = data / "SerenaWilliamsCareer.js"

with open(file_path, "wb") as file:
    file.write(response.content)