"""
MarketAPI for aggregated market endpoints.
"""
import logging
import httpx
from typing import Dict, Any

from ..models.market import (
    MarketStatsRequest, MarketStatsResponse,
    MarketStats, MetricsResponse
)
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

    async def get_market_stats(self, request: MarketStatsRequest) -> MarketStatsResponse:
        """
        GET /market/stats
        
        Get aggregated market stats (24h DEX volume, active addresses).
        """
        url = "/market/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return MarketStatsResponse(stats=MarketStats(
            active_addresses=response_data["activeAddresses"],
            dex_volume=response_data["dexVolume"]
        ))
