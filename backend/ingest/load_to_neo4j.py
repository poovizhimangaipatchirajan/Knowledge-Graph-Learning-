import json
import os

from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)
def load_schemes():

    with open(
        "data/schemes.json",
        "r",
        encoding="utf-8"
    ) as f:

        schemes = json.load(f)

    with driver.session() as session:

        for scheme in schemes:

            session.run(
                """
                MERGE (s:Scheme {
                    name:$name
                })

                SET s.description=$description,
                    s.funding=$funding

                MERGE (b:Beneficiary {
                    name:$beneficiary
                })

                MERGE (t:BenefitType {
                    name:$benefit_type
                })

                MERGE (s)-[:FOR]->(b)

                MERGE (s)-[:OFFERS]->(t)

                """,

                name=scheme["title"],
                description=scheme["description"],
                funding=scheme["funding"],
                beneficiary=scheme["beneficiary"],
                benefit_type=scheme["benefit_type"]
            )

    print("Knowledge Graph Loaded Successfully")

if __name__ == "__main__":
    load_schemes()