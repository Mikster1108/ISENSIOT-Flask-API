import http
import unittest

from app import app


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()


class TestSensorData(BaseTestCase):

    def test_sensor_data(self):
        response = self.client.get("/sensor_data", follow_redirects=True)
        assert response.status_code == http.HTTPStatus.OK

