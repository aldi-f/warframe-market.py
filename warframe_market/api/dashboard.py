from ..common.base import BaseRequest
from ..models.dashboard import DashboardShowcaseModel


class DashboardShowcase(BaseRequest):
    """Get mobile app main screen dashboard with featured items."""

    __endpoint__ = "/dashboard/showcase"

    data: DashboardShowcaseModel