import msgspec
from ..common.options import LanguageCode


class _DashboardI18NModel(msgspec.Struct):
    title: str | None = None
    description: str | None = None


class _DashboardItemModel(msgspec.Struct):
    item: str
    background: str | None = None
    big_card: bool | None = msgspec.field(default=None, name="bigCard")


class DashboardShowcaseModel(msgspec.Struct):
    i18n: dict[LanguageCode, _DashboardI18NModel] = msgspec.field(default_factory=dict)
    items: list[_DashboardItemModel] = msgspec.field(default_factory=list)