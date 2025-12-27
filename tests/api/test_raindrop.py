"""Test all the core methods of the Raindrop API."""

from pathlib import Path

import pytest
import requests

from raindropiopy import Raindrop, RaindropType
from tests.api.conftest import vcr


@pytest.fixture
def sample_raindrop_link():
    """Fixture to return sample raindrop data."""
    return (
        "https://www.google.com/",
        {
            "excerpt": "excerpt/description text",
            "important": True,
            "tags": ["abc", "def"],
            "title": "a Title",
        },
    )


def _assert_raindrop_matches_args(raindrop: Raindrop, link: str, args: dict) -> None:
    """Assert that a raindrop matches the expected link and arguments."""
    assert raindrop is not None
    assert isinstance(raindrop, Raindrop)
    assert raindrop.id
    assert raindrop.link == link
    assert raindrop.important == args.get("important")
    assert raindrop.tags == args.get("tags")
    assert raindrop.title == args.get("title")
    assert raindrop.excerpt == args.get("excerpt")
    assert raindrop.type == RaindropType.link


@vcr.use_cassette()
def test_lifecycle_raindrop_link(api, sample_raindrop_link) -> None:
    """Test that we can roundtrip a regular/link-based raindrop, ie. create, update, get and delete."""
    # TEST: Create
    link, args = sample_raindrop_link
    raindrop = Raindrop.create_link(api, link, **args)
    _assert_raindrop_matches_args(raindrop, link, args)

    # TEST: Edit...
    title = "a NEW/EDITED Title"
    edited_raindrop = Raindrop.update(api, raindrop.id, title=title)
    assert edited_raindrop.title == title

    # TEST: Delete...
    Raindrop.delete(api, id=raindrop.id)
    with pytest.raises(requests.exceptions.HTTPError):
        Raindrop.get(api, raindrop.id)


@vcr.use_cassette()
def test_lifecycle_raindrop_file(api) -> None:
    """Test that we can roundtrip a *file-base* raindrop, ie. create, update, get and delete."""
    # TEST: Create a link using this test file as the file to upload.
    path_ = Path(__file__).parent / Path("test_raindrop.pdf")

    raindrop = Raindrop.create_file(
        api,
        path_,
        "application/pdf",
        title="A Sample Title",
        tags=["SampleTag"],
    )
    assert raindrop is not None
    assert isinstance(raindrop, Raindrop)
    assert raindrop.id
    assert raindrop.file.name == path_.name
    assert raindrop.type == RaindropType.document

    # TEST: Delete...
    Raindrop.delete(api, id=raindrop.id)
    with pytest.raises(requests.exceptions.HTTPError):
        Raindrop.get(api, raindrop.id)
