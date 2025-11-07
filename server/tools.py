"""Move tool for the 2048 game."""

import logging
from typing import Any
from mcp.types import TextContent, ContentBlock
from hud.tools.base import BaseTool
import httpx

logger = logging.getLogger(__name__)


class MoveTool(BaseTool):
    """Tool for making moves in the 2048 game."""

    def __init__(self, env: Any = None):
        """Initialize the move tool.

        Args:
            context: The game instance
        """
        super().__init__(
            env=env,
            name="move",
            title="Move Tiles",
            description="Make a move in the 2048 game by sliding tiles in a direction",
        )

    async def __call__(self, direction: str) -> list[ContentBlock]:
        """Make a move in the 2048 game.

        Args:
            direction: The direction to move ('up', 'down', 'left', 'right')
        """
        if self.env is None:
            return [TextContent(text="ERROR: Game not initialized. Run setup first.", type="text")]

        direction = direction.lower()
        if direction not in ["up", "down", "left", "right"]:
            return [
                TextContent(
                    text=f"ERROR: Invalid direction: {direction}. Use: up, down, left, right",
                    type="text",
                )
            ]

        # Make the move using HTTP client
        try:
            response = await self.env.post("/move", json={"direction": direction})

            if response.status_code == 400:
                error_data = response.json()
                return [
                    TextContent(
                        text=f"ERROR: {error_data.get('detail', 'Invalid move')}",
                        type="text",
                    )
                ]

            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            return [
                TextContent(
                    text=f"ERROR: Failed to make move: {e}",
                    type="text",
                )
            ]

        # Format response
        text = f"Moved {direction.upper()}\n"
        text += f"Score: {data['score']}\n"
        text += f"{data['board_ascii']}"

        if data["game_over"]:
            text += "\nGAME OVER!"

        return [TextContent(text=text, type="text")]
