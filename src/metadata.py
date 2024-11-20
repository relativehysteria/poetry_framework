# Handles YAML metadata parsing and processing
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
import yaml

# Name of the file that stores collection metadata
METADATA_FNAME = "collection_metadata.yaml"


@dataclass
class Poem:
    title: str
    edit: float


class Serializer(type(yaml.YAMLObject)):
    def __new__(cls, name, bases, dct):
        dct['yaml_tag'] = f"!{name}"
        dct['yaml_loader'] = yaml.SafeLoader
        return super().__new__(cls, name, bases, dct)


@dataclass
class LatexConfig(yaml.YAMLObject, metaclass=Serializer):
    geometry: str


@dataclass
class Chapter(yaml.YAMLObject, metaclass=Serializer):
    title: str
    epigraph: Optional[str] = field(default=None)
    poems: Optional[List[Poem]] = field(default=None)

    # Extract metadata for poems in a given chapter
    def load_poetry_metadata(self, chapter_path: Path):
        # If it's cached already, presume it's done.
        if self.poems is not None:
            return
        self.poems = []

        # Read the title of a poem from the file's initial non-blank lines
        def read_title(path: Path) -> str:
            title_lines = []
            with path.open('r') as f:
                for line in f:
                    if line.strip() == "":
                        break
                    title_lines.append(line.strip())
            return " ".join(title_lines)

        for file in sorted(chapter_path.iterdir()):
            edit = file.stat().st_mtime
            title = read_title(file)
            self.poems.append(Poem(title=title, edit=edit))


@dataclass
class Collection(yaml.YAMLObject, metaclass=Serializer):
    title: str
    latex: LatexConfig
    chapters: List[Chapter]


def load_metadata(collection_path: Path) -> Collection:
    """Load metadata from the YAML file and return a Collection object."""
    metadata_path = collection_path / METADATA_FNAME
    return yaml.safe_load(metadata_path.read_text())
