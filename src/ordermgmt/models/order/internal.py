from pydantic import Field

from ordermgmt.models.order import BaseModel


class RefundItem(BaseModel):
    order_id: str = Field(alias='orderId')
    payment_info_id: str = Field(alias='paymentInfoId')
