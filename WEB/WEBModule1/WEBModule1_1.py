from abc import ABC, abstractmethod
import pickle
import json



class SerializationInterface(ABC):

    def dump(self, data, name):
        pass

    def load(self, name):
        pass


class PickleSerialization(SerializationInterface):

    def dump(self, data, name):
        with open(name, "wb") as f:
            pickle.dump(data, f)
        print(f" {data} was dumped to {name} by pickle")

    def load(self, name):
        with open(name, "rb") as f:
            data = pickle.load(f)
        return data


class JSONSerialization(SerializationInterface):

    def dump(self, data, name):
        with open(name, "w") as f:
            json.dump(data, f)
        print(f" {data} was dumped to {name} by JSON")

    def load(self, name):
        with open(name, "r") as f:
            data = json.load(f)
        return data



s = PickleSerialization()
l = [45, 'gfdf', 'df', 34785]
s.dump(l, "test1")
print(s.load("test1"))
j = JSONSerialization()
j.dump(l, "test3")
print(j.load("test3"))
