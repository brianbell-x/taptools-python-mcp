"""
Tests for the OnchainAPI class.
Expanded to cover address info, UTXOs, transactions, etc.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.onchain import OnchainAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_supply_data():
    return {"supply": 1234567}

@pytest.fixture
def sample_address_info():
    return {
        "address": "addr_test1xyz",
        "paymentCred": "abcdef12345",
        "lovelace": "45000000",
        "assets": [
            {"unit": "tokenA", "quantity": "1000"}
        ],
        "stakeAddress": "stake_test1abc"
    }

@pytest.fixture
def sample_utxos_data():
    return [
        {
            "hash": "txhash123",
            "index": 0,
            "lovelace": "3703342",
            "assets": []
        }
    ]

@pytest.fixture
def sample_tx_utxos_data():
    return {
        "hash": "txhashXYZ",
        "inputs": [
            {
                "hash": "inputhash123",
                "index": 0,
                "lovelace": "5000000",
                "assets": []
            }
        ],
        "outputs": [
            {
                "hash": "outputhash456",
                "index": 1,
                "lovelace": "3000000",
                "assets": []
            }
        ]
    }

@pytest.mark.asyncio
class TestOnchainAPI:
    async def test_get_asset_supply_success(self, mock_client, mock_response, sample_supply_data):
        """Test get_asset_supply success."""
        mock_client.get.return_value = mock_response(200, sample_supply_data)
        api = OnchainAPI(mock_client)

        req_obj = {"unit": "testtoken"}
        result = await api.get_asset_supply(req_obj)
        assert result.supply == 1234567
        mock_client.get.assert_called_once_with("/asset/supply", params=req_obj)

    async def test_get_asset_supply_400(self, mock_client, mock_response):
        mock_client.get.return_value = mock_response(400, {"error": "Bad token unit"})
        api = OnchainAPI(mock_client)
        with pytest.raises(TapToolsError):
            await api.get_asset_supply({"unit": "???"})

    async def test_get_address_details(self, mock_client, mock_response, sample_address_info):
        mock_client.get.return_value = mock_response(200, sample_address_info)
        api = OnchainAPI(mock_client)

        req_obj = {"address": "addr_test1xyz"}
        result = await api.get_address_details(req_obj)
        assert result.address == "addr_test1xyz"
        assert len(result.assets) == 1

        mock_client.get.assert_called_once_with("/address/info", params=req_obj)

    async def test_get_address_utxos(self, mock_client, mock_response, sample_utxos_data):
        mock_client.get.return_value = mock_response(200, sample_utxos_data)
        api = OnchainAPI(mock_client)

        req_obj = {"address": "addr_test1xyz", "page": 1, "perPage": 50}
        result = await api.get_address_utxos(req_obj)
        assert len(result.__root__) == 1
        mock_client.get.assert_called_once_with("/address/utxos", params=req_obj)

    async def test_get_transaction_details(self, mock_client, mock_response, sample_tx_utxos_data):
        mock_client.get.return_value = mock_response(200, sample_tx_utxos_data)
        api = OnchainAPI(mock_client)

        req_obj = {"hash": "txhashXYZ"}
        result = await api.get_transaction_details(req_obj)
        assert result.hash == "txhashXYZ"
        assert len(result.inputs) == 1
        assert len(result.outputs) == 1

        mock_client.get.assert_called_once_with("/transaction/utxos", params=req_obj)

    async def test_connection_error(self, mock_client):
        """Test connection error example."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = OnchainAPI(mock_client)
        with pytest.raises(TapToolsError):
            await api.get_asset_supply({"unit": "something"})
