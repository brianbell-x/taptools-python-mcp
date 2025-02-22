import logging
import httpx
from mcp.server.fastmcp import Context

from ..utils.exceptions import TapToolsError, ErrorType
from ..models.nfts import (
    NFTAssetSalesRequest, NFTAssetSalesResponse,
    NFTAssetStatsRequest, NFTAssetStatsResponse,
    NFTAssetTraitsRequest, NFTAssetTraitsResponse,
    NFTCollectionAssetsRequest, NFTCollectionAssetsResponse,
    NFTCollectionInfoRequest, NFTCollectionInfoResponse,
    NFTCollectionStatsRequest, NFTCollectionStatsResponse,
    NFTCollectionExtendedStatsRequest, NFTCollectionExtendedStatsResponse,
    NFTCollectionHoldersDistributionRequest, NFTCollectionHoldersDistributionResponse,
    NFTCollectionTopHoldersRequest, NFTCollectionTopHoldersResponse,
    NFTCollectionHoldersTrendedRequest, NFTCollectionHoldersTrendedResponse,
    NFTCollectionListingsRequest, NFTCollectionListingsResponse,
    NFTCollectionListingsDepthRequest, NFTCollectionListingsDepthResponse,
    NFTCollectionIndividualListingsRequest, NFTCollectionIndividualListingsResponse,
    NFTCollectionListingsTrendedRequest, NFTCollectionListingsTrendedResponse,
    NFTCollectionOHLCVRequest, NFTCollectionOHLCVResponse,
    NFTCollectionTradesRequest, NFTCollectionTradesResponse,
    NFTCollectionTradeStatsRequest, NFTCollectionTradeStatsResponse,
    NFTCollectionVolumeTrendedRequest, NFTCollectionVolumeTrendedResponse,
    NFTCollectionTraitPricesRequest, NFTCollectionTraitPricesResponse,
    NFTCollectionTraitRarityRequest, NFTCollectionTraitRarityResponse,
    NFTCollectionTraitRarityRankRequest, NFTCollectionTraitRarityRankResponse,
    NFTMarketStatsRequest, NFTMarketStatsResponse,
    NFTMarketExtendedStatsRequest, NFTMarketExtendedStatsResponse,
    NFTMarketVolumeTrendedRequest, NFTMarketVolumeTrendedResponse,
    NFTMarketplaceStatsRequest, NFTMarketplaceStatsResponse,
    NFTTopTimeframeRequest, NFTTopTimeframeResponse,
    NFTTopVolumeRequest, NFTTopVolumeResponse,
    NFTTopVolumeExtendedRequest, NFTTopVolumeExtendedResponse
)

logger = logging.getLogger("taptools_mcp.nfts")

class NftsAPI:
    async def get_nft_asset_sales(self, request: NFTAssetSalesRequest, ctx: Context) -> NFTAssetSalesResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/nft/asset/sales", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return NFTAssetSalesResponse(sales=resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    async def get_nft_asset_stats(self, request: NFTAssetStatsRequest, ctx: Context) -> NFTAssetStatsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/nft/asset/stats", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return NFTAssetStatsResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    # ... additional methods omitted for brevity, same pattern ...

    async def get_nft_collection_stats(self, request: NFTCollectionStatsRequest, ctx: Context) -> NFTCollectionStatsResponse:
        client = ctx.request_context.lifespan_context["client"]
        try:
            resp = await client.get("/nft/collection/stats", params=request.dict(exclude_none=True))
            resp.raise_for_status()
            return NFTCollectionStatsResponse(**resp.json())
        except httpx.HTTPStatusError as e:
            raise TapToolsError.from_http_error(e)
        except httpx.RequestError as e:
            raise TapToolsError(
                message=f"Connection error: {str(e)}",
                error_type=ErrorType.CONNECTION
            )

    # ... define the rest similarly ...
