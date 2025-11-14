import unittest
from unittest.mock import patch, Mock

from processor.image_processor import process_thumbnails

class TestImageProcessor(unittest.TestCase):

    @patch('processor.image_processor.requests.Session.get')
    @patch('processor.image_processor.Image.open')
    def test_process_thumbnails_success(self, mock_image_open, mock_requests_get):
        
        # Config Mocks
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'fake-image-bytes'
        mock_requests_get.return_value = mock_response
        
        mock_img = Mock()

        def save_to_buffer(buffer, format):
            buffer.write(b'fake-thumbnail-bytes')
        
        mock_img.save = save_to_buffer
        mock_image_open.return_value.__enter__.return_value = mock_img
        
        urls = ['/img1.png']
        base_url = 'http://example.com'
        results = process_thumbnails(base_url, urls)
        
        # 'ZmFrZS10aHVtYm5haWwtYnl0ZXM=' es 'fake-thumbnail-bytes' en base64
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 'ZmFrZS10aHVtYm5haWwtYnl0ZXM=')
        
        # Verificar que se llamó a requests con la URL absoluta
        mock_requests_get.assert_called_with(
            'http://example.com/img1.png', timeout=5
        )
        # Verificar que se generó el thumbnail
        mock_img.thumbnail.assert_called_with((128, 128))

    @patch('processor.image_processor.requests.Session.get')
    def test_process_thumbnails_fails(self, mock_requests_get):
        # Simular un error de red
        mock_requests_get.side_effect = Exception("Timeout")
        
        results = process_thumbnails('http://example.com', ['/img1.png'])
        
        self.assertEqual(len(results), 0)