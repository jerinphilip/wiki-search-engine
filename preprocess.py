from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from gensim.parsing import stem_text

def preprocess(text):
    # Convert to lowercase
    text = text.lower()

    # Tokenize
    tokenizer = RegexpTokenizer(r'[0-9]{4}|[a-zA-Z]{3,}')
    tokens = tokenizer.tokenize(text)

    # Filter stopwords
    sw = stopwords.words("english")
    sw = set(sw)
    sw.update(['amp','http','com','www','ref','web','url','deadurl','archiveDate','archiveurl',\
                        'quot','accessdate','cite','nbsp','isbn','htm','cols','category'])

    non_sw = filter(lambda x: x not in sw, tokens)
    non_sw = list(non_sw)

    # Stem to obtain reasonable results
    stemmed = [stem_text(x) for x in non_sw]
    return stemmed


