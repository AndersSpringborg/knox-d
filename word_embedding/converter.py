from word_embedding.dependency import Dependency


class Converter():
    """
    Converter class for the dependencies in spacy to known knox dependencies
    """
    @staticmethod
    def dependency(dep: str) -> Dependency:
        converter = {
            "nsubj": Dependency.nsubj,
            "pobj": Dependency.pobj,
            "aux": Dependency.aux,
            "ROOT": Dependency.root,
            "prep": Dependency.prep,
            "pcomp": Dependency.pcomp,
            "compound": Dependency.compound,
            "dobj": Dependency.dobj,
            "quantmod": Dependency.quantmod,
        }

        if dep not in converter.keys():
            return Dependency.other
        return converter[dep]
