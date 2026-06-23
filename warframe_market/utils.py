from .common import BASE_STATIC_ASSETS_URL


def get_static_asset_url(path: str) -> str:
    """Construct a full static asset URL from a relative path.

    Args:
        path: A relative asset path (e.g. "nova_prime_set.png").

    Returns:
        The full static asset URL.
    """
    return f"{BASE_STATIC_ASSETS_URL}/{path}"