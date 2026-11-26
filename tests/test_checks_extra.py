import pandas as pd

from mp035.data_checks import check_spelling, check_target_typos, check_unit_mixup


def test_unit_mixup_found_when_one_zone_is_1000_times_bigger():
    df = pd.DataFrame(
        {
            "station_zone": ["Central"] * 5 + ["Residential"] * 10 + ["Industrial"] * 5,
            "wind_kmph": [10.0] * 15 + [10000.0] * 5,
        }
    )
    result = check_unit_mixup(df)
    assert result["present"] is True
    assert result["group_value"] == "Industrial"
    assert result["factor"] == 1000


def test_target_typo_found_when_value_is_far_above_the_rest():
    df = pd.DataFrame({"pm25_next_day": [100.0] * 20 + [1500.0]})
    result = check_target_typos(df)
    assert result["present"] is True
    assert result["count"] == 1


def test_spelling_variants_found():
    df = pd.DataFrame(
        {"day_type": ["weekday"] * 3, "station_zone": ["Central", "central ", "Central."]}
    )
    result = check_spelling(df)
    assert result["present"] is True
    assert result["column"] == "station_zone"
    assert result["true_levels"] == 1
