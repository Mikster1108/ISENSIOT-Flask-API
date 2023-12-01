import http.client
import json
import os
import unittest

from dotenv import load_dotenv
from faker import Faker
from werkzeug.security import generate_password_hash

from db.create_user_roles import create_roles

os.environ["FLASK_TEST_ENV"] = "test"   # Variable needs to be set before importing app to use test database

from app import app
from app_setup import user_datastore, db, security


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_datastore = user_datastore
        self.security = security
        self.faker = Faker()
        self.headers = {'Content-Type': 'application/json'}

        create_roles()
        load_dotenv()

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
        self.access_code = os.getenv("ACCESS_CODE")

    def test_should_return_status_200_when_logging_in_using_valid_credentials(self):
        password = "valid_credentials"

        user = self.get_random_user(password=password)
        data = json.dumps({"email": user.email, "password": password})

        response = self.client.post(f"{self.base_path}/login", data=data, headers=self.headers)

        assert response.status_code == http.client.OK

    def test_should_return_status_400_when_logging_in_using_invalid_credentials(self):
        false_password = "invalid_credentials"
        actual_password = "random password"

        user = self.get_random_user(password=actual_password)
        bad_password_data = json.dumps({"email": user.email, "password": false_password})
        bad_email_data = json.dumps({"email": self.faker.email(), "password": actual_password})

        bad_password_response = self.client.post(f"{self.base_path}/login", data=bad_password_data, headers=self.headers)
        bad_email_data = self.client.post(f"{self.base_path}/login", data=bad_email_data, headers=self.headers)

        assert bad_password_response.status_code == http.client.UNAUTHORIZED
        assert bad_email_data.status_code == http.client.BAD_REQUEST

    def test_should_return_status_201_when_registering_using_valid_details(self):
        user_data = json.dumps({
            "email": self.faker.email(),
            "password": "henk03",
            "access_code": self.access_code})

        response = self.client.post(f"{self.base_path}/register", data=user_data, headers=self.headers)

        assert response.status_code == http.client.CREATED

    def test_should_return_status_400_when_registering_using_wrong_access_code(self):
        user_data = json.dumps({
            "email": self.faker.email(),
            "password": "henk03",
            "access_code": "Wrong_code"})

        response = self.client.post(f"{self.base_path}/register", data=user_data, headers=self.headers)
        assert response.status_code == http.client.BAD_REQUEST

    def test_should_return_status_401_when_requesting_sensor_data_while_not_logged_in(self):
        response = self.client.get(f"/sensor_data", follow_redirects=True, headers=self.headers)
        assert response.status_code == http.client.UNAUTHORIZED

    def test_should_return_status_401_when_requesting_sensor_data_using_false_token(self):
        headers = self.headers
        fake_token = security.remember_token_serializer.dumps("df55a3a4a2e3481a8c2b37ab70ac3736")
        headers.update({'Authorization': f'Bearer {fake_token}'})
        response = self.client.get(f"/sensor_data", follow_redirects=True, headers=headers)
        assert response.status_code == http.client.UNAUTHORIZED


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
