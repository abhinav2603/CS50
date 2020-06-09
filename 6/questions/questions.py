import nltk
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string
import math
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    #raise NotImplementedError
    di = {}
    for file in os.listdir(directory):
    	with open(os.path.join(directory,file)) as f:
    		di[file] = f.read()
    return di


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #raise NotImplementedError
    stop_words = set(stopwords.words('english'))
    document1 = word_tokenize(document.lower())
    document1 = [x for x in document1 if (x not in stop_words) & (x not in string.punctuation)]
    return document1


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #raise NotImplementedError
    le = len(documents.keys())
    d = {}
    for values in documents.values():
    	d1 = {}
    	for word in values:
    		if word not in d:
    			d[word] = 1
    			d1[word] = 1
    		elif word not in d1:
    			d[word] += 1
    			d1[word] = 1

    for key in d.keys():
    	d[key] = math.log(le/d[key])
    return d

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #raise NotImplementedError
    l1 = []
    for file in files.keys():
    	d = 0
    	for word in query:
    		if word in files[file]:
    			d += idfs[word] * files[file].count(word)
    	l1.append((d,file))
    l1.sort(key=lambda id: id[0],reverse=True)
    l = []
    for k in l1[:n]:
    	l.append(k[1])
    return l


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    #raise NotImplementedError
    l1 = []
    for sent in sentences.keys():
    	qtd,d = 0,0
    	for word in query:
    		if word in sentences[sent]:
    			d += idfs[word]
    		qtd += sent.count(word)
    	l1.append((d,qtd,sent))
    l1.sort(key=lambda id:(id[0],id[1]), reverse=True)
    l = []
    for k in l1[:n]:
    	l.append(k[2])
    return l


if __name__ == "__main__":
    main()
