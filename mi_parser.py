from argparse import ArgumentParser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("--visualisation", "-v", action="store_true", default=False,
                        help="This option visualise the graph, on plotly, after the script have run")

    return parser
