import asyncio
import json
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioClientTransport
from mcp.shared.exceptions import McpError

@pytest.mark.asyncio
class TestTapToolsConnection:
    """Test suite for TapTools MCP server connection."""

    async def test_connection_lifecycle(self):
        """Test complete connection lifecycle including initialization and cleanup."""
        async with ClientSession(
            command="python -m taptools_api_mcp",
            client_info={
                "name": "test-connection",
                "version": "0.1.0"
            }
        ) as session:
            # Test initialization response
            assert session.server_info is not None
            assert "name" in session.server_info
            assert session.server_info["name"] == "taptools-server"

            # Test verify_connection tool
            resp = await session.call_tool("verify_connection", {})
            assert resp is not None
            assert "available_quotes" in resp
            assert isinstance(resp["available_quotes"], list)

    async def test_token_tools(self):
        """Test token-related tools."""
        async with ClientSession(
            command="python -m taptools_api_mcp",
            client_info={"name": "test-connection", "version": "0.1.0"}
        ) as session:
            # Test get_token_mcap
            resp = await session.call_tool("get_token_mcap", {"unit": "test_token"})
            assert resp is not None
            assert isinstance(resp, dict)

            # Test get_token_holders
            resp = await session.call_tool("get_token_holders", {"unit": "test_token"})
            assert resp is not None
            assert isinstance(resp, dict)

    async def test_nft_tools(self):
        """Test NFT-related tools."""
        async with ClientSession(
            command="python -m taptools_api_mcp",
            client_info={"name": "test-connection", "version": "0.1.0"}
        ) as session:
            # Test get_nft_collection_stats
            resp = await session.call_tool("get_nft_collection_stats", {"policy": "test_policy"})
            assert resp is not None
            assert isinstance(resp, dict)

    async def test_error_handling(self):
        """Test error handling for invalid requests."""
        async with ClientSession(
            command="python -m taptools_api_mcp",
            client_info={"name": "test-connection", "version": "0.1.0"}
        ) as session:
            # Test invalid tool name
            with pytest.raises(McpError) as exc:
                await session.call_tool("nonexistent_tool", {})
            assert "Tool not found" in str(exc.value)

            # Test invalid parameters
            with pytest.raises(McpError) as exc:
                await session.call_tool("get_token_mcap", {})  # Missing required unit parameter
            assert "Invalid parameters" in str(exc.value)

    async def test_connection_errors(self):
        """Test handling of connection errors."""
        # Test invalid command
        with pytest.raises(Exception):
            async with ClientSession(
                command="invalid_command",
                client_info={"name": "test-connection", "version": "0.1.0"}
            ):
                pass

        # Test connection timeout
        with pytest.raises(Exception):
            async with ClientSession(
                command="python -m taptools_api_mcp",
                client_info={"name": "test-connection", "version": "0.1.0"},
                timeout=0.001  # Very short timeout
            ):
                pass

if __name__ == "__main__":
    pytest.main([__file__])
