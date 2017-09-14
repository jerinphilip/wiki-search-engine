
from index import InvertedIndex
from preprocess import preprocess
from pprint import pprint

index = InvertedIndex()
index.load("index.dump")

query = input("Enter some shit: ")
reduced_query = preprocess(query)
x = index.query(reduced_query)
pprint(x)




