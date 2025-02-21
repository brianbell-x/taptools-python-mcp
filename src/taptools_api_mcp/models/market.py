from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Market Stats Models
class MarketStatsRequest(BaseModel):
    quote: Optional[str] = Field("ADA", description="Quote currency (e.g. 'ADA')")

class MarketStats(BaseModel):
    active_addresses: int = Field(..., description="Number of active addresses in 24h")
    dex_volume: float = Field(..., description="24h DEX trading volume")

class MarketStatsResponse(BaseModel):
    __root__: MarketStats = Field(..., description="Aggregated market stats")

# Metrics Models
class MetricsCall(BaseModel):
    calls: int = Field(..., description="Number of API calls")
    time: int = Field(..., description="Unix timestamp")

class MetricsResponse(BaseModel):
    __root__: List[MetricsCall] = Field(..., description="Daily request counts from the past 30 days")
