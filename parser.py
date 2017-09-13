import sys
import re
from lxml import etree
from collections import OrderedDict
import mwparserfromhell as mwp
from preprocess import preprocess


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

def pformat(d):
    text = d["revision"]
    ast  = mwp.parse(text)
    text = ast.strip_code()
    text = preprocess(text)
    return {"text": text, "title": d["title"]}


def extract(filename):
    tree = etree.parse(filename)
    data = []
    count = 0
    max_count = 10
    for page in tree.getroot():
        d = pack(page)
        if d:
            r = pformat(d)
            data.append(r)
        count = count + 1
        if count > max_count:
            break
    return data

if __name__ == '__main__':
    print(extract(sys.argv[1]))
