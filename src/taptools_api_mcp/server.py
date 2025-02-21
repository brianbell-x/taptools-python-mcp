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
from .models.market import MarketStatsRequest, MetricsResponse
from .models.integration import (
    IntegrationAssetRequest, IntegrationBlockRequest,
    IntegrationEventsRequest, IntegrationExchangeRequest,
    IntegrationPairRequest
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
        
        # API classes will be initialized in __aenter__
        self.tokens_api: Optional[TokensAPI] = None
        self.nfts_api: Optional[NftsAPI] = None
        self.market_api: Optional[MarketAPI] = None
        self.integration_api: Optional[IntegrationAPI] = None
        self.onchain_api: Optional[OnchainAPI] = None
        self.wallet_api: Optional[WalletAPI] = None

        # Register all tools
        self.register_tools()

    async def __aenter__(self):
        """Initialize client and APIs when entering context"""
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        # Initialize API classes with client
        self.tokens_api = TokensAPI(self._client)
        self.nfts_api = NftsAPI(self._client)
        self.market_api = MarketAPI(self._client)
        self.integration_api = IntegrationAPI(self._client)
        self.onchain_api = OnchainAPI(self._client)
        self.wallet_api = WalletAPI(self._client)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close client when exiting context"""
        await self._client.aclose()

    async def handle_error(self, e: Exception, endpoint: Optional[str] = None, ctx: Optional[Context] = None) -> None:
        """
        Convert TapTools exceptions to McpError with appropriate error codes and enhanced logging.
        
        Args:
            e: The exception to handle
            endpoint: Optional endpoint name for context in error messages
            ctx: Optional Context object for client-side logging
        """
        # Get traceback for complete context
        import traceback
        tb = traceback.format_exc()
        
        # Build error context dictionary for structured logging
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
        
        # Enhanced error logging with context
        error_msg = f"API error{f' in {endpoint}' if endpoint else ''}: {str(e)}"
        if ctx:
            await ctx.log("error", error_msg)
            await ctx.debug(f"Error context:\n{json.dumps(error_context, indent=2)}")
        else:
            logger.error(error_msg, extra=error_context)
            logger.debug(f"Error context:\n{json.dumps(error_context, indent=2)}")
        
        if isinstance(e, TapToolsError):
            error_code, message = e.to_mcp_error()
            
            # Add endpoint context to message
            if endpoint:
                message = f"[{endpoint}] {message}"
            
            # Enhanced error details logging
            if e.error_details:
                debug_msg = (
                    f"Detailed error information:\n"
                    f"{json.dumps(e.error_details, indent=2)}"
                )
                if ctx:
                    await ctx.debug(debug_msg)
                else:
                    logger.debug(debug_msg)
            
            # Log rate limit information if present
            if e.retry_after:
                info_msg = (
                    f"Rate limit will reset at: {e.retry_after.isoformat()} "
                    f"(in {(e.retry_after - datetime.now()).total_seconds():.1f}s)"
                )
                if ctx:
                    await ctx.info(info_msg)
                else:
                    logger.info(info_msg)
            
            # Include status code in message if available
            if e.status_code:
                message = f"{message} (HTTP {e.status_code})"
            
            raise McpError(ErrorData(code=error_code, message=message))
        else:
            # Unexpected errors get logged with full context
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
        # Token Tools
        @self.app.tool(name="get_token_mcap", description="Get token market cap info")
        async def handle_get_token_mcap(request: TokenMcapRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching market cap for token {request.token_id}")
                result = await self.tokens_api.get_token_mcap(request)
                await ctx.info("Successfully retrieved token market cap data")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_mcap", ctx)

        @self.app.tool(name="get_token_holders", description="Get total number of token holders")
        async def handle_get_token_holders(request: TokenHoldersRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching holder count for token {request.token_id}")
                result = await self.tokens_api.get_token_holders(request)
                await ctx.info("Successfully retrieved token holder count")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_holders", ctx)

        @self.app.tool(name="get_token_holders_top", description="Get top token holders")
        async def handle_get_token_holders_top(request: TokenTopHoldersRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching top holders for token {request.token_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating top holders query")
                result = await self.tokens_api.get_token_holders_top(request)
                await ctx.progress(1.0, "Retrieved top holders data")
                await ctx.info("Successfully retrieved top token holders")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_token_holders_top", ctx)

        # NFT Tools
        @self.app.tool(name="get_nft_asset_sales", description="Get NFT asset sales history")
        async def handle_get_nft_asset_sales(request: NFTAssetSalesRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching sales history for NFT asset {request.asset_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating sales history query")
                result = await self.nfts_api.get_asset_sales(request)
                await ctx.progress(1.0, "Retrieved sales history")
                await ctx.info("Successfully retrieved NFT asset sales history")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_asset_sales", ctx)

        @self.app.tool(name="get_nft_asset_stats", description="Get high-level stats on a specific NFT asset")
        async def handle_get_nft_asset_stats(request: NFTAssetStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching stats for NFT asset {request.asset_id}")
                result = await self.nfts_api.get_asset_stats(request)
                await ctx.info("Successfully retrieved NFT asset stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_asset_stats", ctx)

        @self.app.tool(name="get_nft_asset_traits", description="Get trait data and prices for a specific NFT")
        async def handle_get_nft_asset_traits(request: NFTAssetTraitsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trait data for NFT asset {request.asset_id}")
                result = await self.nfts_api.get_asset_traits(request)
                await ctx.info("Successfully retrieved NFT asset trait data")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_asset_traits", ctx)

        @self.app.tool(name="get_nft_collection_assets", description="Get list of NFTs in a collection")
        async def handle_get_nft_collection_assets(request: NFTCollectionAssetsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching assets for collection {request.collection_id}")
                # This is typically a larger dataset, so we'll report progress
                await ctx.progress(0.2, "Initiating collection assets query")
                result = await self.nfts_api.get_collection_assets(request)
                await ctx.progress(1.0, "Retrieved collection assets")
                await ctx.info(f"Successfully retrieved {len(result.assets)} assets from collection")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_assets", ctx)

        @self.app.tool(name="get_nft_collection_info", description="Get basic collection info")
        async def handle_get_nft_collection_info(request: NFTCollectionInfoRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching info for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_info(request)
                await ctx.info("Successfully retrieved collection info")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_info", ctx)

        @self.app.tool(name="get_nft_collection_stats", description="Get collection stats")
        async def handle_get_nft_collection_stats(request: NFTCollectionStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching stats for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_stats(request)
                await ctx.info("Successfully retrieved collection stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_stats", ctx)

        @self.app.tool(name="get_nft_collection_stats_extended", description="Get extended stats with % changes")
        async def handle_get_nft_collection_stats_extended(request: NFTCollectionExtendedStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching extended stats for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_stats_extended(request)
                await ctx.info("Successfully retrieved extended collection stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_stats_extended", ctx)

        @self.app.tool(name="get_nft_collection_holders_distribution", description="Get distribution of NFTs by quantity held")
        async def handle_get_nft_collection_holders_distribution(request: NFTCollectionHoldersDistributionRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching holder distribution for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating holder distribution query")
                result = await self.nfts_api.get_collection_holders_distribution(request)
                await ctx.progress(1.0, "Retrieved holder distribution")
                await ctx.info("Successfully retrieved collection holder distribution")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_holders_distribution", ctx)

        @self.app.tool(name="get_nft_collection_holders_top", description="Get top holders of a collection")
        async def handle_get_nft_collection_holders_top(request: NFTCollectionTopHoldersRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching top holders for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating top holders query")
                result = await self.nfts_api.get_collection_holders_top(request)
                await ctx.progress(1.0, "Retrieved top holders data")
                await ctx.info("Successfully retrieved collection top holders")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_holders_top", ctx)

        @self.app.tool(name="get_nft_collection_holder_counts", description="Get trended holder counts by day")
        async def handle_get_nft_collection_holder_counts(request: NFTCollectionHoldersTrendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trended holder counts for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating holder counts query")
                result = await self.nfts_api.get_collection_holder_counts(request)
                await ctx.progress(1.0, "Retrieved holder counts data")
                await ctx.info("Successfully retrieved trended holder counts")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_holder_counts", ctx)

        @self.app.tool(name="get_nft_collection_listings", description="Get active listings + total supply")
        async def handle_get_nft_collection_listings(request: NFTCollectionListingsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching listings for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_listings(request)
                await ctx.info("Successfully retrieved collection listings")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_listings", ctx)

        @self.app.tool(name="get_nft_collection_listings_depth", description="Get cumulative listing data at price points")
        async def handle_get_nft_collection_listings_depth(request: NFTCollectionListingsDepthRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching listings depth for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating listings depth query")
                result = await self.nfts_api.get_collection_listings_depth(request)
                await ctx.progress(1.0, "Retrieved listings depth data")
                await ctx.info("Successfully retrieved collection listings depth")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_listings_depth", ctx)

        @self.app.tool(name="get_nft_collection_listings_individual", description="Get active listings with pagination")
        async def handle_get_nft_collection_listings_individual(request: NFTCollectionIndividualListingsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching individual listings for collection {request.collection_id}")
                # This operation might take longer due to pagination, so we'll report progress
                await ctx.progress(0.2, "Initiating individual listings query")
                result = await self.nfts_api.get_collection_listings_individual(request)
                await ctx.progress(1.0, "Retrieved individual listings")
                await ctx.info("Successfully retrieved individual collection listings")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_listings_individual", ctx)

        @self.app.tool(name="get_nft_collection_listing_counts", description="Get trended listings + floor price")
        async def handle_get_nft_collection_listing_counts(request: NFTCollectionListingsTrendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trended listing counts for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating trended listings query")
                result = await self.nfts_api.get_collection_listing_counts(request)
                await ctx.progress(1.0, "Retrieved trended listings data")
                await ctx.info("Successfully retrieved trended listing counts")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_listing_counts", ctx)

        @self.app.tool(name="get_nft_collection_ohlcv", description="Get floor price OHLCV data")
        async def handle_get_nft_collection_ohlcv(request: NFTCollectionOHLCVRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching OHLCV data for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_ohlcv(request)
                await ctx.info("Successfully retrieved collection OHLCV data")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_ohlcv", ctx)

        @self.app.tool(name="get_nft_collection_trades", description="Get trades for collection or market")
        async def handle_get_nft_collection_trades(request: NFTCollectionTradesRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trades for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating trades query")
                result = await self.nfts_api.get_collection_trades(request)
                await ctx.progress(1.0, "Retrieved trades data")
                await ctx.info("Successfully retrieved collection trades")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_trades", ctx)

        @self.app.tool(name="get_nft_collection_trades_stats", description="Get volume + sales stats")
        async def handle_get_nft_collection_trades_stats(request: NFTCollectionTradeStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trade stats for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_trades_stats(request)
                await ctx.info("Successfully retrieved collection trade stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_trades_stats", ctx)

        @self.app.tool(name="get_nft_collection_volume_and_sales", description="Get volume and sales trends")
        async def handle_get_nft_collection_volume_and_sales(request: NFTCollectionVolumeTrendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching volume and sales trends for collection {request.collection_id}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating volume and sales query")
                result = await self.nfts_api.get_collection_volume_and_sales(request)
                await ctx.progress(1.0, "Retrieved volume and sales data")
                await ctx.info("Successfully retrieved collection volume and sales trends")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_volume_and_sales", ctx)

        @self.app.tool(name="get_nft_collection_traits_price", description="Get traits and floor prices")
        async def handle_get_nft_collection_traits_price(request: NFTCollectionTraitPricesRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trait prices for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_traits_price(request)
                await ctx.info("Successfully retrieved collection trait prices")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_traits_price", ctx)

        @self.app.tool(name="get_nft_collection_traits_rarity", description="Get metadata attributes + likelihood")
        async def handle_get_nft_collection_traits_rarity(request: NFTCollectionTraitRarityRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trait rarity data for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_traits_rarity(request)
                await ctx.info("Successfully retrieved collection trait rarity data")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_traits_rarity", ctx)

        @self.app.tool(name="get_nft_collection_traits_rarity_rank", description="Get NFT rarity rank")
        async def handle_get_nft_collection_traits_rarity_rank(request: NFTCollectionTraitRarityRankRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching trait rarity rank for collection {request.collection_id}")
                result = await self.nfts_api.get_collection_traits_rarity_rank(request)
                await ctx.info("Successfully retrieved collection trait rarity rank")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_collection_traits_rarity_rank", ctx)

        @self.app.tool(name="get_nft_market_stats", description="Get top-level NFT market stats")
        async def handle_get_nft_market_stats(request: NFTMarketStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching NFT market stats")
                result = await self.nfts_api.get_market_stats(request)
                await ctx.info("Successfully retrieved NFT market stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_market_stats", ctx)

        @self.app.tool(name="get_nft_market_stats_extended", description="Get NFT market stats + % changes")
        async def handle_get_nft_market_stats_extended(request: NFTMarketExtendedStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching extended NFT market stats")
                result = await self.nfts_api.get_market_stats_extended(request)
                await ctx.info("Successfully retrieved extended NFT market stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_market_stats_extended", ctx)

        @self.app.tool(name="get_nft_market_volume_and_sales", description="Get NFT market volume trends")
        async def handle_get_nft_market_volume_and_sales(request: NFTMarketVolumeTrendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching NFT market volume and sales trends")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating market volume query")
                result = await self.nfts_api.get_market_volume_and_sales(request)
                await ctx.progress(1.0, "Retrieved market volume data")
                await ctx.info("Successfully retrieved NFT market volume and sales trends")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_market_volume_and_sales", ctx)

        @self.app.tool(name="get_nft_marketplaces_stats", description="Get marketplace stats")
        async def handle_get_nft_marketplaces_stats(request: NFTMarketplaceStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching NFT marketplace stats")
                result = await self.nfts_api.get_marketplaces_stats(request)
                await ctx.info("Successfully retrieved NFT marketplace stats")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_marketplaces_stats", ctx)

        @self.app.tool(name="get_nft_top_rankings", description="Get top NFT rankings")
        async def handle_get_nft_top_rankings(request: NFTTopTimeframeRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching top NFT rankings for timeframe {request.timeframe}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating rankings query")
                result = await self.nfts_api.get_top_rankings(request)
                await ctx.progress(1.0, "Retrieved rankings data")
                await ctx.info("Successfully retrieved top NFT rankings")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_top_rankings", ctx)

        @self.app.tool(name="get_nft_top_collections_by_volume", description="Get top NFT collections by volume")
        async def handle_get_nft_top_collections_by_volume(request: NFTTopVolumeRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching top NFT collections by volume")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating top collections query")
                result = await self.nfts_api.get_top_collections_by_volume(request)
                await ctx.progress(1.0, "Retrieved top collections data")
                await ctx.info("Successfully retrieved top NFT collections by volume")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_top_collections_by_volume", ctx)

        @self.app.tool(name="get_nft_top_collections_by_volume_with_changes", description="Get top collections with % changes")
        async def handle_get_nft_top_collections_by_volume_with_changes(request: NFTTopVolumeExtendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching top NFT collections by volume with changes")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating extended top collections query")
                result = await self.nfts_api.get_top_collections_by_volume_with_changes(request)
                await ctx.progress(1.0, "Retrieved extended top collections data")
                await ctx.info("Successfully retrieved top NFT collections with changes")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_nft_top_collections_by_volume_with_changes", ctx)

        # Market Tools
        @self.app.tool(name="get_market_stats", description="Get market-wide statistics")
        async def handle_get_market_stats(request: MarketStatsRequest, ctx: Context) -> str:
            try:
                await ctx.debug("Fetching market-wide statistics")
                result = await self.market_api.get_market_stats(request)
                await ctx.info("Successfully retrieved market statistics")
                return json.dumps(result.model_dump(), indent=2)
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

        # Integration Tools
        @self.app.tool(name="get_integration_asset", description="Get asset details by ID")
        async def handle_get_integration_asset(request: IntegrationAssetRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching asset details for ID {request.asset_id}")
                result = await self.integration_api.get_asset(request)
                await ctx.info("Successfully retrieved asset details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_asset", ctx)

        @self.app.tool(name="get_integration_block", description="Get block by number or timestamp")
        async def handle_get_integration_block(request: IntegrationBlockRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching block details for {request.block_number or request.timestamp}")
                result = await self.integration_api.get_block(request)
                await ctx.info("Successfully retrieved block details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_block", ctx)

        @self.app.tool(name="get_integration_events", description="List events within a block range")
        async def handle_get_integration_events(request: IntegrationEventsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching events for block range {request.from_block} to {request.to_block}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating events query")
                result = await self.integration_api.get_events(request)
                await ctx.progress(1.0, "Retrieved events data")
                await ctx.info("Successfully retrieved integration events")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_events", ctx)

        @self.app.tool(name="get_integration_exchange", description="Get DEX details by factory address/ID")
        async def handle_get_integration_exchange(request: IntegrationExchangeRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching DEX details for {request.factory_address or request.factory_id}")
                result = await self.integration_api.get_exchange(request)
                await ctx.info("Successfully retrieved DEX details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_exchange", ctx)

        @self.app.tool(name="get_integration_latest_block", description="Get latest processed block info")
        async def handle_get_integration_latest_block(ctx: Context) -> str:
            try:
                await ctx.debug("Fetching latest processed block info")
                result = await self.integration_api.get_latest_block()
                await ctx.info("Successfully retrieved latest block info")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_latest_block", ctx)

        @self.app.tool(name="get_integration_pair", description="Get pair/pool details by address")
        async def handle_get_integration_pair(request: IntegrationPairRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching pair/pool details for address {request.pair_address}")
                result = await self.integration_api.get_pair(request)
                await ctx.info("Successfully retrieved pair/pool details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_integration_pair", ctx)

        # Onchain Tools
        @self.app.tool(name="get_asset_supply", description="Get onchain asset supply")
        async def handle_get_asset_supply(request: AssetSupplyRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching onchain supply for asset {request.asset_id}")
                result = await self.onchain_api.get_asset_supply(request)
                await ctx.info("Successfully retrieved asset supply")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_asset_supply", ctx)

        @self.app.tool(name="get_address_details", description="Get address info including balances")
        async def handle_get_address_details(request: AddressInfoRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching details for address {request.address}")
                result = await self.onchain_api.get_address_details(request)
                await ctx.info("Successfully retrieved address details")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_address_details", ctx)

        @self.app.tool(name="get_address_utxos", description="Get current UTxOs for an address")
        async def handle_get_address_utxos(request: AddressUTXOsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching UTXOs for address {request.address}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating UTXOs query")
                result = await self.onchain_api.get_address_utxos(request)
                await ctx.progress(1.0, "Retrieved UTXOs data")
                await ctx.info("Successfully retrieved address UTXOs")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_address_utxos", ctx)

        @self.app.tool(name="get_transaction_details", description="Get UTxOs from a specific transaction")
        async def handle_get_transaction_details(request: TransactionUTXOsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching UTXOs for transaction {request.tx_hash}")
                result = await self.onchain_api.get_transaction_details(request)
                await ctx.info("Successfully retrieved transaction UTXOs")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_transaction_details", ctx)

        # Wallet Tools
        @self.app.tool(name="get_wallet_portfolio", description="Get wallet portfolio positions")
        async def handle_get_wallet_portfolio(request: WalletPortfolioPositionsRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching portfolio positions for wallet {request.wallet_address}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating portfolio query")
                result = await self.wallet_api.get_portfolio_positions(request)
                await ctx.progress(1.0, "Retrieved portfolio data")
                await ctx.info("Successfully retrieved wallet portfolio positions")
                return json.dumps(result.model_dump(), indent=2)
            except Exception as e:
                await self.handle_error(e, "get_wallet_portfolio", ctx)

        @self.app.tool(name="get_wallet_trades_tokens", description="Get token trade history for a wallet")
        async def handle_get_wallet_trades_tokens(request: WalletTokenTradesRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching token trade history for wallet {request.wallet_address}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating trade history query")
                result = await self.wallet_api.get_wallet_trades_tokens(request)
                await ctx.progress(1.0, "Retrieved trade history data")
                await ctx.info("Successfully retrieved wallet token trades")
                return json.dumps([trade.model_dump() for trade in result], indent=2)
            except Exception as e:
                await self.handle_error(e, "get_wallet_trades_tokens", ctx)

        @self.app.tool(name="get_wallet_value_trended", description="Get historical wallet value in 4hr intervals")
        async def handle_get_wallet_value_trended(request: WalletValueTrendedRequest, ctx: Context) -> str:
            try:
                await ctx.debug(f"Fetching historical value trends for wallet {request.wallet_address}")
                # This operation might take longer, so we'll report progress
                await ctx.progress(0.2, "Initiating historical value query")
                result = await self.wallet_api.get_wallet_value_trended(request)
                await ctx.progress(1.0, "Retrieved historical value data")
                await ctx.info("Successfully retrieved wallet value trends")
                return json.dumps([trend.model_dump() for trend in result], indent=2)
            except Exception as e:
                await self.handle_error(e, "get_wallet_value_trended", ctx)

        # Verification Tool
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
        """
        Run the MCP server on stdio (main loop).
        """
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(read_stream, write_stream, self.app.create_initialization_options())

async def main():
    """
    Main entry point for the TapTools MCP server.
    """
    try:
        config = ServerConfig.from_env()
        server = TapToolsServer(config)
        async with server:
            await server.run_stdio_async()
    except Exception as e:
        logger.error(f"Failed to start TapToolsServer: {str(e)}")
        raise
