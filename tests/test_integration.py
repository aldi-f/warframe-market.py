import pytest
from unittest.mock import patch
from warframe_market.client import WarframeMarketClient
from warframe_market.exceptions import (
    WFMApiError,
    WFMRateLimitError,
    WFMTooManyConnectionsError,
    WFMAuthError,
    WFMNotFoundError,
    WFMServerError,
)


class MockResponse:
    def __init__(self, status, data_text):
        self.status = status
        self.data_text = data_text

    async def text(self):
        return self.data_text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None


def _mock_get(status, body):
    return lambda *args, **kw: MockResponse(status, body)


@pytest.fixture
def client():
    return WarframeMarketClient()


MOCK_ITEMS_DATA = '''{"apiVersion": "0.23.0", "data": [
    {"id": "i1", "slug": "item_one", "gameRef": "/Lotus/W", "tags": ["mod"], "i18n": {"en": {"name": "Item One", "icon": "x.png", "thumb": "y.png"}}},
    {"id": "i2", "slug": "item_two", "gameRef": "/Lotus/W", "tags": ["weapon"], "i18n": {"en": {"name": "Item Two", "icon": "x.png", "thumb": "y.png"}}}
], "error": null}'''

MOCK_ITEM_DATA = '''{"apiVersion": "0.23.0", "data": {"id": "i1", "slug": "item_one", "gameRef": "/Lotus/W", "tags": ["mod"], "tradable": true, "i18n": {"en": {"name": "Item One", "icon": "x.png", "thumb": "y.png"}}}, "error": null}'''

MOCK_ORDERS_DATA = '''{"apiVersion": "0.23.0", "data": [{"id": "o1", "type": "sell", "platinum": 50, "quantity": 1, "visible": true, "createdAt": "2021-01-01T00:00:00Z", "updatedAt": "2021-01-01T00:00:00Z", "itemId": "i1", "user": {"id": "u1", "ingameName": "Player1", "reputation": 0, "locale": "en", "platform": "pc", "crossplay": true, "status": "online", "activity": {"type": "idle", "details": null, "startedAt": null}, "lastSeen": "2021-01-01T00:00:00Z"}}], "error": null}'''


@pytest.mark.asyncio
async def test_get_all_items_success(client):
    with patch("aiohttp.ClientSession.get", _mock_get(200, MOCK_ITEMS_DATA)):
        result = await client.get_all_items()
    assert len(result.data) == 2
    assert result.data[0].slug == "item_one"


@pytest.mark.asyncio
async def test_get_item_success(client):
    with patch("aiohttp.ClientSession.get", _mock_get(200, MOCK_ITEM_DATA)):
        result = await client.get_item("item_one")
    assert result.data.slug == "item_one"
    assert result.data.tradable is True


@pytest.mark.asyncio
async def test_get_orders_for_item_success(client):
    with patch("aiohttp.ClientSession.get", _mock_get(200, MOCK_ORDERS_DATA)):
        result = await client.get_orders_for_item("item_one")
    assert len(result.data) == 1
    assert result.data[0].platinum == 50
    assert result.data[0].user.ingame_name == "Player1"


@pytest.mark.asyncio
async def test_rate_limit_error(client):
    with patch("aiohttp.ClientSession.get", _mock_get(429, "too many")):
        with pytest.raises(WFMRateLimitError):
            await client.get_all_items()


@pytest.mark.asyncio
async def test_too_many_connections_error(client):
    with patch("aiohttp.ClientSession.get", _mock_get(509, "")):
        with pytest.raises(WFMTooManyConnectionsError):
            await client.get_all_items()


@pytest.mark.asyncio
async def test_not_found_error(client):
    with patch("aiohttp.ClientSession.get", _mock_get(404, "not found")):
        with pytest.raises(WFMNotFoundError):
            await client.get_item("nonexistent")


@pytest.mark.asyncio
async def test_auth_error_401(client):
    with patch("aiohttp.ClientSession.get", _mock_get(401, "unauthorized")):
        with pytest.raises(WFMAuthError) as exc_info:
            await client.get_item("test")
        assert exc_info.value.status == 401


@pytest.mark.asyncio
async def test_server_error(client):
    with patch("aiohttp.ClientSession.get", _mock_get(502, "")):
        with pytest.raises(WFMServerError) as exc_info:
            await client.get_item("test")
        assert exc_info.value.status == 502


@pytest.mark.asyncio
async def test_other_http_error(client):
    with patch("aiohttp.ClientSession.get", _mock_get(418, "teapot")):
        with pytest.raises(WFMApiError) as exc_info:
            await client.get_item("test")
        assert exc_info.value.status == 418


@pytest.mark.asyncio
async def test_get_item_icon_url(client):
    with patch("aiohttp.ClientSession.get", _mock_get(200, MOCK_ITEM_DATA)):
        icon_url = await client.get_item_icon_url("item_one")
    assert icon_url == "https://warframe.market/static/assets/x.png"


@pytest.mark.asyncio
async def test_get_item_thumb_url(client):
    with patch("aiohttp.ClientSession.get", _mock_get(200, MOCK_ITEM_DATA)):
        thumb_url = await client.get_item_thumb_url("item_one")
    assert thumb_url == "https://warframe.market/static/assets/y.png"
