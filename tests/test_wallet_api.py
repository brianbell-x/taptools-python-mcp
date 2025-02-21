"""
Tests for the WalletAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.wallet import WalletAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing."""
    return {
        "address": "addr1...",
        "positions": [
            {
                "unit": "token1",
                "balance": "1000000",
                "value_usd": "1500.50",
                "price_usd": "1.50"
            },
            {
                "unit": "token2",
                "balance": "500000",
                "value_usd": "2500.00",
                "price_usd": "5.00"
            }
        ],
        "total_value_usd": "4000.50",
        "last_updated": "2024-02-20T12:00:00Z"
    }

@pytest.fixture
def sample_transaction_history():
    """Sample transaction history data for testing."""
    return {
        "transactions": [
            {
                "hash": "tx1...",
                "timestamp": "2024-02-20T12:00:00Z",
                "type": "send",
                "amount": "1000000",
                "unit": "token1",
                "to_address": "addr2..."
            },
            {
                "hash": "tx2...",
                "timestamp": "2024-02-19T12:00:00Z",
                "type": "receive",
                "amount": "500000",
                "unit": "token2",
                "from_address": "addr3..."
            }
        ],
        "total": 2
    }

@pytest.mark.asyncio
class TestWalletAPI:
    async def test_get_portfolio_positions_success(self, mock_client, mock_response, sample_portfolio_data):
        """Test successful portfolio positions retrieval."""
        mock_client.get.return_value = mock_response(200, sample_portfolio_data)
        api = WalletAPI(mock_client)
        
        result = await api.get_portfolio_positions("addr1...")
        
        assert result == sample_portfolio_data
        mock_client.get.assert_called_once_with(
            "/wallet/portfolio/positions",
            params={"address": "addr1..."}
        )

    async def test_get_portfolio_positions_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for portfolio positions."""
        error_data = {"error": "Invalid address format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_portfolio_positions("invalid...")
        assert "400" in str(exc.value)

    async def test_get_portfolio_positions_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for portfolio positions."""
        mock_client.get.return_value = mock_response(404, {"error": "Address not found"})
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_portfolio_positions("nonexistent...")
        assert "404" in str(exc.value)

    async def test_get_portfolio_positions_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for portfolio positions."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_portfolio_positions("addr1...")
        assert "429" in str(exc.value)

    async def test_get_portfolio_positions_connection_error(self, mock_client):
        """Test handling of connection errors for portfolio positions."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_portfolio_positions("addr1...")
        assert "Connection error" in str(exc.value)

    async def test_get_transaction_history_success(self, mock_client, mock_response, sample_transaction_history):
        """Test successful transaction history retrieval."""
        mock_client.get.return_value = mock_response(200, sample_transaction_history)
        api = WalletAPI(mock_client)
        
        result = await api.get_transaction_history("addr1...")
        
        assert result == sample_transaction_history
        mock_client.get.assert_called_once_with(
            "/wallet/transactions",
            params={"address": "addr1..."}
        )

    async def test_get_transaction_history_with_pagination(self, mock_client, mock_response, sample_transaction_history):
        """Test transaction history retrieval with pagination."""
        mock_client.get.return_value = mock_response(200, sample_transaction_history)
        api = WalletAPI(mock_client)
        
        result = await api.get_transaction_history(
            "addr1...",
            page=2,
            per_page=50
        )
        
        assert result == sample_transaction_history
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["address"] == "addr1..."
        assert call_params["page"] == 2
        assert call_params["perPage"] == 50

    async def test_get_transaction_history_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for transaction history."""
        error_data = {"error": "Invalid address format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction_history("invalid...")
        assert "400" in str(exc.value)

    async def test_get_transaction_history_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for transaction history."""
        mock_client.get.return_value = mock_response(404, {"error": "Address not found"})
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction_history("nonexistent...")
        assert "404" in str(exc.value)

    async def test_get_transaction_history_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for transaction history."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction_history("addr1...")
        assert "429" in str(exc.value)

    async def test_get_transaction_history_connection_error(self, mock_client):
        """Test handling of connection errors for transaction history."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = WalletAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction_history("addr1...")
        assert "Connection error" in str(exc.value)

    async def test_get_transaction_history_invalid_response(self, mock_client, mock_response):
        """Test handling of invalid response data for transaction history."""
        invalid_data = {"invalid": "response"}  # Missing required fields
        mock_client.get.return_value = mock_response(200, invalid_data)
        api = WalletAPI(mock_client)
        
        result = await api.get_transaction_history("addr1...")
        assert result == invalid_data  # API should return raw response, validation is handled by models

    async def test_get_portfolio_positions_with_filters(self, mock_client, mock_response, sample_portfolio_data):
        """Test portfolio positions retrieval with optional filters."""
        mock_client.get.return_value = mock_response(200, sample_portfolio_data)
        api = WalletAPI(mock_client)
        
        result = await api.get_portfolio_positions(
            "addr1...",
            min_value_usd=100,
            include_zero_balances=False
        )
        
        assert result == sample_portfolio_data
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["address"] == "addr1..."
        assert call_params["minValueUsd"] == 100
        assert call_params["includeZeroBalances"] is False
