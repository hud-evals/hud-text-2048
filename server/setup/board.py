"""Board-size setup function for 2048."""

from mcp.types import TextContent, ContentBlock
from . import setup


@setup.tool("board")
async def setup_board(board_size: int = 4) -> list[ContentBlock]:
    """Initialize a new game with the specified board size."""
    http_client = setup.env

    # Reset the game via HTTP
    response = await http_client.post("/reset", json={"board_size": board_size})
    response.raise_for_status()
    data = response.json()

    # Get the initial board state to show the agent
    board_display = data["board_ascii"]

    # Return the initial board display
    return [
        TextContent(
            text=f"{board_size}x{board_size} game initialized\n\n{board_display}", type="text"
        )
    ]
