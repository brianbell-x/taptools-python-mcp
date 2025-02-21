"""
Tests for the TapTools MCP server implementation.
"""
import os
import pytest
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

    # Token Tools Tests
    async def test_get_token_mcap_tool(self, config, mock_client):
        """Test get_token_mcap tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "circ_supply": 1000000,
            "fdv": 2000000,
            "mcap": 1500000,
            "price": 1.5,
            "ticker": "TEST",
            "total_supply": 2000000
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_token_mcap", {"unit": "test_token"})
        assert "mcap" in result[0].text
        assert "1500000" in result[0].text

    async def test_get_token_holders_tool(self, config, mock_client):
        """Test get_token_holders tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"holders": 1000}
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_token_holders", {"unit": "test_token"})
        assert "holders" in result[0].text
        assert "1000" in result[0].text

    async def test_get_token_holders_top_tool(self, config, mock_client):
        """Test get_token_holders_top tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "holders": [
                {"address": "addr1", "balance": 1000},
                {"address": "addr2", "balance": 500}
            ]
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_token_holders_top", {
            "unit": "test_token",
            "page": 1,
            "per_page": 10
        })
        assert "holders" in result[0].text
        assert "addr1" in result[0].text

    # NFT Tools Tests
    async def test_get_nft_asset_sales_tool(self, config, mock_client):
        """Test get_nft_asset_sales tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{
            "buyer_stake_address": "stake1test123buyer",
            "price": 100.5,
            "seller_stake_address": "stake1test123seller",
            "time": 1234567890
        }]
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_nft_asset_sales", {
            "policy": "policy123",
            "name": "Test NFT"
        })
        assert "buyer_stake_address" in result[0].text
        assert "100.5" in result[0].text

    async def test_get_nft_collection_stats_tool(self, config, mock_client):
        """Test get_nft_collection_stats tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "listings": 100,
            "owners": 50,
            "price": 150.5,
            "sales": 75,
            "supply": 1000,
            "top_offer": 200.0,
            "volume": 15000.0
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_nft_collection_stats", {
            "policy": "policy123"
        })
        assert "listings" in result[0].text
        assert "15000.0" in result[0].text

    # Market Tools Tests
    async def test_get_market_stats_tool(self, config, mock_client):
        """Test get_market_stats tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "active_addresses": 1000,
            "dex_volume": 500000.5
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_market_stats", {"quote": "ADA"})
        assert "active_addresses" in result[0].text
        assert "500000.5" in result[0].text

    # Integration Tools Tests
    async def test_get_integration_asset_tool(self, config, mock_client):
        """Test get_integration_asset tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "circulating_supply": 1000000,
            "id": "asset123",
            "name": "Test Asset",
            "symbol": "TEST",
            "total_supply": 2000000
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_integration_asset", {"id": "asset123"})
        assert "circulating_supply" in result[0].text
        assert "Test Asset" in result[0].text

    # Onchain Tools Tests
    async def test_get_asset_supply_tool(self, config, mock_client):
        """Test get_asset_supply tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"supply": 1000000}
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_asset_supply", {"unit": "test_token"})
        assert "supply" in result[0].text
        assert "1000000" in result[0].text

    # Wallet Tools Tests
    async def test_get_wallet_portfolio_tool(self, config, mock_client):
        """Test get_wallet_portfolio tool success case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "ada_balance": 1000.5,
            "ada_value": 1500.75,
            "liquid_value": 2000.25,
            "num_fts": 5,
            "num_nfts": 10,
            "positions_ft": [{"token": "token1", "amount": 100}],
            "positions_lp": [{"pool": "pool1", "share": 0.1}],
            "positions_nft": [{"policy": "policy1", "name": "nft1"}]
        }
        mock_client.get.return_value = mock_resp

        result = await server.app.call_tool("get_wallet_portfolio", {"address": "addr1test123"})
        assert "ada_balance" in result[0].text
        assert "positions_ft" in result[0].text

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

    # Tool Error Cases
    async def test_get_token_mcap_tool_error(self, config, mock_client):
        """Test get_token_mcap tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 400
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_mcap", {"unit": "invalid_token"})
        assert "400" in str(exc.value)

    async def test_get_token_holders_tool_error(self, config, mock_client):
        """Test get_token_holders tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 404
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_holders", {"unit": "nonexistent_token"})
        assert "404" in str(exc.value)

    async def test_get_nft_asset_sales_tool_error(self, config, mock_client):
        """Test get_nft_asset_sales tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 400
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_nft_asset_sales", {
                "policy": "invalid_policy",
                "name": "Test NFT"
            })
        assert "400" in str(exc.value)

    async def test_get_nft_collection_stats_tool_error(self, config, mock_client):
        """Test get_nft_collection_stats tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 404
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_nft_collection_stats", {
                "policy": "nonexistent_policy"
            })
        assert "404" in str(exc.value)

    async def test_get_market_stats_tool_error(self, config, mock_client):
        """Test get_market_stats tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 500
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Internal Server Error",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_market_stats", {"quote": "INVALID"})
        assert "500" in str(exc.value)

    async def test_get_integration_asset_tool_error(self, config, mock_client):
        """Test get_integration_asset tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 404
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_integration_asset", {"id": "nonexistent_asset"})
        assert "404" in str(exc.value)

    async def test_get_asset_supply_tool_error(self, config, mock_client):
        """Test get_asset_supply tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 400
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_asset_supply", {"unit": "invalid_token"})
        assert "400" in str(exc.value)

    async def test_get_wallet_portfolio_tool_error(self, config, mock_client):
        """Test get_wallet_portfolio tool error case."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 400
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=MagicMock(),
            response=mock_resp
        )
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_wallet_portfolio", {"address": "invalid_address"})
        assert "400" in str(exc.value)

    async def test_tool_connection_error(self, config, mock_client):
        """Test tool connection error handling."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_client.get.side_effect = httpx.ConnectError("Failed to connect")

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_mcap", {"unit": "test_token"})
        assert "Connection error" in str(exc.value)

    async def test_tool_timeout_error(self, config, mock_client):
        """Test tool timeout error handling."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_client.get.side_effect = httpx.TimeoutException("Request timed out")

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_mcap", {"unit": "test_token"})
        assert "Connection error" in str(exc.value)

    async def test_tool_parse_error(self, config, mock_client):
        """Test tool JSON parse error handling."""
        server = TapToolsServer(config)
        server.client = mock_client
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("Invalid JSON")
        mock_client.get.return_value = mock_resp

        with pytest.raises(McpError) as exc:
            await server.app.call_tool("get_token_mcap", {"unit": "test_token"})
        assert "Failed to parse response" in str(exc.value)
