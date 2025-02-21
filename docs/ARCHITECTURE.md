# TapTools API MCP - Architecture

## Overview

The TapTools API MCP server is an application that:
1. Loads your TapTools API key from environment variables.
2. Sets up an MCP server (via `mcp-python-sdk`).
3. Defines "tools" that correspond to TapTools endpoints (e.g. `get_token_info`, `get_nft_collection`).
4. Exposes these tools over standard input/output so that any MCP-compatible LLM can invoke them.

## Components

- **server.py**: Core server logic, sets up the `TapToolsServer` with endpoints.
- **api/tokens.py**: Contains the asynchronous calls to TapTools token-related endpoints (like `/token/mcap`, `/token/holders`, etc.).
- **api/nfts.py**: NFT-related endpoints (like `/nft/collection/stats`, `/nft/collection/trades`, etc.).
- **models/**: Pydantic models to structure request/response data (optional usage).
- **test_connection.py**: Quick script to test the server using a local MCP client.

## Flow

1. **LLM** calls a tool like `get_token_info`.
2. **MCP** receives the request and routes it to the server.
3. **TapToolsServer** calls into the relevant API method (e.g., `TokensAPI.get_mcap`).
4. The server returns JSON response data or an error message.
5. The LLM sees the returned data via standard output to the MCP client.

## Error Handling

- If authentication fails, an MCP error is raised with a code like `AUTHENTICATION_ERROR`.
- If any HTTP request returns a 404 or invalid data, an MCP error is raised with `INVALID_PARAMETERS` or `API_ERROR`.
- Retries for certain HTTP errors can be configured using a decorator.

## Next Steps

- Add more tools for different TapTools endpoints (NFT, market stats, trades).
- Expand test coverage with integration tests that call real TapTools endpoints (requires a valid key with sufficient plan).
- Deploy on a cloud service for easy LLM consumption.
