import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from resources.triple_container import Triple
from resources.json_wrapper import Content
from word_embedding.dependency import Dependency


class KnowledgeGraph:
    """
    Generates triples from the text which has been natural language processed,
    and the metadata extracted from a Content object.
    Triples are saved to the database(.csv) file provided to the object during instantiation.
    """
    column_names = ['subject', 'relation', 'object']
    dataframe = pd.DataFrame(columns=column_names)

    database_path = ''

    def __init__(self, _database_path):
        self.database_path = _database_path

    def generate_triples(self, kg_info: KnowledgeGraphInfo):
        """
        Generates triples (subj, rel, obj) from the text which has been natural language processed
        and the metadata extracted from a Content object
        """
        triples = []

        triples.extend(self.__process_metadata(kg_info.content))
        triples.extend(self.__analyse_sentences(kg_info.sentences))

        self.__create_branches(triples)

        self.__save_to_file()


    def show_graph(self):
        """
        Opens a new window with the graph plotted within
        """
        graph = nx.from_pandas_edgelist(
            self.dataframe, 'subject', 'object', edge_attr=True, create_using=nx.MultiDiGraph())

        plt.figure(figsize=(12, 12))

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, edge_color='black',
                node_color='skyblue', alpha=0.9, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos=pos)

        plt.show()

    def __analyse_sentences(self, sentences):
        triples = []

        for sentence in sentences:
            triples.append(self.__process_sentence(sentence))

        return triples

    def __process_metadata(self, content: Content):
        triples = []

        triples.extend(self.__create_relations_for_manual(content))
        triples.extend(self.__create_relations_for_sections(content))

        return triples

    @staticmethod
    def __create_relations_for_manual(content: Content):
        triples = []

        if content.publisher:
            triples.append(Triple("manual", "publishedBy", content.publisher))

        if content.published_at:
            triples.append(Triple("manual", "publishedAt", content.published_at))

        if content.title:
            triples.append(Triple("manual", "describes", content.title))

        if content.sections:
            for sec in content.sections:
                triples.append(Triple("manual", "contains", sec.header))

        return triples

    @staticmethod
    def __create_relations_for_sections(content: Content):
        triples = []

        if content.sections:
            for sec in content.sections:
                if sec.header and sec.page:
                    triples.append(Triple(sec.header, "isAt", sec.page))

        return triples

    def __process_sentence(self, sentence):
        subj = ''
        obj = ''
        relation = ''

        for token in sentence:
            if self.__is_subject(token) and self.__is_empty(subj):
                subj = token.name
            elif self.__is_object(token) and self.__is_empty(obj):
                obj = token.name
            elif self.__is_relation_candidate(token):
                relation = token.name
            else:
                continue

        return Triple(subj.strip(), relation.strip(), obj.strip())

    @staticmethod
    def __is_subject(token):
        return token.dep == Dependency.nsubj or token.dep == Dependency.csubj or \
                token.dep == Dependency.csubjpass or token.dep == Dependency.nsubjpass

    @staticmethod
    def __is_object(token):
        return token.dep == Dependency.obj or token.dep == Dependency.dobj or \
                token.dep == Dependency.pobj

    @staticmethod
    def __is_empty(text_field):
        return not text_field

    @staticmethod
    def __is_relation_candidate(token):
        return token.dep == Dependency.root

    def __create_branches(self, triples):
        for triple in triples:
            self.dataframe = self.dataframe.append(
                pd.DataFrame(
                    {'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}))

    def __save_to_file(self):
        if not os.path.exists(self.database_path):
            self.dataframe.to_csv(self.database_path, mode='a', index=False)
        elif os.stat(self.database_path).st_size == 0:
            self.dataframe.to_csv(self.database_path, mode='a', index=False)
        else:
            self.dataframe.to_csv(self.database_path, mode='a', index=False, header=None)
