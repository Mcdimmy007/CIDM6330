import os
import unittest


from barkylib.config import (
    get_sqlite_file_url,
    get_sqlite_memory_uri,
    get_postgres_uri,
    get_api_url,
    get_redis_host_and_port,
    get_email_host_and_port,
)


class TestConfig(unittest.TestCase):
    def test_get_sqlite_file_url(self):
        self.assertEqual(get_sqlite_file_url(), "sqlite:///bookmarks.db")

    def test_get_postgres_uri(self):
        os.environ["DB_HOST"] = "example.com"
        os.environ["DB_PASSWORD"] = "testpassword"
        self.assertEqual(get_postgres_uri(), "postgresql://allocation:testpassword@example.com:5432/allocation")
        del os.environ["DB_HOST"]
        del os.environ["DB_PASSWORD"]

    def test_get_api_url(self):
        os.environ["API_HOST"] = "example.com"
        self.assertEqual(get_api_url(), "http://example.com:80")
        del os.environ["API_HOST"]

    def test_get_redis_host_and_port(self):
        os.environ["REDIS_HOST"] = "example.com"
        self.assertEqual(get_redis_host_and_port(), dict(host="example.com", port=6379))
        del os.environ["REDIS_HOST"]

    def test_get_email_host_and_port(self):
        os.environ["EMAIL_HOST"] = "example.com"
        self.assertEqual(get_email_host_and_port(), dict(host="example.com", port=1025, http_port=8025))
        del os.environ["EMAIL_HOST"]