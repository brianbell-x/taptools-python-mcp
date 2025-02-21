from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Market Stats Models
class MarketStats(BaseModel):
    """Market statistics data model."""
    totalMarketCap: float = Field(..., description="Total market capitalization")
    volume24h: float = Field(..., description="24-hour trading volume")
    dominance: Dict[str, float] = Field(..., description="Token dominance percentages")
    activeTokens: int = Field(..., description="Number of active tokens")
    activeTraders: int = Field(..., description="Number of active traders")

# Metrics Models
class MetricsCall(BaseModel):
    calls: int = Field(..., description="Requests count", example=4837)
    time: int = Field(..., description="Unix timestamp", example=1692781200)

class MetricsResponse(BaseModel):
    metrics: List[MetricsCall] = Field(..., description="Daily request counts")

# Market Overview Models
class TokenChange(BaseModel):
    """Token price change information."""
    unit: str = Field(..., description="Token identifier")
    change24h: float = Field(..., description="24-hour price change percentage")

class TokenVolume(BaseModel):
    """Token volume information."""
    unit: str = Field(..., description="Token identifier")
    volume24h: float = Field(..., description="24-hour trading volume")

class MarketOverview(BaseModel):
    """Market overview data including gainers, losers, and trending tokens."""
    gainers: List[TokenChange] = Field(..., description="Top gaining tokens")
    losers: List[TokenChange] = Field(..., description="Top losing tokens")
    trending: List[TokenVolume] = Field(..., description="Trending tokens by volume")
