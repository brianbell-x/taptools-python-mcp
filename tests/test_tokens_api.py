"""
Tests for the TokensAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.tokens import TokensAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.mark.asyncio
class TestTokensAPI:
    async def test_get_token_mcap_success(self, mock_client, mock_response, sample_token_data):
        """Test successful token market cap retrieval."""
        mock_client.get.return_value = mock_response(200, sample_token_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_mcap("test_token")
        
        assert result == sample_token_data
        mock_client.get.assert_called_once_with(
            "/token/mcap",
            params={"unit": "test_token"}
        )

    async def test_get_token_mcap_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request."""
        error_data = {"error": "Invalid token unit"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = TokensAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_token_mcap("invalid_token")
        assert "400" in str(exc.value)

    async def test_get_token_mcap_http_401(self, mock_client, mock_response):
        """Test handling of 401 Unauthorized."""
        mock_client.get.return_value = mock_response(401, {"error": "Unauthorized"})
        api = TokensAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_token_mcap("test_token")
        assert "401" in str(exc.value)

    async def test_get_token_mcap_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = TokensAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_token_mcap("test_token")
        assert "429" in str(exc.value)

    async def test_get_token_mcap_connection_error(self, mock_client):
        """Test handling of connection errors."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = TokensAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_token_mcap("test_token")
        assert "Connection error" in str(exc.value)

    async def test_get_token_holders_success(self, mock_client, mock_response):
        """Test successful token holders retrieval."""
        holders_data = {"total": 1000, "active": 800}
        mock_client.get.return_value = mock_response(200, holders_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_holders("test_token")
        
        assert result == holders_data
        mock_client.get.assert_called_once_with(
            "/token/holders",
            params={"unit": "test_token"}
        )

    async def test_get_token_holders_top_success(self, mock_client, mock_response):
        """Test successful top token holders retrieval."""
        top_holders_data = {
            "holders": [
                {"address": "addr1", "balance": 1000},
                {"address": "addr2", "balance": 500}
            ],
            "total": 2
        }
        mock_client.get.return_value = mock_response(200, top_holders_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_holders_top("test_token", page=1, perPage=10)
        
        assert result == top_holders_data
        mock_client.get.assert_called_once_with(
            "/token/holders/top",
            params={"unit": "test_token", "page": 1, "perPage": 10}
        )

    async def test_post_token_prices_success(self, mock_client, mock_response):
        """Test successful token prices retrieval."""
        prices_data = {"token1": 1.0, "token2": 2.0}
        mock_client.post.return_value = mock_response(200, prices_data)
        api = TokensAPI(mock_client)
        
        result = await api.post_token_prices(["token1", "token2"])
        
        assert result == prices_data
        mock_client.post.assert_called_once_with(
            "/token/prices",
            json=["token1", "token2"]
        )

    async def test_get_token_price_changes_success(self, mock_client, mock_response):
        """Test successful token price changes retrieval."""
        changes_data = {"1h": 1.5, "24h": -2.0, "7d": 5.0}
        mock_client.get.return_value = mock_response(200, changes_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_price_changes("test_token", "1h,24h,7d")
        
        assert result == changes_data
        mock_client.get.assert_called_once_with(
            "/token/prices/chg",
            params={"unit": "test_token", "timeframes": "1h,24h,7d"}
        )

    async def test_get_token_trades_success(self, mock_client, mock_response):
        """Test successful token trades retrieval."""
        trades_data = {
            "trades": [
                {"txHash": "hash1", "amount": 100},
                {"txHash": "hash2", "amount": 200}
            ],
            "total": 2
        }
        mock_client.get.return_value = mock_response(200, trades_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_trades(
            timeframe="30d",
            sort_by="amount",
            order="desc",
            unit="test_token"
        )
        
        assert result == trades_data
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["timeframe"] == "30d"
        assert call_params["sortBy"] == "amount"
        assert call_params["order"] == "desc"
        assert call_params["unit"] == "test_token"

    async def test_get_token_trading_stats_success(self, mock_client, mock_response):
        """Test successful token trading stats retrieval."""
        stats_data = {
            "volume": 1000000,
            "trades": 500,
            "avgPrice": 2.0
        }
        mock_client.get.return_value = mock_response(200, stats_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_trading_stats("test_token", "24h")
        
        assert result == stats_data
        mock_client.get.assert_called_once_with(
            "/token/trading/stats",
            params={"unit": "test_token", "timeframe": "24h"}
        )

    async def test_get_available_quotes_success(self, mock_client, mock_response):
        """Test successful available quotes retrieval."""
        quotes_data = ["USD", "EUR", "ADA"]
        mock_client.get.return_value = mock_response(200, quotes_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_available_quotes()
        
        assert result == quotes_data
        mock_client.get.assert_called_once_with("/token/quote/available")

    async def test_get_token_quote_success(self, mock_client, mock_response):
        """Test successful token quote retrieval."""
        quote_data = {"ADA": {"USD": 0.5}}
        mock_client.get.return_value = mock_response(200, quote_data)
        api = TokensAPI(mock_client)
        
        result = await api.get_token_quote("USD")
        
        assert result == quote_data
        mock_client.get.assert_called_once_with(
            "/token/quote",
            params={"quote": "USD"}
        )
