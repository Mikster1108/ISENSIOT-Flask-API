import http.client
import json
import os
import unittest
from faker import Faker
from werkzeug.security import generate_password_hash

os.environ["FLASK_TEST_ENV"] = "test"   # Variable needs to be set before importing app to use test database

from app import app
from app_setup import user_datastore, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_datastore = user_datastore
        self.faker = Faker()
        self.headers = {'Content-Type': 'application/json'}

    def get_random_user(self, password, email=None):
        with app.app_context():
            with app.test_request_context():
                if not email:
                    email = self.faker.email()

                user = user_datastore.create_user(
                    email=email,
                    password=generate_password_hash(password)
                )

                db.session.commit()
                db.session.refresh(user)
        return user

    def login_as_normal_user(self, password, user=None):
        if not user:
            user = self.get_random_user(password=password)

        data = json.dumps({"email": user.email, "password": password})

        response = self.client.post(f"/user/login", data=data, headers=self.headers)
        token = json.loads(response.data).get('token')

        return token


class TestAuthentication(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_path = "/user"

    def test_should_return_status_200_when_logging_in_using_valid_credentials(self):
        password = "valid_credentials"

        user = self.get_random_user(password=password)
        data = json.dumps({"email": user.email, "password": password})

        response = self.client.post(f"/user/login", data=data, headers=self.headers)

        assert response.status_code == http.client.OK

    def test_should_return_status_400_when_logging_in_using_invalid_credentials(self):
        pass

    def test_should_return_status_201_when_registering_using_valid_details(self):
        pass

    def test_should_return_status_400_when_registering_using_wrong_access_code(self):
        pass

    def test_should_return_status_401_when_requesting_sensor_data_while_not_logged_in(self):
        pass

    def test_should_return_status_401_when_requesting_sensor_data_using_false_token(self):
        pass


class TestSensorData(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.token = self.login_as_normal_user(password='sensor_data')
        self.headers.update({'Authorization': f'Bearer {self.token}'})
        self.base_path = '/sensor_data'

    def test_should_return_status_200_when_requesting_sensor_data(self):
        response = self.client.get(f"{self.base_path}", follow_redirects=True, headers=self.headers)
        assert response.status_code == http.client.OK


if __name__ == "__main__":
    unittest.main()
