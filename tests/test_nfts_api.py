"""
Tests for the NftsAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.nfts import NftsAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_nft_data():
    """Sample NFT data for testing."""
    return {
        "policy": "test_policy",
        "name": "Test NFT",
        "fingerprint": "asset1...",
        "metadata": {
            "name": "Test NFT",
            "description": "A test NFT",
            "image": "ipfs://..."
        }
    }

@pytest.fixture
def sample_sales_data():
    """Sample NFT sales data for testing."""
    return {
        "sales": [
            {
                "txHash": "tx1",
                "price": 50000000,
                "marketplace": "jpg.store",
                "timestamp": "2024-02-20T12:00:00Z"
            },
            {
                "txHash": "tx2",
                "price": 75000000,
                "marketplace": "jpg.store",
                "timestamp": "2024-02-19T12:00:00Z"
            }
        ],
        "total": 2
    }

@pytest.fixture
def sample_collection_stats():
    """Sample collection statistics for testing."""
    return {
        "policy": "test_policy",
        "floor": 50000000,
        "volume24h": 125000000,
        "holders": 100,
        "listed": 10,
        "totalSupply": 1000
    }

@pytest.mark.asyncio
class TestNftsAPI:
    async def test_get_asset_sales_success(self, mock_client, mock_response, sample_sales_data):
        """Test successful NFT asset sales retrieval."""
        mock_client.get.return_value = mock_response(200, sample_sales_data)
        api = NftsAPI(mock_client)
        
        result = await api.get_asset_sales("test_policy", "Test NFT")
        
        assert result == sample_sales_data
        mock_client.get.assert_called_once_with(
            "/nft/asset/sales",
            params={"policy": "test_policy", "name": "Test NFT"}
        )

    async def test_get_asset_sales_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for asset sales."""
        error_data = {"error": "Invalid policy ID"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_sales("invalid_policy", "Test NFT")
        assert "400" in str(exc.value)

    async def test_get_asset_sales_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for asset sales."""
        mock_client.get.return_value = mock_response(404, {"error": "Asset not found"})
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_sales("test_policy", "Nonexistent NFT")
        assert "404" in str(exc.value)

    async def test_get_asset_sales_connection_error(self, mock_client):
        """Test handling of connection errors for asset sales."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset_sales("test_policy", "Test NFT")
        assert "Connection error" in str(exc.value)

    async def test_get_collection_stats_success(self, mock_client, mock_response, sample_collection_stats):
        """Test successful collection stats retrieval."""
        mock_client.get.return_value = mock_response(200, sample_collection_stats)
        api = NftsAPI(mock_client)
        
        result = await api.get_collection_stats("test_policy")
        
        assert result == sample_collection_stats
        mock_client.get.assert_called_once_with(
            "/nft/collection/stats",
            params={"policy": "test_policy"}
        )

    async def test_get_collection_stats_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for collection stats."""
        error_data = {"error": "Invalid policy ID format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_collection_stats("invalid_policy")
        assert "400" in str(exc.value)

    async def test_get_collection_stats_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for collection stats."""
        mock_client.get.return_value = mock_response(404, {"error": "Collection not found"})
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_collection_stats("nonexistent_policy")
        assert "404" in str(exc.value)

    async def test_get_collection_stats_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for collection stats."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_collection_stats("test_policy")
        assert "429" in str(exc.value)

    async def test_get_collection_stats_http_500(self, mock_client, mock_response):
        """Test handling of 500 Internal Server Error for collection stats."""
        mock_client.get.return_value = mock_response(500, {"error": "Internal server error"})
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_collection_stats("test_policy")
        assert "500" in str(exc.value)

    async def test_get_collection_stats_connection_error(self, mock_client):
        """Test handling of connection errors for collection stats."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = NftsAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_collection_stats("test_policy")
        assert "Connection error" in str(exc.value)

    async def test_get_collection_stats_invalid_response(self, mock_client, mock_response):
        """Test handling of invalid response data for collection stats."""
        invalid_data = {"invalid": "response"}  # Missing required fields
        mock_client.get.return_value = mock_response(200, invalid_data)
        api = NftsAPI(mock_client)
        
        result = await api.get_collection_stats("test_policy")
        assert result == invalid_data  # API should return raw response, validation is handled by models
