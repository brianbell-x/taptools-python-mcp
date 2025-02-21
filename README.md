# TapTools API MCP

A Python-based Model Context Protocol (MCP) server that provides access to the [TapTools API](https://taptools.io), enabling Large Language Models (LLMs) (like Claude or GPT) to fetch Cardano-related data (tokens, NFTs, market info, etc.). This server standardizes TapTools API operations into MCP "tools," allowing easy integration into AI workflows.

## Features

- **Async Implementation**: Uses modern Python async patterns and httpx for non-blocking IO.
- **Secure Authentication**: Reads `TAPTOOLS_API_KEY` from environment variables or `.env` file.
- **MCP-Ready**: Exposes TapTools functionality as "tools" accessible by any MCP-compliant client.
- **Token Operations**: Pricing, top tokens, market cap data, volume stats, and more.
- **NFT Operations**: NFT collection stats, trades, listings, distribution, etc.
- **Market Data**: Aggregated stats on volume, addresses, holders, and more.

## Requirements

- Python 3.10 or higher
- TapTools API Key (visit [taptools.io](https://taptools.io) for an account; the key must be placed in your environment)

## Quick Start

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
   - Option A: Add to your `.env` file:
     ```env
     TAPTOOLS_API_KEY=your-real-taptools-api-key
     ```
   - Option B: Set the environment variable:
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

## Deploying

You can containerize or host this Python MCP server on services like AWS ECS, Azure Container Instances, or Google Cloud Run. Make sure to securely store your `TAPTOOLS_API_KEY` as a secret.

## Further Documentation

See the [docs/](docs/) folder for architecture and usage details, as well as the [TapTools API docs](https://taptools.io).
