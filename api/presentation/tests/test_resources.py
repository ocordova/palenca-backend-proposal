from fastapi import status
from fastapi.testclient import TestClient

from api.app import create_app

client = TestClient(create_app())


def test_get_health_check_resource():

    result = client.get("/health")
    expected = {"status": 200}

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected
