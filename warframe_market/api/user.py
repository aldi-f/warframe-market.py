import msgspec
from typing import List
from ..common.base import BaseRequest
from ..models.user import UserModel


class User(BaseRequest):
    """Getting information about particular user by slug/username.

    Requires user slug (username).
    """

    __endpoint__ = "/user/{slug}"
    __slug__ = True

    data: UserModel


class UserById(BaseRequest):
    """Getting information about particular user by user ID."""

    __endpoint__ = "/userId/{slug}"
    __slug__ = True

    data: UserModel
