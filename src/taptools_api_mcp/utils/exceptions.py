from enum import Enum
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx

class ErrorCode:
    AUTHENTICATION_ERROR = -32001
    CONNECTION_ERROR = -32002
    INVALID_PARAMETERS = -32003
    API_ERROR = -32004
    RATE_LIMIT_ERROR = -32005
    NOT_FOUND_ERROR = -32006
    VALIDATION_ERROR = -32007
    TIMEOUT_ERROR = -32008
    PARSE_ERROR = -32009
    SERVER_ERROR = -32010
    BAD_GATEWAY = -32011
    SERVICE_UNAVAILABLE = -32012

class ErrorType(Enum):
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
    def from_http_error(cls, error: httpx.HTTPStatusError, message: Optional[str] = None):
        status_code = error.response.status_code
        error_type = ErrorType.UNKNOWN
        error_details = {}
        retry_after = None

        if status_code == 429:
            ra_header = error.response.headers.get("Retry-After")
            if ra_header:
                try:
                    if ra_header.isdigit():
                        retry_after = datetime.now() + timedelta(seconds=int(ra_header))
                    else:
                        retry_after = datetime.strptime(ra_header, '%a, %d %b %Y %H:%M:%S GMT')
                except:
                    pass

        try:
            error_data = error.response.json()
            error_details = error_data
            api_message = error_data.get('message')
            api_error = error_data.get('error')
            if api_message and api_error:
                message = f"{api_error}: {api_message}"
        except:
            # fallback to raw text
            if not message:
                message = error.response.text or str(error)

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
        elif status_code == 502:
            error_type = ErrorType.BAD_GATEWAY
            if not message:
                message = "Bad gateway error"
        elif status_code == 503:
            error_type = ErrorType.SERVICE_UNAVAILABLE
            if not message:
                message = "Service temporarily unavailable"
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
