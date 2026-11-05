
from pipelines.movie_transformer import build_genre_map, transform_movie



def test_build_genre_map():
    genres = [
        {"id": 28, "name": "Action"},
        {"id": 35, "name": "Comedy"},
        {"id": 18, "name": "Drama"},
    ]
    response = build_genre_map(genres)

    assert response == {
    28: "Action",
    35: "Comedy",
    18: "Drama",
}


def test_transform_movie_success():

    movie = {
        "id": 550,
        "title": "Fight Club",
        "release_date": "1999-10-15",
        "genre_ids": [18, 53],
        "vote_average": 8.4,
        "original_language": "en",
        "popularity": 85.5,
        "overview": "An insomniac office worker meets a soap salesman.",
        "vote_count": 25000,
        "original_title": "Fight Club",
    }

    genre_map = {
        18: "Drama",
        53: "Thriller",
    }

    details = {
        "runtime": 139,
        "poster_path": "/fightclub.jpg",
    }

    response = transform_movie(movie, genre_map, details)

    assert response["tmdb_id"] == 550
    assert response["title"] == "Fight Club"
    assert response["release_date"] == "1999-10-15"
    assert response["original_language"] == "en"
    assert response["popularity"] == 85.5
    assert response["rating"] == 8.4
    assert response["original_title"] == "Fight Club"
    assert response["runtime"] == 139
    assert response["poster_path"] == "/fightclub.jpg"
    assert response["year"] == 1999
    assert response["category"] == "Drama, Thriller"


def test_transform_movie_missing_data():

    movie = {
        "id": 550,
        "title": "Fight Club",
        "release_date": "",
        "genre_ids": [18, 53],
        "vote_average": 8.4,
        "original_language": "en",
        "popularity": 85.5,
        "overview": "An insomniac office worker meets a soap salesman.",
        "vote_count": 25000,
        "original_title": "Fight Club",
    }

    genre_map = {
        18: "Drama",
        53: "Thriller",
    }

    details = None

    response = transform_movie(movie, genre_map, details)


    assert response["release_date"] is None
    assert response["year"] is None
    assert response["poster_path"] is None


