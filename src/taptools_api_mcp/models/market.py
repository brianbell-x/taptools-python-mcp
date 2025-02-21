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
    stats: MarketStats

# Metrics Models
class MetricsCall(BaseModel):
    calls: int = Field(..., description="Number of API calls")
    time: int = Field(..., description="Unix timestamp")

class MetricsResponse(BaseModel):
    metrics: List[MetricsCall]
