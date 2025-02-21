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
    Factory fixture to create sample error responses matching ErrorData model.
    Returns a function that generates error responses for different scenarios.
    """
    def _error_response(error_type="validation"):
        responses = {
            "authentication": {
                "code": -32001,
                "message": "Invalid or unauthorized API key",
                "data": {"error_type": "authentication"}
            },
            "connection": {
                "code": -32002,
                "message": "Failed to connect to API endpoint",
                "data": {"error_type": "connection"}
            },
            "validation": {
                "code": -32003,
                "message": "Required parameter 'unit' is missing",
                "data": {"error_type": "validation"}
            },
            "rate_limit": {
                "code": -32005,
                "message": "Rate limit exceeded. Please try again later",
                "data": {"error_type": "rate_limit"}
            },
            "not_found": {
                "code": -32006,
                "message": "Requested resource not found",
                "data": {"error_type": "not_found"}
            },
            "timeout": {
                "code": -32008,
                "message": "Request timed out",
                "data": {"error_type": "timeout"}
            },
            "parse": {
                "code": -32009,
                "message": "Failed to parse API response",
                "data": {"error_type": "parse"}
            }
        }
        return responses.get(error_type, responses["validation"])
    return _error_response
