from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Token Debt Loans Models
class TokenDebtLoansRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    include: Optional[str] = Field("collateral,debt", description="Data to include, e.g. 'collateral,debt'")
    sortBy: Optional[str] = Field("time", description="Sort field: 'time' or 'expiration'")
    order: Optional[str] = Field("desc", description="Sort order: 'asc' or 'desc'")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class TokenDebtLoan(BaseModel):
    collateralAmount: float = Field(..., description="Amount of collateral token", example=1000)
    collateralToken: str = Field(..., description="Collateral token identifier", example="b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131")
    collateralValue: float = Field(..., description="Value of collateral in ADA", example=500)
    debtAmount: float = Field(..., description="Amount of debt token", example=100)
    debtToken: str = Field(..., description="Debt token identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    debtValue: float = Field(..., description="Value of debt in ADA", example=400)
    expiration: int = Field(..., description="Unix timestamp of loan expiration", example=1692781200)
    hash: str = Field(..., description="Transaction hash", example="505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9")
    health: float = Field(..., description="Loan health factor", example=1.25)
    interestAmount: float = Field(..., description="Amount of interest token", example=10)
    interestToken: str = Field(..., description="Interest token identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    interestValue: float = Field(..., description="Value of interest in ADA", example=40)
    protocol: str = Field(..., description="Protocol name (e.g. 'Levvy')", example="Levvy")
    time: int = Field(..., description="Unix timestamp of loan creation", example=1692694800)

class TokenDebtLoansResponse(BaseModel):
    loans: List[TokenDebtLoan] = Field(..., description="Active P2P loans.", example=[{
        "collateralAmount": 1000,
        "collateralToken": "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131",
        "collateralValue": 500,
        "debtAmount": 100,
        "debtToken": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "debtValue": 400,
        "expiration": 1692781200,
        "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
        "health": 1.25,
        "interestAmount": 10,
        "interestToken": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "interestValue": 40,
        "protocol": "Levvy",
        "time": 1692694800
    }])

# Token Debt Offers Models
class TokenDebtOffersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    include: Optional[str] = Field("collateral,debt", description="Data to include")
    sortBy: Optional[str] = Field("time", description="Sort field")
    order: Optional[str] = Field("desc", description="Sort order")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class TokenDebtOffer(BaseModel):
    collateralAmount: float = Field(..., description="Amount of collateral token", example=1000)
    collateralToken: str = Field(..., description="Collateral token identifier", example="b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131")
    collateralValue: float = Field(..., description="Value of collateral in ADA", example=500)
    debtAmount: float = Field(..., description="Amount of debt token", example=100)
    debtToken: str = Field(..., description="Debt token identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    debtValue: float = Field(..., description="Value of debt in ADA", example=400)
    duration: int = Field(..., description="Loan duration in seconds", example=86400)
    hash: str = Field(..., description="Transaction hash", example="505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9")
    health: float = Field(..., description="Loan health factor", example=1.25)
    interestAmount: float = Field(..., description="Amount of interest token", example=10)
    interestToken: str = Field(..., description="Interest token identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    interestValue: float = Field(..., description="Value of interest in ADA", example=40)
    protocol: str = Field(..., description="Protocol name", example="Levvy")
    time: int = Field(..., description="Unix timestamp of offer creation", example=1692694800)

class TokenDebtOffersResponse(BaseModel):
    offers: List[TokenDebtOffer] = Field(..., description="Active P2P loan offers.", example=[{
        "collateralAmount": 1000,
        "collateralToken": "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131",
        "collateralValue": 500,
        "debtAmount": 100,
        "debtToken": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "debtValue": 400,
        "duration": 86400,
        "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
        "health": 1.25,
        "interestAmount": 10,
        "interestToken": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "interestValue": 40,
        "protocol": "Levvy",
        "time": 1692694800
    }])

# Token Holders Models
class TokenHoldersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenHoldersResponse(BaseModel):
    holders: int = Field(..., description="Total number of token holders", example=1234)

# Token Top Holders Models
class TokenTopHoldersRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(20, description="Specify how many items to return per page. Maximum is `100`, default is `20`.")

class TokenHolder(BaseModel):
    address: str = Field(..., description="Stake address of holder", example="stake1u8mvwfn298a4dkm92hrgeupnnuzhxfwl5lauzuejl5cf8esrtjn6w")
    amount: float = Field(..., description="Token amount held", example=1000000)

class TokenTopHoldersResponse(BaseModel):
    holders: List[TokenHolder] = Field(..., description="Top token holders.", example=[{
        "address": "stake1u8mvwfn298a4dkm92hrgeupnnuzhxfwl5lauzuejl5cf8esrtjn6w",
        "amount": 1000000
    }])

# Token Indicators Models
class TokenIndicatorsRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    interval: str = Field(..., description="Time interval")
    items: Optional[int] = Field(None, description="Number of items, max 1000")
    indicator: Optional[str] = Field(None, description="Indicator type: ma, ema, rsi, macd, bb, bbw")
    quote: Optional[str] = Field(None, description="Quote currency")

class TokenIndicatorsResponse(BaseModel):
    values: List[float] = Field(..., description="Indicator values.", example=[25.4, 26.1, 25.8, 26.3])

# Token Links Models
class TokenLinksRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenLinksResponse(BaseModel):
    description: Optional[str] = Field(None, description="Token description", example="A decentralized exchange token")
    discord: Optional[str] = Field(None, description="Discord link", example="https://discord.gg/example")
    email: Optional[str] = Field(None, description="Contact email", example="contact@example.com")
    facebook: Optional[str] = Field(None, description="Facebook link", example="https://facebook.com/example")
    github: Optional[str] = Field(None, description="GitHub link", example="https://github.com/example")
    instagram: Optional[str] = Field(None, description="Instagram link", example="https://instagram.com/example")
    medium: Optional[str] = Field(None, description="Medium link", example="https://medium.com/example")
    reddit: Optional[str] = Field(None, description="Reddit link", example="https://reddit.com/r/example")
    telegram: Optional[str] = Field(None, description="Telegram link", example="https://t.me/example")
    twitter: Optional[str] = Field(None, description="Twitter link", example="https://twitter.com/example")
    website: Optional[str] = Field(None, description="Website link", example="https://example.com")
    youtube: Optional[str] = Field(None, description="YouTube link", example="https://youtube.com/example")

# Token Market Cap Models
class TokenMcapRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class TokenMcap(BaseModel):
    circSupply: float = Field(..., description="Circulating supply", example=1000000)
    fdv: float = Field(..., description="Fully diluted valuation", example=2000000)
    mcap: float = Field(..., description="Market capitalization", example=1500000)
    price: float = Field(..., description="Current price", example=1.5)
    ticker: str = Field(..., description="Token ticker", example="TEST")
    totalSupply: float = Field(..., description="Total supply", example=2000000)

class TokenMcapResponse(BaseModel):
    circSupply: float = Field(..., description="Circulating supply", example=1000000)
    fdv: float = Field(..., description="Fully diluted valuation", example=2000000)
    mcap: float = Field(..., description="Market capitalization", example=1500000)
    price: float = Field(..., description="Current price", example=1.5)
    ticker: str = Field(..., description="Token ticker", example="TEST")
    totalSupply: float = Field(..., description="Total supply", example=2000000)

# Token OHLCV Models
class TokenOHLCVRequest(BaseModel):
    unit: Optional[str] = Field(None, description="Token unit")
    onchainId: Optional[str] = Field(None, description="Onchain ID")
    interval: str = Field(..., description="Time interval")
    numIntervals: Optional[int] = Field(None, description="Number of intervals")

class TokenOHLCV(BaseModel):
    close: float = Field(..., description="Closing price", example=1.5)
    high: float = Field(..., description="Highest price", example=1.6)
    low: float = Field(..., description="Lowest price", example=1.4)
    open: float = Field(..., description="Opening price", example=1.45)
    time: int = Field(..., description="Unix timestamp", example=1692781200)
    volume: float = Field(..., description="Trading volume", example=100000)

class TokenOHLCVResponse(BaseModel):
    data: List[TokenOHLCV] = Field(..., description="OHLCV data points.", example=[{
        "time": 1692781200,
        "open": 1.45,
        "high": 1.6,
        "low": 1.4,
        "close": 1.5,
        "volume": 100000
    }])

# Token Pools Models
class TokenPoolsRequest(BaseModel):
    unit: Optional[str] = Field(None, description="Token unit")
    onchainId: Optional[str] = Field(None, description="Onchain ID")
    adaOnly: Optional[int] = Field(0, description="Filter for ADA pairs only (0 or 1)")

class TokenPool(BaseModel):
    exchange: str = Field(..., description="Exchange name", example="Minswap")
    lpTokenUnit: str = Field(..., description="LP token unit", example="f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e")
    onchainId: str = Field(..., description="Onchain ID", example="pool1234")
    tokenA: str = Field(..., description="First token unit", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    tokenALocked: float = Field(..., description="Amount of first token locked", example=100000)
    tokenATicker: str = Field(..., description="First token ticker", example="TEST")
    tokenB: str = Field(..., description="Second token unit")
    tokenBLocked: float = Field(..., description="Amount of second token locked", example=200000)
    tokenBTicker: str = Field(..., description="Second token ticker", example="ADA")

class TokenPoolsResponse(BaseModel):
    pools: List[TokenPool] = Field(..., description="Liquidity pools.", example=[{
        "exchange": "Minswap",
        "lpTokenUnit": "f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e",
        "onchainId": "pool1234",
        "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "tokenALocked": 100000,
        "tokenATicker": "TEST",
        "tokenB": "",
        "tokenBLocked": 200000,
        "tokenBTicker": "ADA"
    }])

# Token Prices Models
class TokenPricesRequest(BaseModel):
    units: List[str] = Field(..., description="List of token units to get prices for")

class TokenPricesResponse(BaseModel):
    prices: Dict[str, float] = Field(..., description="Token prices by unit", example={
        "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32": 1.5,
        "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131": 2.3
    })

# Token Price Changes Models
class TokenPriceChangesRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    timeframes: Optional[str] = Field(None, description="Comma-delimited timeframes (5m,1h,4h,6h,24h,7d,30d,60d,90d)")

class TokenPriceChangesResponse(BaseModel):
    changes: Dict[str, float] = Field(..., description="Price changes by timeframe", example={
        "5m": 0.01,
        "1h": 0.02,
        "24h": -0.05,
        "7d": 0.1
    })

# Token Quote Models
class TokenQuoteRequest(BaseModel):
    quote: Optional[str] = Field(None, description="Quote currency (e.g. USD)")

class TokenQuoteResponse(BaseModel):
    price: float = Field(..., description="Current quote price", example=1.5)

class TokenQuoteAvailableResponse(BaseModel):
    currencies: List[str] = Field(..., description="Available quote currencies.", example=["USD", "EUR", "ADA"])

# Token Top Liquidity Models
class TokenTopLiquidityRequest(BaseModel):
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(10, description="Specify how many items to return per page. Maximum is `100`, default is `10`.")

class TokenLiquidity(BaseModel):
    liquidity: float = Field(..., description="Total DEX liquidity", example=1000000)
    price: float = Field(..., description="Current price", example=1.5)
    ticker: str = Field(..., description="Token ticker", example="TEST")
    unit: str = Field(..., description="Token unit", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")

class TokenTopLiquidityResponse(BaseModel):
    tokens: List[TokenLiquidity] = Field(..., description="Tokens ranked by liquidity.", example=[{
        "unit": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "ticker": "TEST",
        "price": 1.5,
        "liquidity": 1000000
    }])

# Token Trading Stats Models
class TokenTradingStatsRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")
    timeframe: Optional[str] = Field("24h", description="Time frame (24h, 7d, 30d)")

class TokenTradingStats(BaseModel):
    buyVolume: float = Field(..., description="Buy volume", example=500000)
    buyers: int = Field(..., description="Number of buyers", example=150)
    buys: int = Field(..., description="Number of buy trades", example=200)
    sellVolume: float = Field(..., description="Sell volume", example=450000)
    sellers: int = Field(..., description="Number of sellers", example=120)
    sells: int = Field(..., description="Number of sell trades", example=180)

class TokenTradingStatsResponse(BaseModel):
    buyVolume: float = Field(..., description="Buy volume", example=500000)
    buyers: int = Field(..., description="Number of buyers", example=150)
    buys: int = Field(..., description="Number of buy trades", example=200)
    sellVolume: float = Field(..., description="Sell volume", example=450000)
    sellers: int = Field(..., description="Number of sellers", example=120)
    sells: int = Field(..., description="Number of sell trades", example=180)

# Token Top Market Cap Models
class TokenTopMcapRequest(BaseModel):
    type: Optional[str] = Field("mcap", description="Ranking type (mcap, fdv). Default is `mcap`.")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(20, description="Specify how many items to return per page. Maximum is `100`, default is `20`.")

class TokenTopMcap(BaseModel):
    circSupply: float = Field(..., description="Circulating supply", example=1000000)
    fdv: float = Field(..., description="Fully diluted valuation", example=2000000)
    mcap: float = Field(..., description="Market capitalization", example=1500000)
    price: float = Field(..., description="Current price", example=1.5)
    ticker: str = Field(..., description="Token ticker", example="TEST")
    totalSupply: float = Field(..., description="Total supply", example=2000000)
    unit: str = Field(..., description="Token unit identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")

class TokenTopMcapResponse(BaseModel):
    tokens: List[TokenTopMcap] = Field(..., description="Tokens ranked by market cap.", example=[{
        "unit": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "ticker": "TEST",
        "price": 1.5,
        "mcap": 1500000,
        "fdv": 2000000,
        "circSupply": 1000000,
        "totalSupply": 2000000
    }])

# Token Top Volume Models
class TokenTopVolumeRequest(BaseModel):
    timeframe: Optional[str] = Field("24h", description="Time frame (24h, 7d, 30d)")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(20, description="Specify how many items to return per page. Maximum is `100`, default is `20`.")

class TokenTopVolume(BaseModel):
    price: float = Field(..., description="Current price", example=1.5)
    ticker: str = Field(..., description="Token ticker", example="TEST")
    unit: str = Field(..., description="Token unit identifier", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    volume: float = Field(..., description="Trading volume", example=1000000)

class TokenTopVolumeResponse(BaseModel):
    tokens: List[TokenTopVolume] = Field(..., description="Tokens ranked by volume.", example=[{
        "unit": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "ticker": "TEST",
        "price": 1.5,
        "volume": 1000000
    }])

# Token Trades Models
class TokenTradesRequest(BaseModel):
    timeframe: Optional[str] = Field("30d", description="Time frame (24h, 7d, 30d, 90d, 180d, 1y, all)")
    sortBy: Optional[str] = Field("amount", description="Sort field (amount, time)")
    order: Optional[str] = Field("desc", description="Sort order (asc, desc)")
    unit: Optional[str] = Field(None, description="Token unit (policy + hex name)")
    minAmount: Optional[int] = Field(None, description="Minimum trade amount in lovelace")
    fromTs: Optional[int] = Field(None, description="Filter trades after this UNIX timestamp")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class TokenTrade(BaseModel):
    action: str = Field(..., description="Trade action (buy/sell)", example="buy")
    address: str = Field(..., description="Trader's address", example="addr1qxvpuw8dmmwvzs4lvjmuamn7l748n9wuvrumuz27v8mt6kzktn257cny8gcw0f99ft99apqdakca6grf9stpptjdyevqffsm7e")
    exchange: str = Field(..., description="Exchange name", example="Minswap")
    hash: str = Field(..., description="Transaction hash", example="505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9")
    lpTokenUnit: str = Field(..., description="LP token unit", example="f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e")
    price: float = Field(..., description="Trade price", example=1.5)
    time: int = Field(..., description="Unix timestamp of trade", example=1692781200)
    tokenA: str = Field(..., description="First token unit", example="63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32")
    tokenAAmount: float = Field(..., description="Amount of first token", example=1000)
    tokenAName: str = Field(..., description="Name of first token", example="TEST")
    tokenB: str = Field(..., description="Second token unit")
    tokenBAmount: float = Field(..., description="Amount of second token", example=1500)
    tokenBName: str = Field(..., description="Name of second token", example="ADA")

class TokenTradesResponse(BaseModel):
    trades: List[TokenTrade] = Field(..., description="Token trades across DEXes.", example=[{
        "action": "buy",
        "address": "addr1qxvpuw8dmmwvzs4lvjmuamn7l748n9wuvrumuz27v8mt6kzktn257cny8gcw0f99ft99apqdakca6grf9stpptjdyevqffsm7e",
        "exchange": "Minswap",
        "hash": "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9",
        "lpTokenUnit": "f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e",
        "price": 1.5,
        "time": 1692781200,
        "tokenA": "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32",
        "tokenAAmount": 1000,
        "tokenAName": "TEST",
        "tokenB": "",
        "tokenBAmount": 1500,
        "tokenBName": "ADA"
    }])
