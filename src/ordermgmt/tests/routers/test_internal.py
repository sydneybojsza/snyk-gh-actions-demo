import pytest
import mock
from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from ordermgmt.models.order.internal import RefundItem
from ordermgmt.routers import internal


@pytest.fixture()
def refunds() -> list[RefundItem]:
    return [
        RefundItem(
            orderId="some_order_id_01",
            paymentInfoId="some_payment_info_id_01"
        ),
        RefundItem(
            orderId="some_order_id_02",
            paymentInfoId="some_payment_info_id_02"
        ),
        RefundItem(
            orderId="some_order_id_03",
            paymentInfoId="some_payment_info_id_03"
        )
    ]


def test_view_internal_refunds(
        test_app: TestClient,
        refunds: list[RefundItem],
        caplog,
):
    with mock.patch.object(internal, "REFUNDS", refunds):

        response = test_app.get(
            url="/internal/refunds"
        )

        assert response.status_code == 200
        assert f"Returning all refund items" in caplog.text
        assert parse_obj_as(list[RefundItem], response.json()) == refunds
