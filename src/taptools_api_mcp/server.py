"""
TapTools MCP server implementation.

Exposes TapTools endpoints as MCP tools.
"""
import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import httpx

from mcp.server.stdio import stdio_server
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import ErrorData
from mcp.shared.exceptions import McpError

from .api.tokens import TokensAPI
from .api.nfts import NftsAPI
from .api.market import MarketAPI
from .api.integration import IntegrationAPI
from .api.onchain import OnchainAPI
from .api.wallet import WalletAPI
from .utils.exceptions import TapToolsError, ErrorCode, ErrorType

# Request/Response Models
from .models.tokens import (
    TokenMcapRequest, TokenHoldersRequest, TokenTopHoldersRequest,
    TokenQuoteRequest, TokenIndicatorsRequest, TokenLinksRequest,
    TokenOHLCVRequest, TokenPoolsRequest, TokenPricesRequest,
    TokenPriceChangesRequest, TokenTradesRequest, TokenTradingStatsRequest,
    TokenDebtLoansRequest, TokenDebtOffersRequest, TokenTopLiquidityRequest,
    TokenTopMcapRequest, TokenTopVolumeRequest
)
from .models.nfts import (
    NFTAssetSalesRequest, NFTCollectionStatsRequest,
    NFTAssetStatsRequest, NFTAssetTraitsRequest,
    NFTCollectionAssetsRequest, NFTCollectionInfoRequest,
    NFTCollectionExtendedStatsRequest, NFTCollectionHoldersDistributionRequest,
    NFTCollectionTopHoldersRequest, NFTCollectionHoldersTrendedRequest,
    NFTCollectionListingsRequest, NFTCollectionListingsDepthRequest,
    NFTCollectionIndividualListingsRequest, NFTCollectionListingsTrendedRequest,
    NFTCollectionOHLCVRequest, NFTCollectionTradesRequest,
    NFTCollectionTradeStatsRequest, NFTCollectionVolumeTrendedRequest,
    NFTCollectionTraitPricesRequest, NFTCollectionTraitRarityRequest,
    NFTCollectionTraitRarityRankRequest, NFTMarketStatsRequest,
    NFTMarketExtendedStatsRequest, NFTMarketVolumeTrendedRequest,
    NFTMarketplaceStatsRequest, NFTTopTimeframeRequest,
    NFTTopVolumeRequest, NFTTopVolumeExtendedRequest
)
from .models.market import (
    MarketStatsRequest, MetricsResponse
)
from .models.integration import (
    IntegrationAssetRequest, IntegrationBlockRequest,
    IntegrationEventsRequest, IntegrationExchangeRequest,
    IntegrationPairRequest, IntegrationPolicyAssetsRequest
)
from .models.onchain import (
    AssetSupplyRequest, AddressInfoRequest,
    AddressUTXOsRequest, TransactionUTXOsRequest
)
from .models.wallet import (
    WalletPortfolioPositionsRequest, WalletTokenTradesRequest,
    WalletValueTrendedRequest
)

logger = logging.getLogger("taptools_mcp")

class ServerConfig(BaseModel):
    """
    Holds config values for the TapTools MCP server.
    """
    api_key: str = Field(..., description="TapTools API key", alias="TAPTOOLS_API_KEY")
    base_url: str = Field(
        default="https://openapi.taptools.io/api/v1",
        description="TapTools API base URL"
    )

    @classmethod
    def from_env(cls, env_file: str = ".env"):
        if os.path.exists(env_file):
            load_dotenv(env_file)
        api_key = os.getenv("TAPTOOLS_API_KEY", "").strip()
        if not api_key:
            raise ValueError("TAPTOOLS_API_KEY not found. Please set it in .env or environment.")
        return cls(TAPTOOLS_API_KEY=api_key)

class TapToolsServer:
    """
    The main server that registers TapTools endpoints as MCP tools.
    """
    def __init__(self, config: ServerConfig):
        self.config = config
        self.app = FastMCP(name="taptools-server")
        self.tokens_api: Optional[TokensAPI] = None
        self.nfts_api: Optional[NftsAPI] = None
        self.market_api: Optional[MarketAPI] = None
        self.integration_api: Optional[IntegrationAPI] = None
        self.onchain_api: Optional[OnchainAPI] = None
        self.wallet_api: Optional[WalletAPI] = None

        # Register all tools
        self.register_tools()

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        self.tokens_api = TokensAPI(self._client)
        self.nfts_api = NftsAPI(self._client)
        self.market_api = MarketAPI(self._client)
        self.integration_api = IntegrationAPI(self._client)
        self.onchain_api = OnchainAPI(self._client)
        self.wallet_api = WalletAPI(self._client)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def handle_error(self, e: Exception, endpoint: Optional[str] = None, ctx: Optional[Context] = None) -> None:
        import traceback
        tb = traceback.format_exc()
        error_context = {
            'endpoint': endpoint,
            'error_type': type(e).__name__,
            'error_class': e.__class__.__name__,
            'traceback': tb
        }
        if isinstance(e, TapToolsError):
            error_context.update({
                'tap_tools_error_type': e.error_type.value,
                'status_code': e.status_code,
                'has_error_details': bool(e.error_details),
                'has_retry_after': bool(e.retry_after)
            })
        error_msg = f"API error{f' in {endpoint}' if endpoint else ''}: {str(e)}"
        if ctx:
            await ctx.log("error", error_msg)
            await ctx.debug(f"Error context:\n{json.dumps(error_context, indent=2)}")
        else:
            logger.error(error_msg, extra=error_context)
            logger.debug(f"Error context:\n{json.dumps(error_context, indent=2)}")

        if isinstance(e, TapToolsError):
            error_code, message = e.to_mcp_error()
            if endpoint:
                message = f"[{endpoint}] {message}"
            if e.error_details:
                debug_msg = (
                    f"Detailed error information:\n"
                    f"{json.dumps(e.error_details, indent=2)}"
                )
                if ctx:
                    await ctx.debug(debug_msg)
                else:
                    logger.debug(debug_msg)
            if e.retry_after:
                info_msg = (
                    f"Rate limit will reset at: {e.retry_after.isoformat()} "
                    f"(in {(e.retry_after - datetime.now()).total_seconds():.1f}s)"
                )
                if ctx:
                    await ctx.info(info_msg)
                else:
                    logger.info(info_msg)
            if e.status_code:
                message = f"{message} (HTTP {e.status_code})"
            raise McpError(ErrorData(code=error_code, message=message))
        else:
            if ctx:
                await ctx.debug(f"Unexpected error traceback:\n{tb}")
            else:
                logger.debug(f"Unexpected error traceback:\n{tb}")
            message = f"Unexpected error: {str(e)}"
            if endpoint:
                message = f"[{endpoint}] {message}"
            raise McpError(ErrorData(
                code=ErrorCode.API_ERROR,
                message=message
            ))

    def register_tools(self):
        """
        Register MCP tools for TapTools endpoints.
        """
        # ----------------------
        # Token Tools
        # ----------------------
        @self.app.tool(name="get_token_mcap", description="Get token market cap info")
        async def handle_get_token_mcap(request: TokenMcapRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching market cap for token {request.unit}")
                result = await self.tokens_api.get_token_mcap(request)
                await ctx.info("Successfully retrieved token market cap data")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_mcap", ctx)

        @self.app.tool(name="get_token_holders", description="Get total number of token holders")
        async def handle_get_token_holders(request: TokenHoldersRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching holder count for token {request.unit}")
                result = await self.tokens_api.get_token_holders(request)
                await ctx.info("Successfully retrieved token holder count")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_holders", ctx)

        @self.app.tool(name="get_token_holders_top", description="Get top token holders")
        async def handle_get_token_holders_top(request: TokenTopHoldersRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching top holders for token {request.unit}")
                await ctx.progress(0.2, "Initiating top holders query")
                result = await self.tokens_api.get_token_holders_top(request)
                await ctx.progress(1.0, "Retrieved top holders data")
                await ctx.info("Successfully retrieved top token holders")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_holders_top", ctx)

        # ----------------------
        # NFT Tools
        # ----------------------
        @self.app.tool(name="get_nft_asset_sales", description="Get NFT asset sales history")
        async def handle_get_nft_asset_sales(request: NFTAssetSalesRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching sales history for NFT policy={request.policy} name={request.name}")
                await ctx.progress(0.2, "Initiating sales history query")
                result = await self.nfts_api.get_asset_sales(request)
                await ctx.progress(1.0, "Retrieved sales history")
                await ctx.info("Successfully retrieved NFT asset sales history")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_asset_sales", ctx)

        @self.app.tool(name="get_nft_collection_stats", description="Get NFT collection stats")
        async def handle_get_nft_collection_stats(request: NFTCollectionStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching stats for collection {request.policy}")
                result = await self.nfts_api.get_collection_stats(request)
                await ctx.info("Successfully retrieved collection stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_stats", ctx)

        # ----------------------
        # Market Tools
        # ----------------------
        @self.app.tool(name="get_market_stats", description="Get market-wide statistics")
        async def handle_get_market_stats(params: Dict[str, Any], ctx: Context) -> str:
            """
            We accept a dict for the convenience of optional
            'quote', 'include_deprecated', 'min_liquidity' etc.
            Example:
              {
                "quote": "USD",
                "include_deprecated": true,
                "min_liquidity": 10000
              }
            """
            try:
                quote = params.get("quote", "ADA")
                include_deprecated = bool(params.get("include_deprecated", False))
                min_liquidity = float(params.get("min_liquidity", 0))
                await ctx.debug(f"Fetching market-wide stats. quote={quote}, deprecated={include_deprecated}, liquidity={min_liquidity}")
                result = await self.market_api.get_market_stats(
                    quote=quote,
                    include_deprecated=include_deprecated,
                    min_liquidity=min_liquidity
                )
                await ctx.info("Successfully retrieved market statistics")
                return json.dumps(result, indent=2)
            except Exception as e:
                await self.handle_error(e, "get_market_stats", ctx)

        @self.app.tool(name="get_market_metrics", description="Get daily request counts from past 30 days")
        async def handle_get_market_metrics(ctx: Context) -> str:
            try:
                await ctx.debug("Fetching daily request counts")
                result = await self.market_api.get_metrics()
                await ctx.info("Successfully retrieved market metrics")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_market_metrics", ctx)

        # NEW tool: get_market_overview
        @self.app.tool(name="get_market_overview", description="Get overview with gainers/losers/trending.")
        async def handle_get_market_overview(ctx: Context) -> str:
            try:
                await ctx.debug("Fetching market overview (gainers, losers, trending)")
                result = await self.market_api.get_market_overview()
                await ctx.info("Successfully retrieved market overview")
                return json.dumps(result, indent=2)
            except Exception as e:
                await self.handle_error(e, "get_market_overview", ctx)

        # ----------------------
        # Integration Tools
        # ----------------------
        @self.app.tool(name="get_integration_asset", description="Get asset details by ID")
        async def handle_get_integration_asset(request: IntegrationAssetRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching asset details for ID {request.id}")
                result = await self.integration_api.get_asset(request)
                await ctx.info("Successfully retrieved asset details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_asset", ctx)

        # NEW tool: get_policy_assets
        @self.app.tool(name="get_policy_assets", description="Get assets under a given policy ID.")
        async def handle_get_policy_assets(request: IntegrationPolicyAssetsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching assets for policy {request.id}, page={request.page}, perPage={request.perPage}")
                result = await self.integration_api.get_policy_assets(request)
                await ctx.info("Successfully retrieved policy assets")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_policy_assets", ctx)

        # ----------------------
        # Onchain Tools
        # ----------------------
        @self.app.tool(name="get_asset_supply", description="Get onchain asset supply")
        async def handle_get_asset_supply(request: AssetSupplyRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching onchain supply for asset {request.unit}")
                result = await self.onchain_api.get_asset_supply(request)
                await ctx.info("Successfully retrieved asset supply")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_asset_supply", ctx)

        @self.app.tool(name="verify_connection", description="Verify TapTools API authentication")
        async def handle_verify_connection(ctx: Context) -> str:
            try:
                await ctx.debug("Verifying TapTools API connection")
                result = await self.tokens_api.verify_connection()
                await ctx.info("Successfully verified API connection")
                return json.dumps(result, indent=2)
            except Exception as e:
                await self.handle_error(e, "verify_connection", ctx)

    async def run_stdio_async(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(read_stream, write_stream, self.app.create_initialization_options())

async def main():
    try:
        config = ServerConfig.from_env()
        server = TapToolsServer(config)
        async with server:
            await server.run_stdio_async()
    except Exception as e:
        logger.error(f"Failed to start TapToolsServer: {str(e)}")
        raise
