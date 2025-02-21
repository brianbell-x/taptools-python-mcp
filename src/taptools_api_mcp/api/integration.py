"""
IntegrationAPI for integration-related endpoints.
"""
import logging
import httpx
from typing import Dict, Any, Optional

from ..models.integration import (
    IntegrationAssetRequest, IntegrationAssetResponse,
    IntegrationBlockRequest, IntegrationBlockResponse,
    IntegrationEventsRequest, IntegrationEventsResponse,
    IntegrationExchangeRequest, IntegrationExchangeResponse,
    IntegrationLatestBlockResponse,
    IntegrationPairRequest, IntegrationPairResponse,
    IntegrationPolicyAssetsRequest, IntegrationPolicyAssetsResponse
)
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

    async def get_asset(self, request: IntegrationAssetRequest) -> IntegrationAssetResponse:
        """
        GET /integration/asset
        
        Return details of a token by ID.
        """
        url = "/integration/asset"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationAssetResponse(asset=response_data)

    async def get_block(self, request: IntegrationBlockRequest) -> IntegrationBlockResponse:
        """
        GET /integration/block
        
        Return a block by number or timestamp.
        """
        url = "/integration/block"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationBlockResponse(block=response_data)

    async def get_events(self, request: IntegrationEventsRequest) -> IntegrationEventsResponse:
        """
        GET /integration/events
        
        List events within a block range.
        """
        url = "/integration/events"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationEventsResponse(events=response_data)

    async def get_exchange(self, request: IntegrationExchangeRequest) -> IntegrationExchangeResponse:
        """
        GET /integration/exchange
        
        Return DEX details by factory address/ID.
        """
        url = "/integration/exchange"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationExchangeResponse(exchange=response_data)

    async def get_latest_block(self) -> IntegrationLatestBlockResponse:
        """
        GET /integration/latest-block
        
        Get the latest processed block info.
        """
        url = "/integration/latest-block"
        response_data = await self._make_request("get", url)
        return IntegrationLatestBlockResponse(block=response_data)

    async def get_pair(self, request: IntegrationPairRequest) -> IntegrationPairResponse:
        """
        GET /integration/pair
        
        Return pair/pool details by address.
        """
        url = "/integration/pair"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationPairResponse(pair=response_data)

    async def get_policy_assets(self, request: IntegrationPolicyAssetsRequest) -> IntegrationPolicyAssetsResponse:
        """
        GET /integration/policy/assets
        
        Return assets under a given policy ID.
        """
        url = "/integration/policy/assets"
        params = request.model_dump(exclude_none=True)
        response_data = await self._make_request("get", url, params=params)
        return IntegrationPolicyAssetsResponse(**response_data)
