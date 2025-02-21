from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# NFT Asset Sales Models
class NFTAssetSalesRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: Optional[str] = Field(None, description="Name of the NFT")

class NFTSale(BaseModel):
    buyerStakeAddress: str = Field(..., description="Stake address of the buyer", example="stake1address2")
    price: float = Field(..., description="Sale price in ADA", example=8000)
    sellerStakeAddress: str = Field(..., description="Stake address of the seller", example="stake1address1")
    time: int = Field(..., description="Unix timestamp of the sale", example=16000840)

class NFTAssetSalesResponse(BaseModel):
    __root__: List[NFTSale] = Field(..., description="NFT Sales.", example=[{
        "buyerStakeAddress": "stake1address2",
        "price": 8000,
        "sellerStakeAddress": "stake1address1",
        "time": 16000840
    }])

# NFT Asset Stats Models
class NFTAssetStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: str = Field(..., description="Name of the NFT")

class NFTAssetStats(BaseModel):
    isListed: bool = Field(..., description="Whether the NFT is currently listed", example=True)
    lastListedPrice: float = Field(..., description="Last listing price in ADA", example=3850)
    lastListedTime: int = Field(..., description="Unix timestamp of last listing", example=160002490)
    lastSoldPrice: float = Field(..., description="Last sale price in ADA", example=4800)
    lastSoldTime: int = Field(..., description="Unix timestamp of last sale", example=160008490)
    owners: int = Field(..., description="Number of unique owners", example=6)
    sales: int = Field(..., description="Total number of sales", example=5)
    timesListed: int = Field(..., description="Number of times listed", example=8)
    volume: float = Field(..., description="Total trading volume in ADA", example=54234)

class NFTAssetStatsResponse(BaseModel):
    isListed: bool = Field(..., description="Whether the NFT is currently listed", example=True)
    lastListedPrice: float = Field(..., description="Last listing price in ADA", example=3850)
    lastListedTime: int = Field(..., description="Unix timestamp of last listing", example=160002490)
    lastSoldPrice: float = Field(..., description="Last sale price in ADA", example=4800)
    lastSoldTime: int = Field(..., description="Unix timestamp of last sale", example=160008490)
    owners: int = Field(..., description="Number of unique owners", example=6)
    sales: int = Field(..., description="Total number of sales", example=5)
    timesListed: int = Field(..., description="Number of times listed", example=8)
    volume: float = Field(..., description="Total trading volume in ADA", example=54234)

# NFT Asset Traits Models
class NFTAssetTraitsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the NFT")
    name: str = Field(..., description="Name of the NFT")
    prices: Optional[str] = Field("1", description="Include prices (0 or 1)")

class NFTTrait(BaseModel):
    category: str = Field(..., description="Trait category", example="background")
    name: str = Field(..., description="Trait name", example="red")
    rarity: float = Field(..., description="Trait rarity score", example=0.4)
    price: float = Field(..., description="Trait floor price", example=100)

class NFTAssetTraits(BaseModel):
    rank: int = Field(..., description="Rarity rank of the NFT", example=51)
    traits: List[NFTTrait] = Field(..., description="List of NFT traits")

class NFTAssetTraitsResponse(BaseModel):
    rank: int = Field(..., description="Rarity rank", example=51)
    traits: List[NFTTrait] = Field(..., description="Traits info")

# NFT Collection Assets Models
class NFTCollectionAssetsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    sortBy: Optional[str] = Field("price", description="Sort field (e.g. 'price')")
    order: Optional[str] = Field("asc", description="Sort order ('asc' or 'desc')")
    search: Optional[str] = Field(None, description="Search term")
    onSale: Optional[str] = Field("0", description="Filter for listed NFTs only (0 or 1)")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class NFTCollectionAsset(BaseModel):
    image: str = Field(..., description="IPFS URL of the NFT image", example="ipfs://QmeDi3J1exQYnGAuwZv7b6sAuDBAo2hYdAMM1KGgS7KFa4")
    name: str = Field(..., description="Name of the NFT", example="ClayNation3725")
    price: float = Field(..., description="Current listing price in ADA", example=20)
    rank: int = Field(..., description="Rarity rank", example=2)

class NFTCollectionAssetsResponse(BaseModel):
    __root__: List[NFTCollectionAsset] = Field(..., description="Collection assets.", example=[{
        "name": "ClayNation3725",
        "rank": 2,
        "price": 20,
        "image": "ipfs://QmeDi3J1exQYnGAuwZv7b6sAuDBAo2hYdAMM1KGgS7KFa4"
    }])

# NFT Collection Holders Distribution Models
class NFTCollectionHoldersDistributionRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionHoldersDistributionResponse(BaseModel):
    __root__: Dict[str, int] = Field(..., description="Distribution of holders by quantity ranges", example={
        "1": 1154,
        "2-4": 631,
        "5-9": 327,
        "10-24": 60,
        "25+": 2
    })

# NFT Collection Top Holders Models
class NFTCollectionTopHoldersRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")
    exclude_exchanges: Optional[int] = Field(None, description="Exclude exchange addresses (0 or 1)")

class NFTCollectionHolder(BaseModel):
    address: str = Field(..., description="Stake address of holder", example="stake1u8mvwfn298a4dkm92hrgeupnnuzhxfwl5lauzuejl5cf8esrtjn6w")
    amount: int = Field(..., description="Number of NFTs held", example=27)

class NFTCollectionTopHoldersResponse(BaseModel):
    __root__: List[NFTCollectionHolder] = Field(..., description="Top collection holders", example=[{
        "address": "stake1u8mvwfn298a4dkm92hrgeupnnuzhxfwl5lauzuejl5cf8esrtjn6w",
        "amount": 27
    }])

# NFT Collection Holders Trended Models
class NFTCollectionHoldersTrendedRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("30d", description="Time frame")

class NFTHolderTrend(BaseModel):
    holders: int = Field(..., description="Number of holders", example=3125)
    time: int = Field(..., description="Unix timestamp", example=1705874400)

class NFTCollectionHoldersTrendedResponse(BaseModel):
    __root__: List[NFTHolderTrend] = Field(..., description="Trended collection holders", example=[{
        "time": 1705874400,
        "holders": 3125
    }])

# NFT Collection Info Models
class NFTCollectionInfoRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionInfo(BaseModel):
    description: str = Field(..., description="Collection description", example="The Ape Society is a collection of 7,000 NFTs generated on the Cardano blockchain.")
    discord: str = Field(..., description="Discord server link", example="https://discord.gg/theapesociety")
    logo: str = Field(..., description="IPFS URL of collection logo", example="ipfs://QmVT8QGerKMLaJkxdUqefw7V7fjccGgcKjLnbMavisELsf")
    name: str = Field(..., description="Collection name", example="The Ape Society")
    supply: int = Field(..., description="Total supply", example=10000)
    twitter: str = Field(..., description="Twitter profile link", example="https://twitter.com/the_ape_society")
    website: str = Field(..., description="Website URL", example="https://www.theapesociety.io/")

class NFTCollectionInfoResponse(BaseModel):
    description: str = Field(..., description="Collection description", example="The Ape Society is a collection of 7,000 NFTs generated on the Cardano blockchain.")
    discord: str = Field(..., description="Discord server link", example="https://discord.gg/theapesociety")
    logo: str = Field(..., description="IPFS URL of collection logo", example="ipfs://QmVT8QGerKMLaJkxdUqefw7V7fjccGgcKjLnbMavisELsf")
    name: str = Field(..., description="Collection name", example="The Ape Society")
    supply: int = Field(..., description="Total supply", example=10000)
    twitter: str = Field(..., description="Twitter profile link", example="https://twitter.com/the_ape_society")
    website: str = Field(..., description="Website URL", example="https://www.theapesociety.io/")

# NFT Collection Listings Models
class NFTCollectionListingsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionListings(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=168)
    supply: int = Field(..., description="Total supply", example=1000)

class NFTCollectionListingsResponse(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=168)
    supply: int = Field(..., description="Total supply", example=1000)

# NFT Collection Listings Depth Models
class NFTCollectionListingsDepthRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    items: Optional[int] = Field(500, description="Number of price points, max 1000")

class ListingDepth(BaseModel):
    avg: float = Field(..., description="Average price at this level", example=4850)
    count: int = Field(..., description="Number of listings", example=96)
    price: float = Field(..., description="Price level in ADA", example=9600)
    total: float = Field(..., description="Total value in ADA", example=456000)

class NFTCollectionListingsDepthResponse(BaseModel):
    __root__: List[ListingDepth] = Field(..., description="Listings depth", example=[{
        "count": 96,
        "price": 9600,
        "avg": 4850,
        "total": 456000
    }])

# NFT Collection Individual Listings Models
class NFTCollectionIndividualListingsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    sort_by: Optional[str] = Field("price", description="Sort field")
    order: Optional[str] = Field("asc", description="Sort order")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page, max 100")

class NFTListing(BaseModel):
    image: str = Field(..., description="IPFS URL of NFT image", example="ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM")
    market: str = Field(..., description="Marketplace name", example="jpg.store")
    name: str = Field(..., description="NFT name", example="ClayNation3725")
    price: float = Field(..., description="Listing price in ADA", example=4925)
    time: int = Field(..., description="Unix timestamp of listing", example=1680135943)

class NFTCollectionIndividualListingsResponse(BaseModel):
    __root__: List[NFTListing] = Field(..., description="Information about listing", example=[{
        "name": "ClayNation3725",
        "image": "ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM",
        "price": 4925,
        "time": 1680135943,
        "market": "jpg.store"
    }])

# NFT Collection Listings Trended Models
class NFTCollectionListingsTrendedRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class ListingTrend(BaseModel):
    listings: int = Field(..., description="Number of listings", example=592)
    price: float = Field(..., description="Floor price", example=205)
    time: int = Field(..., description="Unix timestamp", example=1680574100)

class NFTCollectionListingsTrendedResponse(BaseModel):
    __root__: List[ListingTrend] = Field(..., description="Listings", example=[{
        "time": 1680574100,
        "listings": 592,
        "price": 205
    }])

# NFT Collection OHLCV Models
class NFTCollectionOHLCVRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class NFTOHLCV(BaseModel):
    close: float = Field(..., description="Closing floor price", example=4150)
    high: float = Field(..., description="Highest floor price", example=4150)
    low: float = Field(..., description="Lowest floor price", example=3950)
    open: float = Field(..., description="Opening floor price", example=4000)
    time: int = Field(..., description="Unix timestamp", example=1680574100)
    volume: float = Field(..., description="Trading volume in ADA", example=61480)

class NFTCollectionOHLCVResponse(BaseModel):
    __root__: List[NFTOHLCV] = Field(..., description="OHLCV interval", example=[{
        "time": 1680574100,
        "open": 4000,
        "high": 4150,
        "low": 3950,
        "close": 4150,
        "volume": 61480
    }])

# NFT Collection Stats Models
class NFTCollectionStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")

class NFTCollectionStats(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=673)
    owners: int = Field(..., description="Number of unique owners", example=1124)
    price: float = Field(..., description="Floor price in ADA", example=450)
    sales: int = Field(..., description="Total number of sales", example=4782)
    supply: int = Field(..., description="Total supply", example=10000)
    topOffer: float = Field(..., description="Highest current offer in ADA", example=400)
    volume: float = Field(..., description="Total trading volume in ADA", example=16844521)

class NFTCollectionStatsResponse(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=673)
    owners: int = Field(..., description="Number of unique owners", example=1124)
    price: float = Field(..., description="Floor price in ADA", example=450)
    sales: int = Field(..., description="Total number of sales", example=4782)
    supply: int = Field(..., description="Total supply", example=10000)
    topOffer: float = Field(..., description="Highest current offer in ADA", example=400)
    volume: float = Field(..., description="Total trading volume in ADA", example=16844521)

# NFT Collection Extended Stats Models
class NFTCollectionExtendedStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("24h", description="Time frame")

class NFTCollectionExtendedStats(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=673)
    listingsPctChg: float = Field(..., description="Percent change in listings", example=0.11)
    owners: int = Field(..., description="Number of unique owners", example=1124)
    ownersPctChg: float = Field(..., description="Percent change in owners", example=0.05)
    price: float = Field(..., description="Floor price in ADA", example=450)
    pricePctChg: float = Field(..., description="Percent change in floor price", example=0.024)
    sales: int = Field(..., description="Total number of sales", example=5431)
    salesPctChg: float = Field(..., description="Percent change in sales", example=0.008)
    supply: int = Field(..., description="Total supply", example=10000)
    topOffer: float = Field(..., description="Highest current offer in ADA", example=380)
    volume: float = Field(..., description="Total trading volume in ADA", example=16844521)
    volumePctChg: float = Field(..., description="Percent change in volume", example=0.014)

class NFTCollectionExtendedStatsResponse(BaseModel):
    listings: int = Field(..., description="Number of active listings", example=673)
    listingsPctChg: float = Field(..., description="Percent change in listings", example=0.11)
    owners: int = Field(..., description="Number of unique owners", example=1124)
    ownersPctChg: float = Field(..., description="Percent change in owners", example=0.05)
    price: float = Field(..., description="Floor price in ADA", example=450)
    pricePctChg: float = Field(..., description="Percent change in floor price", example=0.024)
    sales: int = Field(..., description="Total number of sales", example=5431)
    salesPctChg: float = Field(..., description="Percent change in sales", example=0.008)
    supply: int = Field(..., description="Total supply", example=10000)
    topOffer: float = Field(..., description="Highest current offer in ADA", example=380)
    volume: float = Field(..., description="Total trading volume in ADA", example=16844521)
    volumePctChg: float = Field(..., description="Percent change in volume", example=0.014)

# NFT Collection Trades Models
class NFTCollectionTradesRequest(BaseModel):
    policy: Optional[str] = Field(None, description="Policy ID of the collection")
    timeframe: Optional[str] = Field("30d", description="Time frame (24h, 7d, 30d, 90d, 180d, 1y, all)")
    sortBy: Optional[str] = Field("time", description="Sort field")
    order: Optional[str] = Field("desc", description="Sort order")
    minAmount: Optional[int] = Field(None, description="Minimum trade amount")
    fromTime: Optional[int] = Field(None, description="Filter after UNIX timestamp")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class NFTTrade(BaseModel):
    buyer_address: str = Field(..., description="Buyer's address", example="addr1qxvpuw8dmmwvzs4lvjmuamn7l748n9wuvrumuz27v8mt6kzktn257cny8gcw0f99ft99apqdakca6grf9stpptjdyevqffsm7e")
    collection_name: str = Field(..., description="Collection name", example="Clay Nation")
    hash: str = Field(..., description="Transaction hash", example="505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9")
    image: str = Field(..., description="IPFS URL of NFT image", example="ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM")
    market: str = Field(..., description="Marketplace name", example="jpg.store")
    name: str = Field(..., description="NFT name", example="ClayNation3725")
    policy: str = Field(..., description="Policy ID", example="40fa2aa67258b4ce7b5782f74831d46a84c59a0ff0c28262fab21728")
    price: float = Field(..., description="Sale price in ADA", example=4925)
    seller_address: str = Field(..., description="Seller's address", example="addr1q9wmpjmp767fewhqswq89lua7csns8a704hrjljdt5r40ssstt62h0erkvx72zarcydnlldp0sj0ml02w3k06r8mpy8qm8eqkf")
    time: int = Field(..., description="Unix timestamp", example=1680135943)

class NFTCollectionTradesResponse(BaseModel):
    __root__: List[NFTTrade] = Field(..., description="List of NFT trades", example=[{
        "name": "ClayNation3725",
        "price": 4925,
        "market": "jpg.store",
        "time": 1680135943,
        "image": "ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM",
        "buyerAddress": "addr1qxvpuw8dmmwvzs4lvjmuamn7l748n9wuvrumuz27v8mt6kzktn257cny8gcw0f99ft99apqdakca6grf9stpptjdyevqffsm7e",
        "sellerAddress": "addr1q9wmpjmp767fewhqswq89lua7csns8a704hrjljdt5r40ssstt62h0erkvx72zarcydnlldp0sj0ml02w3k06r8mpy8qm8eqkf",
        "policy": "40fa2aa67258b4ce7b5782f74831d46a84c59a0ff0c28262fab21728",
        "collectionName": "Clay Nation",
        "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9"
    }])

# NFT Collection Trade Stats Models
class NFTCollectionTradeStatsRequest(BaseModel):
    policy: str = Field(..., description="Policy ID of the collection")
    timeframe: Optional[str] = Field("24h", description="Time frame")

class NFTCollectionTradeStats(BaseModel):
    buyers: int = Field(..., description="Number of unique buyers", example=35)
    sales: int = Field(..., description="Number of sales", example=42)
    sellers: int = Field(..., description="Number of unique sellers", example=16)
    volume: float = Field(..., description="Trading volume in ADA", example=247521)

class NFTCollectionTradeStatsResponse(BaseModel):
    buyers: int = Field(..., description="Number of unique buyers", example=35)
    sales: int = Field(..., description="Number of sales", example=42)
    sellers: int = Field(..., description="Number of unique sellers", example=16)
    volume: float = Field(..., description="Trading volume in ADA", example=247521)

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
    addresses: int = Field(..., description="Number of unique addresses", example=5321)
    buyers: int = Field(..., description="Number of unique buyers", example=3451)
    sales: int = Field(..., description="Number of sales", example=7832)
    sellers: int = Field(..., description="Number of unique sellers", example=3110)
    volume: float = Field(..., description="Trading volume in ADA", example=876345)

class NFTMarketStatsResponse(BaseModel):
    addresses: int = Field(..., description="Number of unique addresses", example=5321)
    buyers: int = Field(..., description="Number of unique buyers", example=3451)
    sales: int = Field(..., description="Number of sales", example=7832)
    sellers: int = Field(..., description="Number of unique sellers", example=3110)
    volume: float = Field(..., description="Trading volume in ADA", example=876345)

# NFT Market Extended Stats Models
class NFTMarketExtendedStatsRequest(BaseModel):
    timeframe: str = Field(..., description="Time frame")

class NFTMarketExtendedStats(BaseModel):
    addresses: int = Field(..., description="Number of unique addresses", example=5321)
    addresses_pct_chg: float = Field(..., description="Percent change in addresses", example=-0.11)
    buyers: int = Field(..., description="Number of unique buyers", example=3451)
    buyers_pct_chg: float = Field(..., description="Percent change in buyers", example=0.08)
    sales: int = Field(..., description="Number of sales", example=7832)
    sales_pct_chg: float = Field(..., description="Percent change in sales", example=0.02)
    sellers: int = Field(..., description="Number of unique sellers", example=3110)
    sellers_pct_chg: float = Field(..., description="Percent change in sellers", example=-0.15)
    volume: float = Field(..., description="Trading volume in ADA", example=876345)
    volume_pct_chg: float = Field(..., description="Percent change in volume", example=0.08)

class NFTMarketExtendedStatsResponse(BaseModel):
    addresses: int = Field(..., description="Number of unique addresses", example=5321)
    addresses_pct_chg: float = Field(..., description="Percent change in addresses", example=-0.11)
    buyers: int = Field(..., description="Number of unique buyers", example=3451)
    buyers_pct_chg: float = Field(..., description="Percent change in buyers", example=0.08)
    sales: int = Field(..., description="Number of sales", example=7832)
    sales_pct_chg: float = Field(..., description="Percent change in sales", example=0.02)
    sellers: int = Field(..., description="Number of unique sellers", example=3110)
    sellers_pct_chg: float = Field(..., description="Percent change in sellers", example=-0.15)
    volume: float = Field(..., description="Trading volume in ADA", example=876345)
    volume_pct_chg: float = Field(..., description="Percent change in volume", example=0.08)

# NFT Market Volume Trended Models
class NFTMarketVolumeTrendedRequest(BaseModel):
    timeframe: Optional[str] = Field("30d", description="Time frame")

class MarketVolumeTrend(BaseModel):
    time: int = Field(..., description="Unix timestamp", example=1690171200)
    value: float = Field(..., description="Volume value", example=783125)

class NFTMarketVolumeTrendedResponse(BaseModel):
    __root__: List[MarketVolumeTrend] = Field(..., description="Trended NFT market volume", example=[{
        "time": 1690171200,
        "value": 783125
    }])

# NFT Marketplace Stats Models
class NFTMarketplaceStatsRequest(BaseModel):
    timeframe: Optional[str] = Field("7d", description="Time frame")
    marketplace: Optional[str] = Field(None, description="Marketplace name")
    last_day: Optional[int] = Field(None, description="Filter by yesterday's data (0 or 1)")

class NFTMarketplaceStats(BaseModel):
    avg_sale: float = Field(..., description="Average sale price", example=100.5)
    fees: float = Field(..., description="Total fees collected", example=41210.512)
    liquidity: float = Field(..., description="Total liquidity", example=14341.1231)
    listings: int = Field(..., description="Number of listings", example=300)
    name: str = Field(..., description="Marketplace name", example="jpg.store")
    royalties: float = Field(..., description="Total royalties paid", example=645432.3123)
    sales: int = Field(..., description="Number of sales", example=7832)
    users: int = Field(..., description="Number of unique users", example=5321)
    volume: float = Field(..., description="Trading volume", example=876345.312)

class NFTMarketplaceStatsResponse(BaseModel):
    __root__: List[NFTMarketplaceStats] = Field(..., description="Marketplace stats", example=[{
        "name": "jpg.store",
        "volume": 876345.312,
        "sales": 7832,
        "avg_sale": 100.5,
        "listings": 300,
        "users": 5321,
        "fees": 41210.512,
        "liquidity": 14341.1231,
        "royalties": 645432.3123
    }])

# NFT Top Rankings Models
class NFTTopTimeframeRequest(BaseModel):
    ranking: str = Field(..., description="Ranking type: marketCap, volume, gainers, or losers")
    items: Optional[int] = Field(25, description="Number of items, max 100")

class NFTTopRanking(BaseModel):
    listings: int = Field(..., description="Number of listings", example=15)
    logo: str = Field(..., description="Logo URL", example="https://linktologo4.com")
    market_cap: float = Field(..., description="Market cap in ADA", example=25000)
    name: str = Field(..., description="Collection name", example="testCollection4")
    policy: str = Field(..., description="Policy ID", example="e3ff4ab89245ede61b3e2beab0443dbcc7ea8ca2c017478e4e8990e2")
    price: float = Field(..., description="Floor price", example=500)
    price_24h_chg: float = Field(..., description="24h price change", example=0.5)
    price_30d_chg: float = Field(..., description="30d price change", example=0.7)
    price_7d_chg: float = Field(..., description="7d price change", example=0.6)
    rank: int = Field(..., description="Ranking position", example=1)
    supply: int = Field(..., description="Total supply", example=50)
    volume_24h: float = Field(..., description="24h volume", example=4000)
    volume_24h_chg: float = Field(..., description="24h volume change", example=0.11)
    volume_30d: float = Field(..., description="30d volume", example=6000)
    volume_30d_chg: float = Field(..., description="30d volume change", example=0.05)
    volume_7d: float = Field(..., description="7d volume", example=5000)
    volume_7d_chg: float = Field(..., description="7d volume change", example=-0.11)

class NFTTopTimeframeResponse(BaseModel):
    __root__: List[NFTTopRanking] = Field(..., description="NFT Rankings.", example=[{
        "rank": 1,
        "price_24h_chg": 0.5,
        "price_7d_chg": 0.6,
        "price_30d_chg": 0.7,
        "listings": 15,
        "logo": "https://linktologo4.com",
        "market_cap": 25000,
        "name": "testCollection4",
        "policy": "e3ff4ab89245ede61b3e2beab0443dbcc7ea8ca2c017478e4e8990e2",
        "price": 500,
        "supply": 50,
        "volume_24h": 4000,
        "volume_7d": 5000,
        "volume_30d": 6000,
        "volume_24h_chg": 0.11,
        "volume_7d_chg": -0.11,
        "volume_30d_chg": 0.05
    }])

# NFT Top Volume Models
class NFTTopVolumeRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")

class NFTTopVolume(BaseModel):
    listings: int = Field(..., description="Number of listings", example=583)
    logo: str = Field(..., description="Logo URL", example="ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf")
    name: str = Field(..., description="Collection name", example="Stag Alliance")
    policy: str = Field(..., description="Policy ID", example="1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e")
    price: int = Field(..., description="Floor price", example=175)
    sales: int = Field(..., description="Number of sales", example=215)
    supply: int = Field(..., description="Total supply", example=7200)
    volume: int = Field(..., description="Trading volume", example=49606)

class NFTTopVolumeResponse(BaseModel):
    __root__: List[NFTTopVolume] = Field(..., description="List of top NFT volumes", example=[{
        "policy": "1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e",
        "name": "Stag Alliance",
        "logo": "ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf",
        "price": 175,
        "volume": 49606,
        "listings": 583,
        "supply": 7200,
        "sales": 215
    }])

# NFT Top Volume Extended Models
class NFTTopVolumeExtendedRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")

class NFTTopVolumeExtended(BaseModel):
    listings: int = Field(..., description="Number of listings", example=583)
    listings_pct_chg: float = Field(..., description="Percent change in listings", example=0.11)
    logo: str = Field(..., description="Logo URL", example="ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf")
    name: str = Field(..., description="Collection name", example="Stag Alliance")
    owners: int = Field(..., description="Number of owners", example=542)
    owners_pct_chg: float = Field(..., description="Percent change in owners", example=-0.031)
    policy: str = Field(..., description="Policy ID", example="1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e")
    price: int = Field(..., description="Floor price", example=175)
    price_pct_chg: float = Field(..., description="Percent change in price", example=0.024)
    sales: int = Field(..., description="Number of sales", example=50)
    sales_pct_chg: float = Field(..., description="Percent change in sales", example=0.34)
    supply: int = Field(..., description="Total supply", example=7200)
    volume: int = Field(..., description="Trading volume", example=49606)
    volume_pct_chg: float = Field(..., description="Percent change in volume", example=0.014)

class NFTTopVolumeExtendedResponse(BaseModel):
    __root__: List[NFTTopVolumeExtended] = Field(..., description="List of extended top NFT volumes", example=[{
        "policy": "1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e",
        "name": "Stag Alliance",
        "logo": "ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf",
        "price": 175,
        "pricePctChg": 0.024,
        "volume": 49606,
        "volumePctChg": 0.014,
        "listings": 583,
        "listingsPctChg": 0.11,
        "supply": 7200,
        "sales": 50,
        "salesPctChg": 0.34,
        "holders": 542,
        "holdersPctChg": -0.031
    }])
