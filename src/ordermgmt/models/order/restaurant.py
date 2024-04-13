from enum import Enum

from pydantic import BaseModel


class OrderAction(str, Enum):
    ACCEPT = 'Accept'
    REJECT = 'Reject'


class AcceptRejectRequest(BaseModel):
    action: OrderAction
