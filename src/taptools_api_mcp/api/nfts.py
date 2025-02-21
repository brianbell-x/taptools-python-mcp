"""
NftsAPI for NFT-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

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

    async def get_nft_asset_sales(self, policy: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        GET /nft/asset/sales
        
        Get sale history of a specific NFT.
        """
        url = "/nft/asset/sales"
        params = {"policy": policy}
        if name:
            params["name"] = name
        return await self._make_request("get", url, params=params)

    async def get_nft_asset_stats(self, policy: str, name: str) -> Dict[str, Any]:
        """
        GET /nft/asset/stats
        
        Get high-level stats on a specific NFT asset.
        """
        url = "/nft/asset/stats"
        params = {"policy": policy, "name": name}
        return await self._make_request("get", url, params=params)

    async def get_nft_asset_traits(self, policy: str, name: str, prices: str = "1") -> Dict[str, Any]:
        """
        GET /nft/asset/traits
        
        Get trait data and prices for a specific NFT.
        """
        url = "/nft/asset/traits"
        params = {"policy": policy, "name": name, "prices": prices}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_assets(
        self, 
        policy: str, 
        sort_by: str = "price", 
        order: str = "asc", 
        search: str = "", 
        on_sale: str = "0", 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/assets
        
        Get list of NFTs in a collection. Sort/filter by price, rank, traits, etc.
        """
        url = "/nft/collection/assets"
        params = {
            "policy": policy,
            "sortBy": sort_by,
            "order": order,
            "search": search,
            "onSale": on_sale,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_info(self, policy: str) -> Dict[str, Any]:
        """
        GET /nft/collection/info
        
        Get basic collection info (name, socials, logo).
        """
        url = "/nft/collection/info"
        params = {"policy": policy}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_stats(self, policy: str) -> Dict[str, Any]:
        """
        GET /nft/collection/stats

        Get collection stats (floor, volume, supply).
        """
        url = "/nft/collection/stats"
        params = {"policy": policy}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_stats_extended(self, policy: str, timeframe: str = "24h") -> Dict[str, Any]:
        """
        GET /nft/collection/stats/extended
        
        Get extended stats with % changes (from timeframe).
        """
        url = "/nft/collection/stats/extended"
        params = {"policy": policy, "timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_holders_distribution(self, policy: str) -> Dict[str, Any]:
        """
        GET /nft/collection/holders/distribution
        
        Get distribution of NFTs in a collection by quantity held.
        """
        url = "/nft/collection/holders/distribution"
        params = {"policy": policy}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_holders_top(
        self, 
        policy: str, 
        page: int = 1, 
        per_page: int = 10, 
        exclude_exchanges: int = 0
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/holders/top
        
        Get top holders of a collection.
        """
        url = "/nft/collection/holders/top"
        params = {
            "policy": policy,
            "page": page,
            "perPage": per_page,
            "excludeExchanges": exclude_exchanges
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_holders_trended(self, policy: str, timeframe: str = "30d") -> Dict[str, Any]:
        """
        GET /nft/collection/holders/trended
        
        Get trended holder counts by day.
        """
        url = "/nft/collection/holders/trended"
        params = {"policy": policy, "timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_listings(self, policy: str) -> Dict[str, Any]:
        """
        GET /nft/collection/listings
        
        Get active listings + total supply for a collection.
        """
        url = "/nft/collection/listings"
        params = {"policy": policy}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_listings_depth(self, policy: str, items: int = 500) -> Dict[str, Any]:
        """
        GET /nft/collection/listings/depth
        
        Get cumulative listing data at various price points.
        """
        url = "/nft/collection/listings/depth"
        params = {"policy": policy, "items": items}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_listings_individual(
        self, 
        policy: str, 
        sort_by: str = "price", 
        order: str = "asc", 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/listings/individual
        
        Get active listings with optional pagination/sorting.
        """
        url = "/nft/collection/listings/individual"
        params = {
            "policy": policy,
            "sortBy": sort_by,
            "order": order,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_listings_trended(
        self, 
        policy: str, 
        interval: str, 
        num_intervals: int
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/listings/trended
        
        Get trended number of listings + floor price.
        """
        url = "/nft/collection/listings/trended"
        params = {
            "policy": policy,
            "interval": interval,
            "numIntervals": num_intervals
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_ohlcv(
        self, 
        policy: str, 
        interval: str, 
        num_intervals: int
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/ohlcv
        
        Get floor price OHLCV for a collection.
        """
        url = "/nft/collection/ohlcv"
        params = {
            "policy": policy,
            "interval": interval,
            "numIntervals": num_intervals
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_trades(
        self, 
        policy: Optional[str] = None, 
        timeframe: str = "30d", 
        sort_by: str = "time", 
        order: str = "desc", 
        min_amount: Optional[int] = None, 
        from_ts: Optional[int] = None, 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/trades
        
        Get trades for a specific collection or entire NFT market.
        """
        url = "/nft/collection/trades"
        params = {
            "timeframe": timeframe,
            "sortBy": sort_by,
            "order": order,
            "page": page,
            "perPage": per_page
        }
        if policy:
            params["policy"] = policy
        if min_amount:
            params["minAmount"] = min_amount
        if from_ts:
            params["from"] = from_ts
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_trades_stats(
        self, 
        policy: str, 
        timeframe: str = "24h"
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/trades/stats
        
        Get volume + sales stats over timeframe.
        """
        url = "/nft/collection/trades/stats"
        params = {"policy": policy, "timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_volume_trended(
        self, 
        policy: str, 
        interval: str, 
        num_intervals: int
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/volume/trended
        
        Get volume and sales trends for a collection.
        """
        url = "/nft/collection/volume/trended"
        params = {
            "policy": policy,
            "interval": interval,
            "numIntervals": num_intervals
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_traits_price(
        self, 
        policy: str, 
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/traits/price
        
        Get traits within a collection + each trait's floor price.
        """
        url = "/nft/collection/traits/price"
        params = {"policy": policy}
        if name:
            params["name"] = name
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_traits_rarity(self, policy: str) -> Dict[str, Any]:
        """
        GET /nft/collection/traits/rarity
        
        Get metadata attributes + occurrence likelihood.
        """
        url = "/nft/collection/traits/rarity"
        params = {"policy": policy}
        return await self._make_request("get", url, params=params)

    async def get_nft_collection_traits_rarity_rank(
        self, 
        policy: str, 
        name: str
    ) -> Dict[str, Any]:
        """
        GET /nft/collection/traits/rarity/rank
        
        Get a specific NFT's rarity rank.
        """
        url = "/nft/collection/traits/rarity/rank"
        params = {"policy": policy, "name": name}
        return await self._make_request("get", url, params=params)

    async def get_nft_market_stats(self, timeframe: str) -> Dict[str, Any]:
        """
        GET /nft/market/stats
        
        Get top-level NFT market stats (addresses, sales, volume).
        """
        url = "/nft/market/stats"
        params = {"timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_market_stats_extended(self, timeframe: str) -> Dict[str, Any]:
        """
        GET /nft/market/stats/extended
        
        Get NFT market stats + percentage changes.
        """
        url = "/nft/market/stats/extended"
        params = {"timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_market_volume_trended(
        self, 
        timeframe: str = "30d"
    ) -> Dict[str, Any]:
        """
        GET /nft/market/volume/trended
        
        Get overall NFT market volume trends.
        """
        url = "/nft/market/volume/trended"
        params = {"timeframe": timeframe}
        return await self._make_request("get", url, params=params)

    async def get_nft_marketplace_stats(
        self, 
        timeframe: str = "7d", 
        marketplace: str = "", 
        last_day: int = 0
    ) -> Dict[str, Any]:
        """
        GET /nft/marketplace/stats
        
        Get marketplace stats (fees, listings, volumes) for an NFT marketplace.
        """
        url = "/nft/marketplace/stats"
        params = {
            "timeframe": timeframe,
            "marketplace": marketplace,
            "lastDay": last_day
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_top_timeframe(
        self, 
        ranking: str, 
        items: int = 25
    ) -> Dict[str, Any]:
        """
        GET /nft/top/timeframe
        
        Get top NFT rankings by market cap, 24h volume, or top gainers/losers.
        """
        url = "/nft/top/timeframe"
        params = {"ranking": ranking, "items": items}
        return await self._make_request("get", url, params=params)

    async def get_nft_top_volume(
        self, 
        timeframe: str = "24h", 
        page: int = 1, 
        per_page: int = 10
    ) -> Dict[str, Any]:
        """
        GET /nft/top/volume
        
        Get top NFT collections by trading volume over a timeframe.
        """
        url = "/nft/top/volume"
        params = {
            "timeframe": timeframe,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)

    async def get_nft_top_volume_extended(
        self, 
        timeframe: str = "24h", 
        page: int = 1, 
        per_page: int = 10
    ) -> Dict[str, Any]:
        """
        GET /nft/top/volume/extended
        
        Get top NFT collections by volume with % changes.
        """
        url = "/nft/top/volume/extended"
        params = {
            "timeframe": timeframe,
            "page": page,
            "perPage": per_page
        }
        return await self._make_request("get", url, params=params)
