from resources import knox_triples
from resources.json_wrapper import Section, Manual
from word_embedding.dependency import Dependency


def generate_triples_for_metadata(content: Manual):
    triples = []

    triples.extend(generate_triples_for_manual(content))
    triples.extend(generate_triples_for_sections(content))

    return triples


def generate_triples_for_manual(manual: Manual):
    triples = []

    if manual.published_by:
        triples.append(knox_triples.PublishTriple(manual.title, manual.published_by))

    if manual.published_at:
        triples.append(knox_triples.PublishedAtTriple(manual.title, manual.published_at))

    if manual.title:
        triples.append(knox_triples.MetaDataTriple(manual.title))
        triples.append(knox_triples.TitleTriple(manual.title))

    if manual.sections:
        for sec in manual.sections:
            triples.append(knox_triples.SectionTriple(manual.title, sec.header))

    return triples


def generate_triples_for_sections(manual: Manual):
    triples = []

    if manual.sections:
        for sec in manual.sections:

            if __has_header_and_page(sec):
                triples.append(knox_triples.PageTriple(manual.title, sec.page))
                triples.append(knox_triples.PageInSectionTriple(manual.title, sec.page, sec.header))

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
