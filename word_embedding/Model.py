
import abc


class Model(abc):
    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def load(self, path):
        pass

    @abc.abstractmethod
    def save(self, path):
        pass
