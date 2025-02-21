from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Asset Supply Models
class AssetSupplyRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class AssetSupplyResponse(BaseModel):
    supply: int = Field(..., description="Current onchain supply")

# Address Info Models
class AddressInfoRequest(BaseModel):
    address: Optional[str] = Field(None, description="Cardano address")
    payment_cred: Optional[str] = Field(None, description="Payment credential")

class AddressInfo(BaseModel):
    address: str = Field(..., description="Full Cardano address")
    assets: List[Dict] = Field(..., description="List of assets held")
    lovelace: str = Field(..., description="ADA balance in lovelace")
    payment_cred: str = Field(..., description="Payment credential")
    stake_address: str = Field(..., description="Stake address")

class AddressInfoResponse(BaseModel):
    info: AddressInfo

# Address UTXOs Models
class AddressUTXOsRequest(BaseModel):
    address: Optional[str] = Field(None, description="Cardano address")
    payment_cred: Optional[str] = Field(None, description="Payment credential")
    page: Optional[int] = Field(1, description="Page number")
    per_page: Optional[int] = Field(100, description="Items per page, max 100")

class UTXO(BaseModel):
    assets: List[Dict] = Field(..., description="List of assets in UTxO")
    hash: str = Field(..., description="Transaction hash")
    index: int = Field(..., description="UTxO index")
    lovelace: str = Field(..., description="ADA amount in lovelace")

class AddressUTXOsResponse(BaseModel):
    utxos: List[UTXO]

# Transaction UTXOs Models
class TransactionUTXOsRequest(BaseModel):
    hash: str = Field(..., description="Transaction hash")

class TransactionUTXOs(BaseModel):
    hash: str = Field(..., description="Transaction hash")
    inputs: List[Dict] = Field(..., description="List of transaction inputs")
    outputs: List[Dict] = Field(..., description="List of transaction outputs")

class TransactionUTXOsResponse(BaseModel):
    transaction: TransactionUTXOs
