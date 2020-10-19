import networkx as nx
import matplotlib.pyplot as plt
from tokencontainer import GrammarCategories



# How the NLP pipeline works:
# Reciew a text
# Preprocess the text --> divide text into senteces, remove stopwords etc.
# Train the model on the text --> output = vectors
# Send the vectors to the cluster component
# Create tokens for each word in the text --> Tokens is a class containing different attributes
# For each word in the text, create a token, insert word + cluster category

# How the Knowledge Graph works:
# Evaluate each token, determine whether it is usefull or not
# By this we mean, if the token is a subject, object etc.. or a stopword, punctuation etc.
# Determine where in the triple the token should be placed
# Find a way to save the graph
# (Print graph at last) - for debugging purpose


class KnowledgeGraph:
    sentences = []
    triples = []

    def __init__(self, _sentences):
        self.sentences = _sentences
        self.construct_triples()

    def construct_triples(self):
        for sentence in self.sentences:
            self.triples.append(self.process_sentence(sentence))

    def process_sentence(self, sentence):
        subject = ''
        relation = ''
        object = ''
        for token in sentence:
            if token.grammar_cat == GrammarCategories.rel: #Alternative: 'rel' in token.grammar_cat
                relation += token.name + ' '
            elif token.grammar_cat == GrammarCategories.subj: #Alternative: 'subj' in token.grammar_cat
                subject += token.name + ' '
            elif token.grammar_cat == GrammarCategories.obj: #Alternative: 'obj' in token.grammar_cat
                object += token.name + ' '
            else:
                continue
        return subject.strip(), relation.strip(), object.strip()

    def print_graph(self):
        G = nx.Graph()
        for triple in self.triples:
            G.add_node(triple[0])
            G.add_node(triple[1])
            G.add_node(triple[2])
            G.add_edge(triple[0], triple[1])
            G.add_edge(triple[1], triple[2])

        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
                node_size=500, node_color='blue', alpha=0.9,
                labels={node: node for node in G.nodes()})
        plt.axis('off')
        plt.show()

