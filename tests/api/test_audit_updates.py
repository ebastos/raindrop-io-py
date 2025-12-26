"""Test the Highlights and Bulk Operations API updates."""

import json
import pytest
from unittest.mock import patch
from raindropiopy import API, Raindrop, Highlight, Collection

highlight = {
    "_id": "62388e9e48b63606f41e44a6",
    "text": "Orion is the new WebKit-based browser for Mac",
    "note": "Trully native macOS app",
    "color": "red",
    "created": "2022-03-21T14:41:34.059Z",
    "raindropRef": 2000,
    "tags": ["tag1", "tag2"],
}

raindrop_with_highlights = {"_id": 2000, "title": "Example Raindrop", "highlights": [highlight]}


def test_highlight_get_all() -> None:
    """Test Highlight.get_all returns highlights correctly."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"items": [highlight]}
        found = Highlight.get_all(api)
        assert len(found) == 1
        assert found[0].id == highlight["_id"]
        assert found[0].text == highlight["text"]
        assert found[0].raindrop_ref == highlight["raindropRef"]


def test_highlight_get_for_collection() -> None:
    """Test Highlight.get_for_collection uses correct URL."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"items": [highlight]}
        found = Highlight.get_for_collection(api, 123)
        assert m.call_args[0][1] == "https://api.raindrop.io/rest/v1/highlights/123"
        assert len(found) == 1


def test_raindrop_highlights_management() -> None:
    """Test Raindrop highlight add and remove operations."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"item": raindrop_with_highlights}

        # Test add_highlights
        Raindrop.add_highlights(api, 2000, [{"text": "new"}])
        assert json.loads(m.call_args[1]["data"]) == {"highlights": [{"text": "new"}]}

        # Test remove_highlight
        Raindrop.remove_highlight(api, 2000, "62388e9e48b63606f41e44a6")
        assert json.loads(m.call_args[1]["data"]) == {"highlights": [{"_id": "62388e9e48b63606f41e44a6", "text": ""}]}


def test_raindrop_bulk_operations() -> None:
    """Test Raindrop bulk create, update, and delete operations."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        # Test create_many
        m.return_value.json.return_value = {"items": [raindrop_with_highlights]}
        items = Raindrop.create_many(api, [{"link": "https://a.com"}, {"link": "https://b.com"}])
        assert len(items) == 1
        assert m.call_args[0][0] == "POST"
        assert "raindrops" in m.call_args[0][1]

        # Test update_many
        m.return_value.json.return_value = {"modified": 5}
        modified = Raindrop.update_many(api, 0, ids=[1, 2], tags=["new"])
        assert modified == 5
        assert m.call_args[0][0] == "PUT"
        assert json.loads(m.call_args[1]["data"]) == {"ids": [1, 2], "tags": ["new"]}

        # Test delete_many
        m.return_value.json.return_value = {"modified": 3}
        modified = Raindrop.delete_many(api, 0, ids=[1, 2])
        assert modified == 3
        assert m.call_args[0][0] == "DELETE"


def test_collection_bulk_operations() -> None:
    """Test Collection merge, clean, and reorder operations."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        # Test merge
        m.return_value.json.return_value = {"result": True}
        Collection.merge(api, ids=[1, 2], to_id=3)
        assert json.loads(m.call_args[1]["data"]) == {"ids": [1, 2], "to": 3}

        # Test clean
        Collection.clean(api)
        assert "clean" in m.call_args[0][1]

        # Test reorder_all
        Collection.reorder_all(api, sort="-count")
        assert json.loads(m.call_args[1]["data"]) == {"sort": "-count"}


def test_update_highlight() -> None:
    """Test Raindrop.update_highlight method."""
    api = API("dummy")
    with patch("raindropiopy.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"item": raindrop_with_highlights}
        Raindrop.update_highlight(api, 2000, {"_id": "62388e9e48b63606f41e44a6", "note": "Updated note"})
        assert json.loads(m.call_args[1]["data"]) == {
            "highlights": [{"_id": "62388e9e48b63606f41e44a6", "note": "Updated note"}]
        }


def test_create_many_item_limit() -> None:
    """Test that create_many raises ValueError for more than 100 items."""
    api = API("dummy")
    items = [{"link": f"https://example.com/{i}"} for i in range(101)]
    with pytest.raises(ValueError, match="Maximum 100 items allowed"):
        Raindrop.create_many(api, items)


def test_update_many_requires_filter() -> None:
    """Test that update_many raises ValueError without ids or search."""
    api = API("dummy")
    with pytest.raises(ValueError, match="At least one of 'ids' or 'search' must be provided"):
        Raindrop.update_many(api, 0, tags=["new"])


def test_delete_many_requires_filter() -> None:
    """Test that delete_many raises ValueError without ids or search."""
    api = API("dummy")
    with pytest.raises(ValueError, match="At least one of 'ids' or 'search' must be provided"):
        Raindrop.delete_many(api, 0)
