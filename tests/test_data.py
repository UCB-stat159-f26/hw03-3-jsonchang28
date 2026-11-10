from tennis_ages.data import _parse_matches


def test_parse_matches():
    # Sample JavaScript data without downloading from the website
    js_data = 'var morematchmx = [["19951030", "Canadian Open"], ["19970307", "Indian Wells"]];'

    matches = _parse_matches(js_data)

    assert len(matches) == 2
    assert matches[0][0] == "19951030"
    assert matches[0][1] == "Canadian Open"
    assert matches[1][0] == "19970307"


import pandas as pd
from tennis_ages.data import _calculate_opponent_age


def test_female_opponent_age():
    # Sample female opponent birthday
    df = pd.DataFrame({
        "date": [pd.Timestamp("2000-01-01")],
        "opponent_info": ["19800101"]
    })

    result = _calculate_opponent_age(df, "female")

    assert round(result["opponent_age"].iloc[0], 2) == 20.00



def test_male_opponent_age():
    # Male match data already includes opponent age
    df = pd.DataFrame({
        "date": [pd.Timestamp("2000-01-01")],
        "opponent_info": ["25.5"]
    })

    result = _calculate_opponent_age(df, "male")

    assert result["opponent_age"].iloc[0] == 25.5


from tennis_ages.data import _calculate_age_difference

def test_age_difference():
    # Sample player and opponent ages
    df = pd.DataFrame({
        "player_age": [20, 25, 30],
        "opponent_age": [25, 20, 30]
    })

    result = _calculate_age_difference(df)

    assert result["age_diff"].tolist() == [-5, 5, 0]



from tennis_ages.data import _clean_data

def test_clean_data():
    # Sample data with missing values and invalid results
    df = pd.DataFrame({
        "date": ["2020-01-01"] * 4,
        "player_age": [20, 21, 22, 23],
        "opponent_age": [25, None, 19, 24],
        "result": ["W", "L", "R", "L"]
    })

    result = _clean_data(df)

    assert len(result) == 2
    assert result["result"].tolist() == ["W", "L"]


