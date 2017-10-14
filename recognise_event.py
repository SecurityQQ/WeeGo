import base64
import io
import json

import requests
from rdflib.graph import Graph
from requests.auth import HTTPBasicAuth

def getOrgCommercial(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Org:Commercial .
              ?fact_id Basic:label ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getOrgEntertainment(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Org:Entertainment .
              ?fact_id Basic:label ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getPointOfTime(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Time:PointOfTime .
              ?fact_id Basic:label ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getGeographicalRegion(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Geo:GeographicalRegion .
              ?fact_id Basic:identifier ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getGeoInhabitedLocality(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Geo:InhabitedLocality .
              ?fact_id Basic:identifier ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getGeoCapital(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Geo:Capital .
              ?fact_id Basic:identifier ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getPlacementObject(graph):
    try:
        where = graph.query(
            """SELECT DISTINCT ?label
            WHERE {
              ?fact_id rdf:type Placement:Placement .
              ?fact_id Placement:placement_object ?object_id .
              ?object_id Basic:label ?label
           }
           GROUP BY ?fact_id """)
    except Exception:
        return []
    where_facts = []
    for row in where:
        if str(row["label"]) != 'None':
            where_facts.append(str(row["label"]))
    return where_facts

def getGraphFromText(text):
    text = text.encode('utf-8')
    text = base64.b64encode(text)
    comprenoData = {
        "Source": {
        "Extension": "TXT",
        "TxtEncoding": "utf-8",
        "Content": str(text, encoding='ascii')
    },
        "SourceLanguage": "en-US",
        "ProcessingParameters": {
            "ProcessingTimeout": 600000,
            "HtmlParsingMode": "None",
            "MaxSymbolsCount": 0
        },
        "Operations": {
            "EntitiesAndFactsExtraction": {
                "ModelName": "Extended",
            },
            "FiltrationParameters": {
                "Ontologies": [
                    "http://www.abbyy.com/ns/BasicEntity#",
                    "http://www.abbyy.com/ns/BasicFact#"
                ]
            }
        },
    }
    jsonRequest = json.dumps(comprenoData, skipkeys=True)
    newSession = requests.session()
    response = newSession.post("http://infoextractorapitest.abbyy.com/api/tasks?async=false", data=jsonRequest,
          headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}, auth=HTTPBasicAuth(('ABBYY_Labs'),
          ('ABBYY_Labs_password')))
    currentGraph = Graph()
    fakeFile = io.StringIO(response.text)
    # print(response.text)
    currentGraph.parse(fakeFile)
    return currentGraph

def recogniseEvent(text):
    graph = getGraphFromText(text)
    result = dict()
    result['what'] = getOrgCommercial(graph) + getOrgEntertainment(graph) # + getPlacementObject(graph)
    result['when'] = getPointOfTime(graph)
    result['where'] = getGeographicalRegion(graph) + getGeoInhabitedLocality(graph) + getGeoCapital(graph)
    return result

# Ok:
# I want to be in Barcelona tomorrow
# I want to go to bar
# I want to go to cinema
# Let's go to the bar
# I want to go to the theatre.
# I want to go to the club 21.10.17.
# I want to go to Africa

# Not ok:
# I was in the club - problem (also found as an event)

if __name__ == "__main__":
    result = recogniseEvent("I want to go to the club 21.10.17.")
    print(result)

