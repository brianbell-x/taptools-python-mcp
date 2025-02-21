"""
Shared test fixtures for TapTools MCP tests.
"""
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
import httpx

from taptools_api_mcp.server import ServerConfig

@pytest_asyncio.fixture
async def mock_client():
    """
    Creates a mocked httpx.AsyncClient for testing API calls.
    """
    client = AsyncMock(spec=httpx.AsyncClient)
    client.is_closed = False
    return client

@pytest.fixture
def mock_response():
    """
    Factory fixture to create mock HTTP responses with custom status codes and data.
    """
    def _mock_response(status_code=200, json_data=None, headers=None):
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.json.return_value = json_data or {}
        response.headers = headers or {}
        
        if status_code >= 400:
            def raise_for_status():
                raise httpx.HTTPStatusError(
                    f"HTTP {status_code}",
                    request=MagicMock(spec=httpx.Request),
                    response=response
                )
            response.raise_for_status.side_effect = raise_for_status
        else:
            response.raise_for_status.return_value = None
            
        return response
    return _mock_response

@pytest.fixture
def config():
    """
    Creates a test ServerConfig instance.
    """
    return ServerConfig(TAPTOOLS_API_KEY="test-api-key")

@pytest.fixture
def sample_token_data():
    """
    Sample token data for testing responses.
    """
    return {
        "unit": "test_token",
        "mcap": 1000000,
        "price": 1.23,
        "supply": 1000000,
        "holders": 500
    }

@pytest.fixture
def sample_error_response():
    """
    Sample error response data.
    """
    return {
        "error": "Invalid request",
        "message": "Required parameter missing",
        "code": "INVALID_PARAMS"
    }
