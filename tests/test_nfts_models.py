"""
Tests for NFT-related Pydantic models.
"""
import pytest
from pydantic import ValidationError

from taptools_api_mcp.models.nfts import (
    NFTAssetSalesRequest, NFTSale, NFTAssetSalesResponse,
    NFTCollectionStatsRequest, NFTCollectionStats, NFTCollectionStatsResponse,
    NFTCollectionTradesRequest, NFTTrade, NFTCollectionTradesResponse,
    NFTCollectionInfoRequest, NFTCollectionInfo, NFTCollectionInfoResponse,
    NFTTopVolumeRequest, NFTTopVolume, NFTTopVolumeResponse
)

class TestNFTAssetSalesModels:
    def test_nft_asset_sales_request_valid(self):
        """Test NFTAssetSalesRequest with valid data."""
        request = NFTAssetSalesRequest(
            policy="policy123",
            name="Test NFT"
        )
        assert request.policy == "policy123"
        assert request.name == "Test NFT"

    def test_nft_asset_sales_request_missing_policy(self):
        """Test NFTAssetSalesRequest fails without required policy."""
        with pytest.raises(ValidationError) as exc:
            NFTAssetSalesRequest()
        assert "field required" in str(exc.value)
        assert "policy" in str(exc.value)

    def test_nft_sale_valid(self):
        """Test NFTSale with valid data."""
        sale = NFTSale(
            buyer_stake_address="stake1test123buyer",
            price=100.5,
            seller_stake_address="stake1test123seller",
            time=1234567890
        )
        assert sale.buyer_stake_address == "stake1test123buyer"
        assert sale.price == 100.5
        assert sale.seller_stake_address == "stake1test123seller"
        assert sale.time == 1234567890

    def test_nft_sale_invalid_price(self):
        """Test NFTSale with invalid price."""
        with pytest.raises(ValidationError) as exc:
            NFTSale(
                buyer_stake_address="stake1test123buyer",
                price="invalid",
                seller_stake_address="stake1test123seller",
                time=1234567890
            )
        assert "value is not a valid float" in str(exc.value)

class TestNFTCollectionStatsModels:
    def test_nft_collection_stats_request_valid(self):
        """Test NFTCollectionStatsRequest with valid data."""
        request = NFTCollectionStatsRequest(policy="policy123")
        assert request.policy == "policy123"

    def test_nft_collection_stats_valid(self):
        """Test NFTCollectionStats with valid data."""
        stats = NFTCollectionStats(
            listings=100,
            owners=50,
            price=150.5,
            sales=75,
            supply=1000,
            top_offer=200.0,
            volume=15000.0
        )
        assert stats.listings == 100
        assert stats.owners == 50
        assert stats.price == 150.5
        assert stats.sales == 75
        assert stats.supply == 1000
        assert stats.top_offer == 200.0
        assert stats.volume == 15000.0

    def test_nft_collection_stats_invalid_types(self):
        """Test NFTCollectionStats with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            NFTCollectionStats(
                listings="invalid",
                owners="invalid",
                price="invalid",
                sales="invalid",
                supply="invalid",
                top_offer="invalid",
                volume="invalid"
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)

class TestNFTCollectionTradesModels:
    def test_nft_collection_trades_request_defaults(self):
        """Test NFTCollectionTradesRequest with default values."""
        request = NFTCollectionTradesRequest()
        assert request.timeframe == "30d"
        assert request.sort_by == "time"
        assert request.order == "desc"
        assert request.page == 1
        assert request.per_page == 100

    def test_nft_collection_trades_request_custom(self):
        """Test NFTCollectionTradesRequest with custom values."""
        request = NFTCollectionTradesRequest(
            policy="policy123",
            timeframe="7d",
            sort_by="price",
            order="asc",
            min_amount=100,
            from_time=1234567890,
            page=2,
            per_page=50
        )
        assert request.policy == "policy123"
        assert request.timeframe == "7d"
        assert request.sort_by == "price"
        assert request.order == "asc"
        assert request.min_amount == 100
        assert request.from_time == 1234567890
        assert request.page == 2
        assert request.per_page == 50

    def test_nft_trade_valid(self):
        """Test NFTTrade with valid data."""
        trade = NFTTrade(
            buyer_address="addr1test123buyer",
            collection_name="Test Collection",
            hash="tx123",
            image="ipfs://test",
            market="jpg.store",
            name="Test NFT",
            policy="policy123",
            price=100.5,
            seller_address="addr1test123seller",
            time=1234567890
        )
        assert trade.buyer_address == "addr1test123buyer"
        assert trade.collection_name == "Test Collection"
        assert trade.hash == "tx123"
        assert trade.image == "ipfs://test"
        assert trade.market == "jpg.store"
        assert trade.name == "Test NFT"
        assert trade.policy == "policy123"
        assert trade.price == 100.5
        assert trade.seller_address == "addr1test123seller"
        assert trade.time == 1234567890

class TestNFTCollectionInfoModels:
    def test_nft_collection_info_request_valid(self):
        """Test NFTCollectionInfoRequest with valid data."""
        request = NFTCollectionInfoRequest(policy="policy123")
        assert request.policy == "policy123"

    def test_nft_collection_info_valid(self):
        """Test NFTCollectionInfo with valid data."""
        info = NFTCollectionInfo(
            description="Test collection description",
            discord="https://discord.gg/test",
            logo="ipfs://test",
            name="Test Collection",
            supply=1000,
            twitter="https://twitter.com/test",
            website="https://test.com"
        )
        assert info.description == "Test collection description"
        assert info.discord == "https://discord.gg/test"
        assert info.logo == "ipfs://test"
        assert info.name == "Test Collection"
        assert info.supply == 1000
        assert info.twitter == "https://twitter.com/test"
        assert info.website == "https://test.com"

    def test_nft_collection_info_optional_fields(self):
        """Test NFTCollectionInfo with only required fields."""
        info = NFTCollectionInfo(
            description="Test collection description",
            logo="ipfs://test",
            name="Test Collection",
            supply=1000
        )
        assert info.description == "Test collection description"
        assert info.logo == "ipfs://test"
        assert info.name == "Test Collection"
        assert info.supply == 1000
        assert info.discord is None
        assert info.twitter is None
        assert info.website is None

class TestNFTTopVolumeModels:
    def test_nft_top_volume_request_defaults(self):
        """Test NFTTopVolumeRequest with default values."""
        request = NFTTopVolumeRequest()
        assert request.timeframe == "24h"
        assert request.page == 1
        assert request.per_page == 10

    def test_nft_top_volume_request_custom(self):
        """Test NFTTopVolumeRequest with custom values."""
        request = NFTTopVolumeRequest(
            timeframe="7d",
            page=2,
            per_page=50
        )
        assert request.timeframe == "7d"
        assert request.page == 2
        assert request.per_page == 50

    def test_nft_top_volume_valid(self):
        """Test NFTTopVolume with valid data."""
        volume = NFTTopVolume(
            listings=100,
            logo="ipfs://test",
            name="Test Collection",
            policy="policy123",
            price=150.5,
            sales=75,
            supply=1000,
            volume=15000.0
        )
        assert volume.listings == 100
        assert volume.logo == "ipfs://test"
        assert volume.name == "Test Collection"
        assert volume.policy == "policy123"
        assert volume.price == 150.5
        assert volume.sales == 75
        assert volume.supply == 1000
        assert volume.volume == 15000.0

    def test_nft_top_volume_invalid_types(self):
        """Test NFTTopVolume with invalid data types."""
        with pytest.raises(ValidationError) as exc:
            NFTTopVolume(
                listings="invalid",
                logo=123,  # Should be string
                name=123,  # Should be string
                policy=123,  # Should be string
                price="invalid",
                sales="invalid",
                supply="invalid",
                volume="invalid"
            )
        assert "value is not a valid integer" in str(exc.value)
        assert "value is not a valid float" in str(exc.value)
