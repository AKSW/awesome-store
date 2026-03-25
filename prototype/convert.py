from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, SKOS, FOAF
from rdflib.namespace import OWL, RDFS

# namespaces
BASE = "http://awesome.org/iipc/"
CAT_BASE = "http://awesome.org/iipc/categories/"
PROJ_BASE = "http://awesome.org/iipc/projects/"

EX = Namespace("http://awesome.org/schema#")
DOAP = Namespace("http://usefulinc.com/ns/doap#")
SIOC = Namespace("http://rdfs.org/sioc/ns#")

g = Graph()
g.parse("awesome.ttl", format="turtle")

new_graph = Graph()

# mappings
category_map = {}
project_map = {}

# convert categories
for concept in g.subjects(RDF.type, SKOS.Concept):

    iri_str = str(concept)

    if "#" in iri_str:
        slug = iri_str.split("#")[1]
    else:
        slug = iri_str.split("/")[-1]

    new_iri = URIRef(CAT_BASE + slug)

    category_map[concept] = new_iri

# convert projects
for project in g.subjects(RDF.type, SIOC.Item):

    iri_str = str(project)
    slug = iri_str.rstrip("/").split("/")[-1]

    new_iri = URIRef(PROJ_BASE + slug)

    project_map[project] = new_iri

# rewrite triples
for s, p, o in g:

    # rewrite subject
    if s in category_map:
        s = category_map[s]
    elif s in project_map:
        new_project = project_map[s]
        new_graph.add((new_project, OWL.sameAs, s))

        s = new_project

    # rewrite object
    if o in category_map:
        o = category_map[o]

    new_graph.add((s, p, o))

# classify Category / SubCategory
#for concept, new_iri in category_map.items():

#    parent = list(g.objects(concept, SKOS.broader))

#    if parent:
#        new_graph.add((new_iri, RDF.type, EX.SubCategory))
#    else:
#        new_graph.add((new_iri, RDF.type, EX.Category))

# write result
new_graph.serialize("awesome_new.ttl", format="turtle")

print("Converted graph written to awesome_new.ttl")