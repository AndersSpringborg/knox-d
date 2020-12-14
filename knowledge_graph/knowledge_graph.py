import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import requests

from knowledge_graph import triple_generation
from rdf_parser.rdf_parser import RdfParser
from resources.knowledgegraph_info_container import KnowledgeGraphInfo


class KnowledgeGraph:
    """
    Generates triples from the text which has been natural language processed,
    and the metadata extracted from a Content object.
    Triples are saved to the database(.csv) file provided to the object during instantiation.
    """
    knowledge_graph_triples = []

    def __init__(self):
        self.rdf_parser = RdfParser()
        self.knowledge_graph_triples = []

    def generate_triples(self, kg_info: KnowledgeGraphInfo):
        """
        Generates knox_triples (subj, rel, obj) from the text which has been natural language processed
        and the metadata extracted from a Content object
        """
        self.knowledge_graph_triples.extend(triple_generation.generate_triples_for_metadata(kg_info.content))
        self.knowledge_graph_triples.extend(triple_generation.generate_triples_for_sentences(kg_info.sentences))

    def show_graph(self):
        """
        Opens a new window with the graph plotted within
        """
        graph = nx.from_pandas_edgelist(
            self.__create_branches_from_triples(), 'subject', 'object', edge_attr=True, create_using=nx.MultiDiGraph())

        plt.figure(figsize=(12, 12))

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, edge_color='black',
                node_color='skyblue', alpha=0.9, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos=pos)

        plt.show()

    def __create_branches_from_triples(self):
        df = pd.DataFrame(columns=["subject", "relation", "object"])
        for triple in self.knowledge_graph_triples:
            try:
                df = df.append(
                    pd.DataFrame(
                        {'subject': [triple.subj_()], 'relation': [triple.rel_()], 'object': [triple.obj_()]}))
            except KeyError as error:
                print(error)
        return df

    def pretty_print_graph(self):
        import pprint
        for triple in self.knowledge_graph_triples:
            pprint.pprint(triple.parse())

    def save_to_csv(self, csv_file_path):
        triple_dataframe = self.__create_branches_from_triples()

        if not os.path.exists(csv_file_path):
            triple_dataframe.to_csv(csv_file_path, mode='a', index=False)
        elif os.stat(csv_file_path).st_size == 0:
            triple_dataframe.to_csv(csv_file_path, mode='a', index=False)
        else:
            triple_dataframe.to_csv(csv_file_path, mode='a', index=False, header=None)

    def save_to_database(self):
        data = self.__generate_data()

        self.__update_triples(data)
        self.__commit_triples()

    def __update_triples(self, data):
        update_url = 'http://127.0.0.1:8080/update/'
        update_header: dict = {'content-type':
                                   'application/json; charset=utf-8'}
        response = requests.post(update_url,
                                 data=data,
                                 headers=update_header)
        self.__print_response(response)

    def __commit_triples(self):
        commit_url = 'http://127.0.0.1:8080/commit/'

        response = requests.post(commit_url)
        self.__print_response(response)

    def __generate_data(self):
        data = ""
        for triple in self.knowledge_graph_triples:
            try:
                data += repr(triple) + " .\n"
            except KeyError as error:
                pass
        return data

    @staticmethod
    def __print_response(response):
        print("Status code: ", response.status_code)
        print(response.text)
