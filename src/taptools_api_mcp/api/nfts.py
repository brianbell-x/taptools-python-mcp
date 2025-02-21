"""
NftsAPI for NFT-related endpoints.
"""
import httpx
from typing import Dict, Any
from ..utils.exceptions import TapToolsError

class NftsAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_collection_stats(self, policy_id: str) -> Dict[str, Any]:
        """
        GET /nft/collection/stats

        Return NFT collection stats by policy ID.
        """
        url = "/nft/collection/stats"
        try:
            resp = await self.client.get(url, params={"policy": policy_id})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise TapToolsError(f"NFT collection stats error: {str(e)}")
