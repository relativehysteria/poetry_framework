#!/usr/bin/env python

from sys import argv
from pathlib import Path
from metadata import load_metadata
from create_toc import write_collection_readme
from template import write_main_template
from poetry import process_poetry_files
from build_manager import BuildManager

if len(argv) != 2:
    print(f"Usage: {argv[0]} <collection_path>")
    exit(1)

collection_path = Path(argv[1])
build_manager = BuildManager(collection_path)
build_manager.build()
