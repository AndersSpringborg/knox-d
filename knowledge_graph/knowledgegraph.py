import os
from rdf_parser.literal_type import LiteralType
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from resources.triple_container import Triple
from resources.json_wrapper import Content
from word_embedding.dependency import Dependency
from rdf_parser.rdf_parser import RdfParser

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
        self.rdf_parser = RdfParser()

    def generate_triples(self, kg_info: KnowledgeGraphInfo, print_kg: bool = False):
        """
        Generates triples (subj, rel, obj) from the text which has been natural language processed
        and the metadata extracted from a Content object
        """
        triples = []

        triples.extend(self.__process_metadata(kg_info.content))
        triples.extend(self.__analyse_sentences(kg_info.sentences))

        self.__create_branches(triples)

        self.__save_to_file()
        if print_kg:
            self.rdf_parser.pretty_print_knowledge_graph()

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

        triples.extend(self.__create_relations_for_manual(content, self))
        triples.extend(self.__create_relations_for_sections(content, self))

        return triples

    @staticmethod
    def __create_relations_for_manual(content: Content, self):
        triples = []
        
        manual_uri = self.rdf_parser.generate_rdf_uri_ref(ref=content.title, sub_uris=["manual"])

        if content.publisher:
            triples.append(Triple("manual", "publishedBy", content.publisher))
            self.rdf_parser.add_rdf_triple((manual_uri, self.rdf_parser.get_term("rdf", "type"), self.rdf_parser.get_term("grundfos", "Manual")))

        if content.published_at:
            triples.append(Triple("manual", "publishedAt", content.published_at))
            self.rdf_parser.add_rdf_triple((manual_uri, self.rdf_parser.get_term("grundfos", "isPublishedAt"), self.rdf_parser.generate_rdf_literal(content.published_at, LiteralType.DATE)))

        if content.title:
            triples.append(Triple("manual", "describes", content.title))
            self.rdf_parser.add_rdf_triple((manual_uri, self.rdf_parser.get_term("grundfos", "Title"), self.rdf_parser.generate_rdf_literal(content.title, LiteralType.STRING)))

        if content.sections:
            for sec in content.sections:
                section_uri = self.rdf_parser.generate_rdf_uri_ref(ref=sec.header, sub_uris=["manual", content.title, "section"])
                triples.append(Triple("manual", "contains", sec.header))
                self.rdf_parser.add_rdf_triple((section_uri, self.rdf_parser.get_term("rdf", "type"), self.rdf_parser.get_term("grundfos", "Section")))
        return triples

    @staticmethod
    def __create_relations_for_sections(content: Content, self):
        triples = []

        if content.sections:
            for sec in content.sections:
                section_uri = self.rdf_parser.generate_rdf_uri_ref(ref=sec.header, sub_uris=["manual", content.title, "section"])
                if sec.header and sec.page:
                    page_uri = self.rdf_parser.generate_rdf_uri_ref(ref=sec.page, sub_uris=["manual", content.title, "section", "page"])
                    triples.append(Triple(sec.header, "isAt", sec.page))
                    self.rdf_parser.add_rdf_triple((page_uri, self.rdf_parser.get_term("rdf", "type"), self.rdf_parser.get_term("grundfos", "Page")))
                    self.rdf_parser.add_rdf_triple((page_uri, self.rdf_parser.get_term("grundfos", "isInSection"), section_uri))

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

        self.__parse_obj_relation_subj(obj, relation, subj)

        return Triple(subj.strip(), relation.strip(), obj.strip())

    def __parse_obj_relation_subj(self, obj, relation, subj):
        relation_term = self.rdf_parser.get_term("grundfos", relation.strip())
        if relation_term:
            subject_term = self.rdf_parser.get_term("grundfos", subj.strip())
            object_term = self.rdf_parser.get_term("grundfos", obj.strip())

            if not subject_term:
                subject_term = self.rdf_parser.generate_rdf_literal(subj.strip(), LiteralType.STRING)

            if not object_term:
                object_term = self.rdf_parser.generate_rdf_literal(obj.strip(), LiteralType.STRING)

            self.rdf_parser.add_rdf_triple((subject_term, relation_term, object_term))
        else:
            self.rdf_parser.add_rdf_triple(
                (self.rdf_parser.generate_rdf_literal(subj.strip(), LiteralType.STRING),
                 self.rdf_parser.generate_rdf_literal(relation.strip(), LiteralType.STRING),
                 self.rdf_parser.generate_rdf_literal(obj.strip(), LiteralType.STRING)))

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
