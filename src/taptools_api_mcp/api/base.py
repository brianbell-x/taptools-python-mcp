"""
Base API class with shared functionality.
"""
import json
import logging
import time
import asyncio
from typing import Dict, Any, Optional, Tuple, Union
import httpx
from ..utils.exceptions import TapToolsError, ErrorType

logger = logging.getLogger("taptools_mcp")

# Maximum number of retries for transient errors
MAX_RETRIES = 3
# Base delay between retries (will be multiplied by attempt number)
BASE_RETRY_DELAY = 1.0
# Status codes that indicate a transient error that may be resolved by retrying
RETRYABLE_STATUS_CODES = {
    408,  # Request Timeout
    429,  # Too Many Requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504   # Gateway Timeout
}

class BaseAPI:
    """Base class for all TapTools API endpoints."""
    
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        
    def _should_retry(self, attempt: int, status_code: Optional[int], error: Exception) -> Tuple[bool, float]:
        """
        Determine if a request should be retried and the delay before next attempt.
        
        Args:
            attempt: Current attempt number (1-based)
            status_code: HTTP status code if available
            error: The exception that occurred
            
        Returns:
            Tuple of (should_retry: bool, delay: float)
        """
        # Don't retry if we've hit the maximum attempts
        if attempt >= MAX_RETRIES:
            return False, 0
            
        # Check if error type is retryable
        is_retryable = (
            isinstance(error, httpx.TimeoutException) or
            isinstance(error, httpx.NetworkError) or
            (status_code and status_code in RETRYABLE_STATUS_CODES)
        )
        
        if not is_retryable:
            return False, 0
            
        # Calculate delay with exponential backoff
        delay = BASE_RETRY_DELAY * attempt
        
        # If we have a 429 status with Retry-After header, use that
        if (
            status_code == 429 and 
            isinstance(error, httpx.HTTPStatusError) and
            error.response.headers.get('Retry-After')
        ):
            retry_after = error.response.headers['Retry-After']
            try:
                if retry_after.isdigit():
                    delay = float(retry_after)
                else:
                    # Parse HTTP date format
                    retry_time = time.strptime(retry_after, '%a, %d %b %Y %H:%M:%S GMT')
                    delay = max(0, time.mktime(retry_time) - time.time())
            except (ValueError, TypeError):
                pass
                
        return True, delay

    def _validate_response(self, response: httpx.Response) -> None:
        """
        Validate response and raise appropriate error if needed.
        
        Args:
            response: The HTTP response to validate
            
        Raises:
            httpx.HTTPStatusError: If response indicates an error
        """
        if response.status_code >= 400:
            error_info = None
            try:
                error_info = response.json()
                error_message = error_info.get('message', str(response.status_code))
                error_type = error_info.get('error', 'Unknown error')
                detailed_message = f"{error_type}: {error_message}"
            except json.JSONDecodeError:
                detailed_message = f"HTTP {response.status_code}: {response.text or 'No error details available'}"
            
            logger.error(f"API error response: {detailed_message}")
            raise httpx.HTTPStatusError(
                detailed_message,
                request=response.request,
                response=response
            )

    async def _make_request(
        self, 
        method: str, 
        url: str, 
        retry_on_error: bool = True,
        **kwargs
    ) -> Union[Dict[str, Any], list]:
        """
        Make an HTTP request with comprehensive error handling and retry logic.
        
        Args:
            method: HTTP method (get, post, etc.)
            url: API endpoint URL
            retry_on_error: Whether to retry on transient errors
            **kwargs: Additional arguments for the request
            
        Returns:
            API response as dictionary or list
            
        Raises:
            TapToolsError: For any API or connection errors
        """
        attempt = 0
        last_error = None
        
        while True:
            attempt += 1
            try:
                # Log request details for debugging
                logger.debug(
                    f"Making {method.upper()} request to {url} "
                    f"(attempt {attempt}/{MAX_RETRIES})"
                )
                logger.debug(f"Request parameters: {kwargs}")
                
                response = await getattr(self.client, method)(url, **kwargs)
                
                # Validate response and raise error if needed
                self._validate_response(response)
                
                # Parse successful response
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {str(e)}")
                    logger.debug(f"Raw response content: {response.text}")
                    raise TapToolsError(
                        message="Invalid JSON response from API",
                        error_type=ErrorType.PARSE,
                        raw_error=e
                    )
                    
            except Exception as e:
                last_error = e
                status_code = None
                
                if isinstance(e, httpx.HTTPStatusError):
                    status_code = e.response.status_code
                
                # Determine if we should retry
                if retry_on_error:
                    should_retry, delay = self._should_retry(attempt, status_code, e)
                    if should_retry:
                        logger.warning(
                            f"Request failed with error: {str(e)}. "
                            f"Retrying in {delay:.1f} seconds... "
                            f"(attempt {attempt}/{MAX_RETRIES})"
                        )
                        await asyncio.sleep(delay)
                        continue
                
                # If we shouldn't retry or have exhausted retries, raise appropriate error
                if isinstance(e, httpx.TimeoutException):
                    logger.error(f"Request timeout: {str(e)}")
                    raise TapToolsError(
                        message=f"Request timed out: {str(e)}",
                        error_type=ErrorType.TIMEOUT,
                        raw_error=e
                    )
                elif isinstance(e, httpx.NetworkError):
                    logger.error(f"Network error: {str(e)}")
                    raise TapToolsError(
                        message=f"Network error: {str(e)}",
                        error_type=ErrorType.CONNECTION,
                        raw_error=e
                    )
                elif isinstance(e, httpx.HTTPStatusError):
                    logger.error(f"HTTP error: {str(e)}")
                    raise TapToolsError.from_http_error(e)
                else:
                    logger.error(f"Unexpected error: {str(e)}")
                    raise TapToolsError(
                        message=f"Unexpected error: {str(e)}",
                        error_type=ErrorType.UNKNOWN,
                        raw_error=e
                    )
