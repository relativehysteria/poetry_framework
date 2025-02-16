from template import Template as T

class Template(T):
    def generate_main_latex(self) -> str:
        # Combine everything into the final LaTeX file content and return it
        metadata = self.metadata

        return self.text.format(
            packages=metadata.latex.generate_imports(),
            chapters=self.generate_chapters()
        )

    def generate_chapters(self) -> str:
        chapter_template = r"\include{{{index}/_out.tex}}"
        chapters_code = ""

        # Generate \include chapter code
        for index, chapter in enumerate(self.metadata.chapters, start=1):
            chapters_code += chapter_template.format(index=index)
            chapters_code += "\n"

        return chapters_code
