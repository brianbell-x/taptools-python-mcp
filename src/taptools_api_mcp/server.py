"""
TapTools MCP server implementation.

Exposes TapTools endpoints as MCP tools.
"""
import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import httpx

from mcp.server.stdio import stdio_server
from mcp.server.fastmcp import FastMCP
from mcp.types import ErrorData
from mcp.shared.exceptions import McpError

from .api.tokens import TokensAPI
from .api.nfts import NftsAPI
from .api.market import MarketAPI
from .api.integration import IntegrationAPI
from .api.onchain import OnchainAPI
from .api.wallet import WalletAPI
from .utils.exceptions import TapToolsError, ErrorCode, ErrorType

from .models.tokens import *
from .models.nfts import *
from .models.market import *
from .models.integration import *
from .models.onchain import *
from .models.wallet import *

logger = logging.getLogger("taptools_mcp")

class ServerConfig(BaseModel):
    """
    Holds config values for the TapTools MCP server.
    """
    api_key: str = Field(..., description="TapTools API key", alias="TAPTOOLS_API_KEY")

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
        self.client: Optional[httpx.AsyncClient] = None

        # API classes
        self.tokens_api: Optional[TokensAPI] = None
        self.nfts_api: Optional[NftsAPI] = None
        self.market_api: Optional[MarketAPI] = None
        self.integration_api: Optional[IntegrationAPI] = None
        self.onchain_api: Optional[OnchainAPI] = None
        self.wallet_api: Optional[WalletAPI] = None

        # Register all tools
        self.register_tools()

    async def ensure_client(self):
        """
        Ensure we have a valid httpx client.
        """
        if not self.client or self.client.is_closed:
            self.client = httpx.AsyncClient(
                base_url="https://taptools.io",
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            # Initialize the API classes
            self.tokens_api = TokensAPI(self.client)
            self.nfts_api = NftsAPI(self.client)
            self.market_api = MarketAPI(self.client)
            self.integration_api = IntegrationAPI(self.client)
            self.onchain_api = OnchainAPI(self.client)
            self.wallet_api = WalletAPI(self.client)

    def handle_error(self, e: Exception) -> None:
        """
        Convert various exceptions to McpError with appropriate error codes.
        """
        logger.error(f"Error in API call: {str(e)}")
        
        if isinstance(e, TapToolsError):
            error_code, message = e.to_mcp_error()
            raise McpError(ErrorData(code=error_code, message=message))
        elif isinstance(e, httpx.HTTPStatusError):
            error = TapToolsError.from_http_error(e)
            error_code, message = error.to_mcp_error()
            raise McpError(ErrorData(code=error_code, message=message))
        elif isinstance(e, httpx.RequestError):
            raise McpError(ErrorData(
                code=ErrorCode.CONNECTION_ERROR,
                message=f"Connection error: {str(e)}"
            ))
        elif isinstance(e, ValueError):
            raise McpError(ErrorData(
                code=ErrorCode.INVALID_PARAMETERS,
                message=f"Invalid parameters: {str(e)}"
            ))
        else:
            raise McpError(ErrorData(
                code=ErrorCode.API_ERROR,
                message=f"Unexpected error: {str(e)}"
            ))

    def register_tools(self):
        """
        Register MCP tools for TapTools endpoints.
        """
        # Token Tools
        @self.app.tool(name="get_token_mcap", description="Get token market cap info")
        async def handle_get_token_mcap(request: TokenMcapRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.tokens_api.get_token_mcap(request.unit)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        @self.app.tool(name="get_token_holders", description="Get total number of token holders")
        async def handle_get_token_holders(request: TokenHoldersRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.tokens_api.get_token_holders(request.unit)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        @self.app.tool(name="get_token_holders_top", description="Get top token holders")
        async def handle_get_token_holders_top(request: TokenTopHoldersRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.tokens_api.get_token_holders_top(
                    request.unit,
                    page=request.page,
                    perPage=request.per_page
                )
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # NFT Tools
        @self.app.tool(name="get_nft_asset_sales", description="Get NFT asset sales history")
        async def handle_get_nft_asset_sales(request: NFTAssetSalesRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.nfts_api.get_asset_sales(request.policy, request.name)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        @self.app.tool(name="get_nft_collection_stats", description="Get NFT collection stats")
        async def handle_get_nft_collection_stats(request: NFTCollectionStatsRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.nfts_api.get_collection_stats(request.policy)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # Market Tools
        @self.app.tool(name="get_market_stats", description="Get market-wide statistics")
        async def handle_get_market_stats(request: MarketStatsRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.market_api.get_market_stats(request.quote)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # Integration Tools
        @self.app.tool(name="get_integration_asset", description="Get asset details by ID")
        async def handle_get_integration_asset(request: IntegrationAssetRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.integration_api.get_asset(request.id)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # Onchain Tools
        @self.app.tool(name="get_asset_supply", description="Get onchain asset supply")
        async def handle_get_asset_supply(request: AssetSupplyRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.onchain_api.get_asset_supply(request.unit)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # Wallet Tools
        @self.app.tool(name="get_wallet_portfolio", description="Get wallet portfolio positions")
        async def handle_get_wallet_portfolio(request: WalletPortfolioPositionsRequest) -> str:
            await self.ensure_client()
            try:
                result = await self.wallet_api.get_portfolio_positions(request.address)
                return json.dumps(result, indent=2)
            except Exception as e:
                self.handle_error(e)

        # Verification Tool
        @self.app.tool(name="verify_connection", description="Verify TapTools API authentication")
        async def handle_verify_connection() -> str:
            await self.ensure_client()
            try:
                resp = await self.client.get("/token/quote/available")
                resp.raise_for_status()
                data = resp.json()
                return json.dumps({
                    "success": True,
                    "available_quotes": data
                }, indent=2)
            except Exception as e:
                self.handle_error(e)

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None

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
