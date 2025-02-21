"""
Tests for token-related Pydantic models.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from taptools_api_mcp.models.tokens import (
    TokenMcapRequest, TokenMcap, TokenMcapResponse,
    TokenHoldersRequest, TokenHoldersResponse,
    TokenTopHoldersRequest, TokenHolder, TokenTopHoldersResponse,
    TokenTradesRequest, TokenTrade, TokenTradesResponse,
    TokenTradingStatsRequest, TokenTradingStats, TokenTradingStatsResponse
)

class TestTokenMcapModels:
    def test_token_mcap_request_valid(self):
        """Test TokenMcapRequest with valid data."""
        request = TokenMcapRequest(unit="test_token")
        assert request.unit == "test_token"

    def test_token_mcap_request_missing_unit(self):
        """Test TokenMcapRequest fails without required unit."""
        with pytest.raises(ValidationError) as exc:
            TokenMcapRequest()
        assert "field required" in str(exc.value)
        assert "unit" in str(exc.value)

    def test_token_mcap_valid(self):
        """Test TokenMcap with valid data."""
        data = {
            "circ_supply": 1000000.0,
            "fdv": 2000000.0,
            "mcap": 1500000.0,
            "price": 1.5,
            "ticker": "TEST",
            "total_supply": 2000000.0
        }
        mcap = TokenMcap(**data)
        assert mcap.circ_supply == 1000000.0
        assert mcap.fdv == 2000000.0
        assert mcap.mcap == 1500000.0
        assert mcap.price == 1.5
        assert mcap.ticker == "TEST"
        assert mcap.total_supply == 2000000.0

    def test_token_mcap_invalid_types(self):
        """Test TokenMcap validation with invalid types."""
        data = {
            "circ_supply": "invalid",
            "fdv": "invalid",
            "mcap": "invalid",
            "price": "invalid",
            "ticker": 123,  # Should be string
            "total_supply": "invalid"
        }
        with pytest.raises(ValidationError) as exc:
            TokenMcap(**data)
        assert "value is not a valid float" in str(exc.value)

class TestTokenHoldersModels:
    def test_token_holders_request_valid(self):
        """Test TokenHoldersRequest with valid data."""
        request = TokenHoldersRequest(unit="test_token")
        assert request.unit == "test_token"

    def test_token_holders_response_valid(self):
        """Test TokenHoldersResponse with valid data."""
        response = TokenHoldersResponse(holders=1000)
        assert response.holders == 1000

    def test_token_holders_response_invalid(self):
        """Test TokenHoldersResponse with invalid data."""
        with pytest.raises(ValidationError):
            TokenHoldersResponse(holders="invalid")

class TestTokenTopHoldersModels:
    def test_token_top_holders_request_valid(self):
        """Test TokenTopHoldersRequest with valid data and defaults."""
        request = TokenTopHoldersRequest(unit="test_token")
        assert request.unit == "test_token"
        assert request.page == 1  # Default value
        assert request.per_page == 20  # Default value

    def test_token_top_holders_request_custom_pagination(self):
        """Test TokenTopHoldersRequest with custom pagination."""
        request = TokenTopHoldersRequest(
            unit="test_token",
            page=2,
            per_page=50
        )
        assert request.page == 2
        assert request.per_page == 50

    def test_token_holder_valid(self):
        """Test TokenHolder with valid data."""
        holder = TokenHolder(
            address="stake1test123",
            amount=1000.5
        )
        assert holder.address == "stake1test123"
        assert holder.amount == 1000.5

    def test_token_holder_invalid_amount(self):
        """Test TokenHolder with invalid amount."""
        with pytest.raises(ValidationError):
            TokenHolder(
                address="stake1test123",
                amount="invalid"
            )

class TestTokenTradesModels:
    def test_token_trades_request_defaults(self):
        """Test TokenTradesRequest with default values."""
        request = TokenTradesRequest()
        assert request.timeframe == "30d"
        assert request.sort_by == "amount"
        assert request.order == "desc"
        assert request.page == 1
        assert request.per_page == 100

    def test_token_trades_request_custom(self):
        """Test TokenTradesRequest with custom values."""
        request = TokenTradesRequest(
            timeframe="7d",
            sort_by="time",
            order="asc",
            unit="test_token",
            min_amount=100,
            from_ts=1234567890,
            page=2,
            per_page=50
        )
        assert request.timeframe == "7d"
        assert request.sort_by == "time"
        assert request.order == "asc"
        assert request.unit == "test_token"
        assert request.min_amount == 100
        assert request.from_ts == 1234567890
        assert request.page == 2
        assert request.per_page == 50

    def test_token_trade_valid(self):
        """Test TokenTrade with valid data."""
        trade = TokenTrade(
            amount=100.5,
            price=1.23,
            side="buy",
            time=1234567890,
            token="test_token",
            value=123.615
        )
        assert trade.amount == 100.5
        assert trade.price == 1.23
        assert trade.side == "buy"
        assert trade.time == 1234567890
        assert trade.token == "test_token"
        assert trade.value == 123.615

    def test_token_trade_invalid_side(self):
        """Test TokenTrade with invalid side value."""
        with pytest.raises(ValidationError) as exc:
            TokenTrade(
                amount=100.5,
                price=1.23,
                side="invalid",  # Should be 'buy' or 'sell'
                time=1234567890,
                token="test_token",
                value=123.615
            )

class TestTokenTradingStatsModels:
    def test_token_trading_stats_request_valid(self):
        """Test TokenTradingStatsRequest with valid data."""
        request = TokenTradingStatsRequest(unit="test_token")
        assert request.unit == "test_token"
        assert request.timeframe == "24h"  # Default value

    def test_token_trading_stats_request_custom_timeframe(self):
        """Test TokenTradingStatsRequest with custom timeframe."""
        request = TokenTradingStatsRequest(
            unit="test_token",
            timeframe="7d"
        )
        assert request.timeframe == "7d"

    def test_token_trading_stats_valid(self):
        """Test TokenTradingStats with valid data."""
        stats = TokenTradingStats(
            buy_volume=1000.0,
            buyers=50,
            buys=75,
            sell_volume=800.0,
            sellers=40,
            sells=60
        )
        assert stats.buy_volume == 1000.0
        assert stats.buyers == 50
        assert stats.buys == 75
        assert stats.sell_volume == 800.0
        assert stats.sellers == 40
        assert stats.sells == 60

    def test_token_trading_stats_invalid_types(self):
        """Test TokenTradingStats with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            TokenTradingStats(
                buy_volume="invalid",
                buyers="invalid",
                buys="invalid",
                sell_volume="invalid",
                sellers="invalid",
                sells="invalid"
            )
        assert "value is not a valid float" in str(exc.value)
        assert "value is not a valid integer" in str(exc.value)
