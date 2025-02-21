"""
Tests for the IntegrationAPI class.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.integration import IntegrationAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_asset_data():
    """Sample asset data for testing."""
    return {
        "id": "asset1...",
        "policyId": "policy1...",
        "assetName": "TestToken",
        "fingerprint": "asset1...",
        "quantity": "1000000",
        "initialMintTxHash": "tx1...",
        "metadata": {
            "name": "Test Token",
            "description": "A test token",
            "ticker": "TEST",
            "url": "https://test.com",
            "logo": "https://test.com/logo.png",
            "decimals": 6
        }
    }

@pytest.fixture
def sample_policy_data():
    """Sample policy data for testing."""
    return {
        "id": "policy1...",
        "name": "Test Policy",
        "description": "A test policy",
        "assets": [
            {
                "id": "asset1...",
                "name": "Token1"
            },
            {
                "id": "asset2...",
                "name": "Token2"
            }
        ],
        "totalAssets": 2
    }

@pytest.mark.asyncio
class TestIntegrationAPI:
    async def test_get_asset_success(self, mock_client, mock_response, sample_asset_data):
        """Test successful asset retrieval."""
        mock_client.get.return_value = mock_response(200, sample_asset_data)
        api = IntegrationAPI(mock_client)
        
        result = await api.get_asset("asset1...")
        
        assert result == sample_asset_data
        mock_client.get.assert_called_once_with(
            "/integration/asset",
            params={"id": "asset1..."}
        )

    async def test_get_asset_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for asset retrieval."""
        error_data = {"error": "Invalid asset ID format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset("invalid...")
        assert "400" in str(exc.value)

    async def test_get_asset_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for asset retrieval."""
        mock_client.get.return_value = mock_response(404, {"error": "Asset not found"})
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset("nonexistent...")
        assert "404" in str(exc.value)

    async def test_get_asset_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for asset retrieval."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset("asset1...")
        assert "429" in str(exc.value)

    async def test_get_asset_connection_error(self, mock_client):
        """Test handling of connection errors for asset retrieval."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_asset("asset1...")
        assert "Connection error" in str(exc.value)

    async def test_get_policy_assets_success(self, mock_client, mock_response, sample_policy_data):
        """Test successful policy assets retrieval."""
        mock_client.get.return_value = mock_response(200, sample_policy_data)
        api = IntegrationAPI(mock_client)
        
        result = await api.get_policy_assets("policy1...")
        
        assert result == sample_policy_data
        mock_client.get.assert_called_once_with(
            "/integration/policy/assets",
            params={"id": "policy1..."}
        )

    async def test_get_policy_assets_with_pagination(self, mock_client, mock_response, sample_policy_data):
        """Test policy assets retrieval with pagination."""
        mock_client.get.return_value = mock_response(200, sample_policy_data)
        api = IntegrationAPI(mock_client)
        
        result = await api.get_policy_assets(
            "policy1...",
            page=2,
            per_page=50
        )
        
        assert result == sample_policy_data
        mock_client.get.assert_called_once()
        call_params = mock_client.get.call_args[1]["params"]
        assert call_params["id"] == "policy1..."
        assert call_params["page"] == 2
        assert call_params["perPage"] == 50

    async def test_get_policy_assets_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for policy assets retrieval."""
        error_data = {"error": "Invalid policy ID format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_policy_assets("invalid...")
        assert "400" in str(exc.value)

    async def test_get_policy_assets_http_404(self, mock_client, mock_response):
        """Test handling of 404 Not Found for policy assets retrieval."""
        mock_client.get.return_value = mock_response(404, {"error": "Policy not found"})
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_policy_assets("nonexistent...")
        assert "404" in str(exc.value)

    async def test_get_policy_assets_http_429(self, mock_client, mock_response):
        """Test handling of 429 Too Many Requests for policy assets retrieval."""
        mock_client.get.return_value = mock_response(429, {"error": "Rate limit exceeded"})
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_policy_assets("policy1...")
        assert "429" in str(exc.value)

    async def test_get_policy_assets_connection_error(self, mock_client):
        """Test handling of connection errors for policy assets retrieval."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = IntegrationAPI(mock_client)
        
        with pytest.raises(TapToolsError) as exc:
            await api.get_policy_assets("policy1...")
        assert "Connection error" in str(exc.value)

    async def test_get_policy_assets_invalid_response(self, mock_client, mock_response):
        """Test handling of invalid response data for policy assets retrieval."""
        invalid_data = {"invalid": "response"}  # Missing required fields
        mock_client.get.return_value = mock_response(200, invalid_data)
        api = IntegrationAPI(mock_client)
        
        result = await api.get_policy_assets("policy1...")
        assert result == invalid_data  # API should return raw response, validation is handled by models
