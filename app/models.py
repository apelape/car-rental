
import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "magga123")

class Neo4jConnection:

    def __init__(self):
        self.__driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        with self.__driver.session(database=db) as session:
            result = session.run(query, parameters)
            return [dict(record) for record in result]

if __name__ == "__main__":
    db = Neo4jConnection()

db = Neo4jConnection()

print("URI:", os.getenv("NEO4J_URI"))
print("User:", os.getenv("NEO4J_USER"))
print("Password:", os.getenv("NEO4J_PASSWORD"))
