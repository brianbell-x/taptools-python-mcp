"""
Tests for the TapTools MCP server implementation.
"""
import os
import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from taptools_api_mcp.server import TapToolsServer, ServerConfig
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

class TestServerConfig:
    def test_from_env_success(self, monkeypatch):
        """Test successful config creation from environment variables."""
        monkeypatch.setenv("TAPTOOLS_API_KEY", "test-api-key")
        config = ServerConfig.from_env()
        assert config.api_key == "test-api-key"

    def test_from_env_missing_key(self, monkeypatch):
        """Test error handling when API key is missing."""
        monkeypatch.delenv("TAPTOOLS_API_KEY", raising=False)
        with pytest.raises(ValueError) as exc:
            ServerConfig.from_env()
        assert "TAPTOOLS_API_KEY not found" in str(exc.value)

    def test_from_env_empty_key(self, monkeypatch):
        """Test error handling when API key is empty."""
        monkeypatch.setenv("TAPTOOLS_API_KEY", "  ")
        with pytest.raises(ValueError) as exc:
            ServerConfig.from_env()
        assert "TAPTOOLS_API_KEY not found" in str(exc.value)

    def test_from_env_with_file(self, tmp_path):
        """Test loading config from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text("TAPTOOLS_API_KEY=test-api-key-from-file")
        
        config = ServerConfig.from_env(str(env_file))
        assert config.api_key == "test-api-key-from-file"

@pytest.mark.asyncio
class TestTapToolsServer:
    async def test_server_initialization(self, config):
        """Test basic server initialization."""
        server = TapToolsServer(config)
        assert server.config.api_key == "test-api-key"
        assert server.app is not None
        assert server.client is None
        assert server.tokens_api is None
        assert server.nfts_api is None
        assert server.market_api is None
        assert server.integration_api is None
        assert server.onchain_api is None
        assert server.wallet_api is None

    async def test_ensure_client(self, config):
        """Test client initialization."""
        server = TapToolsServer(config)
        await server.ensure_client()
        
        assert server.client is not None
        assert server.tokens_api is not None
        assert server.nfts_api is not None
        assert server.market_api is not None
        assert server.integration_api is not None
        assert server.onchain_api is not None
        assert server.wallet_api is not None
        
        # Test client headers
        assert server.client.headers["Authorization"] == f"Bearer {config.api_key}"
        assert server.client.headers["Content-Type"] == "application/json"

    async def test_client_reuse(self, config):
        """Test client is reused when not closed."""
        server = TapToolsServer(config)
        await server.ensure_client()
        original_client = server.client
        
        await server.ensure_client()
        assert server.client is original_client

    async def test_client_recreation(self, config):
        """Test client is recreated when closed."""
        server = TapToolsServer(config)
        await server.ensure_client()
        original_client = server.client
        
        await server.close()
        await server.ensure_client()
        assert server.client is not original_client

    async def test_verify_connection_tool(self, config, mock_client):
        """Test verify_connection tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = ["USD", "ADA"]
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("verify_connection", {})
        assert "available_quotes" in result[0].text
        assert "USD" in result[0].text
        assert "ADA" in result[0].text

    async def test_invalid_auth(self, config, mock_client):
        """Test handling of invalid authentication."""
        server = TapToolsServer(config)
        server.client = mock_client

        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 401
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("verify_connection", {})
        assert "Invalid or unauthorized TapTools API key" in str(exc.value)

    async def test_rate_limit_error(self, config, mock_client):
        """Test handling of rate limit errors."""
        server = TapToolsServer(config)
        server.client = mock_client

        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 429
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Too Many Requests",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("verify_connection", {})
        assert "Rate limit exceeded" in str(exc.value)

    async def test_connection_error(self, config, mock_client):
        """Test handling of connection errors."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_client.get.side_effect = httpx.RequestError("Connection failed")

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("verify_connection", {})
        assert "Connection error" in str(exc.value)

    async def test_get_token_price_tool(self, config, mock_client):
        """Test get_token_price tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"someTokenUnit": 5.0}
        mock_client.post.return_value = mock_resp

        result = await server.app.call_tool("get_token_price", {"unit": "someTokenUnit"})
        assert '"someTokenUnit": 5.0' in result[0].text

    async def test_invalid_tool_name(self, config):
        """Test handling of invalid tool name."""
        server = TapToolsServer(config)
        
        with pytest.raises(McpError) as exc:
            await server.app.call_tool("nonexistent_tool", {})
        assert "Tool not found" in str(exc.value)

    async def test_invalid_tool_params(self, config, mock_client):
        """Test handling of invalid tool parameters."""
        server = TapToolsServer(config)
        server.client = mock_client
        
        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_price", {})  # Missing required 'unit' parameter
        assert "Invalid parameters" in str(exc.value)

    async def test_server_cleanup(self, config, mock_client):
        """Test server cleanup on close."""
        server = TapToolsServer(config)
        server.client = mock_client
        
        await server.close()
        assert server.client is None
        mock_client.aclose.assert_called_once()
