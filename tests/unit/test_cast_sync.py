
from pipelines import cast_sync
from unittest.mock import MagicMock


def test_sync_cast_tmdb_failure(monkeypatch):
    movie = {
        "id": 1,
        "tmdb_id": 550,
        "title": "Fight Club",
    }

    def fake_table(name):
        raise AssertionError("Supabase sa nemalo volať!")

    monkeypatch.setattr(
        cast_sync,
        "get_movie_cast",
        lambda tmdb_id, limit: None
    )

    monkeypatch.setattr(
        cast_sync.supabase,
        "table",
        fake_table
    )

    result = cast_sync._sync_cast_for_movie(movie)

    assert result == (0, 0, False)






from unittest.mock import MagicMock
from pipelines import cast_sync


