"""Test the ability of the API on the User object."""

import datetime
from unittest.mock import patch

from raindropiopy import API, User, BrokenLevel, FontColor, RaindropSort, View

test_user = {
    "_id": 1000,
    "config": {
        "broken_level": "default",
        "font_color": "sunset",
        "font_size": 20,
        "lang": "en",
        "last_collection": 1,  # Will/should be cast to a CollectionRef.
        "raindrops_sort": "-lastUpdate",
        "raindrops_view": "list",
    },
    "email": "mail@example.com",
    "email_MD5": "1111111111",
    "files": {
        "lastCheckpoint": "2020-01-01T02:02:02.000Z",
        "size": 10000000000,
        "used": 0,
    },
    "fullName": "test user",
    "groups": [
        {
            "collections": [
                2000,
                3000,
            ],
            "hidden": False,
            "sort": 0,
            "title": "My Collections",
        },
    ],
    "password": True,
    "pro": True,
    "proExpire": "2022-01-01T01:01:01.000Z",
    "provider": "twitter",
    "registered": "2020-01-02T01:1:1.0Z",
}


def _assert_user_config(user: User) -> None:
    """Assert user configuration fields."""
    assert user.config.broken_level == BrokenLevel.default
    assert user.config.font_color == FontColor.sunset
    assert user.config.font_size == 20
    assert user.config.lang == "en"
    assert user.config.last_collection.id == 1
    assert user.config.raindrops_sort == RaindropSort.last_update_dn
    assert user.config.raindrops_view == View.list


def _assert_user_files(user: User) -> None:
    """Assert user files fields."""
    assert user.files.size == 10000000000
    assert user.files.used == 0
    assert user.files.last_checkpoint == datetime.datetime(
        2020,
        1,
        1,
        2,
        2,
        2,
        tzinfo=datetime.timezone.utc,
    )


def _assert_user_groups(user: User) -> None:
    """Assert user groups fields."""
    assert user.groups[0].hidden is False
    assert user.groups[0].sort == 0
    assert user.groups[0].title == "My Collections"
    assert list(user.groups[0].collectionids) == [2000, 3000]


def _assert_user_basic(user: User) -> None:
    """Assert basic user fields."""
    assert user.id == 1000
    assert user.email == "mail@example.com"
    assert user.email_md5 == "1111111111"
    assert user.full_name == "test user"
    assert user.password is True
    assert user.pro is True
    assert user.registered == datetime.datetime(
        2020,
        1,
        2,
        1,
        1,
        1,
        tzinfo=datetime.timezone.utc,
    )


def test_get() -> None:
    """Test that we can get/lookup the user."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"user": test_user}
        user = User.get(api)

        _assert_user_basic(user)
        _assert_user_config(user)
        _assert_user_files(user)
        _assert_user_groups(user)
