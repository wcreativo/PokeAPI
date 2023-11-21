import unittest
from unittest.mock import Mock, patch

from ..utils import get_all_berry


class TestGetAllBerry(unittest.TestCase):
    @patch("apps.poke.utils.requests.get")
    def test_get_all_berry_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{"name": "cheri", "url": "https://pokeapi.co/api/v2/berry/1/"}],
        }
        mock_get.return_value = mock_response

        data = get_all_berry()
        assert len(data) == 1
        assert isinstance(data[0], dict)

    @patch("apps.poke.utils.requests.get")
    def test_get_all_berries_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400

        data = get_all_berry()
        assert data == []
