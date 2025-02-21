"""
IntegrationAPI for integration-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

class IntegrationAPI:
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

    async def get_asset(self, id: str) -> Dict[str, Any]:
        """
        GET /integration/asset
        
        Return details of a token by ID.
        """
        url = "/integration/asset"
        params = {"id": id}
        return await self._make_request("get", url, params=params)

    async def get_block(self, number: Optional[int] = None, timestamp: Optional[int] = None) -> Dict[str, Any]:
        """
        GET /integration/block
        
        Return a block by number or timestamp.
        """
        url = "/integration/block"
        params = {}
        if number is not None:
            params["number"] = number
        if timestamp is not None:
            params["timestamp"] = timestamp
        return await self._make_request("get", url, params=params)

    async def get_events(self, from_block: int, to_block: int, limit: int = 1000) -> Dict[str, Any]:
        """
        GET /integration/events
        
        List events within a block range.
        """
        url = "/integration/events"
        params = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "limit": limit
        }
        return await self._make_request("get", url, params=params)

    async def get_exchange(self, id: str) -> Dict[str, Any]:
        """
        GET /integration/exchange
        
        Return DEX details by factory address/ID.
        """
        url = "/integration/exchange"
        params = {"id": id}
        return await self._make_request("get", url, params=params)

    async def get_latest_block(self) -> Dict[str, Any]:
        """
        GET /integration/latest-block
        
        Get the latest processed block info.
        """
        url = "/integration/latest-block"
        return await self._make_request("get", url)

    async def get_pair(self, id: str) -> Dict[str, Any]:
        """
        GET /integration/pair
        
        Return pair/pool details by address.
        """
        url = "/integration/pair"
        params = {"id": id}
        return await self._make_request("get", url, params=params)
