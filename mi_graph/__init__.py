#!/usr/bin/python3
import os
from argparse import ArgumentParser
from loader.file_loader import load_json
from preprocess.cleaner_imp import CleanerImp
from word_embedding.spacy_model import SpacyModel
from mi_graph.knowledge_graph import KnowledgeGraph
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from resources.json_wrapper import Content
from resources.random_number_gen import random_percentage_count


def setup_parser(_parser: ArgumentParser) -> ArgumentParser:
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
        for para in sec.paragraphs:
            text += para.text
    return text


if __name__ == "__main__":

    # Setup the parser and parse the arguments
    parser = setup_parser(ArgumentParser())
    args = parser.parse_args()

    # Make path of the input file real and absolute. Ensures cross platform compatibility
    pathToFile = make_path(args.file)

    # Load json file into data structures (Content, Section, Paragraph)
    print("Loading input JSON file into structures...")
    random_percentage_count()
    inputFile = open(pathToFile)
    content: Content = load_json(inputFile)
    print("...Loading done\n\n")

    # Extract corpus
    CORPUS = extract_all_text_from_paragraphs(content)

    # Preprocess the paragraphs in the json file
    print("Cleaning the JSON file")
    random_percentage_count()
    cleaner = CleanerImp()
    CORPUS = cleaner.remove_special_characters(CORPUS)
    CORPUS = cleaner.numbers_to_text(CORPUS)
    CORPUS = cleaner.lemmatize(CORPUS)
    CORPUS = cleaner.bigrams(CORPUS)
    CORPUS = cleaner.to_lower(CORPUS)
    print("...Cleaning done\n\n")

    # Instantiate model, load corpus into model and extract tokens
    print("Instantiating the word embedding model...")
    random_percentage_count()
    model = SpacyModel()
    model.load(CORPUS)
    tokens = model.tokens()
    print("...Instantiating done\n\n")

    # Instantiate knowledge graph information
    print("Loading knowledge graph data...")
    random_percentage_count()
    kgInfo = KnowledgeGraphInfo(tokens, content)
    print("...Loading done\n\n")

    # Instantiate knowledge graph and create triples
    print("Instantiating knowledge graph...")
    random_percentage_count()
    knowledge_graph = KnowledgeGraph()
    knowledge_graph.generate_triples(kgInfo)
    knowledge_graph.save_to_database()
    print("...Instantiating done\n\n")

    # If --visualisation" or "-v" in args
    if args.visualisation:
        print("Rendering knowledge graph in new window...")
        knowledge_graph.show_graph()
        print("...Visualization closed\n\n")
