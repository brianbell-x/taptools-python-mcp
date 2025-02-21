"""
Custom exceptions for TapTools operations.
"""
from enum import Enum
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class ErrorCode:
    """Error codes for TapTools MCP server."""
    AUTHENTICATION_ERROR = -32001  # Invalid or unauthorized API key
    CONNECTION_ERROR = -32002      # Network/connection issues
    INVALID_PARAMETERS = -32003    # Invalid request parameters
    API_ERROR = -32004            # Generic API error
    RATE_LIMIT_ERROR = -32005     # Rate limit exceeded
    NOT_FOUND_ERROR = -32006      # Resource not found
    VALIDATION_ERROR = -32007     # Input validation error
    TIMEOUT_ERROR = -32008        # Request timeout
    PARSE_ERROR = -32009          # Response parsing error
    SERVER_ERROR = -32010         # Server-side error
    BAD_GATEWAY = -32011         # Bad gateway error
    SERVICE_UNAVAILABLE = -32012  # Service temporarily unavailable

class ErrorType(Enum):
    """Types of TapTools errors."""
    AUTHENTICATION = "authentication"
    CONNECTION = "connection"
    VALIDATION = "validation"
    RATE_LIMIT = "rate_limit"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    PARSE = "parse"
    API = "api"
    SERVER = "server"
    BAD_GATEWAY = "bad_gateway"
    SERVICE_UNAVAILABLE = "service_unavailable"
    UNKNOWN = "unknown"

class TapToolsError(Exception):
    """
    Generic error for TapTools API calls.
    
    Attributes:
        message: Error message
        error_type: Type of error from ErrorType enum
        status_code: HTTP status code if applicable
        raw_error: Original error/exception if available
        retry_after: Optional timestamp when rate-limited requests can resume
        error_details: Additional error details from the API response
    """
    def __init__(
        self, 
        message: str,
        error_type: ErrorType = ErrorType.UNKNOWN,
        status_code: Optional[int] = None,
        raw_error: Optional[Exception] = None,
        retry_after: Optional[datetime] = None,
        error_details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.raw_error = raw_error
        self.retry_after = retry_after
        self.error_details = error_details or {}

    @classmethod
    def from_http_error(cls, error, message: Optional[str] = None):
        """
        Create TapToolsError from an HTTP error with enhanced error details.
        
        Args:
            error: The HTTP error
            message: Optional override message
            
        Returns:
            TapToolsError instance with detailed error information
        """
        status_code = getattr(error.response, 'status_code', None)
        error_type = ErrorType.UNKNOWN
        error_details = {}
        retry_after = None
        
        # Extract retry-after header for rate limits
        if status_code == 429:
            retry_after_header = error.response.headers.get('Retry-After')
            if retry_after_header:
                try:
                    if retry_after_header.isdigit():
                        # If Retry-After is in seconds
                        retry_after = datetime.now() + timedelta(seconds=int(retry_after_header))
                    else:
                        # If Retry-After is an HTTP date
                        retry_after = datetime.strptime(retry_after_header, '%a, %d %b %Y %H:%M:%S GMT')
                except (ValueError, TypeError):
                    pass

        # Try to extract error details from response JSON
        try:
            error_data = error.response.json()
            error_details = error_data
            api_message = error_data.get('message')
            api_error = error_data.get('error')
            if api_message and api_error:
                message = f"{api_error}: {api_message}"
        except (json.JSONDecodeError, AttributeError):
            # Use raw response text if JSON parsing fails
            if hasattr(error.response, 'text') and error.response.text:
                message = error.response.text
            elif not message:
                message = str(error)
        
        if status_code:
            if status_code == 400:
                error_type = ErrorType.VALIDATION
                if not message:
                    message = "Invalid request parameters"
            elif status_code in (401, 403):
                error_type = ErrorType.AUTHENTICATION
                if not message:
                    message = "Authentication failed or insufficient permissions"
            elif status_code == 404:
                error_type = ErrorType.NOT_FOUND
                if not message:
                    message = "Requested resource not found"
            elif status_code == 408:
                error_type = ErrorType.TIMEOUT
                if not message:
                    message = "Request timed out"
            elif status_code == 429:
                error_type = ErrorType.RATE_LIMIT
                if not message:
                    message = "Rate limit exceeded"
                    if retry_after:
                        message += f" (retry after {retry_after.strftime('%Y-%m-%d %H:%M:%S')})"
            elif status_code == 502:
                error_type = ErrorType.BAD_GATEWAY
                if not message:
                    message = "Bad gateway error"
            elif status_code == 503:
                error_type = ErrorType.SERVICE_UNAVAILABLE
                if not message:
                    message = "Service temporarily unavailable"
            elif status_code >= 400 and status_code < 500:
                error_type = ErrorType.VALIDATION
                if not message:
                    message = f"Client error: HTTP {status_code}"
            elif status_code >= 500:
                error_type = ErrorType.SERVER
                if not message:
                    message = f"Server error: HTTP {status_code}"
            else:
                error_type = ErrorType.UNKNOWN
                if not message:
                    message = f"Unknown error: HTTP {status_code}"

        return cls(
            message=message or str(error),
            error_type=error_type,
            status_code=status_code,
            raw_error=error,
            retry_after=retry_after,
            error_details=error_details
        )

    def to_mcp_error(self):
        """Convert to MCP error code and message."""
        error_code = ErrorCode.API_ERROR  # Default
        
        if self.error_type == ErrorType.AUTHENTICATION:
            error_code = ErrorCode.AUTHENTICATION_ERROR
        elif self.error_type == ErrorType.CONNECTION:
            error_code = ErrorCode.CONNECTION_ERROR
        elif self.error_type == ErrorType.VALIDATION:
            error_code = ErrorCode.VALIDATION_ERROR
        elif self.error_type == ErrorType.RATE_LIMIT:
            error_code = ErrorCode.RATE_LIMIT_ERROR
        elif self.error_type == ErrorType.NOT_FOUND:
            error_code = ErrorCode.NOT_FOUND_ERROR
        elif self.error_type == ErrorType.TIMEOUT:
            error_code = ErrorCode.TIMEOUT_ERROR
        elif self.error_type == ErrorType.PARSE:
            error_code = ErrorCode.PARSE_ERROR
        elif self.error_type == ErrorType.SERVER:
            error_code = ErrorCode.SERVER_ERROR
        elif self.error_type == ErrorType.BAD_GATEWAY:
            error_code = ErrorCode.BAD_GATEWAY
        elif self.error_type == ErrorType.SERVICE_UNAVAILABLE:
            error_code = ErrorCode.SERVICE_UNAVAILABLE

        message = self.message
        if self.error_details:
            # Add any additional error details if available
            details = []
            if 'error' in self.error_details and self.error_details['error'] != message:
                details.append(self.error_details['error'])
            if 'status' in self.error_details:
                details.append(f"Status: {self.error_details['status']}")
            if details:
                message = f"{message} ({'; '.join(details)})"

        return error_code, message
