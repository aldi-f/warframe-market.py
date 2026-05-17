from typing import List
from ..common.base import BaseRequest
from ..models.achievement import AchievementModel


class Achievements(BaseRequest):
    """Get list of all available achievements, except secret ones."""

    __endpoint__ = "/achievements"

    data: List[AchievementModel]


class UserAchievements(BaseRequest):
    """Get a list of all user achievements by slug."""

    __endpoint__ = "/achievements/user/{slug}"
    __slug__ = True

    data: List[AchievementModel]


class UserAchievementsById(BaseRequest):
    """Get a list of all user achievements by user ID."""

    __endpoint__ = "/achievements/userId/{slug}"
    __slug__ = True

    data: List[AchievementModel]