import logging
from fastapi import APIRouter, Query, Path, HTTPException

from ordermgmt.models.order.customer import OrderStatus, Order
from ordermgmt.models.order.restaurant import AcceptRejectRequest, OrderAction

from ordermgmt.routers.customers import ORDERS

router = APIRouter(
    tags=["Restaurant use"]
)

logger = logging.getLogger(__name__)


@router.get(path="/restaurant/orders", response_model=list[Order], status_code=200)
async def view_orders_for_a_restaurant(
    status: OrderStatus = Query()
) -> list[Order]:
    """
    Returns all orders for a restaurant, filterable by OrderStatus
    """
    logger.info(f"Returning all orders with status={status}")
    return [order for order in ORDERS.values() if order.status == status]


@router.patch(path="/restaurant/orders/{orderId}", status_code=200)
async def accept_or_reject_an_order(
    request_body: AcceptRejectRequest,
    order_id: str = Path(alias='orderId'),
):
    """
    Allows restaurant to accept or reject an order
    """
    order = ORDERS.get(order_id, None)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status is not OrderStatus.PLACED:
        raise HTTPException(
            status_code=400,
            detail=f"Bad request, order status={order.status} but should be PLACED"
        )

    match request_body.action:
        case OrderAction.ACCEPT:
            order.status = OrderStatus.ACCEPTED
            logger.info(f"Order with order_id={order_id} successfully accepted")
        case OrderAction.REJECT:
            order.status = OrderStatus.REJECTED
            logger.info(f"Order with order_id={order_id} successfully rejected")

    ORDERS[order_id] = order


