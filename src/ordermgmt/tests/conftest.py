from fastapi.testclient import TestClient
import pytest
import datetime

from ordermgmt.models.order.customer import OrderItem, Order, OrderStatus
from ordermgmt.app import app

@pytest.fixture()
def menu_items() -> list[OrderItem]:
    return [
        OrderItem(
            itemId="some_item_id_01",
            quantity=2,
        ),
        OrderItem(
            itemId="some_item_id_02",
            quantity=1,
        )
    ]

@pytest.fixture()
def orders(menu_items: list[OrderItem]) -> dict[str, Order]:
    return {
        "some_order_id_01":
            Order(
                order_id="some_order_id_01",
                customer_id="some_customer_id_01",
                ordered_at=datetime.datetime(2024, 3, 24, 3, 2, 1),
                menu_items=menu_items,
                status=OrderStatus.PLACED
            ),
        "some_order_id_02":
            Order(
                order_id="some_order_id_02",
                customer_id="some_customer_id_02",
                ordered_at=datetime.datetime(2024, 3, 24, 3, 7, 1),
                menu_items=menu_items,
                status=OrderStatus.ACCEPTED
            ),
        "some_order_id_03":
            Order(
                order_id="some_order_id_03",
                customer_id="some_customer_id_03",
                ordered_at=datetime.datetime(2024, 3, 24, 3, 12, 1),
                menu_items=menu_items,
                status=OrderStatus.REJECTED
            )
    }


@pytest.fixture(scope="session")
def test_app() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
