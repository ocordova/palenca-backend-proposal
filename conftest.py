import os
import pytest


def pytest_generate_tests(metafunc):
    from api.misc.env import Env, EnvName

    Env.ENVIRONMENT = EnvName.TESTING
    os.environ["FLASK_ENV"] = "test"


def set_mongoengine():
    from mongoengine import connect

    connect("mongoenginetest", host="mongomock://localhost")


def pytest_runtest_setup():
    set_mongoengine()
