#!/usr/bin/env python

from pathlib import Path
from build_manager import BuildManager
from template import get_templates
from argparse import ArgumentParser

templates = get_templates()

parser = ArgumentParser(prog="poemgen",
                        description="poetry typesetting util")
parser.add_argument("-c", "--collection_directory", default="./",
    help="Path to the poetry collection directory")
parser.add_argument("-b", "--build-directory", type=str, default="build",
    help="The directory where build files (such as .tex files) will be saved")
parser.add_argument("-t", "--template", type=str, choices=templates,
    default="default" if "default" in templates else templates[0],
    help="The main .tex file template to be used")

args = parser.parse_args()

build_manager = BuildManager(
        Path(args.collection_directory),
        Path(args.build_directory),
        args.template)

build_manager.build()
build_manager.compile()
