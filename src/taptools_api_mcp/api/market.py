"""
MarketAPI for aggregated market endpoints.
"""
import logging
import httpx
from typing import Dict, Any, TypedDict

from ..models.market import (
    MarketStats, MetricsResponse, MetricsCall,
    MarketOverview, TokenChange, TokenVolume
)
from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

# Type hints for raw dictionary returns
class MarketStatsDict(TypedDict):
    totalMarketCap: float
    volume24h: float
    dominance: Dict[str, float]
    activeTokens: int
    activeTraders: int

class MarketOverviewDict(TypedDict):
    gainers: list[dict[str, Any]]  # List[TokenChange]
    losers: list[dict[str, Any]]   # List[TokenChange]
    trending: list[dict[str, Any]]  # List[TokenVolume]

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

    async def get_market_stats(
        self,
        quote: str = "ADA",
        include_deprecated: bool = False,
        min_liquidity: float = 0
    ) -> MarketStatsDict:
        """
        GET /market/stats
        Retrieve aggregated market stats with optional filters.

        Args:
            quote: Quote currency (e.g. 'ADA', 'USD')
            include_deprecated: Whether to include deprecated tokens
            min_liquidity: Minimum liquidity threshold to filter by

        Returns:
            Dictionary containing market statistics:
            - totalMarketCap: Total market capitalization
            - volume24h: 24-hour trading volume
            - dominance: Token dominance percentages
            - activeTokens: Number of active tokens
            - activeTraders: Number of active traders
        """
        url = "/market/stats"
        params = {"quote": quote}
        if include_deprecated:
            params["includeDeprecated"] = True
        if min_liquidity > 0:
            params["minLiquidity"] = min_liquidity

        response_data = await self._make_request("get", url, params=params)
        return response_data

    async def get_metrics(self) -> MetricsResponse:
        """
        GET /metrics
        Get daily request counts from the past 30 days.

        Returns:
            MetricsResponse containing a list of daily metrics
        """
        url = "/metrics"
        response_data = await self._make_request("get", url)
        return MetricsResponse(metrics=[MetricsCall(**call) for call in response_data])

    async def get_market_overview(self) -> MarketOverviewDict:
        """
        GET /market/overview
        Return overview data: gainers, losers, trending, etc.

        Returns:
            Dictionary containing market overview data:
            - gainers: List of top gaining tokens with 24h price changes
            - losers: List of top losing tokens with 24h price changes
            - trending: List of trending tokens by 24h volume
        """
        url = "/market/overview"
        response_data = await self._make_request("get", url)
        return response_data
