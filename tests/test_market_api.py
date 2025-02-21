"""
Tests for the MarketAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.market import MarketAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_market_stats():
    """Sample market statistics for testing."""
    return {
        "totalMarketCap": 1000000000,
        "volume24h": 50000000,
        "dominance": {
            "ADA": 80.5,
            "HOSKY": 5.2,
            "SHEN": 3.1
        },
        "activeTokens": 1000,
        "activeTraders": 5000
    }

@pytest.fixture
def sample_market_overview():
    """Sample market overview data for testing."""
    return {
        "gainers": [
            {"unit": "token1", "change24h": 25.5},
            {"unit": "token2", "change24h": 15.2}
        ],
        "losers": [
            {"unit": "token3", "change24h": -12.3},
            {"unit": "token4", "change24h": -8.7}
        ],
        "trending": [
            {"unit": "token5", "volume24h": 1000000},
            {"unit": "token6", "volume24h": 800000}
        ]
    }

@pytest.mark.asyncio
class TestMarketAPI:
    async def test_get_market_stats_success(self, mock_client, mock_response, sample_market_stats):
        """Test successful market stats retrieval."""
        mock_client.get.return_value = mock_response(200, sample_market_stats)
        api = MarketAPI(mock_client)
        
        result = await api.get_market_stats("USD")
        
        assert result == sample_market_stats
        mock_client.get.assert_called_once_with(
            "/market/stats",
            params={"quote": "USD"}
        )

    async def test_get_market_stats_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for market stats."""
        error_data = {"error": "Invalid quote currency"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_stats("INVALID")
        assert "400" in str(exc.value)

    async def test_get_market_stats_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for market stats."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_stats("USD")
        assert "429" in str(exc.value)

    async def test_get_market_stats_http_500(self, mock_client, mock_response):
        """Test handling of 500 Internal Server Error for market stats."""
        mock_client.get.return_value = mock_response(500, {"error": "Internal server error"})
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_stats("USD")
        assert "500" in str(exc.value)

    async def test_get_market_stats_connection_error(self, mock_client):
        """Test handling of connection errors for market stats."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_stats("USD")
        assert "Connection error" in str(exc.value)

    async def test_get_market_overview_success(self, mock_client, mock_response, sample_market_overview):
        """Test successful market overview retrieval."""
        mock_client.get.return_value = mock_response(200, sample_market_overview)
        api = MarketAPI(mock_client)
        
        result = await api.get_market_overview()
        
        assert result == sample_market_overview
        mock_client.get.assert_called_once_with(
            "/market/overview"
        )

    async def test_get_market_overview_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for market overview."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_overview()
        assert "429" in str(exc.value)

    async def test_get_market_overview_http_500(self, mock_client, mock_response):
        """Test handling of 500 Internal Server Error for market overview."""
        mock_client.get.return_value = mock_response(500, {"error": "Internal server error"})
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_overview()
        assert "500" in str(exc.value)

    async def test_get_market_overview_connection_error(self, mock_client):
        """Test handling of connection errors for market overview."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = MarketAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_market_overview()
        assert "Connection error" in str(exc.value)

    async def test_get_market_overview_invalid_response(self, mock_client, mock_response):
        """Test handling of invalid response data for market overview."""
        invalid_data = {"invalid": "response"}  # Missing required fields
        mock_client.get.return_value = mock_response(200, invalid_data)
        api = MarketAPI(mock_client)
        
        result = await api.get_market_overview()
        assert result == invalid_data  # API should return raw response, validation is handled by models

    async def test_get_market_stats_with_optional_params(self, mock_client, mock_response, sample_market_stats):
        """Test market stats retrieval with optional parameters."""
        mock_client.get.return_value = mock_response(200, sample_market_stats)
        api = MarketAPI(mock_client)
        
        result = await api.get_market_stats(
            quote="USD",
            include_deprecated=True,
            min_liquidity=10000
        )
        
        assert result == sample_market_stats
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["quote"] == "USD"
        assert call_params["includeDeprecated"] is True
        assert call_params["minLiquidity"] == 10000
