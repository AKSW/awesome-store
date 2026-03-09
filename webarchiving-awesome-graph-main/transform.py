from rdflib import Graph

g = Graph()
g.parse("awesome.ttl")

queryProject = open("queryProject.sparql").read()
queryConcept = open("queryConcept.sparql").read()

resultProject = g.query(queryProject)
resultConcept = g.query(queryConcept)

out = Graph()

for triple in resultProject:
    out.add(triple)

for triple in resultConcept:
    out.add(triple)

out.serialize("websitesNew.ttl", format="turtle")