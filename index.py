from collections import defaultdict
from pprint import pprint

class InvertedIndex:
    def __init__(self):
        self.map = defaultdict(list)
        self.titles = defaultdict(str)
        self.counter = 0

    def merge(self, posting):
        for key in posting:
            doc_id = self.id(key)
            fposting = (doc_id, posting[key])
            self.map[key].append(fposting)

    def id(self, key):
        if key not in self.titles:
            self.titles[key] = self.counter
            self.counter = self.counter + 1
        return self.titles[key]

    def __str__(self):
        return str(self.map)

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
    for i, datum in enumerate(data):
        title = datum["title"]
        document = datum["text"]
        posting = Posting(document)
        II.merge(posting)

    pprint(II.map)
