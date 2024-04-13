import logging
from uuid import uuid4
from fastapi import APIRouter

from ordermgmt.models.order.internal import RefundItem


router = APIRouter(
    tags=["Internal use"]
)

logger = logging.getLogger(__name__)

# populate a default value for testing
REFUNDS: list[RefundItem] = [
    RefundItem(
        orderId=str(uuid4()),
        paymentInfoId=str(uuid4())
        )
    ]


@router.get(path="/internal/refunds", response_model=list[RefundItem], status_code=200)
async def get_all_refund_items(
) -> list[RefundItem]:
    """
    Returns a list of all items to be refunded with their order and payment metadata
    """
    logger.info("Returning all refund items")
    return REFUNDS

