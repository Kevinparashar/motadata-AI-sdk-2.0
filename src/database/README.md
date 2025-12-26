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

## Input Validation and Error Handling

**All public methods in the database module include comprehensive input validation:**

- **SQLDatabase.__init__()**: Validates `connection_string` (string, non-empty) and `pool_size` (positive integer)
- **SQLDatabase.execute_query()**: Validates `query` (string, 1-10000 chars) and `params` (tuple if provided)
- **SQLDatabase.execute_update()**: Validates `query` (string, 1-10000 chars) and `params` (tuple if provided)
- **SQLDatabase.execute_transaction()**: Validates `queries` (list, non-empty, each item is a tuple)
- **SQLDatabase.create_table()**: Validates `table_name` (string, 1-100 chars) and `schema` (dict, non-empty)
- **NoSQLDatabase.__init__()**: Validates `connection_string` (string, non-empty) and `database_name` (string, 1-100 chars)
- **NoSQLDatabase.insert_one()**: Validates `collection` (string, 1-100 chars) and `document` (dict)
- **NoSQLDatabase.insert_many()**: Validates `collection` (string, 1-100 chars) and `documents` (list, non-empty)
- **NoSQLDatabase.find_one/find_many()**: Validates `collection` (string, 1-100 chars) and `filter` (dict if provided)
- **NoSQLDatabase.update_one()**: Validates `collection` (string, 1-100 chars), `filter` (dict), and `update` (dict)
- **NoSQLDatabase.delete_one()**: Validates `collection` (string, 1-100 chars) and `filter` (dict)
- **VectorDatabase.__init__()**: Validates `provider` (string, 1-50 chars) and `api_key` (string if provided)
- **VectorDatabase.upsert()**: Validates `vectors` (list, non-empty), `ids` (list, non-empty, same length as vectors), and `metadata` (list if provided)
- **VectorDatabase.search()**: Validates `query_vector` (list, non-empty), `top_k` (positive integer), and `filter` (dict if provided)
- **VectorDatabase.delete()**: Validates `ids` (list, non-empty)

**Custom Exceptions Used:**
- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `DatabaseError`: Database operation failures (replaces generic exceptions)
- `ConnectionError`: Connection failures (replaces built-in `ConnectionError`)

All methods raise appropriate custom exceptions with detailed error messages and context information for debugging.

## Libraries
This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Dict, Any, List, Optional, Tuple)
- **abc**: Abstract base classes (ABC, abstractmethod) for defining database interfaces
- **threading**: Thread synchronization primitives (Lock) for thread-safe database operations

## Functions and Classes

### sql_db.py
- **SQLDatabase** (class): SQL database connection and operations
  - `__init__()`: Initialize database with connection_string and pool_size
  - `connect()`: Establish database connection
  - `disconnect()`: Close database connection
  - `execute_query()`: Execute a SELECT query
  - `execute_update()`: Execute an INSERT/UPDATE/DELETE query
  - `execute_transaction()`: Execute multiple queries in a transaction
  - `create_table()`: Create a table with the given schema
  - `is_connected` (property): Check if connected to database
- **PostgreSQLDatabase** (class): PostgreSQL-specific database implementation
- **MySQLDatabase** (class): MySQL-specific database implementation

### no_sql_db.py
- **NoSQLDatabase** (class): Base NoSQL database connection and operations
  - `__init__()`: Initialize database with connection_string and database_name
  - `connect()`: Establish database connection
  - `disconnect()`: Close database connection
  - `insert_one()`: Insert a single document
  - `insert_many()`: Insert multiple documents
  - `find_one()`: Find a single document
  - `find_many()`: Find multiple documents
  - `update_one()`: Update a single document
  - `delete_one()`: Delete a single document
  - `is_connected` (property): Check if connected to database
- **MongoDBDatabase** (class): MongoDB-specific database implementation
- **CassandraDatabase** (class): Cassandra-specific database implementation

### vector_db.py
- **VectorDatabase** (class): Base vector database for similarity search
  - `__init__()`: Initialize vector database with provider, api_key, and config
  - `connect()`: Establish connection to vector database
  - `disconnect()`: Close connection to vector database
  - `upsert()`: Upsert vectors into the database
  - `search()`: Search for similar vectors
  - `delete()`: Delete vectors by IDs
  - `get_stats()`: Get database statistics
  - `is_connected` (property): Check if connected to vector database
- **FAISSDatabase** (class): FAISS vector database implementation
  - `save_index()`: Save FAISS index to disk
  - `load_index()`: Load FAISS index from disk
- **PineconeDatabase** (class): Pinecone vector database implementation
  - `create_index()`: Create a new Pinecone index

