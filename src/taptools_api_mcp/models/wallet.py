from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Wallet Portfolio Positions Models
class WalletPortfolioPositionsRequest(BaseModel):
    address: str = Field(..., description="Wallet address")

class FungibleTokenPosition(BaseModel):
    ticker: str = Field(..., description="Token ticker", example="TEST1")
    balance: float = Field(..., description="Token balance", example=200)
    unit: str = Field(..., description="Token unit", example="b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131")
    fingerprint: str = Field(..., description="Token fingerprint", example="fingerprint1")
    price: float = Field(..., description="Current price", example=100)
    adaValue: float = Field(..., description="Value in ADA", example=10000)
    price_24h: float = Field(..., description="24h price change", example=0.11)
    price_7d: float = Field(..., description="7d price change", example=0.03)
    price_30d: float = Field(..., description="30d price change", example=-0.32)
    liquidBalance: float = Field(..., description="Liquid balance", example=200)
    liquidValue: float = Field(..., description="Liquid value", example=10000)

class LiquidityPosition(BaseModel):
    ticker: str = Field(..., description="LP token ticker", example="TEST2 / ADA LP")
    unit: str = Field(..., description="LP token unit", example="f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e")
    amountLP: float = Field(..., description="LP token amount", example=100)
    tokenA: str = Field(..., description="First token unit", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    tokenAName: str = Field(..., description="First token name", example="TEST2")
    tokenAAmount: float = Field(..., description="First token amount", example=100)
    tokenB: str = Field(..., description="Second token unit")
    tokenBName: str = Field(..., description="Second token name", example="ADA")
    tokenBAmount: float = Field(..., description="Second token amount", example=200)
    adaValue: float = Field(..., description="Value in ADA", example=400)
    exchange: str = Field(..., description="Exchange name", example="Minswap")

class NFTPosition(BaseModel):
    name: str = Field(..., description="Collection name", example="testCollection")
    policy: str = Field(..., description="Policy ID", example="4048d53202b57aec6eb8edd8e9e4196d8eeb9a5fe1dd50d6dfc67be3")
    balance: int = Field(..., description="Number of NFTs held", example=2)
    adaValue: float = Field(..., description="Value in ADA", example=10000)
    floorPrice: float = Field(..., description="Floor price", example=1)
    price_24h: float = Field(..., description="24h price change", example=0.11)
    price_7d: float = Field(..., description="7d price change", example=0.03)
    price_30d: float = Field(..., description="30d price change", example=-0.32)
    listings: int = Field(..., description="Number of listings", example=3)
    liquidValue: float = Field(..., description="Liquid value", example=10)
    holders: int = Field(..., description="Number of holders", example=542)
    holdersPctChg: float = Field(..., description="Percent change in holders", example=-0.031)

class WalletPortfolioPositions(BaseModel):
    adaBalance: float = Field(..., description="ADA balance", example=10)
    adaValue: float = Field(..., description="Total value in ADA", example=10010)
    liquidValue: float = Field(..., description="Total liquid value", example=10010)
    numFTs: int = Field(..., description="Number of fungible tokens", example=2)
    numNFTs: int = Field(..., description="Number of NFTs", example=1)
    positionsFt: List[FungibleTokenPosition] = Field(..., description="Fungible token positions")
    positionsLp: List[LiquidityPosition] = Field(..., description="LP tokens positions")
    positionsNft: List[NFTPosition] = Field(..., description="Non-fungible token positions")

class WalletPortfolioPositionsResponse(BaseModel):
    adaBalance: float = Field(..., description="ADA balance", example=10)
    adaValue: float = Field(..., description="Total value in ADA", example=10010)
    liquidValue: float = Field(..., description="Total liquid value", example=10010)
    numFTs: int = Field(..., description="Number of fungible tokens", example=2)
    numNFTs: int = Field(..., description="Number of NFTs", example=1)
    positionsFt: List[FungibleTokenPosition] = Field(..., description="Fungible token positions")
    positionsLp: List[LiquidityPosition] = Field(..., description="LP tokens positions")
    positionsNft: List[NFTPosition] = Field(..., description="Non-fungible token positions")

# Wallet Token Trades Models
class WalletTokenTradesRequest(BaseModel):
    address: str = Field(..., description="Address to query for")
    unit: Optional[str] = Field(None, description="Token unit (policy + hex name) to filter by")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class WalletTokenTrade(BaseModel):
    action: str = Field(..., description="Trade action (Buy/Sell)", example="Buy")
    time: int = Field(..., description="Unix timestamp", example=1692781200)
    tokenA: str = Field(..., description="First token unit", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    tokenAName: str = Field(..., description="Name of first token", example="TEST1")
    tokenAAmount: float = Field(..., description="Amount of first token", example=10)
    tokenB: str = Field(..., description="Second token unit")
    tokenBName: str = Field(..., description="Name of second token", example="ADA")
    tokenBAmount: float = Field(..., description="Amount of second token", example=5)

class WalletTokenTradesResponse(BaseModel):
    __root__: List[WalletTokenTrade] = Field(..., description="Token trade history for wallet", example=[{
        "action": "Buy",
        "time": 1692781200,
        "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "tokenAName": "TEST1",
        "tokenAAmount": 10,
        "tokenB": "",
        "tokenBName": "ADA",
        "tokenBAmount": 5
    }])

# Wallet Value Trended Models
class WalletValueTrendedRequest(BaseModel):
    address: str = Field(..., description="Address to query for")
    timeframe: Optional[str] = Field("30d", description="The time interval. Options are `24h`, `7d`, `30d`, `90d`, `180d`, `1y`, `all`. Defaults to `30d`.")
    quote: Optional[str] = Field("ADA", description="Quote currency to use (ADA, USD, EUR, ETH, BTC). Default is `ADA`.")

class WalletValueTrend(BaseModel):
    time: int = Field(..., description="Unix timestamp", example=1692781200)
    value: float = Field(..., description="Portfolio value", example=57)

class WalletValueTrendedResponse(BaseModel):
    __root__: List[WalletValueTrend] = Field(..., description="Interval value", example=[{
        "time": 1692781200,
        "value": 57
    }])
