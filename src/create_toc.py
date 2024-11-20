# Handles Table of Contents generation
from datetime import datetime
from pathlib import Path
from metadata import Collection


def write_collection_readme(build_manager):
    """Generate a README file for the collection."""
    metadata = build_manager.metadata
    readme_path = build_manager.collection_path / "README.md"

    # Fill in the poem metadata for each chapter if it hasn't been done so yet
    for idx, chapter in enumerate(metadata.chapters, start=1):
        chapter_path = build_manager.collection_path / str(idx)
        chapter.load_poetry_metadata(chapter_path)

    # Determine edit time range
    edit_times = [poem.edit for ch in metadata.chapters for poem in ch.poems]
    min_date = datetime.fromtimestamp(min(edit_times)).strftime("%Y-%m-%d")
    max_date = datetime.fromtimestamp(max(edit_times)).strftime("%Y-%m-%d")

    # Write the README
    with readme_path.open("w") as file:
        file.write(f"# {metadata.title}\n\n")
        file.write(f"Started {min_date}. Finished {max_date}.\n\n")
        file.write("## Table of Contents\n\n")

        for idx, chapter in enumerate(metadata.chapters, start=1):
            pad = len(str(len(chapter.poems)))
            file.write(f"### {chapter.title}\n\n")
            for poem_idx, poem in enumerate(chapter.poems, start=1):
                poem_idx = f"{poem_idx:0{pad}d}"
                file.write(f"{poem_idx}. [{poem.title}]({idx}/{poem_idx}.txt)\n")
            file.write("\n")
