"""
TokensAPI for token-related endpoints.
"""
import httpx
from typing import Dict, Any
from ..utils.exceptions import TapToolsError

class TokensAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_token_price(self, unit: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        POST /token/prices

        Aggregated price across DEXs for the given token unit.
        """
        url = "/token/prices"
        body = [unit]
        try:
            resp = await self.client.post(url, json=body)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise TapToolsError(f"Token price fetch error: {str(e)}")
