from tokencontainer import Token, GrammarCategories
from Knowledge_Graph.knowledge_graph import KnowledgeGraph

sentences = []
sentence1 = []
sentence2 = []
sentence3 = []

token1 = Token('Kaare', 'NOUN')
token1.grammar_cat = GrammarCategories.subj
sentence1.append(token1)

token2 = Token('likes', 'VERB')
token2.grammar_cat = GrammarCategories.rel
sentence1.append(token2)

token3 = Token('apples', 'NOUN')
token3.grammar_cat = GrammarCategories.obj
sentence1.append(token3)


token4 = Token('Martin', 'NOUN')
token4.grammar_cat = GrammarCategories.subj
sentence2.append(token4)

token5 = Token('dislikes', 'VERB')
token5.grammar_cat = GrammarCategories.rel
sentence2.append(token5)

token6 = Token('flaskesteg', 'NOUN')
token6.grammar_cat = GrammarCategories.obj
sentence2.append(token6)


token7 = Token('Kaare', 'NOUN')
token7.grammar_cat = GrammarCategories.subj
sentence3.append(token7)

token10 = Token('enjoys', 'VERB')
token10.grammar_cat = GrammarCategories.rel
sentence3.append(token10)

token11 = Token('cola', 'NOUN')
token11.grammar_cat = GrammarCategories.obj
sentence3.append(token11)


sentences.append(sentence1)
sentences.append(sentence2)
sentences.append(sentence3)



kg = KnowledgeGraph(sentences)
kg.print_graph()



