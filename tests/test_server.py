import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from taptools_api_mcp.server import TapToolsServer, ServerConfig
from mcp.shared.exceptions import McpError

@pytest_asyncio.fixture
async def mock_client():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.is_closed = False
    return client

@pytest_asyncio.fixture
def config():
    return ServerConfig(TAPTOOLS_API_KEY="test-api-key")

@pytest.mark.asyncio
async def test_server_init(config):
    server = TapToolsServer(config)
    assert server.config.api_key == "test-api-key"
    assert server.app is not None

@pytest.mark.asyncio
async def test_verify_connection_tool(config, mock_client):
    server = TapToolsServer(config)
    server.client = mock_client
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = ["USD", "ADA"]
    mock_client.get.return_value = mock_resp

    result = await server.app.call_tool("verify_connection", {})
    assert "available_quotes" in result[0].text

@pytest.mark.asyncio
async def test_invalid_auth(config, mock_client):
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

@pytest.mark.asyncio
async def test_get_token_price_tool(config, mock_client):
    server = TapToolsServer(config)
    server.client = mock_client
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"someTokenUnit": 5.0}
    mock_client.post.return_value = mock_resp

    result = await server.app.call_tool("get_token_price", {"unit": "someTokenUnit"})
    assert '"someTokenUnit": 5.0' in result[0].text
