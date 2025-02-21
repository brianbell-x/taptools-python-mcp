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

logger = logging.getLogger("taptools_mcp")

# Custom error codes
class ErrorCode:
    AUTHENTICATION_ERROR = -32001
    CONNECTION_ERROR = -32002
    INVALID_PARAMETERS = -32003
    API_ERROR = -32004


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

    def register_tools(self):
        """
        Register MCP tools for TapTools endpoints.
        """

        @self.app.tool(name="verify_connection", description="Verify TapTools API authentication")
        async def handle_verify_connection() -> str:
            """
            Check if the TapTools API key is valid by making a simple request,
            e.g. get available quotes or basic market stats.
            """
            await self.ensure_client()
            try:
                resp = await self.client.get("/token/quote/available")
                resp.raise_for_status()
                data = resp.json()
                return json.dumps({
                    "success": True,
                    "available_quotes": data
                }, indent=2)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise McpError(ErrorData(
                        code=ErrorCode.AUTHENTICATION_ERROR,
                        message="Invalid or unauthorized TapTools API key"
                    ))
                else:
                    raise McpError(ErrorData(
                        code=ErrorCode.API_ERROR,
                        message=f"TapTools API error: {str(e)}"
                    ))
            except Exception as e:
                raise McpError(ErrorData(
                    code=ErrorCode.API_ERROR,
                    message=f"Unexpected error verifying connection: {str(e)}"
                ))

        @self.app.tool(name="get_token_price", description="Get aggregated token price from TapTools")
        async def handle_get_token_price(unit: str) -> str:
            """
            unit: the token unit (policy + hex name) to fetch aggregated price. 
                  Example: 'dda5fdb1002f73...' 
            """
            await self.ensure_client()
            try:
                resp = await self.tokens_api.get_token_price(unit)
                return json.dumps(resp, indent=2)
            except McpError:
                raise
            except Exception as e:
                raise McpError(ErrorData(
                    code=ErrorCode.API_ERROR,
                    message=str(e)
                ))

        @self.app.tool(name="get_nft_collection_stats", description="Get stats for an NFT collection by policy ID")
        async def handle_get_nft_collection_stats(policy_id: str) -> str:
            """
            policy_id: the policy ID of the NFT collection
            """
            await self.ensure_client()
            try:
                resp = await self.nfts_api.get_collection_stats(policy_id)
                return json.dumps(resp, indent=2)
            except McpError:
                raise
            except Exception as e:
                raise McpError(ErrorData(
                    code=ErrorCode.API_ERROR,
                    message=str(e)
                ))

        @self.app.tool(name="get_market_stats", description="Get aggregated 24h market stats from TapTools")
        async def handle_get_market_stats() -> str:
            """
            Return aggregated 24h stats from /market/stats (DEX volume, active addresses, etc.)
            """
            await self.ensure_client()
            try:
                resp = await self.market_api.get_market_stats()
                return json.dumps(resp, indent=2)
            except McpError:
                raise
            except Exception as e:
                raise McpError(ErrorData(
                    code=ErrorCode.API_ERROR,
                    message=str(e)
                ))

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

