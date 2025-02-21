# TapTools API MCP - Features

- **MCP Server**: Adheres to the Model Context Protocol spec, enabling AI assistant integration.
- **Token Tools**:
  - `get_token_mcap`: Retrieve market cap data for a token.
  - `get_token_price`: Return the aggregated price for a token.
  - `list_top_tokens`: Show top tokens by volume or market cap.
- **NFT Tools**:
  - `get_nft_sales`: Fetch sales history for an NFT asset.
  - `get_nft_collection_stats`: Get stats for a specific NFT collection.
  - `list_nft_listings`: List active NFT listings in a collection.
- **Market Tools**:
  - `get_market_stats`: Aggregated 24h volume, active addresses, etc.
  - `get_nft_market_stats`: High-level NFT market data (volume, sales).
- **Configuration**: 
  - Use `.env` or environment variables for `TAPTOOLS_API_KEY`.
- **Testing**: 
  - `test_connection.py` for quick local verification.
  - Additional tests in `tests/` directory.

Enjoy leveraging TapTools data seamlessly in your AI workflows!