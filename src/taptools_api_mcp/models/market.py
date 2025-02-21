from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Market Stats Models
class MarketStatsRequest(BaseModel):
    quote: Optional[str] = Field("ADA", description="Quote currency (e.g. 'ADA')")

class MarketStatsResponse(BaseModel):
    activeAddresses: int = Field(..., description="Number of active addresses in 24h", example=24523)
    dexVolume: float = Field(..., description="24h DEX trading volume", example=8134621.35)

# Metrics Models
class MetricsCall(BaseModel):
    calls: int = Field(..., description="Requests count", example=4837)
    time: int = Field(..., description="Unix timestamp", example=1692781200)

class MetricsResponse(BaseModel):
    __root__: List[MetricsCall] = Field(..., description="Daily request counts.", example=[{
        "time": 1692781200,
        "calls": 4837
    }])
