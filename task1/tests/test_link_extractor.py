import unittest
from unittest.mock import Mock, patch
from task1.scraper.link_extractor import LinkExtractor
from task1.scraper.http_client import HttpClient


class TestLinkExtractor(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=HttpClient)
        self.extractor = LinkExtractor(self.mock_client)

    def test_get_subcategories_empty_response(self):
        """Test get_subcategories with empty response"""
        self.mock_client.get.return_value = None
        result = self.extractor.get_subcategories("https://test.com")
        self.assertEqual(result, [])

    def test_get_product_links_empty_response(self):
        """Test get_product_links with empty response"""
        self.mock_client.get.return_value = None
        result = self.extractor.get_product_links("https://test.com", "Test")
        self.assertEqual(result, [])

    @patch('task1.scraper.link_extractor.html')
    def test_get_subcategories_with_valid_response(self, mock_html):
        """Test get_subcategories with valid HTML response"""
        mock_response = Mock()
        mock_response.content = b"<html><a href='/categories/test'>Test</a></html>"
        self.mock_client.get.return_value = mock_response
        
        mock_tree = Mock()
        mock_tree.xpath.return_value = ['/categories/test']
        mock_html.fromstring.return_value = mock_tree
        
        result = self.extractor.get_subcategories("https://test.com")
        self.assertEqual(len(result), 1)
        self.assertIn("https://www.vendr.com/categories/test", result)

    @patch('task1.scraper.link_extractor.html')
    def test_get_product_links_with_valid_response(self, mock_html):
        """Test get_product_links with valid HTML response"""
        mock_response = Mock()
        mock_response.content = b"<html><a href='/marketplace/test'>Test</a></html>"
        self.mock_client.get.return_value = mock_response
        
        mock_tree = Mock()
        mock_card = Mock()
        mock_card.get.return_value = '/marketplace/test'
        mock_card.xpath.side_effect = [['Test Product'], ['Test Description']]
        mock_tree.xpath.return_value = [mock_card]
        mock_html.fromstring.return_value = mock_tree
        
        result = self.extractor.get_product_links("https://test.com", "Test")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Product')
        self.assertEqual(result[0]['url'], 'https://www.vendr.com/marketplace/test')


if __name__ == '__main__':
    unittest.main()
