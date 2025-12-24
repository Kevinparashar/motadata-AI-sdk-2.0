# Database Integration Module

## WHY
The database module provides unified interfaces for interacting with different types of databases (SQL, NoSQL, and vector databases). This allows your application to work with various data storage solutions without being tightly coupled to a specific database technology.

## WHAT
This module contains:

- **sql_db.py**: SQL database integration for relational databases like PostgreSQL, MySQL, and SQLite. Provides connection management, query execution, and transaction handling
- **no_sql_db.py**: NoSQL database integration for document and key-value stores like MongoDB, Cassandra, and Redis. Handles document operations, collections, and schema-less data management
- **vector_db.py**: Vector database integration for similarity search and embeddings storage. Supports FAISS, Pinecone, Weaviate, and other vector databases for AI/ML applications

## HOW
Use database integrations in your application:

```python
from src.database.sql_db import SQLDatabase
from src.database.no_sql_db import NoSQLDatabase
from src.database.vector_db import VectorDatabase

# SQL Database
sql_db = SQLDatabase(connection_string="postgresql://...")
results = sql_db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))

# NoSQL Database
nosql_db = NoSQLDatabase(connection_string="mongodb://...")
document = nosql_db.find_one("users", {"id": user_id})

# Vector Database
vector_db = VectorDatabase(provider="pinecone", api_key="...")
vector_db.upsert(vectors=[...], ids=[...])
similar = vector_db.search(query_vector, top_k=10)
```

Each database type provides a consistent interface while handling provider-specific optimizations and features.

