#!/usr/bin/env python

from os import listdir
from os.path import getmtime
from pathlib import Path
from typing import List
from yaml import safe_load
from datetime import datetime
from . import metadata

# Extract metadata for poems in a chapter.
def get_chapter_poem_metadata(path: Path) -> List[metadata.Poem]:
    poems = []
    for fname in sorted(path.iterdir()):
        edit = getmtime(fname)
        title = read_title(fname)
        poems.append(metadata.Poem(title=title, edit=edit, stanzas=None))
    return poems


# Read the title of a poem from the file's initial non-blank lines
def read_title(path: Path) -> str:
    title_lines = []
    with path.open('r') as f:
        for line in f:
            if line.strip() == "":
                break
            title_lines.append(line.strip())
    return " ".join(title_lines)


# Generate a README file for a poetry collection
def write_collection_readme(collection_path: Path):
    metadata_path = collection_path / metadata.METADATA_FNAME

    # Load collection metadata
    with metadata_path.open('r') as f:
        meta = safe_load(f)

    # Fill in the poem metedata for each chapter
    for idx, chapter in enumerate(meta.chapters, start=1):
        chapter_path = collection_path / str(idx)
        poems = get_chapter_poem_metadata(chapter_path)
        chapter.poems = get_chapter_poem_metadata(chapter_path)

    # Determine edit time range (creation and finish)
    edit_times = [poem.edit for ch in meta.chapters for poem in ch.poems]
    min_date = datetime.fromtimestamp(min(edit_times)).strftime("%Y-%m-%d")
    max_date = datetime.fromtimestamp(max(edit_times)).strftime("%Y-%m-%d")

    # Write the README
    readme_path = collection_path / "README.md"
    with readme_path.open('w') as f:
        f.write(f"# {meta.title}\n\n")
        f.write(f"Started {min_date}. Finished {max_date}.\n\n")
        f.write("## Table of Contents\n\n")

        for ch_idx, chapter in enumerate(meta.chapters, start=1):
            # Write out the chapter name
            f.write(f"### {chapter.title}\n\n")

            # Determine the width for zero-padded numbering
            n_digits = len(str(len(chapter.poems)))

            # Write out the poems
            for p_idx, poem in enumerate(chapter.poems, start=1):
                p_idx = f"{p_idx:0{n_digits}}"
                f.write(f"{p_idx}. [{poem.title}]({ch_idx}/{p_idx}.txt)\n")
            f.write("\n")
