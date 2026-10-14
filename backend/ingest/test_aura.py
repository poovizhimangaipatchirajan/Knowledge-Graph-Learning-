import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI", "")
user = os.getenv("NEO4J_USERNAME", "")
pwd = os.getenv("NEO4J_PASSWORD", "")

print("=== CHECKING CONFIGURATION ===")
print(f"URI: {uri}")
print(f"USERNAME: {user}")
print(f"PASSWORD: {'*' * len(pwd) if pwd else 'NOT SET'}")

# Extract hostname and port
import re
import socket

clean_host = re.sub(r"^[a-zA-Z0-9\+\-]+://", "", uri).split(":")[0].split("/")[0]
port = 7687
if ":" in uri.replace("://", ""):
    try:
        port = int(uri.split(":")[-1].split("/")[0])
    except ValueError:
        port = 7687

print(f"\nTarget Host: {clean_host} | Port: {port}")

# Test raw TCP socket connection
print("\n--- 1. Testing Raw TCP Socket ---")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5.0)
try:
    s.connect((clean_host, port))
    print(f"SUCCESS: Port {port} on {clean_host} is reachable!")
    s.close()
except Exception as e:
    print(f"FAILED to reach port {port}: {e}")
    print("-> If local: Neo4j server is stopped or port 7687 is blocked.")
    print("-> If AuraDB: Database is paused or firewall/VPN blocks outbound port 7687.")

# Test Neo4j driver protocols
print("\n--- 2. Testing Neo4j Drivers ---")
from neo4j import GraphDatabase

schemes_to_try = [
    uri,
    uri.replace("neo4j+s://", "bolt+s://").replace("neo4j+ssc://", "bolt+ssc://"),
    uri.replace("neo4j+s://", "neo4j+ssc://"),
    uri.replace("neo4j+s://", "bolt+ssc://")
]

for test_uri in list(dict.fromkeys(schemes_to_try)):
    print(f"\nTrying URI: {test_uri}")
    try:
        with GraphDatabase.driver(test_uri, auth=(user, pwd)) as d:
            d.verify_connectivity()
            print(">>> CONNECTED SUCCESSFULLY! <<<")
            print(f"USE THIS WORKING URI IN YOUR .env: NEO4J_URI=\"{test_uri}\"")
            break
    except Exception as err:
        print(f"Failed: {err}")