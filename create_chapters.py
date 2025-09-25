#!/usr/bin/env python3
"""
Script to convert extracted text files into LaTeX chapter files.
"""

import os
import re
from pathlib import Path


def clean_chapter_title(filename):
    """Clean filename to create a proper chapter title."""
    # Remove .txt extension
    title = filename.replace(".txt", "")

    # Remove common prefixes and clean up
    title = re.sub(r"^\[.*?\]\s*", "", title)  # Remove [長文] etc.
    title = re.sub(r"^\(.*?\)\s*", "", title)  # Remove (長文慎入) etc.
    title = title.strip()

    return title


def create_chapter_file(text_file_path, output_dir, chapter_num):
    """Create a LaTeX chapter file from a text file."""
    try:
        # Read the text content
        with open(text_file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"  ⚠️  Skipping empty file: {text_file_path.name}")
            return None

        # Create chapter title from filename
        chapter_title = clean_chapter_title(text_file_path.stem)

        # Create LaTeX content
        latex_content = f"""\\chapter{{{chapter_title}}}

{content}

"""

        # Create output filename
        output_filename = f"{chapter_num:02d}-{text_file_path.stem}.tex"
        output_path = output_dir / output_filename

        # Write the LaTeX file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(latex_content)

        return output_filename

    except Exception as e:
        print(f"  ✗ Error processing {text_file_path.name}: {e}")
        return None


def main():
    # Set up paths
    extracted_texts_dir = Path(
        "/Users/hongjan/Documents/book-cheungmanjaap-長文集/extracted_texts"
    )
    chapters_dir = Path("/Users/hongjan/Documents/book-cheungmanjaap-長文集/chapters")

    # Get all text files, sorted by name
    text_files = sorted(list(extracted_texts_dir.glob("*.txt")))

    print(f"Found {len(text_files)} text files to convert to chapters...")

    # Start chapter numbering from 2 (since 0-sample.tex and 1-stories.tex already exist)
    chapter_num = 2
    created_files = []

    for text_file in text_files:
        print(f"Processing: {text_file.name}")

        output_filename = create_chapter_file(text_file, chapters_dir, chapter_num)

        if output_filename:
            print(f"  ✓ Created: {output_filename}")
            created_files.append(output_filename)
            chapter_num += 1
        else:
            print(f"  ✗ Failed to create chapter from {text_file.name}")

    print(f"\nChapter creation complete!")
    print(f"Successfully created: {len(created_files)} chapter files")
    print(f"Chapter files created:")
    for filename in created_files:
        print(f"  - {filename}")

    # Generate the input statements for the main .tex file
    print(f"\nAdd these lines to your main .tex file after the existing chapters:")
    for filename in created_files:
        print(f"\\input{{chapters/{filename}}}")


if __name__ == "__main__":
    main()
