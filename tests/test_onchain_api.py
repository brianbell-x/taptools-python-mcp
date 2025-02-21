"""
Tests for the OnchainAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.onchain import OnchainAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_asset_supply():
    """Sample asset supply data for testing."""
    return {
        "unit": "test_token",
        "total": "1000000000",
        "circulating": "800000000",
        "treasury": "200000000",
        "burned": "0"
    }

@pytest.fixture
def sample_transaction_data():
    """Sample transaction data for testing."""
    return {
        "hash": "tx1...",
        "block": "block1...",
        "slot": 12345678,
        "index": 1,
        "inputs": [
            {
                "address": "addr1...",
                "amount": "1000000"
            }
        ],
        "outputs": [
            {
                "address": "addr2...",
                "amount": "900000"
            }
        ],
        "metadata": {
            "label": "123",
            "content": {"key": "value"}
        }
    }

@pytest.mark.asyncio
class TestOnchainAPI:
    async def test_get_asset_supply_success(self, mock_client, mock_response, sample_asset_supply):
        """Test successful asset supply retrieval."""
        mock_client.get.return_value = mock_response(200, sample_asset_supply)
        api = OnchainAPI(mock_client)
        
        result = await api.get_asset_supply("test_token")
        
        assert result == sample_asset_supply
        mock_client.get.assert_called_once_with(
            "/onchain/asset/supply",
            params={"unit": "test_token"}
        )

    async def test_get_asset_supply_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for asset supply."""
        error_data = {"error": "Invalid token unit"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_supply("invalid_token")
        assert "400" in str(exc.value)

    async def test_get_asset_supply_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for asset supply."""
        mock_client.get.return_value = mock_response(404, {"error": "Asset not found"})
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_supply("nonexistent_token")
        assert "404" in str(exc.value)

    async def test_get_asset_supply_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for asset supply."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_supply("test_token")
        assert "429" in str(exc.value)

    async def test_get_asset_supply_connection_error(self, mock_client):
        """Test handling of connection errors for asset supply."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_supply("test_token")
        assert "Connection error" in str(exc.value)

    async def test_get_transaction_success(self, mock_client, mock_response, sample_transaction_data):
        """Test successful transaction retrieval."""
        mock_client.get.return_value = mock_response(200, sample_transaction_data)
        api = OnchainAPI(mock_client)
        
        result = await api.get_transaction("tx1...")
        
        assert result == sample_transaction_data
        mock_client.get.assert_called_once_with(
            "/onchain/tx",
            params={"hash": "tx1..."}
        )

    async def test_get_transaction_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for transaction."""
        error_data = {"error": "Invalid transaction hash"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction("invalid...")
        assert "400" in str(exc.value)

    async def test_get_transaction_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for transaction."""
        mock_client.get.return_value = mock_response(404, {"error": "Transaction not found"})
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction("nonexistent...")
        assert "404" in str(exc.value)

    async def test_get_transaction_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for transaction."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction("tx1...")
        assert "429" in str(exc.value)

    async def test_get_transaction_connection_error(self, mock_client):
        """Test handling of connection errors for transaction."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = OnchainAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_transaction("tx1...")
        assert "Connection error" in str(exc.value)

    async def test_get_transaction_invalid_response(self, mock_client, mock_response):
        """Test handling of invalid response data for transaction."""
        invalid_data = {"invalid": "response"}  # Missing required fields
        mock_client.get.return_value = mock_response(200, invalid_data)
        api = OnchainAPI(mock_client)
        
        result = await api.get_transaction("tx1...")
        assert result == invalid_data  # API should return raw response, validation is handled by models

    async def test_get_asset_supply_with_optional_params(self, mock_client, mock_response, sample_asset_supply):
        """Test asset supply retrieval with optional parameters."""
        mock_client.get.return_value = mock_response(200, sample_asset_supply)
        api = OnchainAPI(mock_client)
        
        result = await api.get_asset_supply(
            "test_token",
            include_treasury=True,
            include_burned=True
        )
        
        assert result == sample_asset_supply
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["unit"] == "test_token"
        assert call_params["includeTreasury"] is True
        assert call_params["includeBurned"] is True
