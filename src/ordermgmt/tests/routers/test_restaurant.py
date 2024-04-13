import pytest
import mock
from fastapi.testclient import TestClient
from pydantic import parse_obj_as

from ordermgmt.models.order.customer import Order, OrderStatus
from ordermgmt.models.order.restaurant import AcceptRejectRequest, OrderAction


@pytest.fixture()
def accept_request() -> AcceptRejectRequest:
    return AcceptRejectRequest(
        action=OrderAction.ACCEPT
    )


@pytest.fixture()
def reject_request() -> AcceptRejectRequest:
    return AcceptRejectRequest(
        action=OrderAction.REJECT
    )


@pytest.mark.parametrize(
    "status, order_id",
    [
        pytest.param(OrderStatus.REJECTED, "some_order_id_03"),
        pytest.param(OrderStatus.ACCEPTED, "some_order_id_02"),
        pytest.param(OrderStatus.PLACED, "some_order_id_01"),
    ]
)
def test_view_orders_for_a_restaurant(
        test_app: TestClient,
        orders: dict[str, Order],
        status: OrderStatus,
        order_id: str,
        caplog,
):
    with mock.patch.dict('ordermgmt.routers.restaurant.ORDERS', orders):

        response = test_app.get(
            url="/restaurant/orders",
            params={"status": status.value}
        )

        assert response.status_code == 200
        assert f"Returning all orders with status={status}" in caplog.text


def test_accept_an_order_success(
        test_app: TestClient,
        accept_request: AcceptRejectRequest,
        orders: dict[str, Order],
        caplog,
):
    json = accept_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.restaurant.ORDERS', orders):

        response = test_app.patch(
            url=f"/restaurant/orders/some_order_id_01",
            json=json
        )

        assert "Order with order_id=some_order_id_01 successfully accepted" in caplog.text
        assert response.status_code == 200


def test_reject_an_order_success(
        test_app: TestClient,
        reject_request: AcceptRejectRequest,
        orders: dict[str, Order],
        caplog,
):
    json = reject_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.restaurant.ORDERS', orders):

        response = test_app.patch(
            url=f"/restaurant/orders/some_order_id_01",
            json=json
        )

        assert "Order with order_id=some_order_id_01 successfully rejected" in caplog.text
        assert response.status_code == 200


def test_accept_reject_order_not_placed(
        test_app: TestClient,
        reject_request: AcceptRejectRequest,
        orders: dict[str, Order],
        caplog,
):
    json = reject_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.restaurant.ORDERS', orders):

        response = test_app.patch(
            url=f"/restaurant/orders/some_order_id_02",
            json=json
        )

        assert "Order with order_id=some_order_id_01 successfully rejected" not in caplog.text
        assert response.status_code == 400


def test_accept_reject_order_not_found(
        test_app: TestClient,
        reject_request: AcceptRejectRequest,
        orders: dict[str, Order],
        caplog,
):
    json = reject_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.restaurant.ORDERS', orders):

        response = test_app.patch(
            url=f"/restaurant/orders/some_non_existent_order",
            json=json
        )

        assert "Order with order_id=some_non_existent_order successfully rejected" not in caplog.text
        assert response.status_code == 404
