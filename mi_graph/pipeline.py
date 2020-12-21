import json

import requests

from resources.term_frequency import TermFrequency
from resources.json_wrapper import Manual
from resources.knowledgegraph_info_container import KnowledgeGraphInfo

from preprocess.cleaner_imp import CleanerImp

from word_embedding.spacy_model import SpacyModel
from .knowledge_graph import KnowledgeGraph


def create_knowledge_graph(manual, visual=False):
    corpus = extract_all_text_from_paragraphs(manual)
    corpus = clean_text(corpus)
    tokens = extract_tokens_from(corpus)
    kg_info = KnowledgeGraphInfo(tokens, manual)
    knowledge_graph = KnowledgeGraph()
    knowledge_graph.generate_triples(kg_info)
    if not visual:
        knowledge_graph.save_to_database()
    return knowledge_graph


def clean_text(corpus):
    cleaner = CleanerImp()
    corpus = cleaner.remove_special_characters(corpus)
    corpus = cleaner.numbers_to_text(corpus)
    corpus = cleaner.lemmatize(corpus)
    corpus = cleaner.bigrams(corpus)
    corpus = cleaner.to_lower(corpus)
    return corpus


def extract_tokens_from(corpus):
    model = SpacyModel()
    model.load(corpus)
    tokens = model.tokens()
    return tokens


def extract_all_text_from_paragraphs(data: Manual):
    text: str = ''
    for sec in data.sections:
        text += sec.paragraph.text
    return text


def generate_word_counts(manual: Manual, conn_database=False):
    cleaner = CleanerImp()
    word_counter = TermFrequency()
    for section in manual.sections:
        cleaned_text = cleaner.remove_special_characters(section.paragraph.text)
        cleaned_text = cleaner.to_lower(cleaned_text)
        word_counter.process(manual.title, cleaned_text)

    for doc in word_counter:
        form = {}
        words = [{'word': word, 'amount': frequency} for word, frequency in word_counter[doc].items()]
        form['words'] = words

        form['articletitle'] = doc

        form["filepath"] = f"/test/{doc}"

        form['totalwordsinarticle'] = word_counter[doc].length

        if conn_database:
            # ´har portforward port 8080, fra server til local host
            # ssh username@student.aau.dk@knox-node02.srv.aau.dk -L 8080:localhost:8080
            # url = 'http://knox-node02.srv.aau.dk/wordCountData/'
            url = 'http://127.0.0.1:8080/wordCountData/'
            json_form = json.dumps(form)
            header: dict = {'content-type': 'application/json; charset=utf-8'}
            response = requests.post(url, data=json_form, headers=header)
            print("Status code: ", response.status_code)
            print("Printing Entire Post Request")
            print(response)


def run(manual, visualize=False):
    knowledge_graph = create_knowledge_graph(manual, visualize)
    # If --visualisation" or "-v" in args
    if visualize:
        print("Rendering knowledge graph in new window...")
        knowledge_graph.show_graph()
        print("...Visualization closed\n\n")
    else:
        generate_word_counts(manual)

    return knowledge_graph
