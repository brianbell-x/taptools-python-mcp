"""
NftsAPI for NFT-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

from ..models.nfts import (
    NFTAssetSalesRequest, NFTAssetSalesResponse,
    NFTAssetStatsRequest, NFTAssetStatsResponse,
    NFTAssetTraitsRequest, NFTAssetTraitsResponse,
    NFTCollectionAssetsRequest, NFTCollectionAssetsResponse,
    NFTCollectionInfoRequest, NFTCollectionInfoResponse,
    NFTCollectionStatsRequest, NFTCollectionStatsResponse,
    NFTCollectionExtendedStatsRequest, NFTCollectionExtendedStatsResponse,
    NFTCollectionHoldersDistributionRequest, NFTCollectionHoldersDistributionResponse,
    NFTCollectionTopHoldersRequest, NFTCollectionTopHoldersResponse,
    NFTCollectionHoldersTrendedRequest, NFTCollectionHoldersTrendedResponse,
    NFTCollectionListingsRequest, NFTCollectionListingsResponse,
    NFTCollectionListingsDepthRequest, NFTCollectionListingsDepthResponse,
    NFTCollectionIndividualListingsRequest, NFTCollectionIndividualListingsResponse,
    NFTCollectionListingsTrendedRequest, NFTCollectionListingsTrendedResponse,
    NFTCollectionOHLCVRequest, NFTCollectionOHLCVResponse,
    NFTCollectionTradesRequest, NFTCollectionTradesResponse,
    NFTCollectionTradeStatsRequest, NFTCollectionTradeStatsResponse,
    NFTCollectionVolumeTrendedRequest, NFTCollectionVolumeTrendedResponse,
    NFTCollectionTraitPricesRequest, NFTCollectionTraitPricesResponse,
    NFTCollectionTraitRarityRequest, NFTCollectionTraitRarityResponse,
    NFTCollectionTraitRarityRankRequest, NFTCollectionTraitRarityRankResponse,
    NFTMarketStatsRequest, NFTMarketStatsResponse,
    NFTMarketExtendedStatsRequest, NFTMarketExtendedStatsResponse,
    NFTMarketVolumeTrendedRequest, NFTMarketVolumeTrendedResponse,
    NFTMarketplaceStatsRequest, NFTMarketplaceStatsResponse,
    NFTTopTimeframeRequest, NFTTopTimeframeResponse,
    NFTTopVolumeRequest, NFTTopVolumeResponse,
    NFTTopVolumeExtendedRequest, NFTTopVolumeExtendedResponse
)
from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class NftsAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request with error handling.
        
        Args:
            method: HTTP method (get, post, etc.)
            url: API endpoint URL
            **kwargs: Additional arguments for the request
            
        Returns:
            API response as dictionary
            
        Raises:
            TapToolsError: For any API or connection errors
        """
        try:
            response = await getattr(self.client, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in request to {url}: {str(e)}")
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            logger.error(f"Connection error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )
        except Exception as e:
            logger.error(f"Unexpected error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Unexpected error: {str(e)}",
                error_type=ErrorType.UNKNOWN
            )

    async def get_nft_asset_sales(self, request: NFTAssetSalesRequest) -> NFTAssetSalesResponse:
        """
        GET /nft/asset/sales
        
        Get sale history of a specific NFT.
        """
        url = "/nft/asset/sales"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTAssetSalesResponse(__root__=response_data)

    async def get_nft_asset_stats(self, request: NFTAssetStatsRequest) -> NFTAssetStatsResponse:
        """
        GET /nft/asset/stats
        
        Get high-level stats on a specific NFT asset.
        """
        url = "/nft/asset/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTAssetStatsResponse(__root__=response_data)

    async def get_nft_asset_traits(self, request: NFTAssetTraitsRequest) -> NFTAssetTraitsResponse:
        """
        GET /nft/asset/traits
        
        Get trait data and prices for a specific NFT.
        """
        url = "/nft/asset/traits"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTAssetTraitsResponse(__root__=response_data)

    async def get_nft_collection_assets(self, request: NFTCollectionAssetsRequest) -> NFTCollectionAssetsResponse:
        """
        GET /nft/collection/assets
        
        Get list of NFTs in a collection. Sort/filter by price, rank, traits, etc.
        """
        url = "/nft/collection/assets"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionAssetsResponse(__root__=response_data)

    async def get_nft_collection_info(self, request: NFTCollectionInfoRequest) -> NFTCollectionInfoResponse:
        """
        GET /nft/collection/info
        
        Get basic collection info (name, socials, logo).
        """
        url = "/nft/collection/info"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionInfoResponse(__root__=response_data)

    async def get_nft_collection_stats(self, request: NFTCollectionStatsRequest) -> NFTCollectionStatsResponse:
        """
        GET /nft/collection/stats

        Get collection stats (floor, volume, supply).
        """
        url = "/nft/collection/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionStatsResponse(__root__=response_data)

    async def get_nft_collection_stats_extended(self, request: NFTCollectionExtendedStatsRequest) -> NFTCollectionExtendedStatsResponse:
        """
        GET /nft/collection/stats/extended
        
        Get extended stats with % changes (from timeframe).
        """
        url = "/nft/collection/stats/extended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionExtendedStatsResponse(__root__=response_data)

    async def get_nft_collection_holders_distribution(self, request: NFTCollectionHoldersDistributionRequest) -> NFTCollectionHoldersDistributionResponse:
        """
        GET /nft/collection/holders/distribution
        
        Get distribution of NFTs in a collection by quantity held.
        """
        url = "/nft/collection/holders/distribution"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionHoldersDistributionResponse(__root__=response_data)

    async def get_nft_collection_holders_top(self, request: NFTCollectionTopHoldersRequest) -> NFTCollectionTopHoldersResponse:
        """
        GET /nft/collection/holders/top
        
        Get top holders of a collection.
        """
        url = "/nft/collection/holders/top"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTopHoldersResponse(__root__=response_data)

    async def get_nft_collection_holder_counts(self, request: NFTCollectionHoldersTrendedRequest) -> NFTCollectionHoldersTrendedResponse:
        """
        GET /nft/collection/holders/trended
        
        Get trended holder counts by day.
        """
        url = "/nft/collection/holders/trended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionHoldersTrendedResponse(__root__=response_data)

    async def get_nft_collection_listings(self, request: NFTCollectionListingsRequest) -> NFTCollectionListingsResponse:
        """
        GET /nft/collection/listings
        
        Get active listings + total supply for a collection.
        """
        url = "/nft/collection/listings"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionListingsResponse(__root__=response_data)

    async def get_nft_collection_listings_depth(self, request: NFTCollectionListingsDepthRequest) -> NFTCollectionListingsDepthResponse:
        """
        GET /nft/collection/listings/depth
        
        Get cumulative listing data at various price points.
        """
        url = "/nft/collection/listings/depth"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionListingsDepthResponse(__root__=response_data)

    async def get_nft_collection_listings_individual(self, request: NFTCollectionIndividualListingsRequest) -> NFTCollectionIndividualListingsResponse:
        """
        GET /nft/collection/listings/individual
        
        Get active listings with optional pagination/sorting.
        """
        url = "/nft/collection/listings/individual"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionIndividualListingsResponse(__root__=response_data)

    async def get_nft_collection_listing_counts(self, request: NFTCollectionListingsTrendedRequest) -> NFTCollectionListingsTrendedResponse:
        """
        GET /nft/collection/listings/trended
        
        Get trended number of listings + floor price.
        """
        url = "/nft/collection/listings/trended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionListingsTrendedResponse(__root__=response_data)

    async def get_nft_collection_ohlcv(self, request: NFTCollectionOHLCVRequest) -> NFTCollectionOHLCVResponse:
        """
        GET /nft/collection/ohlcv
        
        Get floor price OHLCV for a collection.
        """
        url = "/nft/collection/ohlcv"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionOHLCVResponse(__root__=response_data)

    async def get_nft_collection_trades(self, request: NFTCollectionTradesRequest) -> NFTCollectionTradesResponse:
        """
        GET /nft/collection/trades
        
        Get trades for a specific collection or entire NFT market.
        """
        url = "/nft/collection/trades"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTradesResponse(__root__=response_data)

    async def get_nft_collection_trades_stats(self, request: NFTCollectionTradeStatsRequest) -> NFTCollectionTradeStatsResponse:
        """
        GET /nft/collection/trades/stats
        
        Get volume + sales stats over timeframe.
        """
        url = "/nft/collection/trades/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTradeStatsResponse(__root__=response_data)

    async def get_nft_collection_volume_and_sales(self, request: NFTCollectionVolumeTrendedRequest) -> NFTCollectionVolumeTrendedResponse:
        """
        GET /nft/collection/volume/trended
        
        Get volume and sales trends for a collection.
        """
        url = "/nft/collection/volume/trended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionVolumeTrendedResponse(__root__=response_data)

    async def get_nft_collection_traits_price(self, request: NFTCollectionTraitPricesRequest) -> NFTCollectionTraitPricesResponse:
        """
        GET /nft/collection/traits/price
        
        Get traits within a collection + each trait's floor price.
        """
        url = "/nft/collection/traits/price"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTraitPricesResponse(**response_data)

    async def get_nft_collection_traits_rarity(self, request: NFTCollectionTraitRarityRequest) -> NFTCollectionTraitRarityResponse:
        """
        GET /nft/collection/traits/rarity
        
        Get metadata attributes + occurrence likelihood.
        """
        url = "/nft/collection/traits/rarity"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTraitRarityResponse(**response_data)

    async def get_nft_collection_traits_rarity_rank(self, request: NFTCollectionTraitRarityRankRequest) -> NFTCollectionTraitRarityRankResponse:
        """
        GET /nft/collection/traits/rarity/rank
        
        Get a specific NFT's rarity rank.
        """
        url = "/nft/collection/traits/rarity/rank"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTCollectionTraitRarityRankResponse(**response_data)

    async def get_nft_market_stats(self, request: NFTMarketStatsRequest) -> NFTMarketStatsResponse:
        """
        GET /nft/market/stats
        
        Get top-level NFT market stats (addresses, sales, volume).
        """
        url = "/nft/market/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTMarketStatsResponse(__root__=response_data)

    async def get_nft_market_stats_extended(self, request: NFTMarketExtendedStatsRequest) -> NFTMarketExtendedStatsResponse:
        """
        GET /nft/market/stats/extended
        
        Get NFT market stats + percentage changes.
        """
        url = "/nft/market/stats/extended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTMarketExtendedStatsResponse(__root__=response_data)

    async def get_nft_market_volume_and_sales(self, request: NFTMarketVolumeTrendedRequest) -> NFTMarketVolumeTrendedResponse:
        """
        GET /nft/market/volume/trended
        
        Get overall NFT market volume trends.
        """
        url = "/nft/market/volume/trended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTMarketVolumeTrendedResponse(__root__=response_data)

    async def get_nft_marketplaces_stats(self, request: NFTMarketplaceStatsRequest) -> NFTMarketplaceStatsResponse:
        """
        GET /nft/marketplace/stats
        
        Get marketplace stats (fees, listings, volumes) for an NFT marketplace.
        """
        url = "/nft/marketplace/stats"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTMarketplaceStatsResponse(__root__=response_data)

    async def get_nft_top_rankings(self, request: NFTTopTimeframeRequest) -> NFTTopTimeframeResponse:
        """
        GET /nft/top/timeframe
        
        Get top NFT rankings by market cap, 24h volume, or top gainers/losers.
        """
        url = "/nft/top/timeframe"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTTopTimeframeResponse(__root__=response_data)

    async def get_nft_top_collections_by_volume(self, request: NFTTopVolumeRequest) -> NFTTopVolumeResponse:
        """
        GET /nft/top/volume
        
        Get top NFT collections by trading volume over a timeframe.
        """
        url = "/nft/top/volume"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTTopVolumeResponse(__root__=response_data)

    async def get_nft_top_collections_by_volume_with_changes(self, request: NFTTopVolumeExtendedRequest) -> NFTTopVolumeExtendedResponse:
        """
        GET /nft/top/volume/extended
        
        Get top NFT collections by volume with % changes.
        """
        url = "/nft/top/volume/extended"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return NFTTopVolumeExtendedResponse(__root__=response_data)
