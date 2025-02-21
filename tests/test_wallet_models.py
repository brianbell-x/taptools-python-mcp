"""
Tests for wallet-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.wallet import (
    WalletPortfolioPositionsRequest, WalletPortfolioPositionsResponse,
    WalletTokenTradesRequest, WalletTokenTrade,
    WalletValueTrendedRequest, WalletValueTrend
)

class TestWalletPortfolioPositionsModels:
    def test_portfolio_positions_request_valid(self):
        """Test WalletPortfolioPositionsRequest with valid data."""
        request = WalletPortfolioPositionsRequest(
            address="addr1test123"
        )
        assert request.address == "addr1test123"

    def test_portfolio_positions_request_missing_address(self):
        """Test WalletPortfolioPositionsRequest fails without required address."""
        with pytest.raises(ValidationError) as exc:
            WalletPortfolioPositionsRequest()
        assert "field required" in str(exc.value)
        assert "address" in str(exc.value)

    def test_portfolio_positions_response_valid(self):
        """Test WalletPortfolioPositionsResponse with valid data."""
        response = WalletPortfolioPositionsResponse(
            ada_balance=1000.5,
            ada_value=1500.75,
            liquid_value=2000.25,
            num_fts=5,
            num_nfts=10,
            positions_ft=[
                {"token": "token1", "amount": 100},
                {"token": "token2", "amount": 200}
            ],
            positions_lp=[
                {"pool": "pool1", "share": 0.1},
                {"pool": "pool2", "share": 0.2}
            ],
            positions_nft=[
                {"policy": "policy1", "name": "nft1"},
                {"policy": "policy2", "name": "nft2"}
            ]
        )
        assert response.ada_balance == 1000.5
        assert response.ada_value == 1500.75
        assert response.liquid_value == 2000.25
        assert response.num_fts == 5
        assert response.num_nfts == 10
        assert len(response.positions_ft) == 2
        assert len(response.positions_lp) == 2
        assert len(response.positions_nft) == 2

    def test_portfolio_positions_response_invalid_types(self):
        """Test WalletPortfolioPositionsResponse with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            WalletPortfolioPositionsResponse(
                ada_balance="invalid",  # Should be float
                ada_value="invalid",    # Should be float
                liquid_value="invalid", # Should be float
                num_fts="invalid",      # Should be int
                num_nfts="invalid",     # Should be int
                positions_ft="invalid",  # Should be list
                positions_lp="invalid",  # Should be list
                positions_nft="invalid"  # Should be list
            )
        assert "value is not a valid float" in str(exc.value)
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid list" in str(exc.value)

class TestWalletTokenTradesModels:
    def test_token_trades_request_valid(self):
        """Test WalletTokenTradesRequest with valid data."""
        request = WalletTokenTradesRequest(
            address="addr1test123",
            unit="token1"
        )
        assert request.address == "addr1test123"
        assert request.unit == "token1"

    def test_token_trades_request_missing_address(self):
        """Test WalletTokenTradesRequest fails without required address."""
        with pytest.raises(ValidationError) as exc:
            WalletTokenTradesRequest()
        assert "field required" in str(exc.value)
        assert "address" in str(exc.value)

    def test_token_trades_request_optional_unit(self):
        """Test WalletTokenTradesRequest with optional unit omitted."""
        request = WalletTokenTradesRequest(address="addr1test123")
        assert request.address == "addr1test123"
        assert request.unit is None

    def test_wallet_token_trade_valid(self):
        """Test WalletTokenTrade with valid data."""
        trade = WalletTokenTrade(
            action="Buy",
            hash="tx123",
            time=1234567890,
            token_a="token1",
            token_a_amount=100.5,
            token_a_name="Token One",
            token_b="token2",
            token_b_amount=200.5,
            token_b_name="Token Two"
        )
        assert trade.action == "Buy"
        assert trade.hash == "tx123"
        assert trade.time == 1234567890
        assert trade.token_a == "token1"
        assert trade.token_a_amount == 100.5
        assert trade.token_a_name == "Token One"
        assert trade.token_b == "token2"
        assert trade.token_b_amount == 200.5
        assert trade.token_b_name == "Token Two"

    def test_wallet_token_trade_invalid_types(self):
        """Test WalletTokenTrade with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            WalletTokenTrade(
                action=123,           # Should be string
                hash=123,             # Should be string
                time="invalid",       # Should be integer
                token_a=123,          # Should be string
                token_a_amount="invalid",  # Should be float
                token_a_name=123,     # Should be string
                token_b=123,          # Should be string
                token_b_amount="invalid",  # Should be float
                token_b_name=123      # Should be string
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)

class TestWalletValueTrendedModels:
    def test_value_trended_request_valid(self):
        """Test WalletValueTrendedRequest with valid data."""
        request = WalletValueTrendedRequest(
            address="addr1test123"
        )
        assert request.address == "addr1test123"
        assert request.timeframe == "30d"  # Default value
        assert request.quote == "ADA"      # Default value

    def test_value_trended_request_custom(self):
        """Test WalletValueTrendedRequest with custom values."""
        request = WalletValueTrendedRequest(
            address="addr1test123",
            timeframe="7d",
            quote="USD"
        )
        assert request.address == "addr1test123"
        assert request.timeframe == "7d"
        assert request.quote == "USD"

    def test_value_trended_request_missing_address(self):
        """Test WalletValueTrendedRequest fails without required address."""
        with pytest.raises(ValidationError) as exc:
            WalletValueTrendedRequest()
        assert "field required" in str(exc.value)
        assert "address" in str(exc.value)

    def test_wallet_value_trend_valid(self):
        """Test WalletValueTrend with valid data."""
        trend = WalletValueTrend(
            time=1234567890,
            value=1000.5
        )
        assert trend.time == 1234567890
        assert trend.value == 1000.5

    def test_wallet_value_trend_invalid_types(self):
        """Test WalletValueTrend with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            WalletValueTrend(
                time="invalid",  # Should be integer
                value="invalid"  # Should be float
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)

    def test_wallet_value_trend_missing_required(self):
        """Test WalletValueTrend fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            WalletValueTrend()
        assert "field required" in str(exc.value)
