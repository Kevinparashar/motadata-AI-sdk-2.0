"""
Unit tests for database integrations
"""
import unittest
from src.database.sql_db import SQLDatabase
from src.database.no_sql_db import NoSQLDatabase
from src.database.vector_db import VectorDatabase


class TestSQLDatabase(unittest.TestCase):
    """Test cases for SQLDatabase"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = SQLDatabase(connection_string="sqlite:///test.db")
    
    def test_database_creation(self):
        """Test database creation"""
        self.assertIsNotNone(self.db)
        self.assertFalse(self.db.is_connected)


class TestNoSQLDatabase(unittest.TestCase):
    """Test cases for NoSQLDatabase"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = NoSQLDatabase(connection_string="mongodb://localhost", database_name="test")
    
    def test_database_creation(self):
        """Test database creation"""
        self.assertIsNotNone(self.db)
        self.assertFalse(self.db.is_connected)


class TestVectorDatabase(unittest.TestCase):
    """Test cases for VectorDatabase"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = VectorDatabase(provider="faiss")
    
    def test_database_creation(self):
        """Test database creation"""
        self.assertEqual(self.db.provider, "faiss")
        self.assertFalse(self.db.is_connected)


if __name__ == '__main__':
    unittest.main()
