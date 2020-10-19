import spacy

nlp = spacy.load('en_core_web_sm')

text = "Kaare likes apples. Martin dislikes flaskesteg. Kaare and Martin enjoys cola."


# Process the text
doc = nlp(text)

for token in doc:
    # Get the token text, part-of-speech tag and dependency label
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    # This is for formatting only
    print('{:<12}{:<10}{:<10}'.format(token_text, token_pos, token_dep))