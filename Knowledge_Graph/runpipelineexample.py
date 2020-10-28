import spacy
from spacy import displacy
from Knowledge_Graph.knowledgegraph import KnowledgeGraph
from Resources.KnowledgeGraphInfoContainer import KnowledgeGraphInfo
from Resources.JsonWrapper import Content

nlp = spacy.load('en_core_web_lg')

text1 = "The ALPHA1_circulator is designed for the circulation of water in heating systems, domestic hot-water systems as well as air-conditioning and cold-water systems."
text2 = "John completed the task."
text3 = "I love French fries."
text4 = "Apple is looking at buying U.K._startup."
text5 = "Her car skidded and halted to a stop."

corpus = ''
corpus += text1
corpus += text2
corpus += text3
corpus += text4
corpus += text5

# Run NLP on corpus
doc = nlp(corpus)

# Split the doc object into sentences
sentences = list(doc.sents)

# instantiate content object
dictionary = {
    "publisher": "Grundfoss",
    "publishedAt": "23/7",
    "title": "ALPHA1"
}
content = Content(dictionary)


# instantiate kgInfo
kgInfo = KnowledgeGraphInfo(sentences, content)

knowledgeGraph = KnowledgeGraph('test_database.csv')
knowledgeGraph.generate_triples(kgInfo)
knowledgeGraph.show_graph()

#for token in doc:
#    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#            token.shape_, token.is_alpha, token.is_stop)

