# Standard Imports
from datetime import date, time
from typing import Annotated

# Third-Party Imports
from pydantic import BaseModel, Field


class ReceiptID(BaseModel):
    """Response model to return the ID of a processed endpoint."""

    id: Annotated[
        str,
        Field(
            pattern=r"^\S+$",
            examples=["adb6b560-0eef-42bc-9d16-df48f30e89b2"],
        ),
    ]


class Item(BaseModel):
    """An item."""

    shortDescription: Annotated[
        str,
        Field(
            description="The Short Product Description for the item.",
            pattern=r"^[\w\s\-]+$",
            examples=["Mountain Dew 12PK"],
        ),
    ]
    price: Annotated[
        str,
        Field(
            description="The total price payed for this item.",
            pattern=r"^\d+\.\d{2}$",
            examples=["6.49"],
        ),
    ]


class Receipt(BaseModel):
    """A receipt."""

    retailer: Annotated[
        str,
        Field(
            description="The name of the retailer or store the receipt is from.",
            pattern=r"^[\w\s\-&]+$",
            examples=["M&M Corner Market"],
        ),
    ]
    purchaseDate: Annotated[
        date,
        Field(
            description="The date of the purchase printed on the receipt.",
            examples=["2022-01-01"],
        ),
    ]
    purchaseTime: Annotated[
        time,
        Field(
            description="The time of the purchase printed on the receipt. 24-hour time expected.",
            examples=["13:01"],
        ),
    ]
    items: Annotated[list[Item], Field(min_length=1)]
    total: Annotated[
        str,
        Field(
            description="The total amount paid on the receipt.",
            pattern=r"^\d+\.\d{2}$",
            examples=["6.49"],
        ),
    ]


class ReceiptPoints(BaseModel):
    """The number of points rewarded for a receipt."""

    points: Annotated[int, Field(examples=[100])]
