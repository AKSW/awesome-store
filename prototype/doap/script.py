import requests
from rdflib import Graph, URIRef
from gitdoap import doapit

ORG = "AKSW"
IRI_BASE = "http://awesome.org/"
FINAL_TTL = "aksw_doap.ttl"

# Base prefixes for Turtle
BASE_PREFIXES = """@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

def fetch_aksw_repos(org=ORG):
    """Fetch all public repository clone URLs for a GitHub organization."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        for repo in data:
            repos.append(repo["html_url"])
        page += 1
    return repos

def clean_uri(url: str) -> str:
    """Convert GitHub URL to a consistent IRI_BASE-based IRI."""
    repo_name = url.rstrip("/").split("/")[-1]
    return IRI_BASE + repo_name

def fetch_doap_graph(repo_url: str) -> Graph:
    """Fetch DOAP RDF for a repository using gitdoap's doapit."""
    graph = doapit(repo_url)

    # Replace GitHub URLs in subject/predicates with IRI_BASE
    mapping = {}
    for s, p, o in graph:
        new_s = URIRef(clean_uri(str(s))) if str(s).startswith("https://github.com/") else s
        new_o = URIRef(clean_uri(str(o))) if str(o).startswith("https://github.com/") else o
        mapping[(s, p, o)] = (new_s, p, new_o)

    cleaned_graph = Graph()
    for (s, p, o), (new_s, new_p, new_o) in mapping.items():
        cleaned_graph.add((new_s, new_p, new_o))

    return cleaned_graph

def merge_all_doap(repos, output_file=FINAL_TTL):
    """Fetch DOAP for all repos and merge into one Turtle RDF file."""
    merged_graph = Graph()
    merged_graph.parse(data=BASE_PREFIXES, format="turtle")

    for repo in repos:
        print(f"Processing {repo} ...")
        try:
            repo_graph = fetch_doap_graph(repo)
            merged_graph += repo_graph
        except Exception as e:
            print(f"Failed to fetch DOAP for {repo}: {e}")

    merged_graph.serialize(destination=output_file, format="turtle")
    print(f"\nAll DOAPs merged into {output_file}")

if __name__ == "__main__":
    repos = fetch_aksw_repos()
    merge_all_doap(repos)