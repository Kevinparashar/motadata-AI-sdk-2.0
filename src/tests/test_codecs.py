"""
Unit tests for codecs
"""
import unittest
from src.codecs.custom_codec import JSONCodec, Base64Codec, CustomCodec
from src.codecs.codec_utils import get_codec, list_codecs


class TestJSONCodec(unittest.TestCase):
    """Test cases for JSONCodec"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.codec = JSONCodec()
    
    def test_encode_decode(self):
        """Test encoding and decoding"""
        data = {"key": "value", "number": 42}
        encoded = self.codec.encode(data)
        decoded = self.codec.decode(encoded)
        self.assertEqual(decoded, data)


class TestBase64Codec(unittest.TestCase):
    """Test cases for Base64Codec"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.codec = Base64Codec()
    
    def test_encode_decode(self):
        """Test encoding and decoding"""
        data = "test string"
        encoded = self.codec.encode(data)
        decoded = self.codec.decode(encoded)
        self.assertEqual(decoded, data)


class TestCustomCodec(unittest.TestCase):
    """Test cases for CustomCodec"""
    
    def test_codec_creation(self):
        """Test custom codec creation"""
        codec = CustomCodec(format="json")
        self.assertIsNotNone(codec)
    
    def test_get_codec(self):
        """Test getting codec from registry"""
        codec = get_codec("json")
        self.assertIsNotNone(codec)
    
    def test_list_codecs(self):
        """Test listing codecs"""
        codecs = list_codecs()
        self.assertIsInstance(codecs, list)
        self.assertGreater(len(codecs), 0)


if __name__ == '__main__':
    unittest.main()
