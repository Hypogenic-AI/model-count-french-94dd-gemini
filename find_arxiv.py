import arxiv
import os

client = arxiv.Client()

queries = [
    'multilingual number representation transformers',
    'French numeral system LLM',
    'compositional numeral systems NLP',
    'numerical reasoning French transformers',
    'vigesimal number systems language models'
]

papers_dir = 'papers'
if not os.path.exists(papers_dir):
    os.makedirs(papers_dir)

for query in queries:
    search = arxiv.Search(
        query = query,
        max_results = 10,
        sort_by = arxiv.SortCriterion.Relevance
    )

    for result in client.results(search):
        print(f"Title: {result.title}")
        print(f"Authors: {', '.join(str(a) for a in result.authors)}")
        print(f"Year: {result.published.year}")
        print(f"Summary: {result.summary[:200]}...")
        print(f"URL: {result.pdf_url}")
        print("-" * 20)

