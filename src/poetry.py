# Handles poetry content generation
from pathlib import Path
from metadata import Collection


def needs_regeneration(input_file: Path, output_file: Path) -> bool:
    """Check if the output file needs to be regenerated."""
    if not output_file.exists():
        return True
    return input_file.stat().st_mtime > output_file.stat().st_mtime


def regenerate_poem(input_file: Path, output_file: Path):
    """Regenerate a LaTeX file for a poem."""
    # Placeholder for actual processing
    output_file.write_text(input_file.read_text())


def process_poetry_files(build_manager):
    """Generate LaTeX files for poems in each chapter."""
    metadata = build_manager.metadata
    for idx, chapter in enumerate(metadata.chapters, start=1):
        chapter_input_path = build_manager.collection_path / str(idx)
        chapter_output_path = build_manager.get_chapter_output_path(idx)

        for inp_file in sorted(chapter_input_path.iterdir()):
            out_file = chapter_output_path / inp_file.with_suffix(".tex").name
            if needs_regeneration(inp_file, out_file):
                regenerate_poem(inp_file, out_file)
