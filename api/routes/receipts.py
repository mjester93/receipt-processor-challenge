# Standard Imports
import logging
import math
from typing import Annotated
from uuid import uuid4

# Third-Party Imports
from fastapi import APIRouter, HTTPException, Path, Request, status

# Local Imports
from api.validation import Receipt, ReceiptID, ReceiptPoints

router = APIRouter(prefix="/receipts", tags=["Receipts"])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("routes")


@router.post(
    "/process",
    responses={
        status.HTTP_200_OK: {"description": "Submits a receipt for processing"},
        status.HTTP_400_BAD_REQUEST: {"description": "The receipt is invalid"},
    },
)
async def process_receipt(
    request: Request,
    receipt: Receipt,
) -> ReceiptID:
    """Submits a receipt for processing."""
    receipt_id = str(uuid4())
    logger.info(f"Adding {receipt_id} to the lifecycle state")
    request.state.receipts[receipt_id] = receipt
    return ReceiptID(id=receipt_id)


def get_points_for_receipt(receipt: Receipt) -> int:
    """Calculate the number of points for a receipt.

    Args:
        receipt: A receipt object.

    Returns:
        The number of points.
    """
    points = 0

    logger.info(f"Getting the points for {receipt}")

    alnum_len = sum(1 for character in receipt.retailer if character.isalnum())
    logger.debug(f"Adding {alnum_len} points for alphanumeric characters")
    points += alnum_len

    if receipt.total[-2:] == "00":
        logger.debug("Adding 50 points because total ends in a round dollar amount")
        points += 50

    if int(receipt.total[-2:]) % 25 == 0:
        logger.debug("Adding 25 points because total is a multiple of 0.25")
        points += 25

    items_length_points = 5 * (len(receipt.items) // 2)
    logger.debug(f"Adding {items_length_points} because of the items length")
    points += items_length_points

    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            item_points = math.ceil(float(item.price) * 0.2)
            logger.debug(f"Adding {item_points} for {item}")
            points += item_points

    if receipt.purchaseDate.day % 2 == 1:
        logger.debug("Adding 6 points because the day is odd")
        points += 6

    if 14 <= receipt.purchaseTime.hour < 16:
        logger.debug("Adding 10 points because the hour is between 2pm and 4pm")
        points += 10

    return points


@router.get(
    "/{id}/points",
    description="Returns the points awarded for the receipt",
    responses={
        status.HTTP_200_OK: {"description": "The number of points awarded"},
        status.HTTP_404_NOT_FOUND: {"description": "No receipt found for that id"},
    },
)
async def get_points_by_receipt_id(
    request: Request,
    id: Annotated[
        str,
        Path(pattern=r"^\S+$"),
    ],
) -> ReceiptPoints:
    """Returns the points awarded for the receipt."""
    receipt: Receipt | None = request.state.receipts.get(id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No receipt found for that id",
        )

    points: int | None = request.state.points.get(id)
    if not points:
        logger.info(f"Points already calculated for {id}")
        points = get_points_for_receipt(receipt)
        request.state.points[id] = points

    return ReceiptPoints(points=points)
