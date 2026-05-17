import msgspec
from typing import Optional

from .user import UserShortModel


class _TransactionItemModel(msgspec.Struct):
    id: str
    rank: int | None = None
    charges: int | None = None
    subtype: str | None = None
    cyan_stars: int | None = msgspec.field(default=None, name="cyanStars")
    amber_stars: int | None = msgspec.field(default=None, name="amberStars")


class TransactionModel(msgspec.Struct):
    id: str
    type: str
    origin_id: str = msgspec.field(name="originId")
    platinum: int
    quantity: int
    created_at: str = msgspec.field(name="createdAt")
    updated_at: str = msgspec.field(name="updatedAt")
    item: _TransactionItemModel
    user: Optional[UserShortModel] = None