#!/usr/bin/env python

from pathlib import Path
from os.path import getmtime
from dataclasses import dataclass, field
from typing import List, Optional
import yaml

# Root path to all poetry collections
COLLECTION_ROOT: Path = Path("collections")

# Path to the build directory of each collection.
# Basically `COLLECTION_ROOT / <collection> / BUILD_PATH`
BUILD_PATH: Path = Path("build")

# Name of the file that stores collection metadata
METADATA_FNAME: str = "collection_metadata.yaml"


@dataclass
class Stanza:
    # Verses content for this stanza
    verses: List[str]


@dataclass
class Poem:
    # Title of the poem
    title: str

    # Last edit time of the poem
    edit: float

    # Stanzas content for this poem
    stanzas: Optional[List[Stanza]] = field(default=None)


class Serializer(type(yaml.YAMLObject)):
    def __new__(cls, name, bases, dct):
        dct['yaml_tag'] = f"!{name}"
        dct['yaml_loader'] = yaml.SafeLoader
        return super().__new__(cls, name, bases, dct)

@dataclass
class LatexConfig(yaml.YAMLObject, metaclass=Serializer):
    # LaTeX geometry configuration (e.g., paper size and margins)
    geometry: str


@dataclass
class Chapter(yaml.YAMLObject, metaclass=Serializer):
    # Chapter title
    title: str

    # Chapter epigraph
    epigraph: Optional[str] = field(default=None)

    # List of poems in this chapter
    poems: Optional[List[Poem]] = field(default=None)


@dataclass
class Collection(yaml.YAMLObject, metaclass=Serializer):
    # Collection title
    title: str

    # LaTeX configuration for the collection
    latex: LatexConfig

    # List of chapters in the collection
    chapters: List[Chapter]
