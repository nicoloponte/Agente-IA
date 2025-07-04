# tests/test_database_query.py
import pytest
import sqlite3
from agent.tools.database_query import DatabaseQueryTool

def test_database_query_tool():
    conn = sqlite3.connect("jaime.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test (name) VALUES ('test')")
    conn.commit()
    conn.close()

    tool = DatabaseQueryTool()
    result = tool.run("SELECT * FROM test")
    assert "(1, 'test')" in str(result) # Aserción corregida