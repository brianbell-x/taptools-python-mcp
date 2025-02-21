"""
Tests for market-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.market import (
    MarketStatsRequest, MarketStats, MarketStatsResponse,
    MetricsCall, MetricsResponse
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
