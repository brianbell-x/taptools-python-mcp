"""
Custom exceptions for TapTools operations.
"""
from enum import Enum
from typing import Optional

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
    UNKNOWN = "unknown"

class TapToolsError(Exception):
    """
    Generic error for TapTools API calls.
    
    Attributes:
        message: Error message
        error_type: Type of error from ErrorType enum
        status_code: HTTP status code if applicable
        raw_error: Original error/exception if available
    """
    def __init__(
        self, 
        message: str,
        error_type: ErrorType = ErrorType.UNKNOWN,
        status_code: Optional[int] = None,
        raw_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.raw_error = raw_error

    @classmethod
    def from_http_error(cls, error, message: Optional[str] = None):
        """Create TapToolsError from an HTTP error."""
        status_code = getattr(error.response, 'status_code', None)
        error_type = ErrorType.UNKNOWN
        
        if status_code:
            if status_code == 400:
                error_type = ErrorType.VALIDATION
            elif status_code in (401, 403):
                error_type = ErrorType.AUTHENTICATION
            elif status_code == 404:
                error_type = ErrorType.NOT_FOUND
            elif status_code == 408:
                error_type = ErrorType.TIMEOUT
            elif status_code == 429:
                error_type = ErrorType.RATE_LIMIT
            elif status_code >= 400 and status_code < 500:
                error_type = ErrorType.VALIDATION
            elif status_code >= 500:
                error_type = ErrorType.API
            else:
                error_type = ErrorType.UNKNOWN

        return cls(
            message=message or str(error),
            error_type=error_type,
            status_code=status_code,
            raw_error=error
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

        return error_code, self.message
