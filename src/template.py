#!/usr/bin/env python

from typing import List
from pathlib import Path
from yaml import safe_load
from os import path
from . import metadata

# Root path to static templates
TEMPLATES_ROOT: Path = path.dirname(path.abspath(__file__)) / Path("templates")

# Name of the main poetry LaTeX template and output file
MAIN_LATEX_FNAME: str = "main.tex"

# The string data of the main poetry LaTeX template
with (TEMPLATES_ROOT / MAIN_LATEX_FNAME).open('r') as f:
    DEFAULT_LATEX_TEMPLATE = f.read()


# Generate the main LaTeX file for a collection
def generate_main_latex(meta: metadata.Collection) -> str:
    chapter_template = r"\placechap{{{title}}}{{{epigraph}}}{{{index}}}"
    chapters_code = ""

    # Generate \placechap chapter code
    for index, chapter in enumerate(meta.chapters, start=1):
        title    = chapter.title.strip()

        epigraph = chapter.epigraph
        epigraph = "" if epigraph is None else epigraph
        epigraph = epigraph.strip() \
                .replace('\n\n', '\\\\ \n') \
                .replace('\n', '\\\\\n')

        chapters_code += "\n"
        chapters_code += chapter_template.format(
            title=title,
            epigraph=epigraph,
            index=index
        )
        chapters_code += "\n"

    # Combine everything into the final LaTeX file content and return it
    return DEFAULT_LATEX_TEMPLATE.format(
        geometry=meta.latex.geometry,
        title=meta.title,
        chapters=chapters_code
    )


def write_main_template(collection_path: Path):
    metadata_path   = collection_path / metadata.METADATA_FNAME
    build_path      = collection_path / metadata.BUILD_PATH
    build_path.mkdir(parents=False, exist_ok=True)

    # Load the collection metadata
    with metadata_path.open('r') as f:
        meta = safe_load(f)

    # Generate the main latex code from the main template
    latex_code = generate_main_latex(meta)

    # Write the final LaTeX code to a file
    with (build_path / MAIN_LATEX_FNAME).open('w') as f:
        f.write(latex_code)
