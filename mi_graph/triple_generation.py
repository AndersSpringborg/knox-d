from resources import knox_triples
from resources.json_wrapper import Content, Section
from word_embedding.dependency import Dependency


def generate_triples_for_metadata(content: Content):
    triples = []

    triples.extend(generate_triples_for_manual(content))
    triples.extend(generate_triples_for_sections(content))

    return triples


def generate_triples_for_manual(content: Content):
    triples = []

    if content.publisher:
        triples.append(knox_triples.PublishTriple(content.title, content.publisher))

    if content.published_at:
        triples.append(knox_triples.PublishedAtTriple(content.title, content.published_at))

    if content.title:
        triples.append(knox_triples.MetaDataTriple(content.title))
        triples.append(knox_triples.TitleTriple(content.title))

    if content.sections:
        for sec in content.sections:
            triples.append(knox_triples.SectionTriple(content.title, sec.header))

    return triples


def generate_triples_for_sections(content: Content):
    triples = []

    if content.sections:
        for sec in content.sections:

            if __has_header_and_page(sec):
                triples.append(knox_triples.PageTriple(content.title, sec.page))
                triples.append(knox_triples.PageInSectionTriple(content.title, sec.page, sec.header))

    return triples


def __has_header_and_page(section: Section):
    return section.header and section.page


def generate_triples_for_sentences(sentences):
    triples = []

    for sentence in sentences:
        triples.append(__process_sentence(sentence))

    return triples


def __process_sentence(sentence):
    subj = ''
    obj = ''
    relation = ''

    for token in sentence:
        if __is_subject(token) and __is_empty(subj):
            subj = token.name
        elif __is_object(token) and __is_empty(obj):
            obj = token.name
        elif __is_relation_candidate(token):
            relation = token.name
        else:
            continue

    return __parse_obj_relation_subj(subj, relation, obj)


def __parse_obj_relation_subj(subj, relation, obj):
    return knox_triples.SentenceTriple(subj, relation, obj)


def __is_subject(token):
    return token.dep == Dependency.nsubj or token.dep == Dependency.csubj or \
           token.dep == Dependency.csubjpass or token.dep == Dependency.nsubjpass


def __is_object(token):
    return token.dep == Dependency.obj or token.dep == Dependency.dobj or \
           token.dep == Dependency.pobj


def __is_empty(text_field):
    return not text_field


def __is_relation_candidate(token):
    return token.dep == Dependency.root
