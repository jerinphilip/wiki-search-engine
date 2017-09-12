import sys
import re
from lxml import etree
from collections import OrderedDict
import mwpfh

tree = etree.parse(sys.argv[1])

def ns_clean(tag):
    pattern = re.compile("\{(.+)\}(.*)")
    ns, tag = pattern.match(tag).groups()
    return (ns, tag)

def pack(tree):
    keys = {"title", "revision"}
    d = OrderedDict()

    def parse_title(t):
        return t.text

    def parse_revision(t):
        return t[-2].text


    parse = {
            "title": parse_title,
            "revision": parse_revision
    }

    for subtree in tree:
        ns, key = ns_clean(subtree.tag)
        if key in keys:
            d[key] = parse[key](subtree)
    return d 

def reduce(text):
    ast = mwpfh.parse(text)
    return ast


for page in tree.getroot():
    d = pack(page)
    if d:
        text = d["revision"]
        ast = reduce(text)
        sections = ast.get_sections()
        print(sections)


