import msgspec
from ..common.options import LanguageCode


class AchievementStateModel(msgspec.Struct):
    featured: bool | None = None
    progress: int | None = None
    completed_at: str | None = msgspec.field(default=None, name="completedAt")


class AchievementI18NModel(msgspec.Struct):
    name: str
    description: str
    icon: str | None = None
    thumb: str | None = None


class AchievementModel(msgspec.Struct):
    id: str
    type: str
    slug: str | None = None
    goal: int | None = None
    icon: str | None = None
    thumb: str | None = None
    i18n: dict[LanguageCode, AchievementI18NModel] = msgspec.field(default_factory=dict)
    state: AchievementStateModel | None = None