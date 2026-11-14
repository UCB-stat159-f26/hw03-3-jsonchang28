# Tennis Ages: Python Package

## Overview

This Python package retrieves professional tennis players' career match data from Tennis Abstract and creates scatter plots comparing a player's age with their opponents' ages.

The package works with both male and female tennis players. It calculates player ages, opponent ages, and age differences, then separates wins and losses for visualization.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-jsonchang28.git
```

## Main Functions

The package contains two public functions:

### 1. get_player_matches(player_name)

Retrieves a player's career match data from Tennis Abstract and returns a cleaned pandas DataFrame.

The DataFrame includes:
- Match date
- Player age
- Opponent age
- Age difference
- Match result (W or L)

### 2. plot_age_comparison(df)

Creates a scatter plot showing the relationship between a player's age and the age difference between the player and their opponents.

- X-axis: Player's age
- Y-axis: Player age minus opponent age
- Blue points: Matches won
- Pink points: Matches lost

## Usage Examples

First, import the functions:

```python
from tennis_ages import get_player_matches, plot_age_comparison
```

### Example 1: Serena Williams

```python
serena = get_player_matches("Serena Williams")
fig = plot_age_comparison(serena)
fig.savefig("serena_matches.png")
```

### Example 2: Rafael Nadal

```python
nadal = get_player_matches("Rafael Nadal")
fig = plot_age_comparison(nadal)
fig.savefig("nadal_matches.png")
```

### Example 3: Invalid Player

```python
get_player_matches("Gaston Sanchez")
```

This produces a meaningful error message:

```text
ValueError: Player 'Gaston Sanchez' not found
```

## Testing

The package includes automated tests covering:

- Parsing JavaScript match data
- Calculating female opponent ages from birthdates
- Processing male opponent ages
- Calculating age differences
- Cleaning match data

Tests use sample data rather than accessing the live Tennis Abstract website.

To run all tests:

```bash
python -m pytest tests/ -v
```

## Dependencies

- Python 3.9+
- pandas
- matplotlib
- requests

## Data Source

All tennis match data comes from [Tennis Abstract](https://www.tennisabstract.com/).
