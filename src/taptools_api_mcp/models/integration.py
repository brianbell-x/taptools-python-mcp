from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# -----------------------------
# Existing classes
# -----------------------------
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

class IntegrationBlockRequest(BaseModel):
    number: Optional[int] = Field(None, description="Block number")
    timestamp: Optional[int] = Field(None, description="Block timestamp")

class IntegrationBlock(BaseModel):
    blockNumber: int = Field(..., description="Block number", example=10937538)
    blockTimestamp: int = Field(..., description="Block timestamp", example=1728408176)

class IntegrationBlockResponse(BaseModel):
    block: IntegrationBlock = Field(..., description="Block information")

class IntegrationEventsRequest(BaseModel):
    fromBlock: int = Field(..., description="Starting block number (inclusive)")
    toBlock: int = Field(..., description="Ending block number (inclusive)")
    limit: Optional[int] = Field(1000, description="Maximum number of events to return. Default 1000, max 1000.")

class IntegrationEvent(BaseModel):
    amount0: str = Field(..., description="Amount of token 0", example="200")
    amount1: str = Field(..., description="Amount of token 1", example="10")
    asset0In: str = Field(..., description="Amount of token 0 in", example="0")
    asset0Out: str = Field(..., description="Amount of token 0 out", example="200")
    asset1In: str = Field(..., description="Amount of token 1 in", example="10")
    asset1Out: str = Field(..., description="Amount of token 1 out", example="0")
    block: IntegrationBlock = Field(..., description="Block info")
    eventIndex: int = Field(..., description="Event index", example=10937538000000)
    eventType: str = Field(..., description="Event type", example="swap")
    maker: str = Field(..., description="Maker address")
    pairId: str = Field(..., description="Pair ID")
    reserves: Dict[str, str] = Field(..., description="Pool reserves")
    txnId: str = Field(..., description="Transaction ID")
    txnIndex: int = Field(..., description="Transaction index")

class IntegrationEventsResponse(BaseModel):
    events: List[IntegrationEvent] = Field(..., description="Events within block range.")

class IntegrationExchangeRequest(BaseModel):
    id: str = Field(..., description="Exchange ID")

class IntegrationExchange(BaseModel):
    factoryAddress: str = Field(..., description="Factory contract address", example="3")
    logoUrl: str = Field(..., description="Exchange logo URL", example="https://www.logos.com/minswap.png")
    name: str = Field(..., description="Exchange name", example="Minswap")

class IntegrationExchangeResponse(BaseModel):
    exchange: IntegrationExchange = Field(..., description="Exchange information")

class IntegrationLatestBlockResponse(BaseModel):
    block: IntegrationBlock = Field(..., description="Block information")

class IntegrationPairRequest(BaseModel):
    id: str = Field(..., description="Pair ID")

class IntegrationPair(BaseModel):
    asset0Id: str = Field(..., description="First asset ID", example="b46b12f0...")
    asset1Id: str = Field(..., description="Second asset ID", example="lovelace")
    createdAtBlockNumber: int = Field(..., description="Block number at creation")
    createdAtBlockTimestamp: int = Field(..., description="Block timestamp at creation")
    createdAtTxnId: str = Field(..., description="Transaction ID at creation")
    factoryAddress: str = Field(..., description="Factory contract address")
    id: str = Field(..., description="Pair ID", example="minswap.b46b12f0...")

class IntegrationPairResponse(BaseModel):
    pair: IntegrationPair = Field(..., description="Pair information")

# -----------------------------
# NEW/UPDATED classes for Policy Assets
# -----------------------------
class IntegrationPolicyAssetsRequest(BaseModel):
    id: str = Field(..., description="Policy ID")
    page: Optional[int] = Field(1, description="Page number")
    perPage: Optional[int] = Field(100, description="Items per page, max 100")

class PolicyAsset(BaseModel):
    id: str = Field(..., description="Asset ID under this policy")
    name: str = Field(..., description="Asset name under this policy")

class IntegrationPolicyAssetsResponse(BaseModel):
    id: str = Field(..., description="Policy ID")
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    assets: List[PolicyAsset] = Field(default_factory=list, description="List of assets under this policy")
    totalAssets: int = Field(..., description="Number of assets under the policy")
