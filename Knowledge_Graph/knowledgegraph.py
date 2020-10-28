import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from Resources.KnowledgeGraphInfoContainer import KnowledgeGraphInfo
from Resources.TripleContainer import Triple
from Resources.JsonWrapper import Content
from word_embedding.dependency import Dependency


class KnowledgeGraph:
    column_names = ['subject', 'relation', 'object']
    dataframe = pd.DataFrame(columns=column_names)

    database_path = ''

    def __init__(self, _database_path):
        self.database_path = _database_path

    def generate_triples(self, kg_info: KnowledgeGraphInfo):
        triples = []

        triples.extend(self.__process_metadata(kg_info.content))
        triples.extend(self.__analyse_sentences(kg_info.sentences))

        self.__create_branches(triples)

        self.__save_to_file()

    def __analyse_sentences(self, sentences):
        triples = []

        for sentence in sentences:
            triples.append(self.__process_sentence(sentence))

        return triples

    def show_graph(self):
        graph = nx.from_pandas_edgelist(self.dataframe, 'subject', 'object', edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12, 12))

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, edge_color='black',
                node_color='skyblue', alpha=0.9, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos=pos)
        plt.show()

    def __process_metadata(self, content: Content):
        triples = []
        triples.extend(self.__create_relations_for_manual(content))

        if hasattr(content, "sections"):
            triples.extend(self.__create_relations_for_sections(content))

        return triples

    def __create_relations_for_manual(self, content: Content):
        triples = []

        if hasattr(content, "publisher"):
            triples.append(Triple("manual", "publishedBy", content.publisher))
        if hasattr(content, "publishedAt"):
            triples.append(Triple("manual", "publishedAt", content.publishedAt))
        if hasattr(content, "title"):
            triples.append(Triple("manual", "describes", content.title))

        if hasattr(content, "sections"):
            for sec in content.sections:
                triples.append(Triple("manual", "contains", sec.header))

        return triples

    def __create_relations_for_sections(self, content):
        triples = []
        for sec in content.sections:
            if hasattr(sec, "header") and hasattr(sec, "page"):
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
        if token.dep == Dependency.nsubj or token.dep == Dependency.csubj or \
                token.dep == Dependency.csubjpass or token.dep == Dependency.nsubjpass:
            return True
        else:
            return False

    @staticmethod
    def __is_object(token):
        if token.dep == Dependency.obj or token.dep == Dependency.dobj or token.dep == Dependency.pobj:
            return True
        else:
            return False

    @staticmethod
    def __is_empty(text_field):
        if not text_field:
            return True
        else:
            return False

    @staticmethod
    def __is_relation_candidate(token):
        if token.dep == Dependency.root:
            return True

        else:
            return False

    def __create_branches(self, triples):
        for triple in triples:
            self.dataframe = self.dataframe.append(
                pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}))

    def __save_to_file(self):
        if not os.path.exists(self.database_path):
            self.dataframe.to_csv(self.database_path, mode='a', index=False)
        elif os.stat(self.database_path).st_size == 0:
            self.dataframe.to_csv(self.database_path, mode='a', index=False)
        else:
            self.dataframe.to_csv(self.database_path, mode='a', index=False, header=None)

    @staticmethod
    def __print_triple(triple):
        return triple.subj + ' --> ' + triple.rel + ' --> ' + triple.obj + '\n'




