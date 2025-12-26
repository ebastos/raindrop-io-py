"""Test the Tag API."""

from unittest.mock import patch

from raindropiopy import API, Tag

TAG = {"_id": "a Sample Tag", "count": 1}


def test_get() -> None:
    """Test that we can lookup a tag."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"items": [TAG]}

        tags = Tag.get(api)

        assert len(tags) == 1

        tag = tags[0]
        assert tag.tag == "a Sample Tag"
        assert tag.count == 1


def test_delete() -> None:
    """Test that we can delete a tag."""
    api = API("dummy")
    tags = ["tag1", "tag2"]
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        Tag.delete(api, tags)
        assert m.call_args[0] == ("DELETE", "https://api.raindrop.io/rest/v1/tags")
        import json

        assert json.loads(m.call_args[1]["data"]) == {"tags": tags}
