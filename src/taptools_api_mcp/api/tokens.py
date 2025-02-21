"""
TokensAPI for token-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional

from ..models.tokens import (
    TokenMcapRequest, TokenMcapResponse,
    TokenHoldersRequest, TokenHoldersResponse,
    TokenTopHoldersRequest, TokenTopHoldersResponse,
    TokenIndicatorsRequest, TokenIndicatorsResponse,
    TokenLinksRequest, TokenLinksResponse,
    TokenOHLCVRequest, TokenOHLCVResponse,
    TokenPoolsRequest, TokenPoolsResponse,
    TokenPricesRequest, TokenPricesResponse,
    TokenPriceChangesRequest, TokenPriceChangesResponse,
    TokenQuoteRequest, TokenQuoteResponse, TokenQuoteAvailableResponse,
    TokenTopLiquidityRequest, TokenTopLiquidityResponse,
    TokenTradingStatsRequest, TokenTradingStatsResponse,
    TokenTopMcapRequest, TokenTopMcapResponse,
    TokenTopVolumeRequest, TokenTopVolumeResponse,
    TokenDebtLoansRequest, TokenDebtLoansResponse,
    TokenDebtOffersRequest, TokenDebtOffersResponse,
    TokenTradesRequest, TokenTradesResponse
)
from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

from .base import BaseAPI

class TokensAPI(BaseAPI):
    async def get_token_mcap(self, request: TokenMcapRequest) -> TokenMcapResponse:
        """
        TapTools endpoint:
        GET /token/mcap
        
        Get supply + market cap of a token (circulating from external repo).
        """
        url = "/token/mcap"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenMcapResponse(__root__=response_data)

    async def get_token_holders(self, request: TokenHoldersRequest) -> TokenHoldersResponse:
        """
        TapTools endpoint:
        GET /token/holders
        
        Get total number of holders (aggregates addresses with same stake).
        """
        url = "/token/holders"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenHoldersResponse(**response_data)

    async def get_token_holders_top(self, request: TokenTopHoldersRequest) -> TokenTopHoldersResponse:
        """
        TapTools endpoint:
        GET /token/holders/top
        
        Read top holders of a token.
        """
        url = "/token/holders/top"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTopHoldersResponse(__root__=response_data)

    async def get_token_indicators(self, request: TokenIndicatorsRequest) -> TokenIndicatorsResponse:
        """
        TapTools endpoint:
        GET /token/indicators
        
        Create indicator values (EMA, RSI, MACD) for a token's price data.
        """
        url = "/token/indicators"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenIndicatorsResponse(__root__=response_data)

    async def get_token_links(self, request: TokenLinksRequest) -> TokenLinksResponse:
        """
        TapTools endpoint:
        GET /token/links
        
        Get a token's social/contact links.
        """
        url = "/token/links"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenLinksResponse(**response_data)

    async def get_token_ohlcv(self, request: TokenOHLCVRequest) -> TokenOHLCVResponse:
        """
        TapTools endpoint:
        GET /token/ohlcv
        
        Get token OHLCV (aggregated or by onchain ID).
        """
        url = "/token/ohlcv"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenOHLCVResponse(__root__=response_data)

    async def get_token_pools(self, request: TokenPoolsRequest) -> TokenPoolsResponse:
        """
        TapTools endpoint:
        GET /token/pools
        
        Get active liquidity pools for a token.
        """
        url = "/token/pools"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenPoolsResponse(__root__=response_data)

    async def post_token_prices(self, request: TokenPricesRequest) -> TokenPricesResponse:
        """
        TapTools endpoint:
        POST /token/prices
        
        Move an array of token units to get aggregated prices. Max batch size: 100.
        """
        url = "/token/prices"
        response_data = await self._make_request("post", url, json=request.units)
        return TokenPricesResponse(__root__=response_data)

    async def get_token_price_percent_changes(self, request: TokenPriceChangesRequest) -> TokenPriceChangesResponse:
        """
        TapTools endpoint:
        GET /token/prices/chg
        
        Get token price % changes over multiple timeframes.
        """
        url = "/token/prices/chg"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenPriceChangesResponse(__root__=response_data)

    async def get_token_trades(self, request: TokenTradesRequest) -> TokenTradesResponse:
        """
        TapTools endpoint:
        GET /token/trades
        
        Get token trades across DEXes.
        """
        url = "/token/trades"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTradesResponse(__root__=response_data)

    async def get_token_trade_stats(self, request: TokenTradingStatsRequest) -> TokenTradingStatsResponse:
        """
        TapTools endpoint:
        GET /token/trading/stats
        
        Get aggregated trading stats for a token over timeframe.
        """
        url = "/token/trading/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTradingStatsResponse(__root__=response_data)

    async def get_token_active_loans(self, request: TokenDebtLoansRequest) -> TokenDebtLoansResponse:
        """
        TapTools endpoint:
        GET /token/debt/loans
        
        Update active P2P loans for a given token (Lenfi, Levvy).
        """
        url = "/token/debt/loans"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenDebtLoansResponse(__root__=response_data)

    async def get_token_loan_offers(self, request: TokenDebtOffersRequest) -> TokenDebtOffersResponse:
        """
        TapTools endpoint:
        GET /token/debt/offers
        
        Get active P2P loan offers (Lenfi, Levvy).
        """
        url = "/token/debt/offers"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenDebtOffersResponse(__root__=response_data)

    async def get_token_top_tokens_by_liquidity(self, request: TokenTopLiquidityRequest) -> TokenTopLiquidityResponse:
        """
        TapTools endpoint:
        GET /token/top/liquidity
        
        Get tokens ranked by total DEX liquidity.
        """
        url = "/token/top/liquidity"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTopLiquidityResponse(__root__=response_data)

    async def get_token_top_tokens_by_mcap(self, request: TokenTopMcapRequest) -> TokenTopMcapResponse:
        """
        TapTools endpoint:
        GET /token/top/mcap
        
        Get tokens with top market cap (excludes deprecated).
        """
        url = "/token/top/mcap"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTopMcapResponse(__root__=response_data)

    async def get_token_top_tokens_by_volume(self, request: TokenTopVolumeRequest) -> TokenTopVolumeResponse:
        """
        TapTools endpoint:
        GET /token/top/volume
        
        Get tokens with top volume for a timeframe.
        """
        url = "/token/top/volume"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenTopVolumeResponse(__root__=response_data)

    async def get_quote_price(self, request: TokenQuoteRequest) -> TokenQuoteResponse:
        """
        TapTools endpoint:
        GET /token/quote
        
        Get current quote price (e.g. ADA/USD).
        """
        url = "/token/quote"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TokenQuoteResponse(**response_data)

    async def list_quote_currencies(self) -> TokenQuoteAvailableResponse:
        """
        TapTools endpoint:
        GET /token/quote/available
        
        List available quote currencies.
        """
        url = "/token/quote/available"
        response_data = await self._make_request("get", url)
        return TokenQuoteAvailableResponse(__root__=response_data)

    async def get_token_price(self, request: TokenPricesRequest) -> TokenPricesResponse:
        """
        TapTools endpoint:
        POST /token/prices

        Aggregated price across DEXs for the given token unit.
        """
        url = "/token/prices"
        response_data = await self._make_request("post", url, json=request.units)
        return TokenPricesResponse(__root__=response_data)
