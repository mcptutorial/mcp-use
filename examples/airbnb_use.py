"""
Example demonstrating how to use mcp_use with Airbnb.

This example shows how to connect an LLM to Airbnb through MCP tools
to perform tasks like searching for accommodations.

Special Thanks to https://github.com/openbnb-org/mcp-server-airbnb for the server.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from mcp_use import MCPAgent, MCPClient


async def run_airbnb_example():
    """Run an example using Airbnb MCP server."""
    # Load environment variables
    load_dotenv()

    # Create MCPClient with Airbnb configuration
    client = MCPClient.from_config_file(os.path.join(os.path.dirname(__file__), "airbnb_mcp.json"))
    # Create LLM - you can choose between different models
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    # Alternative models:
    # llm = init_chat_model(model="llama-3.1-8b-instant", model_provider="groq")
    # llm = ChatOpenAI(model="gpt-4o")
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    try:
        # Run a query to search for accommodations
        result = await agent.run(
            "Find me a nice place to stay in Barcelona for 2 adults "
            "for a week in August. I prefer places with a pool and "
            "good reviews. Show me the top 3 options.",
            max_steps=30,
        )
        print(f"\nResult: {result}")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_airbnb_example())
