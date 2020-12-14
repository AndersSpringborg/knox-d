#!/usr/bin/python3
import os
import json
import sys
from argparse import ArgumentParser

import spacy
from spacy.cli import download

from loader.file_loader import load_json
from mi_graph import api, pipeline
from resources.random_number_gen import random_percentage_count


def setup_parser(_parser: ArgumentParser) -> ArgumentParser:
    _parser.prog = "mi-graph"

    _parser.add_argument("file", help="Please indicate the json file you want to process.")

    _parser.add_argument("--visualisation", "-v", action="store_true", default=False,
                         help="This option visualizes the graph with plotly, "
                              "after the script has run")

    _parser.add_argument("--serve", "-s", action="store_true",
                         help="This option runs mi_graph as an API")

    return _parser


def make_path(path):
    """ Returns a uniformly real, absolute filesystem path."""

    # ~/directory -> /home/user/directory
    path = os.path.expanduser(path)
    # A/.//B -> A/B
    path = os.path.normpath(path)
    # Resolve symbolic links
    path = os.path.realpath(path)
    # Ensure path is absolute
    path = os.path.abspath(path)

    return path


def ensure_models_installed():
    okcyan = '\033[96m'
    endc = '\033[0m'

    if not spacy.util.is_package("en_core_web_sm"):
        print(f"{okcyan}Missing models. Install spacy en-core-web-sm model{endc}")
        download("en_core_web_sm")


def cli():
    # Setup the parser and parse the arguments
    parser = setup_parser(ArgumentParser())
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        raise

    ensure_models_installed()

    if args.serve:
        api.start_api()
        sys.exit(1)

    # Make path of the input file real and absolute. Ensures cross platform compatibility
    path_to_file = make_path(args.file)

    input_file = open(path_to_file)

    manual = load_json(input_file)

    pipeline.run(manual, visualize=args.visualisation)
