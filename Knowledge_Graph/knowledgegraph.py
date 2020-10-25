import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
from Resources.TripleContainer import Triple
from Resources.JsonWrapper import Content


class KnowledgeGraph:
    column_names = ['subject', 'relation', 'object']

    df = pd.DataFrame(columns=column_names)

    database_path = ''

    def __init__(self, _database_path):
        self.database_path = _database_path

    def update(self, sentences):
        for sentence in sentences:
            self.__process_triple(self.__process_sentence(sentence))

        self.__save_to_file()

    def show_graph(self):
        G = nx.from_pandas_edgelist(self.df, 'subject', 'object', edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12, 12))

        pos = nx.spring_layout(G)
        nx.draw(G, pos, edge_color='black',
                node_color='skyblue', alpha=0.9, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos=pos)
        plt.show()

    def __process_sentence(self, sentence):
        subj = ''
        obj = ''
        relation = ''
        for token in sentence:
            if 'subj' in token.dep_:
                subj = token.text
            elif 'obj' in token.dep_:
                obj = token.text
            elif self.__is_relation_candidate(token):
                if not relation:
                    relation += token.text
                else:
                    relation += ' ' + token.text
            else:
                continue

        return Triple(subj.strip(), relation.strip(), obj.strip())

    def __is_relation_candidate(self, token):
        deps = ["ROOT", "adj", "attr", "agent", "amod", "xcomp", "prep"]
        return any(subs in token.dep_ for subs in deps)

    def __process_triple(self, triple: Triple):
        if self.__relation_and_object_exists(triple):
            pass
        else:
            self.__create_branch(triple)

    def __relation_and_object_exists(self, triple):
        pass

    def __create_branch(self, triple):
        self.df = self.df.append(pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}))

    def __update_branch(self, triple):
        pass

    def __create_node(self, triple):
        pass

    def __save_to_file(self):
        if not os.path.exists(self.database_path):
            self.df.to_csv(self.database_path, mode='a', index=False)
        elif os.stat(self.database_path).st_size == 0:
            self.df.to_csv(self.database_path, mode='a', index=False)
        else:
            self.df.to_csv(self.database_path, mode='a', index=False, header=None)

    def __print_triple(self, triple):
        return triple.subj + ' --> ' + triple.rel + ' --> ' + triple.obj + '\n'



