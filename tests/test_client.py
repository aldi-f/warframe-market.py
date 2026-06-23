from warframe_market.client import WarframeMarketClient
from warframe_market.common import BASE_URL, Language, Platform


class TestClientConstruction:
    def test_default_construction(self):
        client = WarframeMarketClient()
        assert client.base_url == "https://api.warframe.market/v2"
        assert client.language == Language.ENGLISH
        assert client.platform == Platform.PC
        assert client.crossplay is True

    def test_custom_construction(self):
        client = WarframeMarketClient(
            base_url="https://example.com",
            language=Language.KOREAN,
            platform=Platform.SWITCH,
            crossplay=False,
        )
        assert client.base_url == "https://example.com"
        assert client.language == Language.KOREAN
        assert client.platform == Platform.SWITCH
        assert client.crossplay is False

    def test_default_single_param(self):
        client = WarframeMarketClient(language=Language.FRENCH)
        assert client.language == Language.FRENCH
        assert client.platform == Platform.PC

    def test_default_platform_only(self):
        client = WarframeMarketClient(platform=Platform.XBOX)
        assert client.platform == Platform.XBOX


class TestClientHeaders:
    def test_default_headers(self):
        client = WarframeMarketClient()
        headers = client.headers
        assert headers["Language"] == "en"
        assert headers["Platform"] == "pc"
        assert headers["Crossplay"] == "true"
        assert headers["Accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"

    def test_custom_headers(self):
        client = WarframeMarketClient(
            language=Language.KOREAN,
            platform=Platform.MOBILE,
            crossplay=False,
        )
        assert client.headers["Language"] == "ko"
        assert client.headers["Platform"] == "mobile"
        assert client.headers["Crossplay"] == "false"


class TestClientHasMethods:
    def test_has_all_get_methods(self):
        client = WarframeMarketClient()
        methods = {m for m in dir(client) if m.startswith("get_")}
        expected = {
            "get_all_items",
            "get_item",
            "get_item_set",
            "get_item_by_id",
            "get_item_set_by_id",
            "get_item_icon_url",
            "get_item_thumb_url",
            "get_orders_for_item",
            "get_top_orders_for_item",
            "get_orders_from_user",
            "get_orders_for_item_by_id",
            "get_top_orders_for_item_by_id",
            "get_orders_from_user_by_id",
            "get_recent_orders",
            "get_order_by_id",
            "get_lich_weapons",
            "get_lich_weapon",
            "get_lich_ephemeras",
            "get_lich_quirks",
            "get_sister_weapons",
            "get_sister_weapon",
            "get_sister_ephemeras",
            "get_sister_quirks",
            "get_riven_weapons",
            "get_riven_weapon",
            "get_riven_attributes",
            "get_locations",
            "get_missions",
            "get_npcs",
            "get_versions",
            "get_user",
            "get_user_by_id",
            "get_achievements",
            "get_user_achievements",
            "get_user_achievements_by_id",
            "get_dashboard_showcase",
        }
        missing = expected - methods
        assert not missing, f"Missing methods: {missing}"
        extra = methods - expected
        assert not extra, f"Unexpected methods: {extra}"

    def test_async_context_manager(self):
        client = WarframeMarketClient()
        # Just verify the methods exist and return the right types
        assert hasattr(client, "__aenter__")
        assert hasattr(client, "__aexit__")
        assert hasattr(client, "get")