# Manages build output structure and paths
from os import system, chdir, getcwd
from contextlib import contextmanager
from pathlib import Path
from metadata import load_metadata

from create_toc import write_collection_readme
from template import format_main_template
from poetry import process_poetry_files

OUTPUT_FILENAME = "main.tex"

@contextmanager
def pushd(new_dir: Path):
    previous = getcwd()
    chdir(new_dir)
    yield
    chdir(previous)

class BuildManager:
    def __init__(self, collection_path: Path, build_path: Path, template: str):
        self.template        = template
        self.collection_path = collection_path
        self.metadata        = load_metadata(collection_path)
        self.build_path      = collection_path / build_path
        self.build_path.mkdir(parents=True, exist_ok=True)

    def get_chapter_output_path(self, chapter_index: int) -> Path:
        """Return the output path for a chapter."""
        chapter_dir = self.build_path / str(chapter_index)
        chapter_dir.mkdir(parents=True, exist_ok=True)
        return chapter_dir

    def build(self):
        """Builds everything!"""
        write_collection_readme(self)
        (self.build_path / OUTPUT_FILENAME) \
            .write_text(format_main_template(self.template, self.metadata))
        process_poetry_files(self)

    def compile(self):
        """Compiles everything!"""
        compiler = self.metadata.latex.compiler
        with pushd(self.build_path):
            system(f"{compiler} {OUTPUT_FILENAME}")
            system(f"{compiler} {OUTPUT_FILENAME}")
        pdf = (self.build_path / OUTPUT_FILENAME).with_suffix(".pdf")
        pdf.replace(pdf.parents[1] / pdf.name)
