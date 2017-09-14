from collections import defaultdict
from pprint import pprint
from copy import deepcopy
import json
import pickle
from collections import Counter

class InvertedIndex:
    def __init__(self):
        self.map = defaultdict(list)
        self.titles = defaultdict(int)
        self.counter = 0
        self.D = defaultdict(float)
        self.inverse = defaultdict(str)

    def load_wikidata(self, data):
        for datum in data:
            title = datum["title"]
            document = datum["text"]
            doc_id = self.id(title)
            self._fD(doc_id, document)
            posting = Posting(document)
            self.merge(doc_id, posting)

    def _fD(self, doc_id, document):
        histogram = Counter(document).values()
        rms = sqrt(sum(map(lambda x: x*2, histogram)))
        self.D[doc_id] = rms

    def merge(self, doc_id, posting):
        for key in posting:
            fposting = (doc_id, posting[key])
            self.map[key].append(fposting)

    def id(self, key):
        if key not in self.titles:
            self.titles[key] = self.counter
            self.inverse[self.counter] = key
            self.counter = self.counter + 1
        return self.titles[key]

    def query(self, key):
        raise NotImplementedError

    def load(self, filename):
        with open(filename, "rb") as fp:
            d = pickle.load(fp)
            self.map = d["map"]
            self.inverse = d["inverse"]
            self.titles = d["titles"]
            self.counter = d["counter"]
            self.D = d["D"]

    def save(self, filename):
        with open(filename, "wb+") as fp:
            d = {
                "map": self.map,
                "inverse": self.inverse,
                "titles": self.titles,
                "counter": self.counter,
                "D": self.D
            }
            pickle.dump(d, fp)

    def __str__(self):
        return str(self.map)

    def __add__(self, other):
        """ Merge two separately created inverted indices """
        result = InvertedIndex()
        result = deepcopy(self)
        for title_id in other.map:
            title = other.inverse[title_id]
            doc_id = self.id(title)
            fposting = (doc_id, posting[key])
            self.map[key].append(fposting)
        return result

class Posting:
    def __init__(self, document):
        self.posting = defaultdict(list)
        for j, token in enumerate(document):
            self.posting[token].append(j)

    def reduce(self):
        return list(self.posting.items())

    def __iter__(self):
        return self.posting.__iter__()
    
    def next(self):
        return self.posting.next()
    
    def __getitem__(self, key):
        return self.posting[key]
    
    def __str__(self):
        return str(self.posting)

if __name__ == '__main__':
    from parser import extract
    import sys
    II = InvertedIndex()

    data = extract(sys.argv[1])
    II.load_wikidata(data)
    II.save("index.dump")

    pprint(II.map)
