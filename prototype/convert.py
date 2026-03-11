from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, SKOS

# namespaces
BASE = "http://awesome.org/iipc/"
NEW_BASE = "http://awesome.org/iipc/categories/"

EX = Namespace("http://awesome.org/schema#")

g = Graph()
g.parse("awesome.ttl", format="turtle")

new_graph = Graph()

# store mapping oldIRI -> newIRI
iri_map = {}

for concept in g.subjects(RDF.type, SKOS.Concept):

    iri_str = str(concept)

    if "#" in iri_str:
        slug = iri_str.split("#")[1]
    else:
        slug = iri_str.split("/")[-1]

    new_iri = URIRef(NEW_BASE + slug)

    iri_map[concept] = new_iri

# rewrite triples
for s, p, o in g:

    if s in iri_map:
        s = iri_map[s]

    if o in iri_map:
        o = iri_map[o]

    new_graph.add((s, p, o))

# classify Category / SubCategory
for concept, new_iri in iri_map.items():

    parent = list(g.objects(concept, SKOS.broader))

    if parent:
        new_graph.add((new_iri, RDF.type, EX.SubCategory))
    else:
        new_graph.add((new_iri, RDF.type, EX.Category))

# write result
new_graph.serialize("awesome_new.ttl", format="turtle")

print("Converted graph written to awesome_new.ttl")