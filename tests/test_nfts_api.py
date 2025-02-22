"""
Tests for the NftsAPI class.
Expanded to cover all NFT-related endpoints.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from taptools_api_mcp.api.nfts import NftsAPI
from taptools_api_mcp.utils.exceptions import TapToolsError

@pytest.fixture
def nft_collection_response():
    return {
        "policy": "test_policy",
        "floor": 500,
        "volume24h": 10000,
        "holders": 200,
        "listed": 20,
        "totalSupply": 1000
    }

@pytest.fixture
def sample_asset_sales_data():
    """Sample NFT asset sales data."""
    return [
        {
            "buyerStakeAddress": "stake_buyer",
            "price": 100.5,
            "sellerStakeAddress": "stake_seller",
            "time": 1690000000
        }
    ]

@pytest.fixture
def sample_nft_collection_info():
    return {
        "description": "Test collection",
        "discord": "https://discord.gg/test",
        "logo": "ipfs://test",
        "name": "Test Collection",
        "supply": 9999,
        "twitter": "https://twitter.com/test",
        "website": "https://testsite.io"
    }

@pytest.fixture
def sample_asset_traits():
    return {
        "rank": 51,
        "traits": [
            {
                "category": "background",
                "name": "red",
                "rarity": 0.4,
                "price": 100
            }
        ]
    }

@pytest.fixture
def sample_collection_assets():
    return [
        {
            "image": "ipfs://QmeDi3J1exQYnGAuwZv7b6sAuDBAo2hYdAMM1KGgS7KFa4",
            "name": "TestNFT1",
            "price": 20,
            "rank": 2
        }
    ]

@pytest.fixture
def sample_holders_distribution():
    return {
        "1": 1154,
        "2-4": 631,
        "5-9": 327,
        "10-24": 60,
        "25+": 2
    }

@pytest.fixture
def sample_collection_trades():
    return [
        {
            "buyer_address": "addr1test",
            "collection_name": "Test Collection",
            "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
            "image": "ipfs://test",
            "market": "jpg.store",
            "name": "TestNFT1",
            "policy": "test_policy",
            "price": 4925,
            "seller_address": "addr2test",
            "time": 1680135943
        }
    ]

@pytest.mark.asyncio
class TestNftsAPI:
    async def test_get_nft_asset_sales_success(self, mock_client, mock_response, sample_asset_sales_data):
        """Test successful get_nft_asset_sales."""
        mock_client.get.return_value = mock_response(200, sample_asset_sales_data)
        api = NftsAPI(mock_client)

        req_obj = {"policy": "testpolicy", "name": "TestNFT"}
        result = await api.get_asset_sales(req_obj)
        assert len(result.__root__) == 1
        assert result.__root__[0].price == 100.5

        mock_client.get.assert_called_once_with("/nft/asset/sales", params=req_obj)

    async def test_get_nft_asset_sales_http_400(self, mock_client, mock_response):
        """Test handling of 400 for get_nft_asset_sales."""
        mock_client.get.return_value = mock_response(400, {"error": "Bad policy"})
        api = NftsAPI(mock_client)

        with pytest.raises(TapToolsError):
            await api.get_asset_sales({"policy": "invalid"})

    async def test_get_nft_collection_stats_success(self, mock_client, mock_response, nft_collection_response):
        """Test get_nft_collection_stats success."""
        mock_client.get.return_value = mock_response(200, nft_collection_response)
        api = NftsAPI(mock_client)

        req_obj = {"policy": "test_policy"}
        result = await api.get_collection_stats(req_obj)
        assert result.__root__["floor"] == 500

        mock_client.get.assert_called_once_with("/nft/collection/stats", params=req_obj)

    async def test_get_nft_collection_stats_error(self, mock_client, mock_response):
        """Test error case for get_nft_collection_stats."""
        mock_client.get.return_value = mock_response(404, {"error": "Not found"})
        api = NftsAPI(mock_client)

        with pytest.raises(TapToolsError):
            await api.get_collection_stats({"policy": "nonexistent"})

    async def test_get_nft_asset_stats(self, mock_client, mock_response):
        mock_client.get.return_value = mock_response(200, {
            "isListed": True,
            "lastListedPrice": 3850,
            "lastListedTime": 1681234567,
            "lastSoldPrice": 4800,
            "lastSoldTime": 1681000000,
            "owners": 6,
            "sales": 5,
            "timesListed": 8,
            "volume": 54234
        })
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy", "name": "TestNFT"}
        result = await api.get_nft_asset_stats(req_obj)
        assert result.lastSoldPrice == 4800
        mock_client.get.assert_called_once_with("/nft/asset/stats", params=req_obj)

    async def test_get_nft_collection_info(self, mock_client, mock_response, sample_nft_collection_info):
        """Test get_nft_collection_info."""
        mock_client.get.return_value = mock_response(200, sample_nft_collection_info)
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy"}
        result = await api.get_nft_collection_info(req_obj)
        assert result.__root__["name"] == "Test Collection"

        mock_client.get.assert_called_once_with("/nft/collection/info", params=req_obj)

    async def test_get_nft_collection_info_400(self, mock_client, mock_response):
        mock_client.get.return_value = mock_response(400, {"error": "Invalid policy"})
        api = NftsAPI(mock_client)

        with pytest.raises(TapToolsError):
            await api.get_nft_collection_info({"policy": "???"})

    async def test_get_nft_asset_traits(self, mock_client, mock_response, sample_asset_traits):
        """Test get_nft_asset_traits."""
        mock_client.get.return_value = mock_response(200, sample_asset_traits)
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy", "name": "TestNFT"}
        result = await api.get_nft_asset_traits(req_obj)
        assert result.rank == 51
        assert len(result.traits) == 1
        assert result.traits[0].category == "background"

        mock_client.get.assert_called_once_with("/nft/asset/traits", params=req_obj)

    async def test_get_nft_collection_assets(self, mock_client, mock_response, sample_collection_assets):
        """Test get_nft_collection_assets."""
        mock_client.get.return_value = mock_response(200, sample_collection_assets)
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy", "sortBy": "price", "order": "asc"}
        result = await api.get_nft_collection_assets(req_obj)
        assert len(result.__root__) == 1
        assert result.__root__[0].price == 20

        mock_client.get.assert_called_once_with("/nft/collection/assets", params=req_obj)

    async def test_get_nft_collection_holders_distribution(self, mock_client, mock_response, sample_holders_distribution):
        """Test get_nft_collection_holders_distribution."""
        mock_client.get.return_value = mock_response(200, sample_holders_distribution)
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy"}
        result = await api.get_nft_collection_holders_distribution(req_obj)
        assert result.__root__["1"] == 1154
        assert result.__root__["25+"] == 2

        mock_client.get.assert_called_once_with("/nft/collection/holders/distribution", params=req_obj)

    async def test_get_nft_collection_trades(self, mock_client, mock_response, sample_collection_trades):
        """Test get_nft_collection_trades."""
        mock_client.get.return_value = mock_response(200, sample_collection_trades)
        api = NftsAPI(mock_client)
        req_obj = {"policy": "test_policy", "timeframe": "24h"}
        result = await api.get_nft_collection_trades(req_obj)
        assert len(result.__root__) == 1
        assert result.__root__[0].price == 4925
        assert result.__root__[0].market == "jpg.store"

        mock_client.get.assert_called_once_with("/nft/collection/trades", params=req_obj)

    async def test_get_nft_market_stats(self, mock_client, mock_response):
        """Test get_nft_market_stats."""
        mock_data = {
            "addresses": 5321,
            "buyers": 3451,
            "sales": 7832,
            "sellers": 3110,
            "volume": 876345
        }
        mock_client.get.return_value = mock_response(200, mock_data)
        api = NftsAPI(mock_client)
        req_obj = {"timeframe": "24h"}
        result = await api.get_nft_market_stats(req_obj)
        assert result.__root__["addresses"] == 5321
        assert result.__root__["volume"] == 876345

        mock_client.get.assert_called_once_with("/nft/market/stats", params=req_obj)

    async def test_get_nft_marketplace_stats(self, mock_client, mock_response):
        """Test get_nft_marketplace_stats."""
        mock_data = [{
            "avg_sale": 100.5,
            "fees": 41210.512,
            "liquidity": 14341.1231,
            "listings": 300,
            "name": "jpg.store",
            "royalties": 645432.3123,
            "sales": 7832,
            "users": 5321,
            "volume": 876345.312
        }]
        mock_client.get.return_value = mock_response(200, mock_data)
        api = NftsAPI(mock_client)
        req_obj = {"timeframe": "7d", "marketplace": "jpg.store"}
        result = await api.get_nft_marketplaces_stats(req_obj)
        assert result.__root__[0].name == "jpg.store"
        assert result.__root__[0].volume == 876345.312

        mock_client.get.assert_called_once_with("/nft/marketplace/stats", params=req_obj)
