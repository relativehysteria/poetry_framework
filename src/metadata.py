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


type LatexPackage = dict[str, Optional[str]]

@dataclass
class LatexConfig(yaml.YAMLObject, metaclass=Serializer):
    imports: Optional[LatexPackage] = field(default_factory=dict)

    def validate(self):
        """Validates the imported packages"""
        # Validate package names are strings
        if not all(isinstance(pkg, str) for pkg in self.imports):
            raise ValueError("All package names must be strings.")
        if not all(isinstance(opt, (str, type(None))) for opt in
                   self.imports.values()):
            raise ValueError("Package options must be strings or None.")

    def import_required(self):
        """Imports required packages if they weren't specified"""
        # Make sure important packages are always defined
        important = {
            "fancyhdr": None,
            "geometry": "a4paper",
            "poemscol": None,
            "fontenc": "T1",
            "inputenc": "utf8",
        }
        for pkg, opt in important.items():
            self.imports.setdefault(pkg, opt)


    def generate_imports(self) -> str:
        """Generate LaTeX import statements."""
        lines = []
        for package, options in self.imports.items():
            if options:
                lines.append(f"\\usepackage[{options}]{{{package}}}")
            else:
                lines.append(f"\\usepackage{{{package}}}")
        return "\n".join(lines)


@dataclass
class Chapter(yaml.YAMLObject, metaclass=Serializer):
    title: str
    epigraph: Optional[str] = field(default=None)

    # Extract metadata for poems in a given chapter
    def load_poetry_metadata(self, chapter_path: Path):
        # If it's cached already, presume it's done.
        if "poems" in dir(self):
            return

        # Inject the poems attribute. This is not specified during
        # initialization so people can't define it in the yaml. This was a bug,
        # oops :D
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
    chapters: List[Chapter]
    header: Optional[str] = field(default=None)
    latex: Optional[LatexConfig] = field(default=None)


def load_metadata(collection_path: Path) -> Collection:
    """Load metadata from the YAML file and return a Collection object."""
    metadata_path = collection_path / METADATA_FNAME
    collection = yaml.safe_load(metadata_path.read_text())

    # I literally don't know how to do this otherwise. I just don't know how
    # `default_factory` works because when i use it, it just doesn't get
    # called when latex isn't specified. :(
    if collection.latex is None:
        collection.latex = LatexConfig()
    collection.latex.validate()
    collection.latex.import_required()

    return collection
