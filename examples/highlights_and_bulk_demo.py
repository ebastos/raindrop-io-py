"""Example demonstrating Highlights and Bulk Operations features."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv

from raindropiopy import API, CollectionRef, Highlight, Raindrop

load_dotenv()


with API(os.environ["RAINDROP_TOKEN"]) as api:
    # ============================================================
    # 1. HIGHLIGHTS API DEMO
    # ============================================================
    print("=" * 60)
    print("HIGHLIGHTS API DEMO")
    print("=" * 60)

    # Get all highlights across raindrops
    print("\nFetching all highlights (limited to 5)...", flush=True, end="")
    all_highlights = Highlight.get_all(api, perpage=5)
    print("Done.")
    print(f"Found {len(all_highlights)} highlight(s) across all raindrops:")
    for h in all_highlights:
        print(f"  - '{h.text[:50]}...' (Color: {h.color})")

    # Create a test raindrop to demonstrate highlights management
    link = "https://example.com/highlights-test"
    title = "Highlights Test Raindrop"
    print(f"\nCreating test raindrop: '{title}'...", flush=True, end="")
    raindrop = Raindrop.create_link(api, link=link, title=title)
    print(f"Done, id={raindrop.id}")

    # Add a highlight to the raindrop
    print("Adding a highlight to the raindrop...", flush=True, end="")
    raindrop = Raindrop.add_highlights(
        api,
        raindrop.id,
        [{"text": "This is a new highlight", "color": "yellow"}],
    )
    print("Done.")

    # Update the highlight with a note
    if raindrop.highlights and len(raindrop.highlights) > 0:
        h_id = raindrop.highlights[0].id
        print(f"Updating highlight {h_id} with a note...", flush=True, end="")
        Raindrop.update_highlight(
            api,
            raindrop.id,
            {"_id": h_id, "note": "Added a note to the highlight"},
        )
        print("Done.")

        # Remove the highlight
        print("Removing the highlight...", flush=True, end="")
        Raindrop.remove_highlight(api, raindrop.id, h_id)
        print("Done.")

    # Clean up the test raindrop
    print("Removing test raindrop...", flush=True, end="")
    Raindrop.delete(api, raindrop.id)
    print("Done.")

    # ============================================================
    # 2. BULK OPERATIONS DEMO
    # ============================================================
    print("\n" + "=" * 60)
    print("BULK OPERATIONS DEMO")
    print("=" * 60)

    # Create multiple raindrops at once
    print("\nCreating multiple raindrops in bulk...", flush=True, end="")
    new_items = [
        {"link": "https://example.com/bulk-1", "title": "Bulk Demo Item 1"},
        {"link": "https://example.com/bulk-2", "title": "Bulk Demo Item 2"},
        {"link": "https://example.com/bulk-3", "title": "Bulk Demo Item 3"},
    ]
    created = Raindrop.create_many(api, new_items)
    print("Done.")
    print(f"Created {len(created)} raindrop(s):")
    for item in created:
        print(f"  - id={item.id}, title='{item.title}'")

    # Update multiple raindrops at once
    bulk_ids = [item.id for item in created]
    print(f"\nUpdating tags for {len(bulk_ids)} raindrop(s)...", flush=True, end="")
    modified = Raindrop.update_many(
        api,
        CollectionRef.Unsorted.id,
        ids=bulk_ids,
        tags=["bulk-demo", "example"],
    )
    print("Done.")
    print(f"Modified {modified} raindrop(s).")

    # Delete multiple raindrops at once
    print(f"Deleting {len(bulk_ids)} raindrop(s) in bulk...", flush=True, end="")
    Raindrop.delete_many(api, CollectionRef.Unsorted.id, ids=bulk_ids)
    print("Done.")

    print("\n" + "=" * 60)
    print("All demonstrations complete!")
    print("=" * 60)
