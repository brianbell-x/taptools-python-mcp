"""
Tests for the IntegrationAPI class.
Expanded to cover all IntegrationAPI methods.
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
        "asset": {
            "circulatingSupply": 1000000,
            "id": "asset1...",
            "name": "TestToken",
            "symbol": "TEST",
            "totalSupply": 2000000
        }
    }

@pytest.fixture
def sample_block_data():
    """Sample block data for testing."""
    return {
        "block": {
            "blockNumber": 12345,
            "blockTimestamp": 1670000000
        }
    }

@pytest.fixture
def sample_events_data():
    """Sample events data for testing."""
    return {
        "events": [
            {
                "amount0": "100",
                "amount1": "200",
                "block": {
                    "blockNumber": 12345,
                    "blockTimestamp": 1670000000
                },
                "eventIndex": 1234500001,
                "eventType": "swap",
                "maker": "addr_test1...",
                "pairId": "pair123",
                "reserves": {"tokenA": "1000", "tokenB": "2000"},
                "txnId": "txhash1...",
                "txnIndex": 0,
                "asset0In": "0",
                "asset0Out": "100",
                "asset1In": "200",
                "asset1Out": "0"
            }
        ]
    }

@pytest.fixture
def sample_exchange_data():
    """Sample exchange data for testing."""
    return {
        "exchange": {
            "factoryAddress": "addr_test1factory",
            "logoUrl": "https://example.com/exchangelogo.png",
            "name": "TestDEX"
        }
    }

@pytest.fixture
def sample_latest_block_data():
    """Sample latest block data for testing."""
    return {
        "block": {
            "blockNumber": 99999,
            "blockTimestamp": 1680000000
        }
    }

@pytest.fixture
def sample_pair_data():
    """Sample pair data for testing."""
    return {
        "pair": {
            "asset0Id": "tokenA",
            "asset1Id": "tokenB",
            "createdAtBlockNumber": 12345,
            "createdAtBlockTimestamp": 1670000000,
            "createdAtTxnId": "txhash2...",
            "factoryAddress": "addr_test1factory",
            "id": "pair_testAB"
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
            {"id": "asset1...", "name": "Token1"},
            {"id": "asset2...", "name": "Token2"}
        ],
        "totalAssets": 2
    }

@pytest.mark.asyncio
class TestIntegrationAPI:
    async def test_get_asset_success(self, mock_client, mock_response, sample_asset_data):
        """Test successful asset retrieval."""
        mock_client.get.return_value = mock_response(200, sample_asset_data)
        api = IntegrationAPI(mock_client)

        request_obj = {"id": "asset1..."}
        result = await api.get_asset(request_obj)
        assert result.asset.id == "asset1..."
        assert result.asset.circulatingSupply == 1000000

        mock_client.get.assert_called_once_with(
            "/integration/asset",
            params=request_obj
        )

    async def test_get_asset_http_400(self, mock_client, mock_response):
        """Test handling of 400 Bad Request for asset retrieval."""
        error_data = {"error": "Invalid asset ID format"}
        mock_client.get.return_value = mock_response(400, error_data)
        api = IntegrationAPI(mock_client)

        with pytest.raises(TapToolsError) as exc:
            await api.get_asset({"id": "invalid..."})
        assert "400" in str(exc.value)

    async def test_get_block_success(self, mock_client, mock_response, sample_block_data):
        """Test get_block endpoint success."""
        mock_client.get.return_value = mock_response(200, sample_block_data)
        api = IntegrationAPI(mock_client)

        req_obj = {"number": 12345}
        result = await api.get_block(req_obj)
        assert result.block.blockNumber == 12345

        mock_client.get.assert_called_once_with("/integration/block", params=req_obj)

    async def test_get_events_success(self, mock_client, mock_response, sample_events_data):
        """Test get_events endpoint success."""
        mock_client.get.return_value = mock_response(200, sample_events_data)
        api = IntegrationAPI(mock_client)

        req_obj = {"fromBlock": 10000, "toBlock": 10010, "limit": 100}
        result = await api.get_events(req_obj)
        assert len(result.events) == 1
        assert result.events[0].eventType == "swap"

        mock_client.get.assert_called_once_with("/integration/events", params=req_obj)

    async def test_get_exchange_success(self, mock_client, mock_response, sample_exchange_data):
        """Test get_exchange endpoint success."""
        mock_client.get.return_value = mock_response(200, sample_exchange_data)
        api = IntegrationAPI(mock_client)

        req_obj = {"id": "testdex123"}
        result = await api.get_exchange(req_obj)
        assert result.exchange.name == "TestDEX"

        mock_client.get.assert_called_once_with("/integration/exchange", params=req_obj)

    async def test_get_latest_block_success(self, mock_client, mock_response, sample_latest_block_data):
        """Test get_latest_block endpoint success."""
        mock_client.get.return_value = mock_response(200, sample_latest_block_data)
        api = IntegrationAPI(mock_client)

        result = await api.get_latest_block()
        assert result.block.blockNumber == 99999

        mock_client.get.assert_called_once_with("/integration/latest-block")

    async def test_get_pair_success(self, mock_client, mock_response, sample_pair_data):
        """Test get_pair endpoint success."""
        mock_client.get.return_value = mock_response(200, sample_pair_data)
        api = IntegrationAPI(mock_client)

        req_obj = {"id": "pair_testAB"}
        result = await api.get_pair(req_obj)
        assert result.pair.id == "pair_testAB"
        assert result.pair.asset0Id == "tokenA"

        mock_client.get.assert_called_once_with("/integration/pair", params=req_obj)

    async def test_get_policy_assets_success(self, mock_client, mock_response, sample_policy_data):
        """Test successful policy assets retrieval."""
        mock_client.get.return_value = mock_response(200, sample_policy_data)
        api = IntegrationAPI(mock_client)

        req_obj = {"id": "policy1...", "page": 1, "perPage": 50}
        result = await api.get_policy_assets(req_obj)
        assert result.id == "policy1..."
        assert len(result.assets) == 2

        mock_client.get.assert_called_once_with("/integration/policy/assets", params=req_obj)

    async def test_connection_error(self, mock_client):
        """Test connection error for any integration endpoint."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = IntegrationAPI(mock_client)

        with pytest.raises(TapToolsError) as exc:
            await api.get_latest_block()
        assert "Connection error" in str(exc.value)
