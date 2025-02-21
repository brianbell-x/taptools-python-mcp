from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Integration Asset Models
class IntegrationAssetRequest(BaseModel):
    id: str = Field(..., description="Asset ID")

class IntegrationAsset(BaseModel):
    circulatingSupply: int = Field(..., description="Current circulating supply", example=1500000)
    id: str = Field(..., description="Asset ID", example="b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131")
    name: str = Field(..., description="Asset name", example="snek coin")
    symbol: str = Field(..., description="Asset symbol", example="SNEK")
    totalSupply: int = Field(..., description="Total supply", example=2000000)

class IntegrationAssetResponse(BaseModel):
    asset: IntegrationAsset = Field(..., description="Asset information")

# Integration Block Models
class IntegrationBlockRequest(BaseModel):
    number: Optional[int] = Field(None, description="Block number")
    timestamp: Optional[int] = Field(None, description="Block timestamp")

class IntegrationBlock(BaseModel):
    blockNumber: int = Field(..., description="Block number", example=10937538)
    blockTimestamp: int = Field(..., description="Block timestamp", example=1728408176)

class IntegrationBlockResponse(BaseModel):
    block: IntegrationBlock = Field(..., description="Block information")

# Integration Events Models
class IntegrationEventsRequest(BaseModel):
    fromBlock: int = Field(..., description="Starting block number (inclusive)")
    toBlock: int = Field(..., description="Ending block number (inclusive)")
    limit: Optional[int] = Field(1000, description="Maximum number of events to return. Default is `1000`, maximum is `1000`.")

class IntegrationEvent(BaseModel):
    amount0: str = Field(..., description="Amount of token 0", example="200")
    amount1: str = Field(..., description="Amount of token 1", example="10")
    asset0In: str = Field(..., description="Amount of token 0 in", example="0")
    asset0Out: str = Field(..., description="Amount of token 0 out", example="200")
    asset1In: str = Field(..., description="Amount of token 1 in", example="10")
    asset1Out: str = Field(..., description="Amount of token 1 out", example="0")
    block: IntegrationBlock = Field(..., description="Block information", example={
        "blockNumber": 10937538,
        "blockTimestamp": 1728408176
    })
    eventIndex: int = Field(..., description="Event index", example=10937538000000)
    eventType: str = Field(..., description="Event type", example="swap")
    maker: str = Field(..., description="Maker address", example="addr1q8ete2wpeulwq5yxutftpqdmgu2rntld85x7ztswahs2t0daytnqe6ea4p09jpv8mz3umpsdk9gkqvkhca7nngxrp2lqnh0x4l")
    pairId: str = Field(..., description="Pair ID", example="nikeswaporderbook.44759dc63605dbf88700b241ee451aa5b0334cf2b34094d836fbdf8642757a7a696542656520.ada")
    reserves: Dict[str, str] = Field(..., description="Pool reserves", example={"asset0": "20000000", "asset1": "10000"})
    txnId: str = Field(..., description="Transaction ID", example="a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b")
    txnIndex: int = Field(..., description="Transaction index", example=115981434)

class IntegrationEventsResponse(BaseModel):
    events: List[IntegrationEvent] = Field(..., description="Events within block range.", example=[{
        "amount0": "200",
        "amount1": "10",
        "asset0In": "0",
        "asset0Out": "200",
        "asset1In": "10",
        "asset1Out": "0",
        "block": {
            "blockNumber": 10937538,
            "blockTimestamp": 1728408176
        },
        "eventIndex": 10937538000000,
        "eventType": "swap",
        "maker": "addr1q8ete2wpeulwq5yxutftpqdmgu2rntld85x7ztswahs2t0daytnqe6ea4p09jpv8mz3umpsdk9gkqvkhca7nngxrp2lqnh0x4l",
        "pairId": "nikeswaporderbook.44759dc63605dbf88700b241ee451aa5b0334cf2b34094d836fbdf8642757a7a696542656520.ada",
        "reserves": {
            "asset0": "20000000",
            "asset1": "10000"
        },
        "txnId": "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b",
        "txnIndex": 115981434
    }])

# Integration Exchange Models
class IntegrationExchangeRequest(BaseModel):
    id: str = Field(..., description="Exchange ID")

class IntegrationExchange(BaseModel):
    factoryAddress: str = Field(..., description="Factory contract address", example="3")
    logoUrl: str = Field(..., description="Exchange logo URL", example="https://www.logos.com/minswap.png")
    name: str = Field(..., description="Exchange name", example="Minswap")

class IntegrationExchangeResponse(BaseModel):
    exchange: IntegrationExchange = Field(..., description="Exchange information")

# Integration Latest Block Models
class IntegrationLatestBlockResponse(BaseModel):
    block: IntegrationBlock = Field(..., description="Block information")

# Integration Pair Models
class IntegrationPairRequest(BaseModel):
    id: str = Field(..., description="Pair ID")

class IntegrationPair(BaseModel):
    asset0Id: str = Field(..., description="First asset ID", example="b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131")
    asset1Id: str = Field(..., description="Second asset ID", example="lovelace")
    createdAtBlockNumber: int = Field(..., description="Block number at creation", example=10937538)
    createdAtBlockTimestamp: int = Field(..., description="Block timestamp at creation", example=1728408176)
    createdAtTxnId: str = Field(..., description="Transaction ID at creation", example="a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b")
    factoryAddress: str = Field(..., description="Factory contract address", example="addr1w8433zk2shufk42hn4x7zznjjuqwwyfmxlv3ljxgj4hgfaq8g6q0x")
    id: str = Field(..., description="Pair ID", example="minswap.b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131.lovelace")

class IntegrationPairResponse(BaseModel):
    pair: IntegrationPair = Field(..., description="Pair information")
