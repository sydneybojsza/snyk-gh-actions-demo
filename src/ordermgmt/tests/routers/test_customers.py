import pytest
import mock
from fastapi.testclient import TestClient

from ordermgmt.models.order.customer import OrderRequest, OrderItem, Order, AddItemRequest
from ordermgmt.routers.customers import check_order_expired


@pytest.fixture()
def order_request(menu_items: list[OrderItem]) -> OrderRequest:
    return OrderRequest(
        customerId="some_customer_id",
        paymentInfoId="some_payment_info_id",
        menuItems=menu_items
    )


@pytest.fixture()
def add_item_request(menu_items: list[OrderItem]) -> AddItemRequest:
    return AddItemRequest(
        paymentInfoId="some_payment_info_id",
        menuItems=menu_items
    )


def test_place_an_order_success(
        test_app: TestClient,
        order_request: order_request,
        orders: dict[str, Order],
        caplog,
):
    json = order_request.model_dump()
    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        response = test_app.post(
            url=f"/customers/{order_request.customer_id}/orders",
            json=json
        )
        assert "Scheduling job with job_id=" in caplog.text
        assert "Job successfully scheduled" in caplog.text
        assert response.status_code == 201


def test_place_an_order_mismatched_customer_ids(
        test_app: TestClient,
        order_request: order_request,
        orders: dict[str, Order],
        caplog,
):
    json = order_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        response = test_app.post(
            url=f"/customers/customer_id_not_matching/orders",
            json=json
        )

        assert "Scheduling job with job_id=" not in caplog.text
        assert "Job successfully scheduled" not in caplog.text
        assert response.status_code == 400


def test_add_items_to_an_existing_order_success(
        test_app: TestClient,
        add_item_request: AddItemRequest,
        orders: dict[str, Order],
        caplog,
):
    json = add_item_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):

        response = test_app.patch(
            url=f"/customers/some_customer_id_01/orders/some_order_id_01",
            json=json
        )

        assert "Order successfully updated" in caplog.text
        assert response.status_code == 200


def test_add_items_to_an_existing_order_wrong_order_id(
        test_app: TestClient,
        add_item_request: AddItemRequest,
        orders: dict[str, Order],
        caplog,
):
    json = add_item_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        response = test_app.patch(
            url=f"/customers/some_customer_id_01/orders/wrong_order_id",
            json=json
        )

        assert "Order successfully updated" not in caplog.text
        assert response.status_code == 404


def test_add_items_to_an_existing_order_wrong_customer_id(
        test_app: TestClient,
        add_item_request: AddItemRequest,
        orders: dict[str, Order],
        caplog,
):
    json = add_item_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        response = test_app.patch(
            url=f"/customers/wrong_customer_id/orders/some_order_id_01",
            json=json
        )

        assert "Order successfully updated" not in caplog.text
        assert response.status_code == 400


def test_add_items_to_an_existing_order_wrong_order_status(
        test_app: TestClient,
        add_item_request: AddItemRequest,
        orders: dict[str, Order],
        caplog,
):
    json = add_item_request.model_dump()

    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        response = test_app.patch(
            url=f"/customers/some_customer_id_02/orders/some_order_id_02",
            json=json
        )

        assert "Order successfully updated" not in caplog.text
        assert response.status_code == 400


def test_check_order_expired(
        orders: dict[str, Order],
):
    with mock.patch.dict('ordermgmt.routers.customers.ORDERS', orders):
        assert check_order_expired("some_order_id_01", "some_payment_info_id_01") is True
        assert check_order_expired("some_order_id_02", "some_payment_info_id_01") is False
        assert check_order_expired("some_order_id_03", "some_payment_info_id_01") is False
        assert check_order_expired("non_existent_order", "some_payment_info_id_01") is False
