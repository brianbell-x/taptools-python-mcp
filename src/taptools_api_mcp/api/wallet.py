"""
WalletAPI for wallet-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class WalletAPI:
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

    async def get_wallet_portfolio_positions(self, address: str) -> Dict[str, Any]:
        """
        GET /wallet/portfolio/positions
        
        Retrieve current wallet positions: tokens, NFTs, LP farms, etc.
        """
        url = "/wallet/portfolio/positions"
        params = {"address": address}
        return await self._make_request("get", url, params=params)

    async def get_wallet_trades_tokens(
        self, 
        address: str, 
        unit: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        GET /wallet/trades/tokens
        
        Get token trade history for a wallet (optionally filter by token).
        """
        url = "/wallet/trades/tokens"
        params = {"address": address}
        if unit:
            params["unit"] = unit
        return await self._make_request("get", url, params=params)

    async def get_wallet_value_trended(
        self, 
        address: str, 
        timeframe: str = "30d", 
        quote: str = "ADA"
    ) -> Dict[str, Any]:
        """
        GET /wallet/value/trended
        
        Get historical value of a wallet in 4hr intervals.
        """
        url = "/wallet/value/trended"
        params = {
            "address": address,
            "timeframe": timeframe,
            "quote": quote
        }
        return await self._make_request("get", url, params=params)
