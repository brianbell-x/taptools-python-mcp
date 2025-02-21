# Test Coverage Matrix

Below is the current status of test coverage for each tool/feature. Nearly every endpoint has dedicated unit tests (mocked HTTP calls) and integration-like tests within the `tests/` directory.

| Tool/Feature                         | Unit Tests | Integration Tests | Status      |
|--------------------------------------|------------|-------------------|-------------|
| **Token Tools** (`tokens.py`)        | Yes        | Yes              | Complete    |
| **NFT Tools** (`nfts.py`)            | Yes        | Yes              | Complete    |
| **Market Tools** (`market.py`)       | Yes        | Yes              | Complete    |
| **Integration Tools** (`integration.py`) | Yes    | Yes              | Complete    |
| **Onchain Tools** (`onchain.py`)     | Yes        | Yes              | Complete    |
| **Wallet Tools** (`wallet.py`)       | Yes        | Yes              | Complete    |
| **Authentication**                   | Yes        | Yes              | Complete    |
| **Error Handling**                   | Yes        | Yes              | Complete    |
| **Deployment** (Docker etc.)         | N/A        | N/A              | Not Tested  |

> Note: “Integration Tests” here typically mock or selectively call the real TapTools endpoints. Full end-to-end integration may require a valid API key and real network calls. Most modules are thoroughly tested within `tests/`.