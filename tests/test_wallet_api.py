"""Tests for the WalletAPI class."""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.wallet import WalletAPI
from taptools_api_mcp.utils.exceptions import TapToolsError, ErrorType
from taptools_api_mcp.models.wallet import (
    WalletPortfolioPositionsRequest, WalletTokenTradesRequest,
    WalletValueTrendedRequest
)

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

@pytest.fixture
def mock_context():
    mock_client = AsyncMock()
    ctx = MagicMock()
    ctx.request_context.lifespan_context = {"client": mock_client}
    return ctx, mock_client

@pytest.mark.asyncio
class TestWalletAPI:
    async def test_get_wallet_portfolio_positions_success(self, mock_context, sample_portfolio):
        """Test get_wallet_portfolio_positions success."""
        ctx, mock_client = mock_context
        mock_client.get.return_value.status_code = 200
        mock_client.get.return_value.json.return_value = sample_portfolio
        
        api = WalletAPI()
        request = WalletPortfolioPositionsRequest(address="addr1xyz...")
        result = await api.get_wallet_portfolio_positions(request, ctx)
        
        assert result.adaBalance == 10.0
        assert len(result.positionsFt) == 1
        assert result.positionsFt[0].ticker == "TEST1"
        
        mock_client.get.assert_called_once_with(
            "/wallet/portfolio/positions",
            params={"address": "addr1xyz..."}
        )

    async def test_get_wallet_trades_tokens_success(self, mock_context, sample_trades):
        """Test get_wallet_trades_tokens success."""
        ctx, mock_client = mock_context
        mock_client.get.return_value.status_code = 200
        mock_client.get.return_value.json.return_value = sample_trades
        
        api = WalletAPI()
        request = WalletTokenTradesRequest(address="addr1xyz...")
        result = await api.get_wallet_trades_tokens(request, ctx)
        
        assert len(result) == 1
        assert result[0].action == "Buy"
        assert result[0].tokenAAmount == 10.5
        
        mock_client.get.assert_called_once_with(
            "/wallet/trades/tokens",
            params={"address": "addr1xyz..."}
        )

    async def test_get_wallet_value_trended_success(self, mock_context, sample_value_trended):
        """Test get_wallet_value_trended success."""
        ctx, mock_client = mock_context
        mock_client.get.return_value.status_code = 200
        mock_client.get.return_value.json.return_value = sample_value_trended
        
        api = WalletAPI()
        request = WalletValueTrendedRequest(
            address="addr1xyz...",
            timeframe="7d",
            quote="USD"
        )
        result = await api.get_wallet_value_trended(request, ctx)
        
        assert len(result) == 2
        assert result[0].value == 57.0
        assert result[1].time == 1692784800
        
        mock_client.get.assert_called_once_with(
            "/wallet/value/trended",
            params={
                "address": "addr1xyz...",
                "timeframe": "7d",
                "quote": "USD"
            }
        )

    async def test_http_status_errors(self, mock_context):
        """Test various HTTP status error handling."""
        ctx, mock_client = mock_context
        
        error_cases = [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (500, "Internal Server Error")
        ]
        
        api = WalletAPI()
        request = WalletPortfolioPositionsRequest(address="addr1xyz...")
        
        for status_code, error_msg in error_cases:
            mock_client.get.return_value = AsyncMock(
                status_code=status_code,
                raise_for_status=AsyncMock(
                    side_effect=httpx.HTTPStatusError(
                        error_msg,
                        request=httpx.Request("GET", "http://test"),
                        response=httpx.Response(status_code)
                    )
                )
            )
            
            with pytest.raises(TapToolsError) as exc_info:
                await api.get_wallet_portfolio_positions(request, ctx)
            assert exc_info.value.error_type == ErrorType.API

    async def test_connection_error(self, mock_context):
        """Test connection error handling."""
        ctx, mock_client = mock_context
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        
        api = WalletAPI()
        request = WalletPortfolioPositionsRequest(address="addr1xyz...")
        
        with pytest.raises(TapToolsError) as exc_info:
            await api.get_wallet_portfolio_positions(request, ctx)
        assert exc_info.value.error_type == ErrorType.CONNECTION
        assert str(exc_info.value.message) == "Connection failed"
