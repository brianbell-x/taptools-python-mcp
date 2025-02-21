from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# NFT Asset Sales Models
class NFTAssetSalesRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: Optional[str] = Field(None, description="Name of the NFT")

class NFTSale(BaseModel):
    buyer_stake_address: str = Field(..., description="Stake address of the buyer")
    price: float = Field(..., description="Sale price in ADA")
    seller_stake_address: str = Field(..., description="Stake address of the seller")
    time: int = Field(..., description="Unix timestamp of the sale")

class NFTAssetSalesResponse(BaseModel):
    __root__: List[NFTSale] = Field(..., description="List of NFT sales")

# NFT Asset Stats Models
class NFTAssetStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: str = Field(..., description="Name of the NFT")

class NFTAssetStats(BaseModel):
    is_listed: bool = Field(..., description="Whether the NFT is currently listed")
    last_listed_price: float = Field(..., description="Last listing price in ADA")
    last_listed_time: int = Field(..., description="Unix timestamp of last listing")
    last_sold_price: float = Field(..., description="Last sale price in ADA")
    last_sold_time: int = Field(..., description="Unix timestamp of last sale")
    owners: int = Field(..., description="Number of unique owners")
    sales: int = Field(..., description="Total number of sales")
    times_listed: int = Field(..., description="Number of times listed")
    volume: float = Field(..., description="Total trading volume in ADA")

class NFTAssetStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT asset statistics")

# NFT Asset Traits Models
class NFTAssetTraitsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: str = Field(..., description="Name of the NFT")
    prices: Optional[str] = Field("1", description="Include prices (0 or 1)")

class NFTAssetTraits(BaseModel):
    rank: int = Field(..., description="Rarity rank of the NFT")
    traits: List[Dict] = Field(..., description="List of NFT traits")

class NFTAssetTraitsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT asset traits and rarity information")

# NFT Collection Assets Models
class NFTCollectionAssetsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    sort_by: Optional[str] = Field("price", description="Sort field (e.g. 'price')")
    order: Optional[str] = Field("asc", description="Sort order ('asc' or 'desc')")
    search: Optional[str] = Field(None, description="Search term")
    on_sale: Optional[str] = Field("0", description="Filter for listed NFTs only (0 or 1)")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page, max 100")

class NFTCollectionAsset(BaseModel):
    image: str = Field(..., description="IPFS URL of the NFT image")
    name: str = Field(..., description="Name of the NFT")
    price: float = Field(..., description="Current listing price in ADA")
    rank: int = Field(..., description="Rarity rank")

class NFTCollectionAssetsResponse(BaseModel):
    __root__: List[NFTCollectionAsset] = Field(..., description="List of NFT collection assets")

# NFT Collection Holders Distribution Models
class NFTCollectionHoldersDistributionRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionHoldersDistributionResponse(BaseModel):
    __root__: Dict[str, int] = Field(..., description="Distribution of holders by quantity ranges")

# NFT Collection Top Holders Models
class NFTCollectionTopHoldersRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")
    exclude_exchanges: Optional[int] = Field(None, description="Exclude exchange addresses (0 or 1)")

class NFTCollectionHolder(BaseModel):
    address: str = Field(..., description="Stake address of holder")
    amount: int = Field(..., description="Number of NFTs held")

class NFTCollectionTopHoldersResponse(BaseModel):
    __root__: List[NFTCollectionHolder] = Field(..., description="List of top NFT holders")

# NFT Collection Holders Trended Models
class NFTCollectionHoldersTrendedRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("30d", description="Time frame")

class NFTHolderTrend(BaseModel):
    holders: int = Field(..., description="Number of holders")
    time: int = Field(..., description="Unix timestamp")

class NFTCollectionHoldersTrendedResponse(BaseModel):
    __root__: List[NFTHolderTrend] = Field(..., description="List of holder trend data points")

# NFT Collection Info Models
class NFTCollectionInfoRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionInfo(BaseModel):
    description: str = Field(..., description="Collection description")
    discord: Optional[str] = Field(None, description="Discord server link")
    logo: str = Field(..., description="IPFS URL of collection logo")
    name: str = Field(..., description="Collection name")
    supply: int = Field(..., description="Total supply")
    twitter: Optional[str] = Field(None, description="Twitter profile link")
    website: Optional[str] = Field(None, description="Website URL")

class NFTCollectionInfoResponse(BaseModel):
    __root__: Dict[str, str] = Field(..., description="NFT collection information")

# NFT Collection Listings Models
class NFTCollectionListingsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionListings(BaseModel):
    listings: int = Field(..., description="Number of active listings")
    supply: int = Field(..., description="Total supply")

class NFTCollectionListingsResponse(BaseModel):
    __root__: Dict[str, int] = Field(..., description="NFT collection listings information")

# NFT Collection Listings Depth Models
class NFTCollectionListingsDepthRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    items: Optional[int] = Field(500, description="Number of price points, max 1000")

class ListingDepth(BaseModel):
    avg: float = Field(..., description="Average price at this level")
    count: int = Field(..., description="Number of listings")
    price: float = Field(..., description="Price level in ADA")
    total: float = Field(..., description="Total value in ADA")

class NFTCollectionListingsDepthResponse(BaseModel):
    __root__: List[ListingDepth] = Field(..., description="List of listing depth data points")

# NFT Collection Individual Listings Models
class NFTCollectionIndividualListingsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    sort_by: Optional[str] = Field("price", description="Sort field")
    order: Optional[str] = Field("asc", description="Sort order")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page, max 100")

class NFTListing(BaseModel):
    image: str = Field(..., description="IPFS URL of NFT image")
    market: str = Field(..., description="Marketplace name")
    name: str = Field(..., description="NFT name")
    price: float = Field(..., description="Listing price in ADA")
    time: int = Field(..., description="Unix timestamp of listing")

class NFTCollectionIndividualListingsResponse(BaseModel):
    __root__: List[NFTListing] = Field(..., description="List of individual NFT listings")

# NFT Collection Listings Trended Models
class NFTCollectionListingsTrendedRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class ListingTrend(BaseModel):
    listings: int = Field(..., description="Number of listings")
    price: float = Field(..., description="Floor price")
    time: int = Field(..., description="Unix timestamp")

class NFTCollectionListingsTrendedResponse(BaseModel):
    __root__: List[ListingTrend] = Field(..., description="List of listing trend data points")

# NFT Collection OHLCV Models
class NFTCollectionOHLCVRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class NFTOHLCV(BaseModel):
    close: float = Field(..., description="Closing floor price")
    high: float = Field(..., description="Highest floor price")
    low: float = Field(..., description="Lowest floor price")
    open: float = Field(..., description="Opening floor price")
    time: int = Field(..., description="Unix timestamp")
    volume: float = Field(..., description="Trading volume in ADA")

class NFTCollectionOHLCVResponse(BaseModel):
    __root__: List[NFTOHLCV] = Field(..., description="List of OHLCV data points")

# NFT Collection Stats Models
class NFTCollectionStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionStats(BaseModel):
    listings: int = Field(..., description="Number of active listings")
    owners: int = Field(..., description="Number of unique owners")
    price: float = Field(..., description="Floor price in ADA")
    sales: int = Field(..., description="Total number of sales")
    supply: int = Field(..., description="Total supply")
    top_offer: float = Field(..., description="Highest current offer in ADA")
    volume: float = Field(..., description="Total trading volume in ADA")

class NFTCollectionStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT collection statistics")

# NFT Collection Extended Stats Models
class NFTCollectionExtendedStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("24h", description="Time frame")

class NFTCollectionExtendedStats(BaseModel):
    listings: int = Field(..., description="Number of active listings")
    listings_pct_chg: float = Field(..., description="Percent change in listings")
    owners: int = Field(..., description="Number of unique owners")
    owners_pct_chg: float = Field(..., description="Percent change in owners")
    price: float = Field(..., description="Floor price in ADA")
    price_pct_chg: float = Field(..., description="Percent change in floor price")
    sales: int = Field(..., description="Total number of sales")
    sales_pct_chg: float = Field(..., description="Percent change in sales")
    supply: int = Field(..., description="Total supply")
    top_offer: float = Field(..., description="Highest current offer in ADA")
    volume: float = Field(..., description="Total trading volume in ADA")
    volume_pct_chg: float = Field(..., description="Percent change in volume")

class NFTCollectionExtendedStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT collection extended statistics")

# NFT Collection Trades Models
class NFTCollectionTradesRequest(BaseModel):
    policy: Optional[str] = Field(None, description="Policy ID of the collection")
    timeframe: Optional[str] = Field("30d", description="Time frame")
    sort_by: Optional[str] = Field("time", description="Sort field")
    order: Optional[str] = Field("desc", description="Sort order")
    min_amount: Optional[int] = Field(None, description="Minimum trade amount")
    from_time: Optional[int] = Field(None, description="Filter after UNIX timestamp")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page, max 100")

class NFTTrade(BaseModel):
    buyer_address: str = Field(..., description="Buyer's address")
    collection_name: str = Field(..., description="Collection name")
    hash: str = Field(..., description="Transaction hash")
    image: str = Field(..., description="IPFS URL of NFT image")
    market: str = Field(..., description="Marketplace name")
    name: str = Field(..., description="NFT name")
    policy: str = Field(..., description="Policy ID")
    price: float = Field(..., description="Sale price in ADA")
    seller_address: str = Field(..., description="Seller's address")
    time: int = Field(..., description="Unix timestamp")

class NFTCollectionTradesResponse(BaseModel):
    __root__: List[NFTTrade] = Field(..., description="List of NFT trades")

# NFT Collection Trade Stats Models
class NFTCollectionTradeStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("24h", description="Time frame")

class NFTCollectionTradeStats(BaseModel):
    buyers: int = Field(..., description="Number of unique buyers")
    sales: int = Field(..., description="Number of sales")
    sellers: int = Field(..., description="Number of unique sellers")
    volume: float = Field(..., description="Trading volume in ADA")

class NFTCollectionTradeStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT collection trade statistics")

# NFT Collection Trait Prices Models
class NFTCollectionTraitPricesRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    name: Optional[str] = Field(None, description="Trait name")

class NFTCollectionTraitPricesResponse(BaseModel):
    traits: Dict[str, Dict[str, float]] = Field(..., description="Trait categories and their floor prices")

# NFT Collection Trait Rarity Models
class NFTCollectionTraitRarityRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionTraitRarityResponse(BaseModel):
    traits: Dict[str, Dict[str, float]] = Field(..., description="Trait categories and their rarity scores")

# NFT Collection Trait Rarity Rank Models
class NFTCollectionTraitRarityRankRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    name: str = Field(..., description="NFT name")

class NFTCollectionTraitRarityRankResponse(BaseModel):
    rank: int = Field(..., description="Rarity rank of the NFT")

# NFT Collection Volume Trended Models
class NFTCollectionVolumeTrendedRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class VolumeTrend(BaseModel):
    price: float = Field(..., description="Floor price")
    sales: int = Field(..., description="Number of sales")
    time: int = Field(..., description="Unix timestamp")
    volume: float = Field(..., description="Trading volume")

class NFTCollectionVolumeTrendedResponse(BaseModel):
    __root__: List[VolumeTrend] = Field(..., description="List of volume trend data points")

# NFT Market Stats Models
class NFTMarketStatsRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame")

class NFTMarketStats(BaseModel):
    addresses: int = Field(..., description="Number of unique addresses")
    buyers: int = Field(..., description="Number of unique buyers")
    sales: int = Field(..., description="Number of sales")
    sellers: int = Field(..., description="Number of unique sellers")
    volume: float = Field(..., description="Trading volume in ADA")

class NFTMarketStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT market statistics")

# NFT Market Extended Stats Models
class NFTMarketExtendedStatsRequest(BaseModel):
    timeframe: str = Field(..., description="Time frame")

class NFTMarketExtendedStats(BaseModel):
    addresses: int = Field(..., description="Number of unique addresses")
    addresses_pct_chg: float = Field(..., description="Percent change in addresses")
    buyers: int = Field(..., description="Number of unique buyers")
    buyers_pct_chg: float = Field(..., description="Percent change in buyers")
    sales: int = Field(..., description="Number of sales")
    sales_pct_chg: float = Field(..., description="Percent change in sales")
    sellers: int = Field(..., description="Number of unique sellers")
    sellers_pct_chg: float = Field(..., description="Percent change in sellers")
    volume: float = Field(..., description="Trading volume in ADA")
    volume_pct_chg: float = Field(..., description="Percent change in volume")

class NFTMarketExtendedStatsResponse(BaseModel):
    __root__: Dict[str, float] = Field(..., description="NFT market extended statistics")

# NFT Market Volume Trended Models
class NFTMarketVolumeTrendedRequest(BaseModel):
    timeframe: Optional[str] = Field("30d", description="Time frame")

class MarketVolumeTrend(BaseModel):
    time: int = Field(..., description="Unix timestamp")
    value: float = Field(..., description="Volume value")

class NFTMarketVolumeTrendedResponse(BaseModel):
    __root__: List[MarketVolumeTrend] = Field(..., description="List of market volume trend data points")

# NFT Marketplace Stats Models
class NFTMarketplaceStatsRequest(BaseModel):
    timeframe: Optional[str] = Field("7d", description="Time frame")
    marketplace: Optional[str] = Field(None, description="Marketplace name")
    last_day: Optional[int] = Field(None, description="Filter by yesterday's data (0 or 1)")

class NFTMarketplaceStats(BaseModel):
    avg_sale: float = Field(..., description="Average sale price")
    fees: float = Field(..., description="Total fees collected")
    liquidity: float = Field(..., description="Total liquidity")
    listings: int = Field(..., description="Number of listings")
    name: str = Field(..., description="Marketplace name")
    royalties: float = Field(..., description="Total royalties paid")
    sales: int = Field(..., description="Number of sales")
    users: int = Field(..., description="Number of unique users")
    volume: float = Field(..., description="Trading volume")

class NFTMarketplaceStatsResponse(BaseModel):
    __root__: List[NFTMarketplaceStats] = Field(..., description="List of marketplace statistics")

# NFT Top Rankings Models
class NFTTopTimeframeRequest(BaseModel):
    ranking: str = Field(..., description="Ranking type: marketCap, volume, gainers, or losers")
    items: Optional[int] = Field(25, description="Number of items, max 100")

class NFTTopRanking(BaseModel):
    listings: int = Field(..., description="Number of listings")
    logo: str = Field(..., description="Logo URL")
    market_cap: float = Field(..., description="Market cap in ADA")
    name: str = Field(..., description="Collection name")
    policy: str = Field(..., description="Policy ID")
    price: float = Field(..., description="Floor price")
    price_24h_chg: float = Field(..., description="24h price change")
    price_30d_chg: float = Field(..., description="30d price change")
    price_7d_chg: float = Field(..., description="7d price change")
    rank: int = Field(..., description="Ranking position")
    supply: int = Field(..., description="Total supply")
    volume_24h: float = Field(..., description="24h volume")
    volume_24h_chg: float = Field(..., description="24h volume change")
    volume_30d: float = Field(..., description="30d volume")
    volume_30d_chg: float = Field(..., description="30d volume change")
    volume_7d: float = Field(..., description="7d volume")
    volume_7d_chg: float = Field(..., description="7d volume change")

class NFTTopTimeframeResponse(BaseModel):
    __root__: List[NFTTopRanking] = Field(..., description="List of top NFT rankings")

# NFT Top Volume Models
class NFTTopVolumeRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")

class NFTTopVolume(BaseModel):
    listings: int = Field(..., description="Number of listings")
    logo: str = Field(..., description="Logo URL")
    name: str = Field(..., description="Collection name")
    policy: str = Field(..., description="Policy ID")
    price: float = Field(..., description="Floor price")
    sales: int = Field(..., description="Number of sales")
    supply: int = Field(..., description="Total supply")
    volume: float = Field(..., description="Trading volume")

class NFTTopVolumeResponse(BaseModel):
    __root__: List[NFTTopVolume] = Field(..., description="List of top NFT volumes")

# NFT Top Volume Extended Models
class NFTTopVolumeExtendedRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")

class NFTTopVolumeExtended(BaseModel):
    listings: int = Field(..., description="Number of listings")
    listings_pct_chg: float = Field(..., description="Percent change in listings")
    logo: str = Field(..., description="Logo URL")
    name: str = Field(..., description="Collection name")
    owners: int = Field(..., description="Number of owners")
    owners_pct_chg: float = Field(..., description="Percent change in owners")
    policy: str = Field(..., description="Policy ID")
    price: float = Field(..., description="Floor price")
    price_pct_chg: float = Field(..., description="Percent change in price")
    sales: int = Field(..., description="Number of sales")
    sales_pct_chg: float = Field(..., description="Percent change in sales")
    supply: int = Field(..., description="Total supply")
    volume: float = Field(..., description="Trading volume")
    volume_pct_chg: float = Field(..., description="Percent change in volume")

class NFTTopVolumeExtendedResponse(BaseModel):
    __root__: List[NFTTopVolumeExtended] = Field(..., description="List of extended top NFT volumes")
