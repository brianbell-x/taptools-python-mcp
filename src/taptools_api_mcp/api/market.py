import logging
import httpx
from mcp.server.fastmcp import Context

from ..utils.exceptions import TapToolsError, ErrorType
from ..models.market import MetricsResponse
# (We can define a typed model for the stats if needed.)

logger = logging.getLogger("taptools_mcp.market")

class MarketAPI:
    async def get_market_stats(self, quote: str, include_deprecated: bool, min_liquidity: float, ctx: Context) -> dict:
        client = ctx.request_context.lifespan_context["client"]
        params = {
            "quote": quote,
            "includeDeprecated": include_deprecated,
            "minLiquidity": min_liquidity
        }
        try:
            resp = await client.get("/market/stats", params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(message=str(e), error_type=ErrorType.CONNECTION)

    async def get_metrics(self, ctx: Context) -> MetricsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/metrics")
            resp.raise_for_status()
            data = resp.json()
            return MetricsResponse(metrics=data)
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(message=str(e), error_type=ErrorType.CONNECTION)

    async def get_market_overview(self, ctx: Context) -> dict:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/market/overview")
            resp.raise_for_status()
            return resp.json()  # e.g. { "gainers": [...], "losers": [...], "trending": [...] }
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(message=str(e), error_type=ErrorType.CONNECTION)
