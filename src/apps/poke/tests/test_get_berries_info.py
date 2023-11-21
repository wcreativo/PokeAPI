import json
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from ..utils import get_all_berries_info

settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "mydatabase",
            "USER": "myuser",
            "PASSWORD": "mypassword",
            "HOST": "localhost",
            "PORT": "",
        }
    }
)


class TestBerriesInfo(TestCase):
    @patch("apps.poke.utils.redis")
    @patch("apps.poke.utils.requests")
    def test_get_all_berries_info_redis(self, mock_requests, mock_redis):
        # Simulate berries and growth_times in Redis
        mock_redis_client = mock_redis.StrictRedis.return_value
        mock_redis_client.get.side_effect = [
            json.dumps([{"name": "cheri", "url": "https://pokeapi.co/api/v2/berry/1/"}]),
            json.dumps([10]),
        ]

        # Call the function
        names, growth_times = get_all_berries_info()

        # Assertions
        self.assertIsNotNone(names)
        self.assertIsNotNone(growth_times)
        mock_requests.get.assert_not_called()
