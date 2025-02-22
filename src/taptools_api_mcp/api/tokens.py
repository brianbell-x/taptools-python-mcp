import logging
import httpx
from typing import Any
from mcp.server.fastmcp import Context

from ..utils.exceptions import TapToolsError, ErrorType
from ..models.tokens import (
    TokenMcapRequest, TokenMcapResponse,
    TokenHoldersRequest, TokenHoldersResponse,
    TokenTopHoldersRequest, TokenTopHoldersResponse,
    TokenPricesRequest, TokenPricesResponse,
    TokenPriceChangesRequest, TokenPriceChangesResponse,
    TokenOHLCVRequest, TokenOHLCVResponse,
    TokenTradesRequest, TokenTradesResponse,
    TokenTradingStatsRequest, TokenTradingStatsResponse,
    TokenDebtLoansRequest, TokenDebtLoansResponse,
    TokenDebtOffersRequest, TokenDebtOffersResponse,
    TokenTopLiquidityRequest, TokenTopLiquidityResponse,
    TokenTopMcapRequest, TokenTopMcapResponse,
    TokenTopVolumeRequest, TokenTopVolumeResponse,
    TokenLinksRequest, TokenLinksResponse,
    TokenIndicatorsRequest, TokenIndicatorsResponse,
    TokenPoolsRequest, TokenPoolsResponse,
    TokenQuoteRequest, TokenQuoteResponse
)

logger = logging.getLogger("taptools_mcp.tokens")

class TokensAPI:
    """Implementation of token-related endpoints."""

    async def verify_connection(self, ctx: Context) -> dict:
        """Call a simple TapTools endpoint to verify the API key."""
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/quote/available")
            resp.raise_for_status()
            data = resp.json()
            return {"available_quotes": data}
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_mcap(self, request: TokenMcapRequest, ctx: Context) -> TokenMcapResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/mcap", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenMcapResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_holders(self, request: TokenHoldersRequest, ctx: Context) -> TokenHoldersResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/holders", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenHoldersResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_holders_top(self, request: TokenTopHoldersRequest, ctx: Context) -> TokenTopHoldersResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/holders/top", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTopHoldersResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def post_token_prices(self, request: TokenPricesRequest, ctx: Context) -> TokenPricesResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.post("/token/prices", json=request.units)
            resp.raise_for_status()
            return TokenPricesResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_price_percent_changes(self, request: TokenPriceChangesRequest, ctx: Context) -> TokenPriceChangesResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/prices/chg", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenPriceChangesResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_trades(self, request: TokenTradesRequest, ctx: Context) -> TokenTradesResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/trades", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTradesResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_trade_stats(self, request: TokenTradingStatsRequest, ctx: Context) -> TokenTradingStatsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/trading/stats", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTradingStatsResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_ohlcv(self, request: TokenOHLCVRequest, ctx: Context) -> TokenOHLCVResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/ohlcv", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenOHLCVResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_links(self, request: TokenLinksRequest, ctx: Context) -> TokenLinksResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/links", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenLinksResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_indicators(self, request: TokenIndicatorsRequest, ctx: Context) -> TokenIndicatorsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/indicators", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenIndicatorsResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_pools(self, request: TokenPoolsRequest, ctx: Context) -> TokenPoolsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/pools", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenPoolsResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_active_loans(self, request: TokenDebtLoansRequest, ctx: Context) -> TokenDebtLoansResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/debt/loans", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenDebtLoansResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_loan_offers(self, request: TokenDebtOffersRequest, ctx: Context) -> TokenDebtOffersResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/debt/offers", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenDebtOffersResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_top_tokens_by_liquidity(self, request: TokenTopLiquidityRequest, ctx: Context) -> TokenTopLiquidityResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/top/liquidity", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTopLiquidityResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_top_tokens_by_mcap(self, request: TokenTopMcapRequest, ctx: Context) -> TokenTopMcapResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/top/mcap", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTopMcapResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_token_top_tokens_by_volume(self, request: TokenTopVolumeRequest, ctx: Context) -> TokenTopVolumeResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/top/volume", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenTopVolumeResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_quote_price(self, request: TokenQuoteRequest, ctx: Context) -> TokenQuoteResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/token/quote", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return TokenQuoteResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )
