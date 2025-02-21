"""
Tests for market-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.market import (
    MarketStatsRequest, MarketStats, MarketStatsResponse,
    MetricsCall, MetricsResponse,
    MarketOverviewToken, MarketOverviewResponse
)

class TestMarketStatsModels:
    def test_market_stats_request_defaults(self):
        """Test MarketStatsRequest with default values."""
        request = MarketStatsRequest()
        assert request.quote == "ADA"  # Default value

    def test_market_stats_request_custom(self):
        """Test MarketStatsRequest with custom quote."""
        request = MarketStatsRequest(quote="USD")
        assert request.quote == "USD"

    def test_market_stats_valid(self):
        """Test MarketStats with valid data."""
        stats = MarketStats(
            active_addresses=1000,
            dex_volume=500000.5
        )
        assert stats.active_addresses == 1000
        assert stats.dex_volume == 500000.5

    def test_market_stats_invalid_types(self):
        """Test MarketStats with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            MarketStats(
                active_addresses="invalid",  # Should be integer
                dex_volume="invalid"  # Should be float
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)

    def test_market_stats_missing_required(self):
        """Test MarketStats fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            MarketStats()
        assert "field required" in str(exc.value)

    def test_market_stats_response_valid(self):
        """Test MarketStatsResponse with valid data."""
        stats = MarketStats(
            active_addresses=1000,
            dex_volume=500000.5
        )
        response = MarketStatsResponse(stats=stats)
        assert response.stats.active_addresses == 1000
        assert response.stats.dex_volume == 500000.5

    def test_market_stats_response_invalid(self):
        """Test MarketStatsResponse with invalid data."""
        with pytest.raises(ValidationError) as exc:
            MarketStatsResponse(stats="invalid")  # Should be MarketStats object
        assert "value is not a valid dict" in str(exc.value)

class TestMetricsModels:
    def test_metrics_call_valid(self):
        """Test MetricsCall with valid data."""
        call = MetricsCall(
            calls=100,
            time=1234567890
        )
        assert call.calls == 100
        assert call.time == 1234567890

    def test_metrics_call_invalid_types(self):
        """Test MetricsCall with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            MetricsCall(
                calls="invalid",  # Should be integer
                time="invalid"    # Should be integer
            )
        assert "value is not a valid integer" in str(exc.value)

    def test_metrics_call_missing_required(self):
        """Test MetricsCall fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            MetricsCall()
        assert "field required" in str(exc.value)

    def test_metrics_response_valid(self):
        """Test MetricsResponse with valid data."""
        calls = [
            MetricsCall(calls=100, time=1234567890),
            MetricsCall(calls=200, time=1234567891)
        ]
        response = MetricsResponse(metrics=calls)
        assert len(response.metrics) == 2
        assert response.metrics[0].calls == 100
        assert response.metrics[0].time == 1234567890
        assert response.metrics[1].calls == 200
        assert response.metrics[1].time == 1234567891

    def test_metrics_response_empty_list(self):
        """Test MetricsResponse with empty metrics list."""
        response = MetricsResponse(metrics=[])
        assert len(response.metrics) == 0

    def test_metrics_response_invalid_list_items(self):
        """Test MetricsResponse with invalid list items."""
        with pytest.raises(ValidationError) as exc:
            MetricsResponse(metrics=[
                "invalid",  # Should be MetricsCall object
                123        # Should be MetricsCall object
            ])
        assert "value is not a valid dict" in str(exc.value)

    def test_metrics_response_missing_required(self):
        """Test MetricsResponse fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            MetricsResponse()
        assert "field required" in str(exc.value)

class TestMarketOverviewModels:
    def test_market_overview_token_valid(self):
        """Test MarketOverviewToken with valid data."""
        token = MarketOverviewToken(
            unit="token1",
            change24h=10.5,
            volume24h=1000000.0
        )
        assert token.unit == "token1"
        assert token.change24h == 10.5
        assert token.volume24h == 1000000.0

    def test_market_overview_token_optional_fields(self):
        """Test MarketOverviewToken with only required fields."""
        token = MarketOverviewToken(unit="token1")
        assert token.unit == "token1"
        assert token.change24h is None
        assert token.volume24h is None

    def test_market_overview_token_invalid_types(self):
        """Test MarketOverviewToken with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            MarketOverviewToken(
                unit=123,  # Should be string
                change24h="invalid",  # Should be float
                volume24h="invalid"  # Should be float
            )
        assert "value is not a valid string" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)

    def test_market_overview_token_missing_required(self):
        """Test MarketOverviewToken fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            MarketOverviewToken()
        assert "field required" in str(exc.value)

    def test_market_overview_response_valid(self):
        """Test MarketOverviewResponse with valid data."""
        response = MarketOverviewResponse(
            gainers=[
                MarketOverviewToken(unit="token1", change24h=15.5),
                MarketOverviewToken(unit="token2", change24h=12.3)
            ],
            losers=[
                MarketOverviewToken(unit="token3", change24h=-10.2),
                MarketOverviewToken(unit="token4", change24h=-8.5)
            ],
            trending=[
                MarketOverviewToken(unit="token5", volume24h=2000000.0),
                MarketOverviewToken(unit="token6", volume24h=1500000.0)
            ]
        )
        assert len(response.gainers) == 2
        assert len(response.losers) == 2
        assert len(response.trending) == 2
        assert response.gainers[0].unit == "token1"
        assert response.gainers[0].change24h == 15.5
        assert response.losers[0].unit == "token3"
        assert response.losers[0].change24h == -10.2
        assert response.trending[0].unit == "token5"
        assert response.trending[0].volume24h == 2000000.0

    def test_market_overview_response_defaults(self):
        """Test MarketOverviewResponse with default empty lists."""
        response = MarketOverviewResponse()
        assert len(response.gainers) == 0
        assert len(response.losers) == 0
        assert len(response.trending) == 0

    def test_market_overview_response_invalid_list_items(self):
        """Test MarketOverviewResponse with invalid list items."""
        with pytest.raises(ValidationError) as exc:
            MarketOverviewResponse(
                gainers=["invalid"],  # Should be MarketOverviewToken objects
                losers=[123],         # Should be MarketOverviewToken objects
                trending=[456]        # Should be MarketOverviewToken objects
            )
        assert "value is not a valid dict" in str(exc.value)
