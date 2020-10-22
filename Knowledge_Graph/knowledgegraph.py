import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
pd.set_option('display.max_colwidth', 200)


class Triple:
    subj = ''
    obj = ''
    rel = ''

    def __init__(self, _subj, _rel, _obj):
        self.subj = _subj
        self.obj = _obj
        self.rel = _rel


class KnowledgeGraph:
    KGFILE = 'knowledgegraph.txt'

    column_names = ['subject', 'relation', 'object']

    df = pd.DataFrame(columns=column_names)


    def __init__(self):
        pass

    def update(self, sentences: list):
        for sentence in sentences:
            self.__process_triple(self.__process_sentence(sentence))

    def show_graph(self):
        G = nx.from_pandas_edgelist(self.df, 'subject', 'object', edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12, 12))

        pos = nx.spring_layout(G)
        nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
                node_size=500, node_color='blue', alpha=0.9, with_labels=True)
        plt.show()

    def __process_sentence(self, sentence: list):
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
        deps = ["ROOT", "adj", "attr", "agent", "amod"]
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
        self.__save_to_file()

    def __update_branch(self, triple):
        pass

    def __create_node(self, triple):
        pass

    def __save_to_file(self):
        self.df.to_csv('knowledgegraphtestfile.csv', index=False)

    def __print_triple(self, triple):
        return triple.subj + ' --> ' + triple.rel + ' --> ' + triple.obj + '\n'

    def get_knowledge_graph(self):
        file = open(self.KGFILE)
        return file.read()


