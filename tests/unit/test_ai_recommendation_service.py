from services.ai_prompt_parser import normalize_filters

def test_normalize_filters_valid_values():
    filters = {
        "actor": "  Brad Pitt ",
        "mood": "  DARK ",
        "theme": "  REVENGE ",
        "year": "2020",
        "year_from": "2010",
        "year_to": "2024",
        "min_rating": "7.5",
    }
    response = normalize_filters(filters)

    assert filters["actor"] == "  Brad Pitt "
    assert filters["year"] == "2020"
    assert response["actor"] == "Brad Pitt"
    assert response["mood"] == "dark"
    assert response["theme"] == "revenge"
    assert response["year"] == 2020
    assert response["year_from"] == 2010
    assert response["year_to"] == 2024
    assert response["min_rating"] == 7.5


def test_normalize_filters_invalid_values():
    filters = {
        "actor": "   ",
        "mood": "   ",
        "year": "unknown",
        "year_from": "",
        "year_to": "abc",
        "min_rating": "invalid",
    }
    response = normalize_filters(filters)


    assert response["min_rating"] == 0
    assert response["year_from"] is None
    assert response["year_to"] is None
    assert response["year"] is None
    assert response["actor"] is None
    assert response["mood"] is None


