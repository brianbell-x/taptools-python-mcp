from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Token Debt Loans Models
class TokenDebtLoansRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    include: Optional[str] = Field("collateral,debt", description="Data to include, e.g. 'collateral,debt'")
    sort_by: Optional[str] = Field("time", description="Sort field: 'time' or 'expiration'")
    order: Optional[str] = Field("desc", description="Sort order: 'asc' or 'desc'")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page")

class TokenDebtLoan(BaseModel):
    collateral_amount: float = Field(..., description="Amount of collateral token")
    collateral_token: str = Field(..., description="Collateral token identifier")
    collateral_value: float = Field(..., description="Value of collateral in ADA")
    debt_amount: float = Field(..., description="Amount of debt token")
    debt_token: str = Field(..., description="Debt token identifier")
    debt_value: float = Field(..., description="Value of debt in ADA")
    expiration: int = Field(..., description="Unix timestamp of loan expiration")
    hash: str = Field(..., description="Transaction hash")
    health: float = Field(..., description="Loan health factor")
    interest_amount: float = Field(..., description="Amount of interest token")
    interest_token: str = Field(..., description="Interest token identifier")
    interest_value: float = Field(..., description="Value of interest in ADA")
    protocol: str = Field(..., description="Protocol name (e.g. 'Levvy')")
    time: int = Field(..., description="Unix timestamp of loan creation")

class TokenDebtLoansResponse(BaseModel):
    loans: List[TokenDebtLoan]

# Token Debt Offers Models
class TokenDebtOffersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    include: Optional[str] = Field("collateral,debt", description="Data to include")
    sort_by: Optional[str] = Field("time", description="Sort field")
    order: Optional[str] = Field("desc", description="Sort order")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page")

class TokenDebtOffer(BaseModel):
    collateral_amount: float = Field(..., description="Amount of collateral token")
    collateral_token: str = Field(..., description="Collateral token identifier")
    collateral_value: float = Field(..., description="Value of collateral in ADA")
    debt_amount: float = Field(..., description="Amount of debt token")
    debt_token: str = Field(..., description="Debt token identifier")
    debt_value: float = Field(..., description="Value of debt in ADA")
    duration: int = Field(..., description="Loan duration in seconds")
    hash: str = Field(..., description="Transaction hash")
    health: float = Field(..., description="Loan health factor")
    interest_amount: float = Field(..., description="Amount of interest token")
    interest_token: str = Field(..., description="Interest token identifier")
    interest_value: float = Field(..., description="Value of interest in ADA")
    protocol: str = Field(..., description="Protocol name")
    time: int = Field(..., description="Unix timestamp of offer creation")

class TokenDebtOffersResponse(BaseModel):
    offers: List[TokenDebtOffer]

# Token Holders Models
class TokenHoldersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenHoldersResponse(BaseModel):
    holders: int = Field(..., description="Total number of token holders")

# Token Top Holders Models
class TokenTopHoldersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(20, description="Items per page, max 100")

class TokenHolder(BaseModel):
    address: str = Field(..., description="Stake address of holder")
    amount: float = Field(..., description="Token amount held")

class TokenTopHoldersResponse(BaseModel):
    holders: List[TokenHolder]

# Token Indicators Models
class TokenIndicatorsRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    interval: str = Field(..., description="Time interval")
    items: Optional[int] = Field(None, description="Number of items, max 1000")
    indicator: Optional[str] = Field(None, description="Indicator type: ma, ema, rsi, macd, bb, bbw")
    quote: Optional[str] = Field(None, description="Quote currency")

class TokenIndicatorsResponse(BaseModel):
    values: List[float]

# Token Links Models
class TokenLinksRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenLinks(BaseModel):
    description: Optional[str] = Field(None, description="Token description")
    discord: Optional[str] = Field(None, description="Discord link")
    email: Optional[str] = Field(None, description="Contact email")
    facebook: Optional[str] = Field(None, description="Facebook link")
    github: Optional[str] = Field(None, description="GitHub link")
    instagram: Optional[str] = Field(None, description="Instagram link")
    medium: Optional[str] = Field(None, description="Medium link")
    reddit: Optional[str] = Field(None, description="Reddit link")
    telegram: Optional[str] = Field(None, description="Telegram link")
    twitter: Optional[str] = Field(None, description="Twitter link")
    website: Optional[str] = Field(None, description="Website link")
    youtube: Optional[str] = Field(None, description="YouTube link")

class TokenLinksResponse(BaseModel):
    links: TokenLinks

# Token Market Cap Models
class TokenMcapRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenMcap(BaseModel):
    circ_supply: float = Field(..., description="Circulating supply")
    fdv: float = Field(..., description="Fully diluted valuation")
    mcap: float = Field(..., description="Market capitalization")
    price: float = Field(..., description="Current price")
    ticker: str = Field(..., description="Token ticker")
    total_supply: float = Field(..., description="Total supply")

class TokenMcapResponse(BaseModel):
    market_cap: TokenMcap

# Token OHLCV Models
class TokenOHLCVRequest(BaseModel):
    unit: Optional[str] = Field(None, description="Token unit")
    onchain_id: Optional[str] = Field(None, description="Onchain ID")
    interval: str = Field(..., description="Time interval")
    num_intervals: Optional[int] = Field(None, description="Number of intervals")

class TokenOHLCV(BaseModel):
    close: float = Field(..., description="Closing price")
    high: float = Field(..., description="Highest price")
    low: float = Field(..., description="Lowest price")
    open: float = Field(..., description="Opening price")
    time: int = Field(..., description="Unix timestamp")
    volume: float = Field(..., description="Trading volume")

class TokenOHLCVResponse(BaseModel):
    ohlcv: List[TokenOHLCV]

# Token Pools Models
class TokenPoolsRequest(BaseModel):
    unit: Optional[str] = Field(None, description="Token unit")
    onchain_id: Optional[str] = Field(None, description="Onchain ID")
    ada_only: Optional[int] = Field(0, description="Filter for ADA pairs only (0 or 1)")

class TokenPool(BaseModel):
    exchange: str = Field(..., description="Exchange name")
    lp_token_unit: str = Field(..., description="LP token unit")
    onchain_id: str = Field(..., description="Onchain ID")
    token_a: str = Field(..., description="First token unit")
    token_a_locked: float = Field(..., description="Amount of first token locked")
    token_a_ticker: str = Field(..., description="First token ticker")
    token_b: str = Field(..., description="Second token unit")
    token_b_locked: float = Field(..., description="Amount of second token locked")
    token_b_ticker: str = Field(..., description="Second token ticker")

class TokenPoolsResponse(BaseModel):
    pools: List[TokenPool]

# Token Prices Models
class TokenPricesRequest(BaseModel):
    units: List[str] = Field(..., description="List of token units")

class TokenPricesResponse(BaseModel):
    prices: Dict[str, float]

# Token Price Changes Models
class TokenPriceChangesRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    timeframes: Optional[str] = Field(None, description="Comma-delimited timeframes")

class TokenPriceChangesResponse(BaseModel):
    changes: Dict[str, float]

# Token Quote Models
class TokenQuoteRequest(BaseModel):
    quote: Optional[str] = Field(None, description="Quote currency (e.g. USD)")

class TokenQuoteResponse(BaseModel):
    price: float = Field(..., description="Current quote price")

class TokenQuoteAvailableResponse(BaseModel):
    quotes: List[str]

# Token Top Liquidity Models
class TokenTopLiquidityRequest(BaseModel):
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(10, description="Items per page, max 100")

class TokenLiquidity(BaseModel):
    liquidity: float = Field(..., description="Total DEX liquidity")
    price: float = Field(..., description="Current price")
    ticker: str = Field(..., description="Token ticker")
    unit: str = Field(..., description="Token unit")

class TokenTopLiquidityResponse(BaseModel):
    tokens: List[TokenLiquidity]

# Token Trading Stats Models
class TokenTradingStatsRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    timeframe: Optional[str] = Field("24h", description="Time frame")

class TokenTradingStats(BaseModel):
    buy_volume: float = Field(..., description="Buy volume")
    buyers: int = Field(..., description="Number of buyers")
    buys: int = Field(..., description="Number of buy trades")
    sell_volume: float = Field(..., description="Sell volume")
    sellers: int = Field(..., description="Number of sellers")
    sells: int = Field(..., description="Number of sell trades")

class TokenTradingStatsResponse(BaseModel):
    stats: TokenTradingStats
