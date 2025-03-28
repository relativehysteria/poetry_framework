# Manages LaTeX template processing
import importlib
from os import listdir
from pathlib import Path
from metadata import Collection

TEMPLATES_ROOT = Path(__file__).parent / "templates"

def format_main_template(template: str, metadata: Collection) -> str:
    # Create a Template object using the selected template module
    module   = importlib.import_module(f"templates.{template}")
    template = module.Template(TEMPLATES_ROOT / f"{template}.tex", metadata)

    # Generate the main latex file using this template
    template.inject_preamble()
    return template.generate_main_latex()


class Template:
    def __init__(self, template_path: Path, metadata: Collection):
        self.metadata = metadata
        self.path     = template_path
        self.text     = template_path.read_text()

    def generate_main_latex(self) -> str:
        raise NotImplementedError

    def inject_preamble(self):
        begin_doc = r"\begin{{document}}"
        preamble = self.metadata.latex.preamble
        preamble = preamble.replace("{", "{{").replace("}", "}}")

        self.text = self.text.replace(begin_doc, f"{preamble}\n{begin_doc}")


def get_templates():
    """Returns a list of .tex template files."""
    return [name[:-len(".tex")] for name in listdir(TEMPLATES_ROOT)
            if name.endswith(".tex")]
