import os
import json
import logging
from typing import Optional
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import ErrorData

from .api.tokens import TokensAPI
from .api.nfts import NftsAPI
from .api.market import MarketAPI
from .api.integration import IntegrationAPI
from .api.onchain import OnchainAPI
from .api.wallet import WalletAPI

from .models.tokens import (
    TokenMcapRequest, TokenMcapResponse,
    TokenHoldersRequest, TokenHoldersResponse,
    TokenTopHoldersRequest, TokenTopHoldersResponse,
    TokenPricesRequest, TokenPricesResponse,
    TokenPriceChangesRequest, TokenPriceChangesResponse,
    TokenOHLCVRequest, TokenOHLCVResponse,
    TokenTradesRequest, TokenTradesResponse,
    TokenTradingStatsRequest, TokenTradingStatsResponse,
    TokenTopLiquidityRequest, TokenTopLiquidityResponse,
    TokenTopMcapRequest, TokenTopMcapResponse,
    TokenTopVolumeRequest, TokenTopVolumeResponse,
    TokenLinksRequest, TokenLinksResponse,
    TokenIndicatorsRequest, TokenIndicatorsResponse,
    TokenDebtLoansRequest, TokenDebtLoansResponse,
    TokenDebtOffersRequest, TokenDebtOffersResponse,
    TokenPoolsRequest, TokenPoolsResponse,
    TokenQuoteRequest, TokenQuoteResponse
)

from .models.nfts import (
    NFTAssetSalesRequest, NFTAssetSalesResponse,
    NFTCollectionStatsRequest, NFTCollectionStatsResponse,
    NFTAssetStatsRequest, NFTAssetStatsResponse,
    NFTAssetTraitsRequest, NFTAssetTraitsResponse,
    NFTCollectionAssetsRequest, NFTCollectionAssetsResponse,
    NFTCollectionInfoRequest, NFTCollectionInfoResponse,
    NFTCollectionExtendedStatsRequest, NFTCollectionExtendedStatsResponse,
    NFTCollectionHoldersDistributionRequest, NFTCollectionHoldersDistributionResponse,
    NFTCollectionTopHoldersRequest, NFTCollectionTopHoldersResponse,
    NFTCollectionHoldersTrendedRequest, NFTCollectionHoldersTrendedResponse,
    NFTCollectionListingsRequest, NFTCollectionListingsResponse,
    NFTCollectionListingsDepthRequest, NFTCollectionListingsDepthResponse,
    NFTCollectionIndividualListingsRequest, NFTCollectionIndividualListingsResponse,
    NFTCollectionListingsTrendedRequest, NFTCollectionListingsTrendedResponse,
    NFTCollectionOHLCVRequest, NFTCollectionOHLCVResponse,
    NFTCollectionTradesRequest, NFTCollectionTradesResponse,
    NFTCollectionTradeStatsRequest, NFTCollectionTradeStatsResponse,
    NFTCollectionVolumeTrendedRequest, NFTCollectionVolumeTrendedResponse,
    NFTCollectionTraitPricesRequest, NFTCollectionTraitPricesResponse,
    NFTCollectionTraitRarityRequest, NFTCollectionTraitRarityResponse,
    NFTCollectionTraitRarityRankRequest, NFTCollectionTraitRarityRankResponse,
    NFTMarketStatsRequest, NFTMarketStatsResponse,
    NFTMarketExtendedStatsRequest, NFTMarketExtendedStatsResponse,
    NFTMarketVolumeTrendedRequest, NFTMarketVolumeTrendedResponse,
    NFTMarketplaceStatsRequest, NFTMarketplaceStatsResponse,
    NFTTopTimeframeRequest, NFTTopTimeframeResponse,
    NFTTopVolumeRequest, NFTTopVolumeResponse,
    NFTTopVolumeExtendedRequest, NFTTopVolumeExtendedResponse
)

from .models.market import (
    MarketStatsRequest,
    MetricsResponse
)

from .models.integration import (
    IntegrationAssetRequest, IntegrationAssetResponse,
    IntegrationPolicyAssetsRequest, IntegrationPolicyAssetsResponse,
    IntegrationBlockRequest, IntegrationBlockResponse,
    IntegrationEventsRequest, IntegrationEventsResponse,
    IntegrationExchangeRequest, IntegrationExchangeResponse,
    IntegrationPairRequest, IntegrationPairResponse
)

from .models.onchain import (
    AssetSupplyRequest, AssetSupplyResponse,
    AddressInfoRequest, AddressInfoResponse,
    AddressUTXOsRequest, AddressUTXOsResponse,
    TransactionUTXOsRequest, TransactionUTXOsResponse
)

from .models.wallet import (
    WalletPortfolioPositionsRequest, WalletPortfolioPositionsResponse,
    WalletTokenTradesRequest, WalletTokenTrade,
    WalletValueTrendedRequest, WalletValueTrend
)


logger = logging.getLogger("taptools_mcp")

class ServerConfig(BaseModel):
    """Holds config values for the TapTools MCP server."""
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


@asynccontextmanager
async def taptools_lifespan(config: ServerConfig):
    """
    Lifespan context manager for the TapToolsServer.
    Creates an httpx.AsyncClient at startup, closes at shutdown.
    """
    client = httpx.AsyncClient(
        base_url=config.base_url,
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )
    try:
        yield {"client": client}
    finally:
        await client.aclose()


class TapToolsServer:
    """
    The main server that registers TapTools endpoints as MCP tools.
    """
    def __init__(self, config: ServerConfig):
        self.config = config

        # Create the MCP app with a lifespan manager
        self.app = FastMCP(
            name="taptools-server",
            lifespan=lambda: taptools_lifespan(config)
        )

        # Attach API interfaces
        self.tokens_api = TokensAPI()
        self.nfts_api = NftsAPI()
        self.market_api = MarketAPI()
        self.integration_api = IntegrationAPI()
        self.onchain_api = OnchainAPI()
        self.wallet_api = WalletAPI()

        # Register all tools
        self.register_tools()

    def register_tools(self):
        """Register MCP tools for TapTools endpoints."""

        #----------------------------------
        # Connection / Auth
        #----------------------------------
        @self.app.tool(name="verify_connection", description="Verify TapTools API authentication")
        async def verify_connection(_: dict, ctx: Context) -> dict:
            """
            No parameters. Verifies the API key is valid by calling a simple endpoint.
            """
            return await self.tokens_api.verify_connection(ctx)

        #----------------------------------
        # Tokens Tools
        #----------------------------------
        @self.app.tool(name="get_token_mcap", description="Get token market cap info")
        async def handle_get_token_mcap(request: TokenMcapRequest, ctx: Context) -> TokenMcapResponse:
            return await self.tokens_api.get_token_mcap(request, ctx)

        @self.app.tool(name="get_token_holders", description="Get total number of token holders")
        async def handle_get_token_holders(request: TokenHoldersRequest, ctx: Context) -> TokenHoldersResponse:
            return await self.tokens_api.get_token_holders(request, ctx)

        @self.app.tool(name="get_token_holders_top", description="Get top token holders")
        async def handle_get_token_holders_top(request: TokenTopHoldersRequest, ctx: Context) -> TokenTopHoldersResponse:
            return await self.tokens_api.get_token_holders_top(request, ctx)

        @self.app.tool(name="post_token_prices", description="Get aggregated prices for up to 100 token units.")
        async def handle_post_token_prices(request: TokenPricesRequest, ctx: Context) -> TokenPricesResponse:
            return await self.tokens_api.post_token_prices(request, ctx)

        @self.app.tool(name="get_token_price_changes", description="Get token price % changes over multiple timeframes.")
        async def handle_get_token_price_changes(request: TokenPriceChangesRequest, ctx: Context) -> TokenPriceChangesResponse:
            return await self.tokens_api.get_token_price_percent_changes(request, ctx)

        @self.app.tool(name="get_token_trades", description="Get token trades across DEXes.")
        async def handle_get_token_trades(request: TokenTradesRequest, ctx: Context) -> TokenTradesResponse:
            return await self.tokens_api.get_token_trades(request, ctx)

        @self.app.tool(name="get_token_trade_stats", description="Get aggregated trading stats for a token.")
        async def handle_get_token_trade_stats(request: TokenTradingStatsRequest, ctx: Context) -> TokenTradingStatsResponse:
            return await self.tokens_api.get_token_trade_stats(request, ctx)

        @self.app.tool(name="get_token_ohlcv", description="Get token OHLCV data.")
        async def handle_get_token_ohlcv(request: TokenOHLCVRequest, ctx: Context) -> TokenOHLCVResponse:
            return await self.tokens_api.get_token_ohlcv(request, ctx)

        @self.app.tool(name="get_token_links", description="Get a token's social/contact links.")
        async def handle_get_token_links(request: TokenLinksRequest, ctx: Context) -> TokenLinksResponse:
            return await self.tokens_api.get_token_links(request, ctx)

        @self.app.tool(name="get_token_indicators", description="Get technical indicators (EMA, RSI, MACD) for a token.")
        async def handle_get_token_indicators(request: TokenIndicatorsRequest, ctx: Context) -> TokenIndicatorsResponse:
            return await self.tokens_api.get_token_indicators(request, ctx)

        @self.app.tool(name="get_token_pools", description="Get active liquidity pools for a token.")
        async def handle_get_token_pools(request: TokenPoolsRequest, ctx: Context) -> TokenPoolsResponse:
            return await self.tokens_api.get_token_pools(request, ctx)

        @self.app.tool(name="get_token_debt_loans", description="Get active P2P loans for a given token.")
        async def handle_get_token_debt_loans(request: TokenDebtLoansRequest, ctx: Context) -> TokenDebtLoansResponse:
            return await self.tokens_api.get_token_active_loans(request, ctx)

        @self.app.tool(name="get_token_debt_offers", description="Get active P2P loan offers for a given token.")
        async def handle_get_token_debt_offers(request: TokenDebtOffersRequest, ctx: Context) -> TokenDebtOffersResponse:
            return await self.tokens_api.get_token_loan_offers(request, ctx)

        @self.app.tool(name="get_token_top_tokens_by_liquidity", description="Get tokens ranked by total DEX liquidity.")
        async def handle_get_token_top_tokens_by_liquidity(request: TokenTopLiquidityRequest, ctx: Context) -> TokenTopLiquidityResponse:
            return await self.tokens_api.get_token_top_tokens_by_liquidity(request, ctx)

        @self.app.tool(name="get_token_top_tokens_by_mcap", description="Get tokens ranked by market cap.")
        async def handle_get_token_top_tokens_by_mcap(request: TokenTopMcapRequest, ctx: Context) -> TokenTopMcapResponse:
            return await self.tokens_api.get_token_top_tokens_by_mcap(request, ctx)

        @self.app.tool(name="get_token_top_tokens_by_volume", description="Get tokens ranked by volume.")
        async def handle_get_token_top_tokens_by_volume(request: TokenTopVolumeRequest, ctx: Context) -> TokenTopVolumeResponse:
            return await self.tokens_api.get_token_top_tokens_by_volume(request, ctx)

        @self.app.tool(name="get_token_quote", description="Get current quote price (e.g., ADA/USD).")
        async def handle_get_token_quote(request: TokenQuoteRequest, ctx: Context) -> TokenQuoteResponse:
            return await self.tokens_api.get_quote_price(request, ctx)

        #----------------------------------
        # NFTs Tools
        #----------------------------------
        @self.app.tool(name="get_nft_asset_sales", description="Get NFT asset sales history")
        async def handle_get_nft_asset_sales(request: NFTAssetSalesRequest, ctx: Context) -> NFTAssetSalesResponse:
            return await self.nfts_api.get_nft_asset_sales(request, ctx)

        @self.app.tool(name="get_nft_asset_stats", description="Get stats for a specific NFT asset.")
        async def handle_get_nft_asset_stats(request: NFTAssetStatsRequest, ctx: Context) -> NFTAssetStatsResponse:
            return await self.nfts_api.get_nft_asset_stats(request, ctx)

        @self.app.tool(name="get_nft_asset_traits", description="Get trait data for a specific NFT asset.")
        async def handle_get_nft_asset_traits(request: NFTAssetTraitsRequest, ctx: Context) -> NFTAssetTraitsResponse:
            return await self.nfts_api.get_nft_asset_traits(request, ctx)

        @self.app.tool(name="get_nft_collection_assets", description="Get a list of NFTs in a collection.")
        async def handle_get_nft_collection_assets(request: NFTCollectionAssetsRequest, ctx: Context) -> NFTCollectionAssetsResponse:
            return await self.nfts_api.get_nft_collection_assets(request, ctx)

        @self.app.tool(name="get_nft_collection_info", description="Get basic info for an NFT collection.")
        async def handle_get_nft_collection_info(request: NFTCollectionInfoRequest, ctx: Context) -> NFTCollectionInfoResponse:
            return await self.nfts_api.get_nft_collection_info(request, ctx)

        @self.app.tool(name="get_nft_collection_stats", description="Get NFT collection stats")
        async def handle_get_nft_collection_stats(request: NFTCollectionStatsRequest, ctx: Context) -> NFTCollectionStatsResponse:
            return await self.nfts_api.get_nft_collection_stats(request, ctx)

        @self.app.tool(name="get_nft_collection_stats_extended", description="Get extended NFT collection stats.")
        async def handle_get_nft_collection_stats_extended(request: NFTCollectionExtendedStatsRequest, ctx: Context) -> NFTCollectionExtendedStatsResponse:
            return await self.nfts_api.get_nft_collection_stats_extended(request, ctx)

        @self.app.tool(name="get_nft_collection_holders_distribution", description="Get distribution of NFT holders for a collection.")
        async def handle_get_nft_collection_holders_distribution(request: NFTCollectionHoldersDistributionRequest, ctx: Context) -> NFTCollectionHoldersDistributionResponse:
            return await self.nfts_api.get_nft_collection_holders_distribution(request, ctx)

        @self.app.tool(name="get_nft_collection_holders_top", description="Get top NFT holders in a collection.")
        async def handle_get_nft_collection_holders_top(request: NFTCollectionTopHoldersRequest, ctx: Context) -> NFTCollectionTopHoldersResponse:
            return await self.nfts_api.get_nft_collection_holders_top(request, ctx)

        @self.app.tool(name="get_nft_collection_holders_trended", description="Get trended holder counts by day.")
        async def handle_get_nft_collection_holders_trended(request: NFTCollectionHoldersTrendedRequest, ctx: Context) -> NFTCollectionHoldersTrendedResponse:
            return await self.nfts_api.get_nft_collection_holders_trended(request, ctx)

        @self.app.tool(name="get_nft_collection_listings", description="Get active listings for an NFT collection.")
        async def handle_get_nft_collection_listings(request: NFTCollectionListingsRequest, ctx: Context) -> NFTCollectionListingsResponse:
            return await self.nfts_api.get_nft_collection_listings(request, ctx)

        @self.app.tool(name="get_nft_collection_listings_depth", description="Get listings depth data for an NFT collection.")
        async def handle_get_nft_collection_listings_depth(request: NFTCollectionListingsDepthRequest, ctx: Context) -> NFTCollectionListingsDepthResponse:
            return await self.nfts_api.get_nft_collection_listings_depth(request, ctx)

        @self.app.tool(name="get_nft_collection_listings_individual", description="Get individual listings for an NFT collection.")
        async def handle_get_nft_collection_listings_individual(request: NFTCollectionIndividualListingsRequest, ctx: Context) -> NFTCollectionIndividualListingsResponse:
            return await self.nfts_api.get_nft_collection_listings_individual(request, ctx)

        @self.app.tool(name="get_nft_collection_listings_trended", description="Get trended listing counts/floor for an NFT collection.")
        async def handle_get_nft_collection_listings_trended(request: NFTCollectionListingsTrendedRequest, ctx: Context) -> NFTCollectionListingsTrendedResponse:
            return await self.nfts_api.get_nft_collection_listings_trended(request, ctx)

        @self.app.tool(name="get_nft_collection_ohlcv", description="Get floor price OHLCV for an NFT collection.")
        async def handle_get_nft_collection_ohlcv(request: NFTCollectionOHLCVRequest, ctx: Context) -> NFTCollectionOHLCVResponse:
            return await self.nfts_api.get_nft_collection_ohlcv(request, ctx)

        @self.app.tool(name="get_nft_collection_trades", description="Get trades for an NFT collection.")
        async def handle_get_nft_collection_trades(request: NFTCollectionTradesRequest, ctx: Context) -> NFTCollectionTradesResponse:
            return await self.nfts_api.get_nft_collection_trades(request, ctx)

        @self.app.tool(name="get_nft_collection_trade_stats", description="Get trade stats for an NFT collection.")
        async def handle_get_nft_collection_trade_stats(request: NFTCollectionTradeStatsRequest, ctx: Context) -> NFTCollectionTradeStatsResponse:
            return await self.nfts_api.get_nft_collection_trades_stats(request, ctx)

        @self.app.tool(name="get_nft_collection_volume_and_sales", description="Get volume/sales trends for an NFT collection.")
        async def handle_get_nft_collection_volume_and_sales(request: NFTCollectionVolumeTrendedRequest, ctx: Context) -> NFTCollectionVolumeTrendedResponse:
            return await self.nfts_api.get_nft_collection_volume_and_sales(request, ctx)

        @self.app.tool(name="get_nft_collection_traits_price", description="Get trait floor prices in an NFT collection.")
        async def handle_get_nft_collection_traits_price(request: NFTCollectionTraitPricesRequest, ctx: Context) -> NFTCollectionTraitPricesResponse:
            return await self.nfts_api.get_nft_collection_traits_price(request, ctx)

        @self.app.tool(name="get_nft_collection_traits_rarity", description="Get trait rarity for an NFT collection.")
        async def handle_get_nft_collection_traits_rarity(request: NFTCollectionTraitRarityRequest, ctx: Context) -> NFTCollectionTraitRarityResponse:
            return await self.nfts_api.get_nft_collection_traits_rarity(request, ctx)

        @self.app.tool(name="get_nft_collection_traits_rarity_rank", description="Get an NFT's rarity rank within a collection.")
        async def handle_get_nft_collection_traits_rarity_rank(request: NFTCollectionTraitRarityRankRequest, ctx: Context) -> NFTCollectionTraitRarityRankResponse:
            return await self.nfts_api.get_nft_collection_traits_rarity_rank(request, ctx)

        @self.app.tool(name="get_nft_market_stats", description="Get top-level NFT market stats (addresses, sales, volume).")
        async def handle_get_nft_market_stats(request: NFTMarketStatsRequest, ctx: Context) -> NFTMarketStatsResponse:
            return await self.nfts_api.get_nft_market_stats(request, ctx)

        @self.app.tool(name="get_nft_market_stats_extended", description="Get NFT market stats + percentage changes.")
        async def handle_get_nft_market_stats_extended(request: NFTMarketExtendedStatsRequest, ctx: Context) -> NFTMarketExtendedStatsResponse:
            return await self.nfts_api.get_nft_market_stats_extended(request, ctx)

        @self.app.tool(name="get_nft_market_volume_and_sales", description="Get overall NFT market volume trends.")
        async def handle_get_nft_market_volume_and_sales(request: NFTMarketVolumeTrendedRequest, ctx: Context) -> NFTMarketVolumeTrendedResponse:
            return await self.nfts_api.get_nft_market_volume_and_sales(request, ctx)

        @self.app.tool(name="get_nft_marketplaces_stats", description="Get stats for an NFT marketplace.")
        async def handle_get_nft_marketplaces_stats(request: NFTMarketplaceStatsRequest, ctx: Context) -> NFTMarketplaceStatsResponse:
            return await self.nfts_api.get_nft_marketplaces_stats(request, ctx)

        @self.app.tool(name="get_nft_top_rankings", description="Get top NFT rankings by market cap, volume, etc.")
        async def handle_get_nft_top_rankings(request: NFTTopTimeframeRequest, ctx: Context) -> NFTTopTimeframeResponse:
            return await self.nfts_api.get_nft_top_rankings(request, ctx)

        @self.app.tool(name="get_nft_top_collections_by_volume", description="Get top NFT collections by volume.")
        async def handle_get_nft_top_collections_by_volume(request: NFTTopVolumeRequest, ctx: Context) -> NFTTopVolumeResponse:
            return await self.nfts_api.get_nft_top_collections_by_volume(request, ctx)

        @self.app.tool(name="get_nft_top_collections_by_volume_with_changes", description="Get top NFT collections by volume with % changes.")
        async def handle_get_nft_top_collections_by_volume_with_changes(request: NFTTopVolumeExtendedRequest, ctx: Context) -> NFTTopVolumeExtendedResponse:
            return await self.nfts_api.get_nft_top_collections_by_volume_with_changes(request, ctx)

        #----------------------------------
        # Market Tools
        #----------------------------------
        @self.app.tool(name="get_market_stats", description="Get market-wide statistics")
        async def handle_get_market_stats(request: dict, ctx: Context) -> dict:
            """
            For demonstration, we show a basic dict approach. 
            Expects fields: quote (str), include_deprecated (bool), min_liquidity (float).
            """
            quote = request.get("quote", "ADA")
            include_deprecated = bool(request.get("include_deprecated", False))
            min_liquidity = float(request.get("min_liquidity", 0))
            return await self.market_api.get_market_stats(quote, include_deprecated, min_liquidity, ctx)

        @self.app.tool(name="get_market_metrics", description="Get daily request counts from past 30 days")
        async def handle_get_market_metrics(_: dict, ctx: Context) -> MetricsResponse:
            return await self.market_api.get_metrics(ctx)

        @self.app.tool(name="get_market_overview", description="Get overview with gainers/losers/trending.")
        async def handle_get_market_overview(_: dict, ctx: Context) -> dict:
            return await self.market_api.get_market_overview(ctx)

        #----------------------------------
        # Integration Tools
        #----------------------------------
        @self.app.tool(name="get_integration_asset", description="Get asset details by ID")
        async def handle_get_integration_asset(request: IntegrationAssetRequest, ctx: Context) -> IntegrationAssetResponse:
            return await self.integration_api.get_asset(request, ctx)

        @self.app.tool(name="get_policy_assets", description="Get assets under a given policy ID.")
        async def handle_get_policy_assets(request: IntegrationPolicyAssetsRequest, ctx: Context) -> IntegrationPolicyAssetsResponse:
            return await self.integration_api.get_policy_assets(request, ctx)

        #----------------------------------
        # Onchain Tools
        #----------------------------------
        @self.app.tool(name="get_asset_supply", description="Get onchain asset supply")
        async def handle_get_asset_supply(request: AssetSupplyRequest, ctx: Context) -> AssetSupplyResponse:
            return await self.onchain_api.get_asset_supply(request, ctx)

        #----------------------------------
        # Wallet Tools
        #----------------------------------
        @self.app.tool(name="get_wallet_portfolio", description="Get wallet portfolio positions.")
        async def handle_get_wallet_portfolio(request: WalletPortfolioPositionsRequest, ctx: Context) -> WalletPortfolioPositionsResponse:
            return await self.wallet_api.get_wallet_portfolio_positions(request, ctx)

        @self.app.tool(name="get_wallet_trades_tokens", description="Get token trade history for a wallet.")
        async def handle_get_wallet_trades_tokens(request: WalletTokenTradesRequest, ctx: Context) -> list:
            # or we can return a Pydantic model that has a field of trades
            trades = await self.wallet_api.get_wallet_trades_tokens(request, ctx)
            return [t.dict() for t in trades]

        @self.app.tool(name="get_wallet_value_trended", description="Get historical wallet value in 4hr intervals.")
        async def handle_get_wallet_value_trended(request: WalletValueTrendedRequest, ctx: Context) -> list:
            trends = await self.wallet_api.get_wallet_value_trended(request, ctx)
            return [t.dict() for t in trends]

    def run(self, transport: str = "stdio"):
        """
        Run the MCP server using the specified transport.
        For now, we only support "stdio".
        SSE or other transports can be added in future.
        """
        if transport != "stdio":
            raise ValueError("Currently only 'stdio' transport is supported.")
        # Start the server on stdio
        self.app.run("stdio")


def main():
    config = ServerConfig.from_env()
    server = TapToolsServer(config)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
