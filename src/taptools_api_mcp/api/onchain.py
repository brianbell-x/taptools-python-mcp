"""
OnchainAPI for onchain data endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

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

    async def get_asset_supply(self, unit: str) -> Dict[str, Any]:
        """
        GET /asset/supply
        
        Get onchain supply for a token.
        """
        url = "/asset/supply"
        params = {"unit": unit}
        return await self._make_request("get", url, params=params)

    async def get_address_info(
        self, 
        address: Optional[str] = None, 
        payment_cred: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        GET /address/info
        
        Read address info: payment cred, stake address, lovelace, multi-asset balances.
        """
        url = "/address/info"
        params = {}
        if address:
            params["address"] = address
        if payment_cred:
            params["paymentCred"] = payment_cred
        return await self._make_request("get", url, params=params)

    async def get_address_utxos(
        self, 
        address: Optional[str] = None, 
        payment_cred: Optional[str] = None, 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict[str, Any]:
        """
        GET /address/utxos
        
        Get current UTxOs for an address or payment credential.
        """
        url = "/address/utxos"
        params = {
            "page": page,
            "perPage": per_page
        }
        if address:
            params["address"] = address
        if payment_cred:
            params["paymentCred"] = payment_cred
        return await self._make_request("get", url, params=params)

    async def get_transaction_utxos(self, hash: str) -> Dict[str, Any]:
        """
        GET /transaction/utxos
        
        Retrieve UTxOs from a specific transaction.
        """
        url = "/transaction/utxos"
        params = {"hash": hash}
        return await self._make_request("get", url, params=params)
