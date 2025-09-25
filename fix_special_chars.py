#!/usr/bin/env python3
"""
Script to fix special characters in LaTeX chapter files.
"""

import os
import re
from pathlib import Path


def fix_special_chars(file_path):
    """Fix special characters in a LaTeX file."""
    try:
        # Read the file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix special characters
        # Escape # characters (but not if they're already escaped)
        content = re.sub(r"(?<!\\)#", r"\\#", content)
        # Escape _ characters (but not if they're already escaped)
        content = re.sub(r"(?<!\\)_", r"\\_", content)

        # Write back the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    chapters_dir = Path("/Users/hongjan/Documents/book-cheungmanjaap-長文集/chapters")

    # Get all .tex files
    tex_files = list(chapters_dir.glob("*.tex"))

    print(f"Fixing special characters in {len(tex_files)} chapter files...")

    fixed_count = 0
    for tex_file in tex_files:
        if fix_special_chars(tex_file):
            print(f"  ✓ Fixed: {tex_file.name}")
            fixed_count += 1
        else:
            print(f"  ✗ Failed: {tex_file.name}")

    print(f"\nFixed special characters in {fixed_count} files")


if __name__ == "__main__":
    main()
