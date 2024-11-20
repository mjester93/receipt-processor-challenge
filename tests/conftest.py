# Standard Imports
from collections.abc import Iterator

# Third-Party Imports
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Local Imports
from api.main import application


@pytest.fixture(name="application")
def fixture_application() -> Iterator[FastAPI]:
    """Return an instance of the application."""
    yield application


@pytest.fixture(name="client")
def fixture_client(application: FastAPI) -> TestClient:
    """Return an instance of a TestClient."""
    return TestClient(application)
