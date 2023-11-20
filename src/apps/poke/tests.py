import unittest
from unittest.mock import Mock, patch

from apps.poke.utils import get_all_berry


class TestGetAllBerry(unittest.TestCase):
    @patch("apps.poke.utils.requests.get")
    def test_get_all_berry_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 10,
            "next": "some_url",
            "previous": None,
            "results": ["berry1", "berry2"],
        }
        mock_get.return_value = mock_response

        result = get_all_berry()
        self.assertIsNotNone(result)
        self.assertEqual(result["count"], 10)
        self.assertEqual(result["next"], "some_url")
        self.assertIsNone(result["previous"])
        self.assertEqual(result["results"], ["berry1", "berry2"])

    @patch("apps.poke.utils.requests.get")
    def test_get_all_berry_invalid_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_all_berry()
        self.assertIsNone(result)
