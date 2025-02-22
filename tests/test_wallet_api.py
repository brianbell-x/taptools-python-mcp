"""
Tests for the WalletAPI class.
Expanded to cover get_wallet_portfolio, get_wallet_trades_tokens, etc.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.wallet import WalletAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def sample_portfolio():
    return {
        "adaBalance": 10.0,
        "adaValue": 10000.0,
        "liquidValue": 10000.0,
        "numFTs": 2,
        "numNFTs": 1,
        "positionsFt": [
            {
                "ticker": "TEST1",
                "balance": 200.0,
                "unit": "b46b12f0...",
                "fingerprint": "fingerprint1",
                "price": 100.0,
                "adaValue": 20000.0,
                "price_24h": 0.11,
                "price_7d": 0.03,
                "price_30d": -0.32,
                "liquidBalance": 200.0,
                "liquidValue": 20000.0
            }
        ],
        "positionsLp": [],
        "positionsNft": []
    }

@pytest.fixture
def sample_trades():
    return [
        {
            "action": "Buy",
            "time": 1692781200,
            "tokenA": "tokenX",
            "tokenAName": "TestTokenX",
            "tokenAAmount": 10.5,
            "tokenB": "lovelace",
            "tokenBName": "ADA",
            "tokenBAmount": 500.0
        }
    ]

@pytest.fixture
def sample_value_trended():
    return [
        {"time": 1692781200, "value": 57.0},
        {"time": 1692784800, "value": 60.2},
    ]

@pytest.mark.asyncio
class TestWalletAPI:
    async def test_get_wallet_portfolio_positions_success(self, mock_client, mock_response, sample_portfolio):
        """Test get_wallet_portfolio_positions success."""
        mock_client.get.return_value = mock_response(200, sample_portfolio)
        api = WalletAPI(mock_client)

        req_obj = {"address": "addr1xyz..."}
        result = await api.get_wallet_portfolio_positions(req_obj)
        assert result.adaBalance == 10.0
        assert len(result.positionsFt) == 1

        mock_client.get.assert_called_once_with("/wallet/portfolio/positions", params=req_obj)

    async def test_get_wallet_trades_tokens_success(self, mock_client, mock_response, sample_trades):
        """Test get_wallet_trades_tokens success."""
        mock_client.get.return_value = mock_response(200, sample_trades)
        api = WalletAPI(mock_client)

        req_obj = {"address": "addr1xyz..."}
        result = await api.get_wallet_trades_tokens(req_obj)
        assert len(result) == 1
        assert result[0].action == "Buy"

        mock_client.get.assert_called_once_with("/wallet/trades/tokens", params=req_obj)

    async def test_get_wallet_value_trended_success(self, mock_client, mock_response, sample_value_trended):
        """Test get_wallet_value_trended success."""
        mock_client.get.return_value = mock_response(200, sample_value_trended)
        api = WalletAPI(mock_client)

        req_obj = {"address": "addr1xyz...", "timeframe": "7d", "quote": "USD"}
        result = await api.get_wallet_value_trended(req_obj)
        assert len(result) == 2
        assert result[0].value == 57.0

        mock_client.get.assert_called_once_with("/wallet/value/trended", params=req_obj)

    async def test_portfolio_positions_400(self, mock_client, mock_response):
        """Test error handling for invalid address."""
        mock_client.get.return_value = mock_response(400, {"error": "Invalid address"})
        api = WalletAPI(mock_client)

        with pytest.raises(TapToolsError):
            await api.get_wallet_portfolio_positions({"address": "???"})

    async def test_connection_error(self, mock_client):
        """Test connection error example."""
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        api = WalletAPI(mock_client)

        with pytest.raises(TapToolsError):
            await api.get_wallet_portfolio_positions({"address": "addr1xyz..."})
