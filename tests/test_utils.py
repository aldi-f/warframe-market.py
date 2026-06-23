from warframe_market.utils import get_static_asset_url


def test_get_static_asset_url_simple():
    assert get_static_asset_url("x.png") == "https://warframe.market/static/assets/x.png"


def test_get_static_asset_url_subdirectory():
    assert get_static_asset_url("icons/frame.png") == "https://warframe.market/static/assets/icons/frame.png"