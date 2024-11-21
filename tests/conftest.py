# Standard Imports
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from unittest.mock import Mock

# Third-Party Imports
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Local Imports
from api.main import State, application


@pytest.fixture(name="application")
def fixture_application() -> Iterator[FastAPI]:
    """Return an instance of the application."""
    yield application


@pytest.fixture(name="client")
def fixture_client(application: FastAPI) -> TestClient:
    """Return an instance of a TestClient."""
    return TestClient(application)


@pytest.fixture(name="pending_application")
def fixture_pending_application() -> Iterator[FastAPI]:
    """Return an instance of the application where the points calculation is pending."""
    yield application


@asynccontextmanager
async def pending_lifespan(app: FastAPI) -> AsyncIterator[State]:
    """Load an in-memory dictionary to hold receipts.

    Note: This would be if the receipt is still processing the points to test
    the GET endpoint when that case happens.

    Args:
        app: The FastAPI applications, not currently used.

    Yields:
        An empty State instance.
    """
    yield {
        "receipts": {
            "adb6b560-0eef-42bc-9d16-df48f30e89b2": Mock(),
        },
        "points": {},
    }


@pytest.fixture(name="pending_client")
def fixture_pending_client(application: FastAPI) -> TestClient:
    """Return an instance of a TestClient  where the points calculation is pending."""
    application.router.lifespan_context = pending_lifespan
    return TestClient(application)
