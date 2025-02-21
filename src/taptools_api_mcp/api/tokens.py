"""
TokensAPI for token-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional

from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class TokensAPI:
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

    async def get_token_mcap(self, unit: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/mcap
        
        Get supply + market cap of a token (circulating from external repo).
        """
        url = "/token/mcap"
        params = {"unit": unit}
        return await self._make_request("get", url, params=params)

    async def get_token_holders(self, unit: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/holders
        
        Get total number of holders (aggregates addresses with same stake).
        """
        url = "/token/holders"
        params = {"unit": unit}
        return await self._make_request("get", url, params=params)

    async def get_token_holders_top(self, unit: str, page: int = 1, perPage: int = 20) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/holders/top
        
        Read top holders of a token.
        """
        url = "/token/holders/top"
        params = {
            "unit": unit,
            "page": page,
            "perPage": perPage
        }
        return await self._make_request("get", url, params=params)

    async def get_token_indicators(self, unit: str, interval: str, items: int, indicator: str, quote: str, **kwargs) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/indicators
        
        Create indicator values (EMA, RSI, MACD) for a token's price data.
        """
        url = "/token/indicators"
        params = {
            "unit": unit,
            "interval": interval,
            "items": items,
            "indicator": indicator,
            "quote": quote,
            **kwargs  # Additional indicator-specific parameters
        }
        return await self._make_request("get", url, params=params)

    async def get_token_links(self, unit: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/links
        
        Get a token's social/contact links.
        """
        url = "/token/links"
        params = {"unit": unit}
        return await self._make_request("get", url, params=params)

    async def get_token_ohlcv(self, unit: str, interval: str, numIntervals: int) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/ohlcv
        
        Get token OHLCV (aggregated or by onchain ID).
        """
        url = "/token/ohlcv"
        params = {
            "unit": unit,
            "interval": interval,
            "numIntervals": numIntervals
        }
        return await self._make_request("get", url, params=params)

    async def get_token_pools(self, unit: str, adaOnly: int = 0) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/pools
        
        Get active liquidity pools for a token.
        """
        url = "/token/pools"
        params = {
            "unit": unit,
            "adaOnly": adaOnly
        }
        return await self._make_request("get", url, params=params)

    async def post_token_prices(self, units: List[str]) -> Dict[str, Any]:
        """
        TapTools endpoint:
        POST /token/prices
        
        Move an array of token units to get aggregated prices. Max batch size: 100.
        """
        url = "/token/prices"
        return await self._make_request("post", url, json=units)

    async def get_token_price_changes(self, unit: str, timeframes: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/prices/chg
        
        Get token price % changes over multiple timeframes.
        """
        url = "/token/prices/chg"
        params = {
            "unit": unit,
            "timeframes": timeframes
        }
        return await self._make_request("get", url, params=params)

    async def get_token_trades(
        self, 
        timeframe: str = "30d", 
        sort_by: str = "amount", 
        order: str = "desc", 
        unit: str = "", 
        min_amount: Optional[int] = None, 
        from_ts: Optional[int] = None, 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/trades
        
        Get token trades across DEXes.
        """
        url = "/token/trades"
        params = {
            "timeframe": timeframe,
            "sortBy": sort_by,
            "order": order,
            "page": page,
            "perPage": per_page
        }
        if unit:
            params["unit"] = unit
        if min_amount is not None:
            params["minAmount"] = min_amount
        if from_ts is not None:
            params["from"] = from_ts
            
        return await self._make_request("get", url, params=params)

    async def get_token_trading_stats(self, unit: str, timeframe: str = "24h") -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/trading/stats
        
        Get aggregated trading stats for a token over timeframe.
        """
        url = "/token/trading/stats"
        params = {
            "unit": unit,
            "timeframe": timeframe
        }
        return await self._make_request("get", url, params=params)

    async def get_token_debt_loans(
        self, 
        unit: str, 
        include: str = "collateral,debt", 
        sort_by: str = "time", 
        order: str = "desc", 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/debt/loans
        
        Update active P2P loans for a given token (Lenfi, Levvy).
        """
        url = "/token/debt/loans"
        params = {
            "unit": unit,
            "include": include,
            "sortBy": sort_by,
            "order": order,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_token_debt_offers(
        self, 
        unit: str, 
        include: str = "collateral,debt", 
        sort_by: str = "time", 
        order: str = "desc", 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/debt/offers
        
        Get active P2P loan offers (Lenfi, Levvy).
        """
        url = "/token/debt/offers"
        params = {
            "unit": unit,
            "include": include,
            "sortBy": sort_by,
            "order": order,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_top_tokens_by_liquidity(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/top/liquidity
        
        Get tokens ranked by total DEX liquidity.
        """
        url = "/token/top/liquidity"
        params = {
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_top_tokens_by_mcap(self, type: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/top/mcap
        
        Get tokens with top market cap (excludes deprecated).
        """
        url = "/token/top/mcap"
        params = {
            "type": type,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_top_tokens_by_volume(self, timeframe: str = "24h", page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/top/volume
        
        Get tokens with top volume for a timeframe.
        """
        url = "/token/top/volume"
        params = {
            "timeframe": timeframe,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_token_quote(self, quote: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/quote
        
        Get current quote price (e.g. ADA/USD).
        """
        url = "/token/quote"
        params = {"quote": quote}
        return await self._make_request("get", url, params=params)

    async def get_available_quotes(self) -> Dict[str, Any]:
        """
        TapTools endpoint:
        GET /token/quote/available
        
        List available quote currencies.
        """
        url = "/token/quote/available"
        return await self._make_request("get", url)

    async def get_token_price(self, unit: str) -> Dict[str, Any]:
        """
        TapTools endpoint:
        POST /token/prices

        Aggregated price across DEXs for the given token unit.
        """
        url = "/token/prices"
        body = [unit]
        return await self._make_request("post", url, json=body)
