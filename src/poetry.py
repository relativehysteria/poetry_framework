# Handles poetry content generation
from pathlib import Path
from metadata import Collection
from typing import List
import re


def needs_regeneration(input_file: Path, output_file: Path) -> bool:
    """Check if the output file needs to be regenerated."""
    if not output_file.exists():
        return True
    return input_file.stat().st_mtime > output_file.stat().st_mtime


def regenerate_poem(input_file: Path) -> str:
    """Regenerate a LaTeX file for a poem."""
    splits = input_file.read_text().rstrip().split("\n\n")
    title = (splits[0] if splits[0] else "(Untitled)").replace("&", "\\&")
    stanzas = [i.split("\n") for i in splits[1:]]

    # Correct the quotes
    stanzas = correct_quotes(stanzas)

    # Correct special characters if any
    stanzas = correct_specials(stanzas)

    # \testsc the first word of the poem.
    stanzas[0][0] = textsc_first(stanzas[0][0])

    # Generate the LaTeX
    poem  = f"\\poemtitle{{{title}}}\n\n"
    poem += "\\begin{poem}"
    for stanza in stanzas:
        poem += "\n\\begin{stanza}\n"
        for verse in stanza:
            poem += f"{verse}\\verseline\n"
        poem  = poem[:-len("\\verseline\n")]
        poem += "\n\\end{stanza}\n"
    poem += "\\end{poem}"

    # Don't strip whitespace
    poem = re.sub(r'  +', lambda match: '~' * len(match.group()), poem)
    poem = re.sub(r'^ ', '~', poem, flags=re.MULTILINE)

    return poem


def correct_specials(stanzas: List[List[str]]) -> List[List[str]]:
    """Escapes special characters"""
    for stanza in stanzas:
        for (idx, line) in enumerate(stanza):
            stanza[idx] = line.replace("&", "\\&")

    return stanzas


def correct_quotes(stanzas: List[List[str]]) -> List[List[str]]:
    """Replaces opening quotes with `` and ''; keeps ending quotes."""
    in_quote = False
    for stanza in stanzas:
        for i, line in enumerate(stanza):
            new_line = []
            idx = 0
            while idx < len(line):
                char = line[idx]

                # Double quotes
                if char == '"':
                    if in_quote:
                        new_line.append("''")
                        in_quote = False
                    else:
                        new_line.append("``")
                        in_quote = True

                # Single quotes, apostrophe etc
                elif char == "'":
                    if idx == 0 or new_line[idx-1].isspace():
                        new_line.append("`")
                    else:
                        new_line.append("'")

                else:
                    new_line.append(char)
                idx += 1
            stanza[i] = "".join(new_line)

    return stanzas


def textsc_first(verse: str) -> str:
    r"""Applies \textsc to the first word of a verse, preserving whitespace."""
    verse = verse.split(' ')

    if len(verse) == 0:
        return ""

    # Some poems indent their very first word with spaces.
    # Find the first non-space word and \textsc{} it.
    # If the very first line is empty for some reason,
    # just return from the function
    idx_word = next(x for x in enumerate(verse) if x[1] != '')
    if idx_word is None:
        return ""

    ret  = ' ' * idx_word[0] + f"\\textsc{{{idx_word[1].strip()}}}"
    if idx_word[1][-1] == '\n':
        ret += '\n'
    else:
        ret += ' '
    ret += ' '.join(verse[idx_word[0]+1:])
    return ret


def process_poetry_files(build_manager):
    """Generate LaTeX files for poems in each chapter."""
    metadata = build_manager.metadata
    for idx, chapter in enumerate(metadata.chapters, start=1):
        chapter_input_path = build_manager.collection_path / str(idx)
        chapter_output_path = build_manager.get_chapter_output_path(idx)

        # All .tex files are appended to this file at the end such that it can
        # be included in the main LaTeX file
        chapter_out_file = chapter_output_path / "_out.tex"
        with chapter_out_file.open('w') as _:
            pass

        # Regenerate all files that need regeneration and put all generated .tex
        # files into a single includable out_file
        for inp_file in sorted(chapter_input_path.iterdir()):
            out_file = chapter_output_path / inp_file.with_suffix(".tex").name
            output = None
            if needs_regeneration(inp_file, out_file):
                output = regenerate_poem(inp_file)
                out_file.write_text(output)

            # Append the output to the chapter out_file
            output  = output if output else out_file.read_text()
            output += "\n\n\\newpage %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
            with chapter_out_file.open('a') as f:
                f.write(output)
