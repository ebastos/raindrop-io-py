# Feature Request: Add `note` parameter support to `Raindrop.update()`

## Summary

The `Raindrop.update()` method does not support updating the `note` field of a bookmark, even though:
1. The Raindrop API supports this field
2. The `Raindrop` model includes `note` in its schema

## Current Behavior

The `Raindrop.update()` method signature:

```python
@classmethod
def update(
    cls,
    api: API,
    id: int,
    collection: Collection | CollectionRef | int | None = None,
    cover: str | None = None,
    excerpt: str | None = None,  # ← This exists
    important: bool | None = None,
    link: str | None = None,
    media: list[dict[str, Any]] | None = None,
    order: int | None = None,
    please_parse: bool | None = False,
    tags: list[str] | None = None,
    title: str | None = None,
    # note: str | None = None,  # ← This is MISSING
) -> Raindrop:
```

The method only processes these attributes:

```python
for attr in [
    "cover",
    "excerpt",
    "important",
    "link",
    "media",
    "order",
    "tags",
    "title",
]:
```

## Expected Behavior

The `note` parameter should be supported, allowing users to update bookmark notes:

```python
Raindrop.update(
    api,
    id=bookmark_id,
    note="My personal notes about this bookmark",
    tags=["tag1", "tag2"],
)
```

## Raindrop API Reference

The [Raindrop.io API documentation](https://developer.raindrop.io/v1/raindrops/single#update-raindrop) confirms that `note` is a valid field for PUT requests to `/rest/v1/raindrop/{id}`:

| Field | Type | Description |
|-------|------|-------------|
| `note` | String | User's personal notes (supports Markdown) |
| `excerpt` | String | Description/summary (max 10,000 chars) |

These are **different fields** with different purposes:
- `excerpt`: A description or summary of the bookmark content
- `note`: The user's personal annotations/notes about the bookmark

## Proposed Fix

In `models.py`, add `note` to the `update()` method:

```python
@classmethod
def update(
    cls,
    api: API,
    id: int,
    collection: Collection | CollectionRef | int | None = None,
    cover: str | None = None,
    excerpt: str | None = None,
    important: bool | None = None,
    link: str | None = None,
    media: list[dict[str, Any]] | None = None,
    note: str | None = None,  # ← ADD THIS
    order: int | None = None,
    please_parse: bool | None = False,
    tags: list[str] | None = None,
    title: str | None = None,
) -> Raindrop:
```

And add `"note"` to the attributes list:

```python
for attr in [
    "cover",
    "excerpt",
    "important",
    "link",
    "media",
    "note",  # ← ADD THIS
    "order",
    "tags",
    "title",
]:
```

## Use Case

I'm building a bookmark organizer that uses AI to analyze bookmarks and generate:
- Tags for categorization
- A collection assignment
- **Notes** summarizing the bookmark content

Without `note` support in `update()`, I cannot save the AI-generated notes to Raindrop bookmarks.

## Environment

- raindropiopy version: (current)
- Python version: 3.12+

## Workaround Attempted

I tried making a direct API call as a workaround:

```python
from raindropiopy.models import URL

def update_note(api: API, raindrop_id: int, note: str) -> None:
    url = URL.format(path=f"raindrop/{raindrop_id}")
    api.put(url, json={"note": note})
```

However, this results in 404 errors, suggesting the URL construction or API access pattern differs from what the library uses internally.

## Related

- Raindrop model schema includes `note` field: ✅
- Raindrop API supports `note` in updates: ✅
- Library exposes `note` in `update()`: ❌
