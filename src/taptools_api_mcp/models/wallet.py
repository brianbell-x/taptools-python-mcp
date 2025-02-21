from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Wallet Portfolio Positions Models
class WalletPortfolioPositionsRequest(BaseModel):
    address: str = Field(..., description="Wallet address")

class WalletPortfolioPositions(BaseModel):
    ada_balance: float = Field(..., description="ADA balance")
    ada_value: float = Field(..., description="Total value in ADA")
    liquid_value: float = Field(..., description="Total liquid value")
    num_fts: int = Field(..., description="Number of fungible tokens")
    num_nfts: int = Field(..., description="Number of NFTs")
    positions_ft: List[Dict] = Field(..., description="Fungible token positions")
    positions_lp: List[Dict] = Field(..., description="Liquidity pool positions")
    positions_nft: List[Dict] = Field(..., description="NFT positions")

class WalletPortfolioPositionsResponse(BaseModel):
    __root__: WalletPortfolioPositions = Field(..., description="Current wallet positions")

# Wallet Token Trades Models
class WalletTokenTradesRequest(BaseModel):
    address: str = Field(..., description="Wallet address")
    unit: Optional[str] = Field(None, description="Token unit to filter by")

class WalletTokenTrade(BaseModel):
    action: str = Field(..., description="Trade action (Buy/Sell)")
    hash: str = Field(..., description="Transaction hash")
    time: int = Field(..., description="Unix timestamp")
    token_a: str = Field(..., description="First token unit")
    token_a_amount: float = Field(..., description="Amount of first token")
    token_a_name: str = Field(..., description="Name of first token")
    token_b: str = Field(..., description="Second token unit")
    token_b_amount: float = Field(..., description="Amount of second token")
    token_b_name: str = Field(..., description="Name of second token")

class WalletTokenTradesResponse(BaseModel):
    __root__: List[WalletTokenTrade] = Field(..., description="Token trade history for wallet")

# Wallet Value Trended Models
class WalletValueTrendedRequest(BaseModel):
    address: str = Field(..., description="Wallet address")
    timeframe: Optional[str] = Field("30d", description="Time frame")
    quote: Optional[str] = Field("ADA", description="Quote currency")

class WalletValueTrend(BaseModel):
    time: int = Field(..., description="Unix timestamp")
    value: float = Field(..., description="Portfolio value")

class WalletValueTrendedResponse(BaseModel):
    __root__: List[WalletValueTrend] = Field(..., description="Historical wallet value in 4hr intervals")
