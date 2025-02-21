from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Integration Asset Models
class IntegrationAssetRequest(BaseModel):
    id: str = Field(..., description="Asset ID")

class IntegrationAsset(BaseModel):
    circulating_supply: int = Field(..., description="Current circulating supply")
    id: str = Field(..., description="Asset ID")
    name: str = Field(..., description="Asset name")
    symbol: str = Field(..., description="Asset symbol")
    total_supply: int = Field(..., description="Total supply")

class IntegrationAssetResponse(BaseModel):
    asset: IntegrationAsset

# Integration Block Models
class IntegrationBlockRequest(BaseModel):
    number: Optional[int] = Field(None, description="Block number")
    timestamp: Optional[int] = Field(None, description="Block timestamp")

class IntegrationBlock(BaseModel):
    block_number: int = Field(..., description="Block number")
    block_timestamp: int = Field(..., description="Block timestamp")

class IntegrationBlockResponse(BaseModel):
    block: IntegrationBlock

# Integration Events Models
class IntegrationEventsRequest(BaseModel):
    from_block: int = Field(..., description="Starting block number")
    to_block: int = Field(..., description="Ending block number")
    limit: Optional[int] = Field(1000, description="Maximum number of events to return")

class IntegrationEventsResponse(BaseModel):
    events: List[Dict] = Field(..., description="List of events")

# Integration Exchange Models
class IntegrationExchangeRequest(BaseModel):
    id: str = Field(..., description="Exchange ID")

class IntegrationExchange(BaseModel):
    factory_address: str = Field(..., description="Factory contract address")
    logo_url: str = Field(..., description="Exchange logo URL")
    name: str = Field(..., description="Exchange name")

class IntegrationExchangeResponse(BaseModel):
    exchange: IntegrationExchange

# Integration Latest Block Models
class IntegrationLatestBlockResponse(BaseModel):
    block: IntegrationBlock = Field(..., description="Latest block information")

# Integration Pair Models
class IntegrationPairRequest(BaseModel):
    id: str = Field(..., description="Pair ID")

class IntegrationPair(BaseModel):
    asset0_id: str = Field(..., description="First asset ID")
    asset1_id: str = Field(..., description="Second asset ID")
    created_at_block_number: int = Field(..., description="Block number at creation")
    created_at_block_timestamp: int = Field(..., description="Block timestamp at creation")
    created_at_txn_id: int = Field(..., description="Transaction ID at creation")
    factory_address: str = Field(..., description="Factory contract address")
    id: str = Field(..., description="Pair ID")

class IntegrationPairResponse(BaseModel):
    pair: IntegrationPair
