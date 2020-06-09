import os
import random
import re
import sys
import numpy as np
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #raise NotImplementedError
    d = {}
    num_pages = len(corpus)
    if len(corpus[page]) == 0:
        for pages in corpus.keys():
            d[pages] = 1/num_pages
    else:
        for pages in corpus.keys():
            d[pages] = (1-damping_factor) * (1/num_pages)
        for pages in corpus[page]:
            d[pages] += damping_factor * (1/len(corpus[page]))
    return d



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError
    d = {}
    for page in corpus:
        d[page] = 0
    page = np.random.choice(list(corpus.keys()))
    for i in range(n):
        d[page] += 1
        prob = transition_model(corpus,page,damping_factor)
        value = list(prob.values())
        key = list(prob.keys())
        page = np.random.choice(key,p=value)
    for k in d:
        d[k] /= n 
    return d


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError
    d = {}
    num_pages = len(corpus)
    for page in corpus.keys():
        d[page] = 1/num_pages
    state = True
    while state:
        d1 = {}
        for page in corpus:
            d1[page] = (1-damping_factor)/num_pages
            sum1 = 0
            for page1 in corpus:
                if {page}.issubset(corpus[page1]):
                    sum1 += damping_factor*(d[page1]/len(corpus[page1]))
            d1[page] = d1[page]+sum1
        dif = .001
        for k in d:
            if dif < abs(d[k]-d1[k]):
                dif = abs(d[k]-d1[k])
        if dif == .001:
            break
        else:
            d=d1.copy()
    return d



if __name__ == "__main__":
    main()
