import msgspec
from warframe_market.api import (
    Items, Item, ItemSet, ItemById, ItemSetById,
    OrdersRecent, OrdersItem, OrdersItemTop, OrdersUser, OrderId,
    OrdersItemById, OrdersItemTopById, OrdersUserById,
    LichWeapons, LichWeapon, LichEphemeras, LichQuirks,
    SisterWeapons, SisterWeapon, SisterEphemeras, SisterQuirks,
    Rivens, Riven, RivenAttributes,
    Locations, Missions, NPCs, Versions,
    User, UserById,
    Achievements, UserAchievements, UserAchievementsById,
    DashboardShowcase,
)


ENDPOINT_TESTS = [
    (Items, {}, "/items", None),
    (Item, {}, "/item/mesa_prime_bp", "mesa_prime_bp"),
    (ItemSet, {}, "/item/abc/set", "abc"),
    (ItemById, {}, "/itemId/id123", "id123"),
    (ItemSetById, {}, "/itemId/id123/set", "id123"),
    (OrdersRecent, {}, "/orders/recent", None),
    (OrdersItem, {}, "/orders/item/abc", "abc"),
    (OrdersUser, {}, "/orders/user/KycKyc", "KycKyc"),
    (OrderId, {}, "/order/ord123", "ord123"),
    (OrdersItemById, {}, "/orders/itemId/abc123", "abc123"),
    (OrdersItemTopById, {}, "/orders/itemId/abc123/top", "abc123"),
    (OrdersUserById, {}, "/orders/userId/uid123", "uid123"),
    (LichWeapons, {}, "/lich/weapons", None),
    (LichWeapon, {}, "/lich/weapon/kuva_bramma", "kuva_bramma"),
    (LichEphemeras, {}, "/lich/ephemeras", None),
    (LichQuirks, {}, "/lich/quirks", None),
    (SisterWeapons, {}, "/sister/weapons", None),
    (SisterWeapon, {}, "/sister/weapon/tenet_tetra", "tenet_tetra"),
    (SisterEphemeras, {}, "/sister/ephemeras", None),
    (SisterQuirks, {}, "/sister/quirks", None),
    (Rivens, {}, "/riven/weapons", None),
    (Riven, {}, "/riven/weapon/kulstar", "kulstar"),
    (RivenAttributes, {}, "/riven/attributes", None),
    (Locations, {}, "/locations", None),
    (Missions, {}, "/missions", None),
    (NPCs, {}, "/npcs", None),
    (Versions, {}, "/versions", None),
    (User, {}, "/user/kyckyc", "kyckyc"),
    (UserById, {}, "/userId/uid123", "uid123"),
    (Achievements, {}, "/achievements", None),
    (UserAchievements, {}, "/achievements/user/kyckyc", "kyckyc"),
    (UserAchievementsById, {}, "/achievements/userId/uid123", "uid123"),
    (DashboardShowcase, {}, "/dashboard/showcase", None),
]

ORDERS_TOP_KWARGS = {"rank": 5}


class TestEndpointPaths:
    def test_all_endpoints(self):
        for cls, kwargs, expected, slug in ENDPOINT_TESTS:
            kw = kwargs.copy()
            if slug:
                got = cls._get_endpoint(slug=slug, **kw)
            else:
                got = cls._get_endpoint(**kw)
            assert got == expected, f"{cls.__name__}: expected {expected}, got {got}"

    def test_orders_item_top_with_params(self):
        got = OrdersItemTop._get_endpoint(slug="abc", rank=5)
        assert got == "/orders/item/abc/top?rank=5"
        got = OrdersItemTop._get_endpoint(slug="abc")
        assert got == "/orders/item/abc/top"

    def test_orders_item_top_all_params(self):
        got = OrdersItemTop._get_endpoint(
            slug="abc",
            rank=4, rankLt=5,
            charges=2, chargesLt=3,
            amberStars=1, amberStarsLt=2,
            cyanStars=1, cyanStarsLt=2,
            subtype="blueprint",
        )
        assert "rank=4" in got
        assert "charges=2" in got
        assert "subtype=blueprint" in got

    def test_orders_item_top_by_id_with_params(self):
        got = OrdersItemTopById._get_endpoint(slug="id123", rank=5)
        assert got == "/orders/itemId/id123/top?rank=5"

    def test_orders_item_top_ignores_none_params(self):
        got = OrdersItemTop._get_endpoint(slug="abc", rank=None, rankLt=None)
        assert got == "/orders/item/abc/top"

    def test_default_endpoint_no_slug(self):
        got = Items._get_endpoint()
        assert got == "/items"


class TestEndpointTypes:
    def test_items_has_list_data(self):
        assert hasattr(Items, "data")

    def test_item_has_single_data(self):
        assert hasattr(Item, "data")

    def test_orders_item_top_data_is_orders_data(self):
        assert hasattr(OrdersItemTop, "data")

    def test_get_endpoint_with_extra_kwargs_ignored(self):
        got = Items._get_endpoint(unknown_param="val")
        assert got == "/items"

    # Check __slug__ is set for slug-requiring endpoints
    def test_slug_endpoints_have_slug_true(self):
        slug_classes = [Item, ItemSet, ItemById, ItemSetById,
                        OrdersItem, OrdersItemTop, OrdersUser, OrderId,
                        OrdersItemById, OrdersItemTopById, OrdersUserById,
                        LichWeapon, Riven,
                        SisterWeapon,
                        User, UserById,
                        UserAchievements, UserAchievementsById]
        for cls in slug_classes:
            assert cls.__slug__, f"{cls.__name__} should have __slug__ = True"