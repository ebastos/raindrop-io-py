"""Example of using the new Highlights and Bulk Operations features."""

import os
from dotenv import load_dotenv
from raindropiopy import API, Raindrop, Highlight, CollectionRef

load_dotenv()


def demo():
    """Demonstrate the Highlights and Bulk Operations API features."""
    token = os.environ.get("RAINDROP_TOKEN")
    if not token:
        print("Please set RAINDROP_TOKEN in your .env file.")
        return

    with API(token) as api:
        # 1. Highlights Demo
        print("--- Highlights Demo ---")
        all_highlights = Highlight.get_all(api, perpage=5)
        print(f"Found {len(all_highlights)} highlights across all raindrops.")
        for h in all_highlights:
            print(f"- {h.text} (Color: {h.color})")

        # Create a test link to manage highlights
        link = "https://example.com/highlights-test"
        print(f"\nCreating test raindrop: {link}")
        raindrop = Raindrop.create_link(api, link=link, title="Highlights Test")

        print("Adding a highlight...")
        raindrop = Raindrop.add_highlights(api, raindrop.id, [{"text": "This is a new highlight", "color": "yellow"}])

        if raindrop.highlights:
            h_id = raindrop.highlights[0].id
            print(f"Updating highlight {h_id}...")
            Raindrop.update_highlight(api, raindrop.id, {"_id": h_id, "note": "Added a note to the highlight"})

            print("Removing highlight...")
            Raindrop.remove_highlight(api, raindrop.id, h_id)

        # 2. Bulk Operations Demo
        print("\n--- Bulk Operations Demo ---")
        print("Creating multiple raindrops...")
        new_items = [
            {"link": "https://example.com/bulk-1", "title": "Bulk 1"},
            {"link": "https://example.com/bulk-2", "title": "Bulk 2"},
        ]
        created = Raindrop.create_many(api, new_items)
        print(f"Created {len(created)} raindrops.")

        bulk_ids = [item.id for item in created]
        print(f"Updating tags for {len(bulk_ids)} raindrops...")
        modified = Raindrop.update_many(api, CollectionRef.Unsorted.id, ids=bulk_ids, tags=["bulk-demo"])
        print(f"Modified {modified} raindrops.")

        print("Cleaning up (deleting bulk raindrops)...")
        Raindrop.delete_many(api, CollectionRef.Unsorted.id, ids=bulk_ids)

        # Clean up test raindrop
        Raindrop.delete(api, raindrop.id)
        print("\nDemo complete.")


if __name__ == "__main__":
    demo()
