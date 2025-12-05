# 2048 Text Environment

ASCII-based 2048 game as an MCP server for HUD SDK evaluation.

## Quick Start

```bash
# Build the Docker image
hud build

# Start hot-reload development server
hud dev

# Run the sample tasks
hud eval 2048_taskconfigs.json
```

## Deploy

When you're ready to use this environment in production:

1. Push your code to GitHub
2. Connect your repo at [hud.ai](https://hud.ai/environments/new)
3. Builds will trigger automatically on each push

## Tools

- **move** - Slide tiles: `move(direction="up|down|left|right")`
- **setup** - Initialize game: `setup(name="board", arguments={"board_size": 4})`
- **evaluate** - Check progress: `evaluate(name="max_number|efficiency")`

## Cursor Integration

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "text-2048": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "hud-text-2048"]
    }
  }
}
```

## Learn More

For complete documentation on building environments and running evaluations, visit [docs.hud.ai](https://docs.hud.ai).