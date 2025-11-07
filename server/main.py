"""
MCP server for text-based 2048 game environment using BaseHub pattern.
"""

import sys
import logging
import os

from hud.server import MCPServer
import httpx

from server.tools import MoveTool

# Configure logging to stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress MCP server logs
logging.getLogger("mcp.server.lowlevel.server").setLevel(logging.WARNING)

# Global http client (initialized during startup)
http_client = None

# Import setup/evaluate layers
from server.setup import setup as setup_hub
from server.evaluate import evaluate as evaluate_hub

# Create main server first
mcp = MCPServer(name="text-2048")


@mcp.initialize
async def initialize_environment(ctx):
    """Initialize the 2048 environment."""
    global http_client

    logger.info("Initializing 2048 environment...")

    # Connect to environment server (must be running)
    ENV_SERVER_URL = os.getenv("ENV_SERVER_URL", "http://localhost:8000")
    http_client = httpx.AsyncClient(
        base_url=ENV_SERVER_URL,
        timeout=30.0,
        headers={"User-Agent": "HUD-Text2048-Server/1.0"},
    )

    try:
        response = await http_client.get("/health")
        response.raise_for_status()
        logger.info("Connected to environment server")
    except Exception as e:
        logger.error(f"Failed to connect to environment server at {ENV_SERVER_URL}: {e}")
        raise

    # Get current game state
    response = await http_client.get("/state")
    state = response.json()

    # Log whether we're resuming or starting fresh
    if state["moves"] > 0:
        logger.info(f"Resuming game - Score: {state['score']}, Moves: {state['moves']}")
    else:
        logger.info("Starting fresh game")

    # Set up the http client on hubs and tools
    setup_hub.env = http_client
    evaluate_hub.env = http_client

    # Mount hubs
    logger.info(f"Mounting hubs: {setup_hub} and {evaluate_hub}")

    mcp.mount(setup_hub)
    mcp.mount(evaluate_hub)

    # Create and register move tool
    mcp.add_tool(MoveTool(env=http_client))

    logger.info("2048 environment ready")


if __name__ == "__main__":
    mcp.run()
