import os
import random
import re
import sys

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
    num_pages = len(corpus)
    distribution = dict()
    
   
    linked_prob = damping_factor / len(corpus[page]) if page in corpus else 0
    
    random_prob = (1 - damping_factor) / num_pages
    
   
    for linked_page in corpus[page]:
        distribution[linked_page] = linked_prob
    
    for other_page in corpus:
        if other_page not in distribution:
            distribution[other_page] = random_prob
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    num_pages = len(corpus)
    
    
    for page in corpus:
        pagerank[page] = 0
    
    
    first_sample = random.choice(list(corpus.keys()))
    pagerank[first_sample] += 1
    
    
    for _ in range(2, n+1):
        previous_sample = first_sample
        probabilities = transition_model(corpus, previous_sample, damping_factor)
        next_sample = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
        pagerank[next_sample] += 1
        first_sample = next_sample
    
    
    for page in pagerank:
        pagerank[page] /= n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus}
    convergence_threshold = 0.001
    converged = False
    
    while not converged:
        new_pagerank = pagerank.copy()
        max_diff = 0
        
        for page in corpus:
            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * sum(pagerank[link] / len(corpus[link]) for link in corpus if page in corpus[link])
            diff = abs(new_pagerank[page] - pagerank[page])
            max_diff = max(max_diff, diff)
        
        if max_diff < convergence_threshold:
            converged = True
        
        pagerank = new_pagerank
    
    return pagerank


if __name__ == "__main__":
    main()
