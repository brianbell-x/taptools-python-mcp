"""
OnchainAPI for onchain data endpoints.
"""
import logging
import httpx
from typing import Dict, Any

from ..models.onchain import (
    AssetSupplyRequest, AssetSupplyResponse,
    AddressInfoRequest, AddressInfoResponse,
    AddressUTXOsRequest, AddressUTXOsResponse,
    TransactionUTXOsRequest, TransactionUTXOsResponse
)
from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class OnchainAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request with error handling.
        
        Args:
            method: HTTP method (get, post, etc.)
            url: API endpoint URL
            **kwargs: Additional arguments for the request
            
        Returns:
            API response as dictionary
            
        Raises:
            TapToolsError: For any API or connection errors
        """
        try:
            response = await getattr(self.client, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error in request to {url}: {str(e)}")
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            logger.error(f"Connection error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )
        except Exception as e:
            logger.error(f"Unexpected error in request to {url}: {str(e)}")
            raise TapToolsError(
                message=f"Unexpected error: {str(e)}",
                error_type=ErrorType.UNKNOWN
            )

    async def get_asset_supply(self, request: AssetSupplyRequest) -> AssetSupplyResponse:
        """
        GET /asset/supply
        
        Get onchain supply for a token.
        """
        url = "/asset/supply"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return AssetSupplyResponse(**response_data)

    async def get_address_details(self, request: AddressInfoRequest) -> AddressInfoResponse:
        """
        GET /address/info
        
        Read address info: payment cred, stake address, lovelace, multi-asset balances.
        """
        url = "/address/info"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return AddressInfoResponse(**response_data)

    async def get_address_utxos(self, request: AddressUTXOsRequest) -> AddressUTXOsResponse:
        """
        GET /address/utxos
        
        Get current UTxOs for an address or payment credential.
        """
        url = "/address/utxos"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return AddressUTXOsResponse(**response_data)

    async def get_transaction_details(self, request: TransactionUTXOsRequest) -> TransactionUTXOsResponse:
        """
        GET /transaction/utxos
        
        Retrieve UTxOs from a specific transaction.
        """
        url = "/transaction/utxos"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return TransactionUTXOsResponse(**response_data)
