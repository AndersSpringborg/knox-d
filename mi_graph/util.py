# !/usr/bin/python3
import os
import sys
from argparse import ArgumentParser

import spacy
from spacy.cli import download

from loader.file_loader import load_json
from mi_graph import api, pipeline, __version__
from resources.error import error

MODE_FILE = 'file'
MODE_SERVE = 'flask'


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.prog = "mi-graph"

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument("mode", choices=[MODE_FILE, MODE_SERVE],
                        help='Choose if you want to process a file, or run the program as a rest api')
    parser.add_argument("--file", "-f", help="Please indicate the json file you want to process.",
                        metavar='')  # makes help prettier

    parser.add_argument("--visualisation", action="store_true", default=False,
                        help="This option visualizes the graph with plotly, "
                             "after the script has run")
    return parser


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

    args = parser.parse_args()

    ensure_models_installed()

    if args.mode == MODE_SERVE:
        api.start_api()
        sys.exit(1)

    # we know it is a file input
    if not args.file:
        error("Specify a file, you want to parse pls")
        parser.print_help()
        sys.exit(0)

    # Make path of the input file real and absolute. Ensures cross platform compatibility
    path_to_file = make_path(args.file)

    print(path_to_file)
    input_file = open(path_to_file, encoding='utf-16')
    manual = load_json(input_file)

    pipeline.run(manual, visualize=args.visualisation)
