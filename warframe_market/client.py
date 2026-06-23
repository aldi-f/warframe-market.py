import aiohttp
from typing import TypeVar, Type, Optional

from .common import *
from .api import *
from .utils import get_static_asset_url
from .exceptions import (
    WFMApiError,
    WFMRateLimitError,
    WFMTooManyConnectionsError,
    WFMAuthError,
    WFMNotFoundError,
    WFMServerError,
)


Klass = TypeVar("Klass", bound=BaseRequest)


class WarframeMarketClient:

    def __init__(self,
                 base_url: str = BASE_URL,
                 language: Language = Language.ENGLISH,
                 platform: Platform = Platform.PC,
                 crossplay: bool = True):
        self.base_url = base_url
        self.response = None
        self.language = language
        self.platform = platform
        self.crossplay = crossplay

    @property
    def headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Language": self.language.value,
            "Platform": self.platform.value,
            "Crossplay": str(self.crossplay).lower()
        }

    async def get(self, request_class: Type[Klass], slug: str = "", **kwargs) -> Klass:
        endpoint = request_class._get_endpoint(slug=slug, **kwargs)
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                body = await response.text()
                if response.status == 429:
                    raise WFMRateLimitError(body=body)
                if response.status == 509:
                    raise WFMTooManyConnectionsError(body=body)
                if response.status == 404:
                    raise WFMNotFoundError(body=body)
                if response.status == 401 or response.status == 403:
                    raise WFMAuthError(status=response.status, body=body)
                if response.status >= 500:
                    raise WFMServerError(status=response.status, body=body)
                if response.status != 200:
                    raise WFMApiError(status=response.status, body=body)
                return request_class._decode(body)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    ####################
    ## ITEM APIs
    ####################
    async def get_all_items(self) -> Items:
        return await self.get(Items)

    async def get_item(self, slug: str) -> Item:
        return await self.get(Item, slug=slug)

    async def get_item_set(self, slug: str) -> ItemSet:
        return await self.get(ItemSet, slug=slug)

    async def get_item_by_id(self, item_id: str) -> Item:
        return await self.get(ItemById, slug=item_id)

    async def get_item_set_by_id(self, item_id: str) -> ItemSet:
        return await self.get(ItemSetById, slug=item_id)

    async def get_item_icon_url(self, slug: str) -> str:
        item = await self.get_item(slug)
        return get_static_asset_url(item.data.i18n[self.language.value].icon)

    async def get_item_thumb_url(self, slug: str) -> str:
        item = await self.get_item(slug)
        return get_static_asset_url(item.data.i18n[self.language.value].thumb)

    ####################
    ## ORDER APIs
    ####################
    async def get_orders_for_item(self, slug: str) -> OrdersItem:
        return await self.get(OrdersItem, slug=slug)

    async def get_orders_for_item_by_id(self, item_id: str) -> OrdersItem:
        return await self.get(OrdersItemById, slug=item_id)

    async def get_top_orders_for_item(
            self,
            slug: str,
            rank: Optional[int] = None,
            rankLt: Optional[int] = None,
            charges: Optional[int] = None,
            chargesLt: Optional[int] = None,
            amberStars: Optional[int] = None,
            amberStarsLt: Optional[int] = None,
            cyanStars: Optional[int] = None,
            cyanStarsLt: Optional[int] = None,
            subtype: Optional[Subtype] = None
            ) -> OrdersItemTop:
        return await self.get(
            OrdersItemTop,
            slug=slug,
            rank=rank,
            rankLt=rankLt,
            charges=charges,
            chargesLt=chargesLt,
            amberStars=amberStars,
            amberStarsLt=amberStarsLt,
            cyanStars=cyanStars,
            cyanStarsLt=cyanStarsLt,
            subtype=subtype.value if subtype else None
        )

    async def get_top_orders_for_item_by_id(
            self,
            item_id: str,
            rank: Optional[int] = None,
            rankLt: Optional[int] = None,
            charges: Optional[int] = None,
            chargesLt: Optional[int] = None,
            amberStars: Optional[int] = None,
            amberStarsLt: Optional[int] = None,
            cyanStars: Optional[int] = None,
            cyanStarsLt: Optional[int] = None,
            subtype: Optional[Subtype] = None
            ) -> OrdersItemTop:
        return await self.get(
            OrdersItemTopById,
            slug=item_id,
            rank=rank,
            rankLt=rankLt,
            charges=charges,
            chargesLt=chargesLt,
            amberStars=amberStars,
            amberStarsLt=amberStarsLt,
            cyanStars=cyanStars,
            cyanStarsLt=cyanStarsLt,
            subtype=subtype.value if subtype else None
        )

    async def get_orders_from_user(
            self,
            username: str,
            platform: Platform = Platform.PC
            ) -> OrdersUser:
        return await self.get(OrdersUser, slug=username, platform=platform.value)

    async def get_orders_from_user_by_id(
            self,
            user_id: str) -> OrdersUser:
        return await self.get(OrdersUserById, slug=user_id)

    async def get_recent_orders(self) -> OrdersRecent:
        return await self.get(OrdersRecent)

    async def get_order_by_id(self, order_id: str) -> OrderId:
        return await self.get(OrderId, slug=order_id)

    ####################
    ## LICH APIs
    ####################
    async def get_lich_weapons(self) -> LichWeapons:
        return await self.get(LichWeapons)

    async def get_lich_weapon(self, slug: str) -> LichWeapon:
        return await self.get(LichWeapon, slug=slug)

    async def get_lich_ephemeras(self) -> LichEphemeras:
        return await self.get(LichEphemeras)

    async def get_lich_quirks(self) -> LichQuirks:
        return await self.get(LichQuirks)

    ####################
    ## SISTER APIs
    ####################
    async def get_sister_weapons(self) -> SisterWeapons:
        return await self.get(SisterWeapons)

    async def get_sister_weapon(self, slug: str) -> SisterWeapon:
        return await self.get(SisterWeapon, slug=slug)

    async def get_sister_ephemeras(self) -> SisterEphemeras:
        return await self.get(SisterEphemeras)

    async def get_sister_quirks(self) -> SisterQuirks:
        return await self.get(SisterQuirks)

    ####################
    ## RIVEN APIs
    ####################
    async def get_riven_weapons(self) -> Rivens:
        return await self.get(Rivens)

    async def get_riven_weapon(self, slug: str) -> Riven:
        return await self.get(Riven, slug=slug)

    async def get_riven_attributes(self) -> RivenAttributes:
        return await self.get(RivenAttributes)

    ####################
    ## MISC APIs
    ####################
    async def get_locations(self) -> Locations:
        return await self.get(Locations)

    async def get_missions(self) -> Missions:
        return await self.get(Missions)

    async def get_npcs(self) -> NPCs:
        return await self.get(NPCs)

    async def get_versions(self) -> Versions:
        return await self.get(Versions)

    ####################
    ## USER APIs
    ####################
    async def get_user(self, slug: str) -> User:
        return await self.get(User, slug=slug)

    async def get_user_by_id(self, user_id: str) -> User:
        return await self.get(UserById, slug=user_id)

    ####################
    ## ACHIEVEMENT APIs
    ####################
    async def get_achievements(self) -> Achievements:
        return await self.get(Achievements)

    async def get_user_achievements(self, slug: str) -> UserAchievements:
        return await self.get(UserAchievements, slug=slug)

    async def get_user_achievements_by_id(self, user_id: str) -> UserAchievements:
        return await self.get(UserAchievementsById, slug=user_id)

    ####################
    ## DASHBOARD APIs
    ####################
    async def get_dashboard_showcase(self) -> DashboardShowcase:
        return await self.get(DashboardShowcase)