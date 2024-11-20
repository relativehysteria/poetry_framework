# Manages build output structure and paths
from pathlib import Path
from metadata import load_metadata

from create_toc import write_collection_readme
from template import write_main_template
from poetry import process_poetry_files


class BuildManager:
    BUILD_PATH = "build"

    def __init__(self, collection_path: Path):
        self.collection_path = collection_path
        self.metadata        = load_metadata(collection_path)
        self.build_path      = collection_path / self.BUILD_PATH
        self.build_path.mkdir(parents=True, exist_ok=True)

    def get_chapter_output_path(self, chapter_index: int) -> Path:
        """Return the output path for a chapter."""
        chapter_dir = self.build_path / str(chapter_index)
        chapter_dir.mkdir(parents=True, exist_ok=True)
        return chapter_dir

    def build(self):
        """Builds everything!"""
        write_collection_readme(self)
        write_main_template(self)
        process_poetry_files(self)
