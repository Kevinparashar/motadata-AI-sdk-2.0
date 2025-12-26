# Database Integration Module

## WHY

The database module provides PostgreSQL database integration with optimized connection pooling, transaction handling, and query execution. PostgreSQL is the primary database for the SDK, providing robust relational data storage with advanced features like JSON support, full-text search, and extensibility.

## WHAT

This module contains:

- **sql_db.py**: PostgreSQL database integration with connection pooling, query execution, and transaction handling. Optimized for production use with psycopg2.
- **no_sql_db.py**: NoSQL database integration (optional) for document and key-value stores like MongoDB, Cassandra, and Redis
- **vector_db.py**: Vector database integration (optional) for similarity search and embeddings storage

## HOW

Use PostgreSQL database in your application:

```python
from src.database.sql_db import PostgreSQLDatabase

# Connect to PostgreSQL
db = PostgreSQLDatabase(connection_string="postgresql://user:pass@localhost/dbname")
db.connect()

# Execute queries
results = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))

# Execute updates
db.execute_update("INSERT INTO users (name, email) VALUES (%s, %s)", ("John", "john@example.com"))

# Transactions
db.execute_transaction([
    ("INSERT INTO users (name) VALUES (%s)", ("Alice",)),
    ("UPDATE users SET status = %s WHERE name = %s", ("active", "Alice"))
])

# Create tables
db.create_table("users", {
    "id": "SERIAL PRIMARY KEY",
    "name": "VARCHAR(100) NOT NULL",
    "email": "VARCHAR(255) UNIQUE"
})
```

PostgreSQL provides a robust, production-ready database solution with advanced features and excellent performance.

## Input Validation and Error Handling

**All public methods in the database module include comprehensive input validation:**

- **PostgreSQLDatabase.__init__()**: Validates `connection_string` (string, non-empty, must start with "postgresql://" or "postgres://") and `pool_size` (positive integer)
- **PostgreSQLDatabase.execute_query()**: Validates `query` (string, 1-10000 chars) and `params` (tuple if provided)
- **PostgreSQLDatabase.execute_update()**: Validates `query` (string, 1-10000 chars) and `params` (tuple if provided)
- **PostgreSQLDatabase.execute_transaction()**: Validates `queries` (list, non-empty, each item is a tuple)
- **PostgreSQLDatabase.create_table()**: Validates `table_name` (string, 1-100 chars) and `schema` (dict, non-empty)
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
- **psycopg2-binary**: PostgreSQL database adapter for Python (connection pooling, transactions)

## Functions and Classes

### sql_db.py

- **PostgreSQLDatabase** (class): PostgreSQL database connection and operations (primary database)
  - `__init__()`: Initialize PostgreSQL database with connection_string and pool_size
  - `connect()`: Establish PostgreSQL connection with connection pooling (psycopg2)
  - `disconnect()`: Close database connection and connection pool
  - `execute_query()`: Execute a SELECT query with parameterized queries
  - `execute_update()`: Execute an INSERT/UPDATE/DELETE query
  - `execute_transaction()`: Execute multiple queries in a PostgreSQL transaction
  - `create_table()`: Create a PostgreSQL table with the given schema
  - `is_connected` (property): Check if connected to database
- **SQLDatabase** (alias): Alias for PostgreSQLDatabase for backward compatibility

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
