from datetime import datetime
from enum import Enum

from pydantic import Field

from ordermgmt.models.order import BaseModel


class OrderItem(BaseModel):
    item_id: str = Field(alias='itemId')
    quantity: int


class OrderRequest(BaseModel):
    customer_id: str = Field(alias='customerId')
    payment_info_id: str = Field(alias='paymentInfoId')
    menu_items: list[OrderItem] = Field(alias='menuItems')


class OrderStatus(str, Enum):
    PLACED = 'Placed'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'


class Order(BaseModel):
    order_id: str = Field(alias='orderId')
    customer_id: str = Field(alias='customerId')
    ordered_at: datetime = Field(alias='orderedAt')
    menu_items: list[OrderItem] = Field(alias='menuItems')
    status: OrderStatus = OrderStatus.PLACED


class AddItemRequest(BaseModel):
    menu_items: list[OrderItem] = Field(alias='menuItems')
    payment_info_id: str = Field(alias='paymentInfoId')

