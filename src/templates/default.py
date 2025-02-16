from template import Template as T

class Template(T):
    def generate_main_latex(self) -> str:
        # Combine everything into the final LaTeX file content and return it
        metadata = self.metadata

        return self.text.format(
            packages=metadata.latex.generate_imports(),
            title=metadata.title,
            header=metadata.header if metadata.header else metadata.title,
            chapters=self.generate_chapters()
        )

    def generate_chapters(self) -> str:
        chapter_template = r"\placechap{{{title}}}{{{index}}}{{{epigraph}}}"
        chapters_code = ""

        # Generate \placechap chapter code
        for index, chapter in enumerate(self.metadata.chapters, start=1):
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

        return chapters_code
