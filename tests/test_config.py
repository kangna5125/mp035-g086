from mp035.config import load_params


def test_params_has_required_sections():
    params = load_params()
    for key in ["paths", "cleaning", "model"]:
        assert key in params


def test_model_lists_target_and_features():
    m = load_params()["model"]
    assert m["target"] == "pm25_next_day"
    assert len(m["features_numeric"]) == 6
    assert len(m["features_categorical"]) == 2
