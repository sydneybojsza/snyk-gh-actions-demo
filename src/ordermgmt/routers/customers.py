import uuid
from datetime import timezone, datetime, timedelta
import logging

from fastapi import APIRouter, Path, HTTPException, Request

from ordermgmt.models.order.customer import (
    OrderRequest,
    Order,
    OrderStatus,
    AddItemRequest
)
from ordermgmt.models.order.internal import (RefundItem)
from ordermgmt.routers.internal import REFUNDS

logger = logging.getLogger(__name__)


# dict[orderId, Order]
ORDERS: dict[str, Order] = dict()

router = APIRouter(
    tags=['Customer use']
)


@router.post(
    path="/customers/{customerId}/orders",
    status_code=201,
    response_model=Order,
    responses={
        400: {"description": "Bad request"},
        201: {"description": "Order placed successfully"}
    }
)
async def place_an_order(
    request: Request,
    request_body: OrderRequest,
    customer_id: str = Path(alias='customerId')
) -> Order:
    """
    Allows customers to place an order to be processed by the restaurant
    """

    if customer_id != request_body.customer_id:
        raise HTTPException(status_code=400, detail=f"Bad request, mismatched "
                                                    f"customer_ids provided in body={request_body.customer_id} "
                                                    f"and path={customer_id}")

    order_id: str = str(uuid.uuid4())
    ordered_at: datetime = datetime.now(timezone.utc)

    order: Order = Order(
        orderId=order_id,
        customerId=customer_id,
        orderedAt=ordered_at,
        menuItems=request_body.menu_items,
        status=OrderStatus.PLACED,
    )

    ORDERS[order_id] = order

    job_id = str(uuid.uuid4())

    logger.info(f"Scheduling job with job_id={job_id} to check if order is processed.")

    run_date = ordered_at + timedelta(minutes=5)

    # scheduled job will run once 5 minutes from the time the order is placed
    request.app.scheduler.add_job(
        func=check_order_expired,
        trigger='date',
        run_date=run_date,
        args=[order_id, request_body.payment_info_id],
        id=job_id,
    )

    logger.info(f"Job successfully scheduled for {run_date}")

    return order


@router.patch(
    path="/customers/{customerId}/orders/{orderId}",
    status_code=200,
    responses={
        200: {"description": "Item added successfully"},
        400: {"description": "Bad request"},
        404: {"description": "Order not found"},
    }
)
async def add_items_to_an_existing_order(
    request_body: AddItemRequest,
    customer_id: str = Path(alias='customerId'),
    order_id: str = Path(alias='orderId')
):
    """
    Allows customers to add items to an existing order
    """
    order = ORDERS.get(order_id, None)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status is not OrderStatus.PLACED:
        raise HTTPException(status_code=400, detail=f"Bad request, order status={order.status} but should be PLACED")

    if order.customer_id != customer_id:
        raise HTTPException(status_code=400, detail=f"Bad request, invalid customer_id={customer_id}")

    order.menu_items = order.menu_items + request_body.menu_items

    ORDERS[order_id] = order

    logger.info(f"Order successfully updated. order={order}")

    return order


def check_order_expired(
        order_id: str,
        payment_info_id: str
) -> bool:
    """
    Used by the scheduler to automatically reject orders that have not been
    processed after 5 minutes

    :param payment_info_id: (str) uuid4 unique payment id used to refund order
    :param order_id: (str) uuid4 unique order id used to retrieve the order
    :return: None
    """

    order = ORDERS.get(order_id)

    if order is None:
        return False

    logger.info(f"Found order with order_id={order_id}, checking if order has been processed")

    if order.status is not OrderStatus.PLACED:
        logger.info(f"Order with order_id={order_id} has already been processed")
        return False

    logger.info(f"Order has not been processed, rejecting order and adding to refunds collection. Order={order}")

    order.status = OrderStatus.REJECTED

    refund_item = REFUNDS.append(
        RefundItem(
            orderId=order_id,
            paymentInfoId=payment_info_id,
        )
    )

    ORDERS[order_id] = order

    logger.info(f"Order successfully rejected. order={order}, refundItem={refund_item}")
    return True
