"""
MarketAPI for aggregated market endpoints.
"""
import httpx
from typing import Dict, Any
from ..utils.exceptions import TapToolsError

class MarketAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_market_stats(self) -> Dict[str, Any]:
        """
        GET /market/stats

        Example aggregated 24h DEX volume, active addresses, etc.
        """
        url = "/market/stats"
        try:
            resp = await self.client.get(url)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise TapToolsError(f"Market stats error: {str(e)}")