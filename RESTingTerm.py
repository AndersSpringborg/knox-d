from flask import Flask
from flask_restful import Api, Resource
from preprocess.cleaner_imp import CleanerImp

app = Flask(__name__)
api = Api(app)

class Term(Resource):
    def get(self, word):
        cleaner = CleanerImp()
        lemmatized_word = cleaner.lemmatize(word)
        return {'lemma' : lemmatized_word}

api.add_resource(Term, '/term/<word>')

if __name__ == '__main__':
    app.run(debug=True)