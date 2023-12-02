import os


def in_testing_mode():
    return os.getenv("FLASK_TEST_ENV") == "test"

