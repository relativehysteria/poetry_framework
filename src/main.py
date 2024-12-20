#!/usr/bin/env python

from sys import argv
from pathlib import Path
from build_manager import BuildManager

if len(argv) != 2:
    print(f"Usage: {argv[0]} <collection_path>")
    print(f"Attempting current directory...")
    argv.append("./")

collection_path = Path(argv[1])
build_manager = BuildManager(collection_path)
build_manager.build()
build_manager.compile()
