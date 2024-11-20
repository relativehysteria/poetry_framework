#!/usr/bin/env python

from pathlib import Path
from src.create_toc import write_collection_readme
from src.template import write_main_template

collection_path = Path("example_collection")
write_collection_readme(collection_path)
write_main_template(collection_path)
