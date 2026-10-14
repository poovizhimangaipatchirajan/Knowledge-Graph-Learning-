import os
import pickle
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# NETWORKX FALLBACK
# ==================================================

GRAPH_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "knowledge_graph.pkl"
)

G = None

if GRAPH_PATH.exists():

    try:

        with open(GRAPH_PATH, "rb") as f:
            G = pickle.load(f)

    except Exception as e:

        print(
            f"[GraphRetriever] Error loading graph: {e}"
        )

# ==================================================
# NEO4J CONNECTION
# ==================================================

driver = None

try:

    from neo4j import GraphDatabase

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    pwd = os.getenv("NEO4J_PASSWORD")

    if uri and user and pwd:

        driver = GraphDatabase.driver(
            uri,
            auth=(user, pwd)
        )

        driver.verify_connectivity()

        print(
            "[GraphRetriever] Neo4j Connected ✅"
        )

except Exception as err:

    driver = None

    print(
        f"[GraphRetriever] Neo4j unavailable: {err}"
    )

# ==================================================
# STOP WORDS
# ==================================================

STOP_WORDS = {
    "what",
    "which",
    "where",
    "when",
    "who",
    "is",
    "are",
    "the",
    "for",
    "and",
    "scheme",
    "schemes",
    "available"
}

# ==================================================
# NEO4J SEARCH
# ==================================================

def search_neo4j(query, limit=10):

    if not driver:
        return []

    tokens = [
        t.lower()
        for t in query.split()
        if len(t) > 2 and t.lower() not in STOP_WORDS
    ]

    if not tokens:
        return []

    cypher = """
    UNWIND $tokens AS token

    MATCH (s:Scheme)

    OPTIONAL MATCH (s)-[:FOR]->(b:Beneficiary)

    OPTIONAL MATCH (s)-[:OFFERS]->(t:BenefitType)

    WHERE

    toLower(s.name) CONTAINS token

    OR

    toLower(coalesce(s.description,'')) CONTAINS token

    OR

    toLower(coalesce(s.funding,'')) CONTAINS token

    OR

    toLower(coalesce(b.name,'')) CONTAINS token

    OR

    toLower(coalesce(t.name,'')) CONTAINS token

    RETURN DISTINCT

    s.name AS scheme,

    s.description AS description,

    s.funding AS funding,

    b.name AS beneficiary,

    t.name AS benefit_type,

    COLLECT(
        DISTINCT
        coalesce(
            b.name,
            t.name
        )
    ) AS related

    LIMIT $limit
    """

    try:

        with driver.session() as session:

            result = session.run(
                cypher,
                tokens=tokens,
                limit=limit
            )

            return [
                dict(record)
                for record in result
            ]

    except Exception as e:

        print(
            f"[GraphRetriever] Neo4j query failed: {e}"
        )

        return []

# ==================================================
# NETWORKX FALLBACK SEARCH
# ==================================================

def search_networkx(
    query,
    limit=10
):

    if not G:
        return []

    query_words = {

        word.lower()

        for word in query.split()

        if (
            len(word) > 2
            and word.lower() not in STOP_WORDS
        )
    }

    scored = []

    for node, data in G.nodes(data=True):

        text = f"""

        {node}

        {data.get('description','')}

        {data.get('funding','')}

        {data.get('beneficiary','')}

        {data.get('benefit_type','')}
        """.lower()

        score = sum(
            1
            for w in query_words
            if w in text
        )

        if score > 0:

            scored.append(
                (
                    score,
                    node,
                    data
                )
            )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    results = []

    for _, node, data in scored[:limit]:

        neighbors = []

        try:

            neighbors = list(
                G.neighbors(node)
            )

        except:
            pass

        results.append(
            {
                "scheme": node,
                "description": data.get(
                    "description",
                    ""
                ),
                "funding": data.get(
                    "funding",
                    ""
                ),
                "beneficiary": data.get(
                    "beneficiary",
                    ""
                ),
                "benefit_type": data.get(
                    "benefit_type",
                    ""
                ),
                "related": neighbors
            }
        )

    return results

# ==================================================
# HYBRID RETRIEVER
# ==================================================

def search_graph(query):

    results = search_neo4j(query)

    if results:

        return results

    return search_networkx(query)

# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    result = search_graph(
        "maize subsidy"
    )

    print(result)