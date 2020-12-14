#!/usr/bin/python3
import os
from argparse import ArgumentParser

import spacy
from spacy.cli import download
from loader.file_loader import load_json
from preprocess.cleaner_imp import CleanerImp
from word_embedding.spacy_model import SpacyModel
from mi_graph.knowledge_graph import KnowledgeGraph
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from resources.json_wrapper import Content
from resources.random_number_gen import random_percentage_count


def setup_parser(_parser: ArgumentParser) -> ArgumentParser:

    _parser.prog = "mi-graph"

    _parser.add_argument("file", help="Please indicate the json file you want to process.")

    _parser.add_argument("--visualisation", "-v", action="store_true", default=False,
                         help="This option visualizes the graph with plotly, "
                              "after the script has run")

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


def extract_all_text_from_paragraphs(data: Content):
    text: str = ''
    for sec in data.sections:
        text += sec.paragraph.text
    return text


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

    # Make path of the input file real and absolute. Ensures cross platform compatibility
    path_to_file = make_path(args.file)

    # Load json file into data structures (Content, Section, Paragraph)
    print("Loading input JSON file into structures...")
    random_percentage_count()
    
    input_file = open(path_to_file)
    content: Content = load_json(input_file)
    print("...Loading done\n\n")

    # Extract corpus
    corpus = extract_all_text_from_paragraphs(content)

    # Preprocess the paragraphs in the json file
    print("Cleaning the JSON file")
    random_percentage_count()
    cleaner = CleanerImp()
    
    corpus = cleaner.remove_special_characters(corpus)
    corpus = cleaner.numbers_to_text(corpus)
    corpus = cleaner.lemmatize(corpus)
    corpus = cleaner.bigrams(corpus)
    corpus = cleaner.to_lower(corpus)
    
    print("...Cleaning done\n\n")

    # Instantiate model, load corpus into model and extract tokens
    print("Instantiating the word embedding model...")
    random_percentage_count()
    model = SpacyModel()

    model.load(corpus)

    tokens = model.tokens()
    print("...Instantiating done\n\n")

    # Instantiate knowledge graph information
    print("Loading knowledge graph data...")
    random_percentage_count()

    kg_info = KnowledgeGraphInfo(tokens, content)

    print("...Loading done\n\n")

    # Instantiate knowledge graph and create triples
    print("Instantiating knowledge graph...")
    random_percentage_count()
    knowledge_graph = KnowledgeGraph()
    
    knowledge_graph.generate_triples(kg_info)

    knowledge_graph.save_to_database()
    print("...Instantiating done\n\n")

    # If --visualisation" or "-v" in args
    if args.visualisation:
        print("Rendering knowledge graph in new window...")
        knowledge_graph.show_graph()
        print("...Visualization closed\n\n")
