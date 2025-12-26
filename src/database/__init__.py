"""
Database integrations - PostgreSQL (primary), NoSQL and Vector DBs (optional)
"""
from .sql_db import SQLDatabase, PostgreSQLDatabase
from .no_sql_db import NoSQLDatabase, MongoDBDatabase, CassandraDatabase
from .vector_db import VectorDatabase, FAISSDatabase, PineconeDatabase

__all__ = [
    "SQLDatabase",  # Alias for PostgreSQLDatabase
    "PostgreSQLDatabase",  # Primary database
    "NoSQLDatabase",  # Optional
    "MongoDBDatabase",  # Optional
    "CassandraDatabase",  # Optional
    "VectorDatabase",  # Optional
    "FAISSDatabase",  # Optional
    "PineconeDatabase",  # Optional
]
