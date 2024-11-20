# Standard Imports
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, TypedDict

# Third-Party Imports
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Local Imports
from api.routes.receipts import router
from api.validation import Receipt


class State(TypedDict):
    """Lifespan state to be used on requests."""

    receipts: dict[str, Receipt]
    points: dict[str, int | None]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    """Load an in-memory dictionary to hold receipts.

    Args:
        app: The FastAPI applications, not currently used.

    Yields:
        An empty State instance.
    """
    yield {"receipts": {}, "points": {}}


application = FastAPI(
    title="Receipt Processor",
    description="A simple receipt processor",
    lifespan=lifespan,
)
application.include_router(router)


@application.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Change the status of pydantic validation errors from 422 to 400."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )
