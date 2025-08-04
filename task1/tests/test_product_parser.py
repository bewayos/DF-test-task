import unittest
from unittest.mock import Mock, patch
from task1.scraper.product_parser import ProductParser
from task1.scraper.http_client import HttpClient
from task1.scraper.models import Product


class TestProductParser(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=HttpClient)
        self.parser = ProductParser(self.mock_client)

    def test_parse_product_page_empty_response(self):
        """Test parse_product_page with empty response"""
        self.mock_client.get.return_value = None
        result = self.parser.parse_product_page("https://test.com", "Test", {})
        self.assertIsNone(result)

    @patch('task1.scraper.product_parser.html')
    def test_parse_product_page_with_valid_response(self, mock_html):
        """Test parse_product_page with valid HTML response"""
        mock_response = Mock()
        mock_response.content = b"<html><h1>Test Product</h1><p>Test Description</p></html>"
        self.mock_client.get.return_value = mock_response

        mock_tree = Mock()

        def xpath_mock(path):
            if 'rt-Heading' in path:
                return ['Test Product']
            elif 'rt-Text' in path:
                return ['Test Description']
            return []

        mock_tree.xpath.side_effect = xpath_mock
        mock_html.fromstring.return_value = mock_tree

        with patch.object(self.parser, 'parse_price', return_value='$100'):
            result = self.parser.parse_product_page("https://test.com", "Test", {})

        self.assertIsInstance(result, Product)
        self.assertEqual(result.name, 'Test Product')
        self.assertEqual(result.category, 'Test')
        self.assertEqual(result.median_price, '$100')
        self.assertEqual(result.description, 'Test Description')
        self.assertEqual(result.url, 'https://test.com')


    @patch('task1.scraper.product_parser.html')
    def test_parse_product_page_fallback_to_base_info(self, mock_html):
        """Test parse_product_page with fallback to base_info when parsing fails"""
        mock_response = Mock()
        mock_response.content = b"<html></html>"
        self.mock_client.get.return_value = mock_response

        mock_tree = Mock()
        mock_tree.xpath.return_value = []
        mock_html.fromstring.return_value = mock_tree

        base_info = {
            "name": "Fallback Name",
            "description": "Fallback Description"
        }

        with patch.object(self.parser, 'parse_price', return_value='Unknown'):
            result = self.parser.parse_product_page("https://test.com", "Test", base_info)

        self.assertIsInstance(result, Product)
        self.assertEqual(result.name, 'Fallback Name')
        self.assertEqual(result.description, 'Fallback Description')

    def test_parse_price_with_valid_price(self):
        """Test parse_price with valid price in HTML"""
        mock_tree = Mock()
        mock_tree.xpath.return_value = ['$100']
        result = self.parser.parse_price(mock_tree)
        self.assertEqual(result, '$100')

    def test_parse_price_no_price_found(self):
        """Test parse_price when no price is found"""
        mock_tree = Mock()
        mock_tree.xpath.return_value = []
        result = self.parser.parse_price(mock_tree)
        self.assertEqual(result, 'Unknown')


if __name__ == '__main__':
    unittest.main()
