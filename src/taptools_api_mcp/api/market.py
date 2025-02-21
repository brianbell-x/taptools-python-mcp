"""
MarketAPI for aggregated market endpoints.
"""
import logging
import httpx
from typing import Dict, Any

from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class MarketAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request with error handling.
        
        Args:
            method: HTTP method (get, post, etc.)
            url: API endpoint URL
            **kwargs: Additional arguments for the request
            
        Returns:
            API response as dictionary
            
        Raises:
            TapToolsError: For any API or connection errors
        """
        try:
            response = await getattr(self.client, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in request to {url}: {str(e)}")
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            logger.error(f"Connection error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )
        except Exception as e:
            logger.error(f"Unexpected error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Unexpected error: {str(e)}",
                error_type=ErrorType.UNKNOWN
            )

    async def get_market_stats(self, quote: str = "ADA") -> Dict[str, Any]:
        """
        GET /market/stats
        
        Get aggregated market stats (24h DEX volume, active addresses).
        
        Args:
            quote (str, optional): Quote currency (e.g. 'ADA'). Defaults to 'ADA'.
        
        Returns:
            Dict[str, Any]: Market stats including:
                - activeAddresses: Number of active addresses
                - dexVolume: 24h DEX volume in quote currency
        
        Example response:
            {
                "activeAddresses": 24523,
                "dexVolume": 8134621.35
            }
        """
        url = "/market/stats"
        params = {"quote": quote}
        return await self._make_request("get", url, params=params)
