import asyncio
import json
from mcp.client.client import Client
from mcp.client.stdio import StdioClientTransport

async def test_connection():
    """
    Test script to launch the TapTools MCP server via stdio and call the 'verify_connection' tool.
    """
    transport = StdioClientTransport("python -m taptools_api_mcp")
    client = Client()

    await client.connect(transport)
    try:
        # Initialize
        init_response = await client.initialize(
            protocol_version="1.0.0",
            capabilities={},
            client_info={
                "name": "test-connection",
                "version": "0.1.0"
            }
        )
        print("Init Response:", json.dumps(init_response, indent=2))

        # Call verify_connection
        resp = await client.call_tool("verify_connection", {})
        print("\nVerify Connection Response:\n", resp)

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
