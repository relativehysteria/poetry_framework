# Manages LaTeX template processing
from pathlib import Path
from metadata import Collection

TEMPLATES_ROOT = Path(__file__).parent / "templates"
MAIN_FNAME = "main.tex"
MAIN_TEMPLATE = (TEMPLATES_ROOT / MAIN_FNAME).read_text()


def generate_main(metadata: Collection) -> str:
    chapter_template = r"\placechap{{{title}}}{{{index}}}{{{epigraph}}}"
    chapters_code = ""

    # Generate \placechap chapter code
    for index, chapter in enumerate(metadata.chapters, start=1):
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
    return MAIN_TEMPLATE.format(
        packages=metadata.latex.generate_imports(),
        title=metadata.title,
        chapters=chapters_code
    )


def write_main_template(build_manager):
    """Generate the main LaTeX file for the poetry collection."""
    metadata = build_manager.metadata
    (build_manager.build_path / MAIN_FNAME).write_text(generate_main(metadata))
