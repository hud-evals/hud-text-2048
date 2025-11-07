"""
FastAPI server for 2048 game environment.
"""

import logging
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .game import Game2048

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


class MoveRequest(BaseModel):
    direction: str


class ResetRequest(BaseModel):
    board_size: int = 4


class StateResponse(BaseModel):
    board: list[list[int]]
    score: int
    moves: int
    game_over: bool
    won: bool
    highest_tile: int
    board_ascii: str


game = Game2048()

app = FastAPI(
    title="2048 Game Environment API",
    description="HTTP API for 2048 game state",
    version="0.1.0",
)


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"status": "healthy"}


@app.get("/state", response_model=StateResponse)
async def get_state() -> StateResponse:
    state = game.get_state()
    return StateResponse(
        board=state["board"],
        score=state["score"],
        moves=state["moves"],
        game_over=state["game_over"],
        won=state["won"],
        highest_tile=state["highest_tile"],
        board_ascii=game.get_board_ascii(),
    )


@app.post("/move")
async def make_move(request: MoveRequest) -> Dict[str, Any]:
    direction = request.direction.lower()
    if direction not in ["up", "down", "left", "right"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid direction: {direction}. Use: up, down, left, right",
        )

    moved = game.move(direction)
    if not moved:
        raise HTTPException(
            status_code=400, detail=f"Cannot move {direction} - no valid moves in that direction"
        )

    state = game.get_state()
    return {
        "success": True,
        "board": state["board"],
        "score": state["score"],
        "moves": state["moves"],
        "game_over": state["game_over"],
        "won": state["won"],
        "highest_tile": state["highest_tile"],
        "board_ascii": game.get_board_ascii(),
    }


@app.post("/reset")
async def reset_game(request: ResetRequest) -> Dict[str, Any]:
    game.reset(size=request.board_size)
    state = game.get_state()
    return {
        "success": True,
        "board": state["board"],
        "score": state["score"],
        "moves": state["moves"],
        "game_over": state["game_over"],
        "won": state["won"],
        "highest_tile": state["highest_tile"],
        "board_ascii": game.get_board_ascii(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
