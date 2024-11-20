# Standard Imports
from typing import Any
from unittest.mock import Mock, patch

# Third-Party Imports
import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_get_receipt_id_points_missing_id(client: TestClient) -> None:
    """Assert the GET receipts/{id}/points returns a 404."""
    with client:
        response = client.get("/receipts/missing-id/points")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No receipt found for that id"


def test_post_receipts_process_validation_error(client: TestClient) -> None:
    """Assert the POST receipts/process returns a 400 on invalid requests."""
    with client:
        response = client.post(
            "/receipts/process",
            json={"retailer": ""},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] is not None


@patch("api.routes.receipts.get_points_for_receipt")
def test_state_keeps_points(
    mock_get_points: Mock,
    client: TestClient,
) -> None:
    """Assert the function to calculate points only happens once per ID."""
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
        ],
        "total": "9.00",
    }
    with client:
        post_response = client.post("/receipts/process", json=receipt)
        receipt_id = post_response.json()["id"]
        client.get(f"/receipts/{receipt_id}/points")
        client.get(f"/receipts/{receipt_id}/points")
        mock_get_points.assert_called_once()


@pytest.mark.parametrize(
    ("receipt", "expected_points"),
    [
        (
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            },
            109,
        ),
        (
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            },
            28,
        ),
        (
            {
                "retailer": "Walgreens",
                "purchaseDate": "2022-01-02",
                "purchaseTime": "08:13",
                "total": "2.65",
                "items": [
                    {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                    {"shortDescription": "Dasani", "price": "1.40"},
                ],
            },
            15,
        ),
        (
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-02",
                "purchaseTime": "13:13",
                "total": "1.25",
                "items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
            },
            31,
        ),
    ],
    ids=[
        "M&M Corner Market",
        "Target with multiple items",
        "Morning receipt",
        "Simple receipt",
    ],
)
def test_receipt_end_to_end(
    receipt: dict[str, Any],
    expected_points: int,
    client: TestClient,
) -> None:
    """Submit and validation multiple receipts."""
    with client:
        post_response = client.post("/receipts/process", json=receipt)
        assert post_response.status_code == status.HTTP_200_OK
        receipt_id = post_response.json()["id"]
        assert receipt_id is not None

        get_response = client.get(f"/receipts/{receipt_id}/points")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json() == {"points": expected_points}
