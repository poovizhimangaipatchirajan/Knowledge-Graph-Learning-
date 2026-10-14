import json
import networkx as nx
import pickle

G = nx.Graph()

with open(
    "data/schemes.json",
    "r",
    encoding="utf-8"
) as f:

    schemes = json.load(f)

for scheme in schemes:

    scheme_name = scheme["title"]

    G.add_node(
    scheme_name,
    type="Scheme",
    description=scheme.get("description", ""),
    funding=scheme.get("funding", ""),
    beneficiary=scheme.get("beneficiary", ""),
    benefit_type=scheme.get("benefit_type", "")
    )


    beneficiary = scheme["beneficiary"]

    G.add_node(
        beneficiary,
        type="Beneficiary"
    )

    G.add_edge(
        scheme_name,
        beneficiary,
        relation="FOR"
    )

    benefit = scheme["benefit_type"]

    G.add_node(
        benefit,
        type="Benefit"
    )

    G.add_edge(
        scheme_name,
        benefit,
        relation="OFFERS"
    )

with open(
    "data/knowledge_graph.pkl",
    "wb"
) as f:

    pickle.dump(G, f)

print(
    "Knowledge Graph Created"
)

print(
    "Nodes:",
    len(G.nodes())
)

print(
    "Edges:",
    len(G.edges())
)