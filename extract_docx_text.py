#!/usr/bin/env python3
"""
Script to extract text from Word documents (.docx) and save as individual text files.
"""

import os
import re
from pathlib import Path
from docx import Document
import unicodedata


def clean_filename(filename):
    """Clean filename to be safe for filesystem."""
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove extra spaces and normalize
    filename = re.sub(r"\s+", " ", filename).strip()
    return filename


def extract_text_from_docx(docx_path):
    """Extract text from a .docx file."""
    try:
        doc = Document(docx_path)
        text_content = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only add non-empty paragraphs
                text_content.append(paragraph.text.strip())

        return "\n\n".join(text_content)
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return None


def main():
    # Set up paths
    cheungmanjaap_dir = Path(
        "/Users/hongjan/Documents/book-cheungmanjaap-長文集/cheungmanjaap"
    )
    output_dir = Path(
        "/Users/hongjan/Documents/book-cheungmanjaap-長文集/extracted_texts"
    )

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Get all .docx files
    docx_files = list(cheungmanjaap_dir.glob("*.docx"))

    print(f"Found {len(docx_files)} Word documents to process...")

    processed_count = 0
    failed_count = 0

    for docx_file in docx_files:
        print(f"Processing: {docx_file.name}")

        # Extract text
        text_content = extract_text_from_docx(docx_file)

        if text_content:
            # Create clean filename
            base_name = docx_file.stem  # Remove .docx extension
            clean_name = clean_filename(base_name)
            txt_filename = f"{clean_name}.txt"

            # Save to text file
            output_path = output_dir / txt_filename
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                print(f"  ✓ Saved as: {txt_filename}")
                processed_count += 1
            except Exception as e:
                print(f"  ✗ Error saving {txt_filename}: {e}")
                failed_count += 1
        else:
            print(f"  ✗ Failed to extract text from {docx_file.name}")
            failed_count += 1

    print(f"\nProcessing complete!")
    print(f"Successfully processed: {processed_count} files")
    print(f"Failed: {failed_count} files")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
