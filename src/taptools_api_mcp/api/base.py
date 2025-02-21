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
        self._base_url = str(client.base_url)

    @property
    def base_url(self) -> str:
        """Get the base URL for the API."""
        return self._base_url

    async def verify_connection(self) -> Dict[str, bool]:
        """
        Verify API connection by making a test request.
        
        Returns:
            Dict with success status
        """
        await self._make_request('get', '/token/quote/available')
        return {"success": True}
        
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
        Validate response and raise appropriate TapToolsError if needed.
        
        Args:
            response: The HTTP response to validate
            
        Raises:
            TapToolsError: If response indicates an error
        """
        if response.status_code >= 400:
            error_details = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'url': str(response.url)
            }
            
            try:
                error_info = response.json()
                error_message = error_info.get('message', str(response.status_code))
                error_type = error_info.get('error', 'Unknown error')
                detailed_message = f"{error_type}: {error_message}"
                error_details['api_error'] = error_info
            except json.JSONDecodeError:
                # Truncate response text for logging
                truncated_text = response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                detailed_message = f"HTTP {response.status_code}: {truncated_text or 'No error details available'}"
                error_details['response_text'] = truncated_text
                error_details['content_type'] = response.headers.get('content-type')
            
            logger.error(f"API error response: {detailed_message}", extra=error_details)
            
            # Convert to httpx.HTTPStatusError first to maintain compatibility with from_http_error
            http_error = httpx.HTTPStatusError(
                detailed_message,
                request=response.request,
                response=response
            )
            
            # Then convert to TapToolsError with all context
            raise TapToolsError.from_http_error(
                http_error,
                message=detailed_message  # Use our enhanced message
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
        request_context = {
            'method': method.upper(),
            'url': url,
            'kwargs': kwargs,
            'max_retries': MAX_RETRIES
        }
        
        while True:
            attempt += 1
            request_context['attempt'] = attempt
            
            try:
                # Enhanced request logging
                logger.debug(
                    f"Making {method.upper()} request to {url} "
                    f"(attempt {attempt}/{MAX_RETRIES})",
                    extra=request_context
                )
                
                response = await getattr(self.client, method)(url, **kwargs)
                
                # Validate response and raise error if needed
                self._validate_response(response)
                
                # Parse successful response
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    # Truncate response text for logging to avoid overwhelming logs
                    truncated_text = response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                    logger.error(
                        f"Failed to parse JSON response: {str(e)}",
                        extra={'response_text': truncated_text}
                    )
                    
                    raise TapToolsError(
                        message=f"Invalid JSON response from API: {str(e)}",
                        error_type=ErrorType.PARSE,
                        raw_error=e,
                        error_details={
                            'response_text': truncated_text,
                            'content_type': response.headers.get('content-type'),
                            'content_length': len(response.text)
                        }
                    )
                    
            except Exception as e:
                last_error = e
                status_code = getattr(e.response, 'status_code', None) if isinstance(e, httpx.HTTPStatusError) else None
                error_context = {
                    **request_context,
                    'error_type': type(e).__name__,
                    'status_code': status_code
                }
                
                # Determine if we should retry
                if retry_on_error:
                    should_retry, delay = self._should_retry(attempt, status_code, e)
                    if should_retry:
                        logger.warning(
                            f"Request failed ({type(e).__name__}): {str(e)}. "
                            f"Retrying in {delay:.1f}s (attempt {attempt}/{MAX_RETRIES})",
                            extra=error_context
                        )
                        await asyncio.sleep(delay)
                        continue
                
                # Convert all errors to TapToolsError with enhanced context
                if isinstance(e, TapToolsError):
                    # Re-raise TapToolsError but add request context
                    e.error_details = {
                        **(e.error_details or {}),
                        'request': {
                            'method': method,
                            'url': url,
                            'attempt': attempt
                        }
                    }
                    raise
                elif isinstance(e, httpx.TimeoutException):
                    raise TapToolsError(
                        message=f"Request timed out after {self.client.timeout.read} seconds",
                        error_type=ErrorType.TIMEOUT,
                        raw_error=e,
                        error_details={'timeout_value': self.client.timeout.read}
                    )
                elif isinstance(e, httpx.NetworkError):
                    raise TapToolsError(
                        message=f"Network error during {method.upper()} request to {url}: {str(e)}",
                        error_type=ErrorType.CONNECTION,
                        raw_error=e,
                        error_details={'request_context': request_context}
                    )
                elif isinstance(e, httpx.HTTPStatusError):
                    # from_http_error already provides good error context
                    raise TapToolsError.from_http_error(e)
                else:
                    raise TapToolsError(
                        message=f"Unexpected error during API request: {str(e)}",
                        error_type=ErrorType.UNKNOWN,
                        raw_error=e,
                        error_details={
                            'request_context': request_context,
                            'error_class': e.__class__.__name__
                        }
                    )
