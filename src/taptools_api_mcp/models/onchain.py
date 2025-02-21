from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

# Asset Supply Models
class AssetSupplyRequest(BaseModel):
    unit: str = Field(..., description="Token unit identifier")

class AssetSupplyResponse(BaseModel):
    supply: float = Field(..., description="Current onchain supply", example=233838354)

# Address Info Models
class AddressInfoRequest(BaseModel):
    address: Optional[str] = Field(None, description="Cardano address")
    paymentCred: Optional[str] = Field(None, description="Payment credential")

class AssetBalance(BaseModel):
    unit: str = Field(..., description="Native asset unit", example="dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53")
    quantity: str = Field(..., description="Native asset amount", example="12000000")

class AddressInfo(BaseModel):
    address: str = Field(..., description="Address", example="addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq")
    paymentCred: str = Field(..., description="Payment credential", example="654902e0eda93d803768175c48b603d010f6a5ea4829a10e7c6f215d")
    lovelace: str = Field(..., description="ADA balance in lovelace", example="45000000")
    assets: List[AssetBalance] = Field(..., description="Native asset balances")
    stakeAddress: Optional[str] = Field(None, description="Stake address", example="stake1u8rphunzxm9lr4m688peqmnthmap35yt38rgvaqgsk5jcrqdr2vuc")

class AddressInfoResponse(BaseModel):
    address: str = Field(..., description="Address", example="addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq")
    paymentCred: str = Field(..., description="Payment credential", example="654902e0eda93d803768175c48b603d010f6a5ea4829a10e7c6f215d")
    lovelace: str = Field(..., description="ADA balance in lovelace", example="45000000")
    assets: List[AssetBalance] = Field(..., description="Native asset balances")
    stakeAddress: Optional[str] = Field(None, description="Stake address", example="stake1u8rphunzxm9lr4m688peqmnthmap35yt38rgvaqgsk5jcrqdr2vuc")

# Address UTXOs Models
class AddressUTXOsRequest(BaseModel):
    address: Optional[str] = Field(None, description="Address to query for")
    paymentCred: Optional[str] = Field(None, description="Payment credential to query for")
    page: Optional[int] = Field(1, description="This endpoint supports pagination. Default page is `1`.")
    perPage: Optional[int] = Field(100, description="Specify how many items to return per page. Maximum is `100`, default is `100`.")

class UTXO(BaseModel):
    assets: List[AssetBalance] = Field(..., description="Native asset balances")
    hash: str = Field(..., description="Transaction hash", example="a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b")
    index: int = Field(..., description="UTxO index", example=0)
    lovelace: str = Field(..., description="ADA amount in lovelace", example="3703342")

class AddressUTXOsResponse(BaseModel):
    __root__: List[UTXO] = Field(..., description="UTxOs", example=[{
        "hash": "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b",
        "index": 0,
        "lovelace": "3703342",
        "assets": [
            {
                "unit": "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53",
                "quantity": "12000000"
            }
        ]
    }])

# Transaction UTXOs Models
class TransactionUTXOsRequest(BaseModel):
    hash: str = Field(..., description="Transaction hash to query for")

class TransactionUTXOsResponse(BaseModel):
    hash: str = Field(..., description="Transaction hash", example="8be33680ec04da1cc98868699c5462fbbf6975529fb6371669fa735d2972d69b")
    inputs: List[UTXO] = Field(..., description="UTxOs")
    outputs: List[UTXO] = Field(..., description="UTxOs")
