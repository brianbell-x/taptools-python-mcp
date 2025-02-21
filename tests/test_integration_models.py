"""
Tests for integration-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.integration import (
    IntegrationAssetRequest, IntegrationAsset, IntegrationAssetResponse,
    IntegrationBlockRequest, IntegrationBlock, IntegrationBlockResponse,
    IntegrationEventsRequest, IntegrationEventsResponse,
    IntegrationExchangeRequest, IntegrationExchange, IntegrationExchangeResponse,
    IntegrationLatestBlockResponse,
    IntegrationPairRequest, IntegrationPair, IntegrationPairResponse,
    IntegrationPolicyAssetsRequest, PolicyAsset, IntegrationPolicyAssetsResponse
)

class TestIntegrationAssetModels:
    def test_integration_asset_request_valid(self):
        """Test IntegrationAssetRequest with valid data."""
        request = IntegrationAssetRequest(id="asset123")
        assert request.id == "asset123"

    def test_integration_asset_request_missing_id(self):
        """Test IntegrationAssetRequest fails without required id."""
        with pytest.raises(ValidationError) as exc:
            IntegrationAssetRequest()
        assert "field required" in str(exc.value)
        assert "id" in str(exc.value)

    def test_integration_asset_valid(self):
        """Test IntegrationAsset with valid data."""
        asset = IntegrationAsset(
            circulating_supply=1000000,
            id="asset123",
            name="Test Asset",
            symbol="TEST",
            total_supply=2000000
        )
        assert asset.circulating_supply == 1000000
        assert asset.id == "asset123"
        assert asset.name == "Test Asset"
        assert asset.symbol == "TEST"
        assert asset.total_supply == 2000000

    def test_integration_asset_invalid_types(self):
        """Test IntegrationAsset with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            IntegrationAsset(
                circulating_supply="invalid",  # Should be integer
                id=123,  # Should be string
                name=123,  # Should be string
                symbol=123,  # Should be string
                total_supply="invalid"  # Should be integer
            )
        assert "value is not a valid integer" in str(exc.value)

class TestIntegrationBlockModels:
    def test_integration_block_request_optional_fields(self):
        """Test IntegrationBlockRequest with optional fields."""
        request = IntegrationBlockRequest()
        assert request.number is None
        assert request.timestamp is None

    def test_integration_block_request_with_values(self):
        """Test IntegrationBlockRequest with provided values."""
        request = IntegrationBlockRequest(
            number=12345,
            timestamp=1234567890
        )
        assert request.number == 12345
        assert request.timestamp == 1234567890

    def test_integration_block_valid(self):
        """Test IntegrationBlock with valid data."""
        block = IntegrationBlock(
            block_number=12345,
            block_timestamp=1234567890
        )
        assert block.block_number == 12345
        assert block.block_timestamp == 1234567890

    def test_integration_block_invalid_types(self):
        """Test IntegrationBlock with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            IntegrationBlock(
                block_number="invalid",  # Should be integer
                block_timestamp="invalid"  # Should be integer
            )
        assert "value is not a valid integer" in str(exc.value)

class TestIntegrationPolicyAssetsModels:
    def test_integration_policy_assets_request_valid(self):
        """Test IntegrationPolicyAssetsRequest with valid data."""
        request = IntegrationPolicyAssetsRequest(id="policy123")
        assert request.id == "policy123"
        assert request.page == 1  # Default value
        assert request.per_page == 100  # Default value

    def test_integration_policy_assets_request_custom_pagination(self):
        """Test IntegrationPolicyAssetsRequest with custom pagination."""
        request = IntegrationPolicyAssetsRequest(
            id="policy123",
            page=2,
            per_page=50
        )
        assert request.id == "policy123"
        assert request.page == 2
        assert request.per_page == 50

    def test_integration_policy_assets_request_missing_id(self):
        """Test IntegrationPolicyAssetsRequest fails without required id."""
        with pytest.raises(ValidationError) as exc:
            IntegrationPolicyAssetsRequest()
        assert "field required" in str(exc.value)
        assert "id" in str(exc.value)

    def test_policy_asset_valid(self):
        """Test PolicyAsset with valid data."""
        asset = PolicyAsset(
            id="asset123",
            name="Test Asset"
        )
        assert asset.id == "asset123"
        assert asset.name == "Test Asset"

    def test_policy_asset_invalid_types(self):
        """Test PolicyAsset with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            PolicyAsset(
                id=123,  # Should be string
                name=123  # Should be string
            )
        assert "str type expected" in str(exc.value)

    def test_integration_policy_assets_response_valid(self):
        """Test IntegrationPolicyAssetsResponse with valid data."""
        assets = [
            PolicyAsset(id="asset1", name="Asset One"),
            PolicyAsset(id="asset2", name="Asset Two")
        ]
        response = IntegrationPolicyAssetsResponse(
            id="policy123",
            name="Test Policy",
            description="A test policy",
            assets=assets,
            total_assets=2
        )
        assert response.id == "policy123"
        assert response.name == "Test Policy"
        assert response.description == "A test policy"
        assert len(response.assets) == 2
        assert response.total_assets == 2

    def test_integration_policy_assets_response_optional_description(self):
        """Test IntegrationPolicyAssetsResponse with optional description omitted."""
        response = IntegrationPolicyAssetsResponse(
            id="policy123",
            name="Test Policy",
            total_assets=0
        )
        assert response.id == "policy123"
        assert response.name == "Test Policy"
        assert response.description is None
        assert len(response.assets) == 0
        assert response.total_assets == 0

    def test_integration_policy_assets_response_invalid_types(self):
        """Test IntegrationPolicyAssetsResponse with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            IntegrationPolicyAssetsResponse(
                id=123,  # Should be string
                name=123,  # Should be string
                description=123,  # Should be string if provided
                total_assets="invalid"  # Should be integer
            )
        assert "str type expected" in str(exc.value)
        assert "value is not a valid integer" in str(exc.value)
        assert "id" in str(exc.value)

class TestIntegrationEventsModels:
    def test_integration_events_request_valid(self):
        """Test IntegrationEventsRequest with valid data."""
        request = IntegrationEventsRequest(
            from_block=12345,
            to_block=12350
        )
        assert request.from_block == 12345
        assert request.to_block == 12350
        assert request.limit == 1000  # Default value

    def test_integration_events_request_custom_limit(self):
        """Test IntegrationEventsRequest with custom limit."""
        request = IntegrationEventsRequest(
            from_block=12345,
            to_block=12350,
            limit=500
        )
        assert request.limit == 500

    def test_integration_events_response_valid(self):
        """Test IntegrationEventsResponse with valid data."""
        events = [
            {"type": "transfer", "amount": 100},
            {"type": "mint", "amount": 200}
        ]
        response = IntegrationEventsResponse(events=events)
        assert len(response.events) == 2
        assert response.events[0]["type"] == "transfer"
        assert response.events[1]["type"] == "mint"

class TestIntegrationExchangeModels:
    def test_integration_exchange_request_valid(self):
        """Test IntegrationExchangeRequest with valid data."""
        request = IntegrationExchangeRequest(id="exchange123")
        assert request.id == "exchange123"

    def test_integration_exchange_valid(self):
        """Test IntegrationExchange with valid data."""
        exchange = IntegrationExchange(
            factory_address="0x123abc",
            logo_url="https://example.com/logo.png",
            name="Test Exchange"
        )
        assert exchange.factory_address == "0x123abc"
        assert exchange.logo_url == "https://example.com/logo.png"
        assert exchange.name == "Test Exchange"

    def test_integration_exchange_invalid_types(self):
        """Test IntegrationExchange with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            IntegrationExchange(
                factory_address=123,  # Should be string
                logo_url=123,  # Should be string
                name=123  # Should be string
            )
        assert "str type expected" in str(exc.value)

class TestIntegrationPairModels:
    def test_integration_pair_request_valid(self):
        """Test IntegrationPairRequest with valid data."""
        request = IntegrationPairRequest(id="pair123")
        assert request.id == "pair123"

    def test_integration_pair_valid(self):
        """Test IntegrationPair with valid data."""
        pair = IntegrationPair(
            asset0_id="asset1",
            asset1_id="asset2",
            created_at_block_number=12345,
            created_at_block_timestamp=1234567890,
            created_at_txn_id=67890,
            factory_address="0x123abc",
            id="pair123"
        )
        assert pair.asset0_id == "asset1"
        assert pair.asset1_id == "asset2"
        assert pair.created_at_block_number == 12345
        assert pair.created_at_block_timestamp == 1234567890
        assert pair.created_at_txn_id == 67890
        assert pair.factory_address == "0x123abc"
        assert pair.id == "pair123"

    def test_integration_pair_invalid_types(self):
        """Test IntegrationPair with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            IntegrationPair(
                asset0_id=123,  # Should be string
                asset1_id=123,  # Should be string
                created_at_block_number="invalid",  # Should be integer
                created_at_block_timestamp="invalid",  # Should be integer
                created_at_txn_id="invalid",  # Should be integer
                factory_address=123,  # Should be string
                id=123  # Should be string
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "str type expected" in str(exc.value)

    def test_integration_pair_missing_required(self):
        """Test IntegrationPair fails without required fields."""
        with pytest.raises(ValidationError) as exc:
            IntegrationPair()
        assert "field required" in str(exc.value)
