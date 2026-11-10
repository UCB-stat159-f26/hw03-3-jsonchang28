from tennis_ages.data 
import _parse_matches


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
