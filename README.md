# TapTools API MCP
[![smithery badge](https://smithery.ai/badge/@brianbell-x/tadpoletools-mcp)](https://smithery.ai/server/@brianbell-x/tadpoletools-mcp)

A Python-based Model Context Protocol (MCP) server that provides access to the [TapTools API](https://taptools.io), enabling Large Language Models (LLMs) (like Claude or GPT) to fetch Cardano-related data (tokens, NFTs, market info, etc.). This server standardizes TapTools API operations into MCP "tools," allowing easy integration into AI workflows.

## Features

- **Async Implementation**: Uses modern Python async patterns and httpx for non-blocking IO.
- **Secure Authentication**: Reads `TAPTOOLS_API_KEY` from environment variables or `.env` file.
- **MCP-Ready**: Exposes TapTools functionality as "tools" accessible by any MCP-compliant client.
- **Token Operations**: Pricing, top tokens, market cap data, volume stats, and more.
- **NFT Operations**: NFT collection stats, trades, listings, distribution, etc.
- **Market Data**: Aggregated stats on volume, addresses, holders, and more.
- **Integration & Onchain**: Access to onchain data, block info, events, DEX pairs, etc.
- **Wallet Data**: Portfolio positions, token/NFT holdings, transaction history, trades.

## Quick Start

### Installing via Smithery

To install TapTools API Integration for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@brianbell-x/tadpoletools-mcp):

```bash
npx -y @smithery/cli install @brianbell-x/tadpoletools-mcp --client claude
```

### Manual Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/taptools-api-mcp.git
   cd taptools-api-mcp
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Set up your TapTools API key**:
   - **Option A**: Add to your `.env` file:
     ```env
     TAPTOOLS_API_KEY=your-real-taptools-api-key
     ```
   - **Option B**: Set the environment variable:
     ```bash
     export TAPTOOLS_API_KEY="your-real-taptools-api-key"
     ```

5. **Run the MCP server**:
   ```bash
   python -m taptools_api_mcp
   ```
   By default, it will run on standard input/output (stdio) for MCP integration.

6. **Test the connection** (optional):
   ```bash
   python test_connection.py
   ```

## Usage Example

If you have an MCP client (such as the `mcp` Python CLI tools), you can start the server and call any of the available tools:

```bash
# In one terminal, start the server:
python -m taptools_api_mcp

# In another terminal (or from the same, if you prefer):
mcp cli
```

Once inside the `mcp cli`, you can call tools like:
```plaintext
> tool verify_connection
```
This will verify that your TapTools API key is valid and accessible.

Or, for example, to get token market cap info:
```plaintext
> tool get_token_mcap {"unit": "lovelace"}
```
You should receive JSON data with the token’s market cap, price, supply, etc.

## API Documentation: MCP Tools

Below is a list of available MCP tools, their parameters, and brief descriptions. These tools must be called with the correct JSON payloads. All JSON requests must match the Pydantic models found in `src/taptools_api_mcp/models/`.

**1. `verify_connection`**
- **Description**: Verify TapTools API authentication.
- **Parameters**: *(No parameters.)*
- **Sample Usage**:
  ```json
  { }
  ```

**2. `get_token_mcap`**
- **Description**: Get token market cap info.
- **Parameters** (`TokenMcapRequest`):
  ```json
  {
    "unit": "string"    // required: token unit identifier
  }
  ```
- **Sample Usage**:
  ```json
  {
    "unit": "lovelace"
  }
  ```

**3. `get_token_holders`**
- **Description**: Get total number of token holders.
- **Parameters** (`TokenHoldersRequest`):
  ```json
  {
    "unit": "string"    // required: token unit identifier
  }
  ```
- **Sample Usage**:
  ```json
  {
    "unit": "lovelace"
  }
  ```

**4. `get_token_holders_top`**
- **Description**: Get top token holders.
- **Parameters** (`TokenTopHoldersRequest`):
  ```json
  {
    "unit": "string",   // required
    "page": "number",   // optional (default 1)
    "per_page": "number"// optional (default 20)
  }
  ```
- **Sample Usage**:
  ```json
  {
    "unit": "some_token_unit",
    "page": 1,
    "per_page": 5
  }
  ```

**5. `get_nft_asset_sales`**
- **Description**: Get NFT asset sales history.
- **Parameters** (`NFTAssetSalesRequest`):
  ```json
  {
    "policy": "string", // required: NFT policy ID
    "name": "string"    // optional: NFT name
  }
  ```
- **Sample Usage**:
  ```json
  {
    "policy": "abc123polid",
    "name": "coolNFT"
  }
  ```

**6. `get_nft_collection_stats`**
- **Description**: Get NFT collection stats.
- **Parameters** (`NFTCollectionStatsRequest`):
  ```json
  {
    "policy": "string"  // required: NFT collection policy ID
  }
  ```
- **Sample Usage**:
  ```json
  {
    "policy": "abc123polid"
  }
  ```

**7. `get_market_stats`**
- **Description**: Get market-wide statistics.
- **Parameters** (`MarketStatsRequest`):
  ```json
  {
    "quote": "string"    // optional, default "ADA"
  }
  ```
- **Sample Usage**:
  ```json
  {
    "quote": "USD"
  }
  ```

**8. `get_integration_asset`**
- **Description**: Get asset details by ID (integration endpoint).
- **Parameters** (`IntegrationAssetRequest`):
  ```json
  {
    "id": "string"       // required: ID of the asset
  }
  ```
- **Sample Usage**:
  ```json
  {
    "id": "asset123abc"
  }
  ```

**9. `get_asset_supply`**
- **Description**: Get onchain asset supply.
- **Parameters** (`AssetSupplyRequest`):
  ```json
  {
    "unit": "string"     // required: token unit identifier
  }
  ```
- **Sample Usage**:
  ```json
  {
    "unit": "lovelace"
  }
  ```

**10. `get_wallet_portfolio`**
- **Description**: Get wallet portfolio positions.
- **Parameters** (`WalletPortfolioPositionsRequest`):
  ```json
  {
    "address": "string"  // required: wallet address
  }
  ```
- **Sample Usage**:
  ```json
  {
    "address": "addr1xyz..."
  }
  ```

*(Additional endpoints for tokens, NFTs, onchain, etc. can be added in the same format if needed. See the `src/taptools_api_mcp/models/` folder for more possible requests.)*

## Deployment

You can containerize or host this Python MCP server on services like AWS ECS, Azure Container Instances, or Google Cloud Run. Make sure to securely store your `TAPTOOLS_API_KEY` as a secret. For Docker-based deployment:

```bash
# Example Dockerfile snippet
FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install -e .

# environment variable for TapTools API key
ENV TAPTOOLS_API_KEY=your-real-taptools-api-key

CMD ["python", "-m", "taptools_api_mcp"]
```

**Note**: The server listens on stdio by default, per the MCP spec. For advanced deployment or custom integration, you can adapt `server.py` to run with alternative transports (like sockets) if your environment requires it.

-