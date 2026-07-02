# Placeholder script to query the OKF knowledge graph using SPARQL

def query(sparql_str: str) -> str:
    print(f"Executing SPARQL query:\n{sparql_str}")
    return "[]"

if __name__ == "__main__":
    test_query = """
    SELECT ?crop ?condition WHERE {
        ?crop agri:requiresNPK ?condition .
    }
    """
    query(test_query)
