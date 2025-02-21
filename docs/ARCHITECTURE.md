# TapTools API MCP - Architecture

## Overview

The TapTools API MCP server is an application that:

1. Loads your TapTools API key from environment variables or `.env` file.
2. Sets up an MCP server (via `mcp-python-sdk`) on standard input/output by default (or optionally other transports).
3. Defines "tools" that correspond to TapTools endpoints (e.g., `get_token_mcap`, `get_nft_collection_stats`, etc.).
4. Exposes these tools so any MCP-compatible LLM/client can invoke them, receiving JSON responses.

## Components

- **server.py**: Core server logic, sets up the `TapToolsServer` with endpoints and registers each tool.
- **api/**:
  - `tokens.py`: Token-related endpoints (market cap, holders, price data, trades).
  - `nfts.py`: NFT-related endpoints (collections, stats, listings, trades).
  - `market.py`: Market data endpoints (aggregated stats, active addresses, volume).
  - `integration.py`: Integration endpoints (asset, block, events, pair, exchange).
  - `onchain.py`: Onchain data endpoints (asset supply, address UTxOs, transaction details).
  - `wallet.py`: Wallet endpoints (portfolio positions, trades, historical value).
- **models/**: Pydantic models specifying request/response schemas for each endpoint (tokens, NFTs, market, etc.).
- **utils/**: Utility modules (custom exceptions, error handling).
- **test_connection.py**: A script to test the server using a local MCP client session.
- **tests/**: Comprehensive test suite (Pytest), including unit and integration tests for each API module and the server.

## Flow

1. An **LLM** (or other MCP client) calls a tool, e.g. `get_token_mcap`.
2. **MCP** routes the call to the server with JSON parameters.
3. **TapToolsServer** delegates to the relevant API method (e.g., `TokensAPI.get_token_mcap`).
4. The API method issues an HTTP request to TapTools with the provided parameters, returning JSON data.
5. The server returns the data to the LLM through MCP in JSON format.

## Error Handling

- All internal HTTPX errors or TapTools API issues raise custom `TapToolsError`, which is converted to an `McpError` with appropriate codes (e.g., authentication, rate limits, invalid parameters).
- Tools must pass valid JSON payloads matching the Pydantic models; otherwise `McpError` is raised for invalid parameters.

## Additional Notes

- For advanced usage or custom expansions, you can define new endpoints in `api/` and create corresponding Pydantic models in `models/`.
- All network calls are asynchronous; concurrency is handled by `asyncio`.
