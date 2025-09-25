#!/usr/bin/env python3
"""
Script to rename chapter files to use only numbers and remove Chinese characters.
"""

import os
import re
from pathlib import Path


def clean_filename(filename):
    """Clean filename to remove Chinese characters and special characters."""
    # Remove .tex extension first
    name = filename.replace(".tex", "")

    # Extract the number at the beginning
    match = re.match(r"^(\d+)", name)
    if match:
        number = match.group(1)
        return f"{number}.tex"
    else:
        # If no number found, try to extract from the pattern
        # Look for patterns like "02-" or "03-"
        match = re.match(r"^(\d+)-", name)
        if match:
            number = match.group(1)
            return f"{number}.tex"
        else:
            # Fallback: use original name but clean it
            cleaned = re.sub(r"[^\w\-\.]", "_", name)
            return f"{cleaned}.tex"


def rename_chapter_files():
    """Rename all chapter files to use only numbers."""
    chapters_dir = Path("/Users/hongjan/Documents/book-cheungmanjaap-長文集/chapters")

    # Get all .tex files
    tex_files = list(chapters_dir.glob("*.tex"))

    print(f"Found {len(tex_files)} chapter files to rename...")

    renamed_files = []

    for tex_file in tex_files:
        old_name = tex_file.name
        new_name = clean_filename(old_name)

        if old_name != new_name:
            old_path = tex_file
            new_path = tex_file.parent / new_name

            try:
                # Rename the file
                old_path.rename(new_path)
                print(f"  ✓ Renamed: {old_name} → {new_name}")
                renamed_files.append((old_name, new_name))
            except Exception as e:
                print(f"  ✗ Error renaming {old_name}: {e}")
        else:
            print(f"  - No change needed: {old_name}")

    print(f"\nRenaming complete!")
    print(f"Successfully renamed: {len(renamed_files)} files")

    return renamed_files


def update_main_tex_file(renamed_files):
    """Update the main .tex file with new chapter filenames."""
    main_tex_path = Path(
        "/Users/hongjan/Documents/book-cheungmanjaap-長文集/cheungmanjaap.tex"
    )

    try:
        # Read the main .tex file
        with open(main_tex_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Create a mapping of old names to new names
        rename_map = dict(renamed_files)

        # Update all \input{chapters/...} lines
        updated_content = content
        for old_name, new_name in rename_map.items():
            old_pattern = f"\\input{{chapters/{old_name}}}"
            new_pattern = f"\\input{{chapters/{new_name}}}"
            updated_content = updated_content.replace(old_pattern, new_pattern)

        # Write the updated content back
        with open(main_tex_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"✓ Updated main .tex file with new chapter names")

    except Exception as e:
        print(f"✗ Error updating main .tex file: {e}")


def main():
    print("Renaming chapter files to use only numbers...")

    # Rename the files
    renamed_files = rename_chapter_files()

    if renamed_files:
        # Update the main .tex file
        print("\nUpdating main .tex file...")
        update_main_tex_file(renamed_files)

    print("\nAll done!")


if __name__ == "__main__":
    main()
