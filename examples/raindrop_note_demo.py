"""Demonstrate creating and updating a Raindrop with the 'note' parameter."""

import os
import sys

# Add the project root to the path so we can import raindropiopy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from raindropiopy import API, Raindrop

load_dotenv()


def main():
    """Demonstrate creating and updating a Raindrop with a note."""
    if not os.environ.get("RAINDROP_TOKEN"):
        print("Error: RAINDROP_TOKEN environment variable not set.")
        sys.exit(1)

    with API(os.environ["RAINDROP_TOKEN"]) as api:
        link = "https://www.google.com"
        title = "Google Search"
        note = "This is a personal note about Google."

        # 1. Create a Raindrop with a note
        print(f"Creating Raindrop: '{link}' with a note...", flush=True, end="")
        try:
            raindrop = Raindrop.create_link(api, link=link, title=title, note=note, tags=["example", "note-test"])
            print("Done.")
            print(f"Created Raindrop ID: {raindrop.id}")
            print(f"Initial Note: {raindrop.note}")
        except Exception as exc:
            print(f"\nSorry, unable to create Raindrop! {exc}")
            sys.exit(1)

        # 2. Update the note
        new_note = "This is an UPDATED personal note about Google."
        print(f"Updating note for Raindrop {raindrop.id}...", flush=True, end="")
        try:
            raindrop = Raindrop.update(api, id=raindrop.id, note=new_note)
            print("Done.")
            print(f"Updated Note: {raindrop.note}")
        except Exception as exc:
            print(f"\nSorry, unable to update Raindrop! {exc}")
            # Don't exit here, we still want to clean up

        # 3. Cleanup
        print(f"Removing Raindrop {raindrop.id}...", flush=True, end="")
        try:
            Raindrop.delete(api, id=raindrop.id)
            print("Done.")
        except Exception as exc:
            print(f"\nSorry, unable to delete Raindrop! {exc}")


if __name__ == "__main__":
    main()
