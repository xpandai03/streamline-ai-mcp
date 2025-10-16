#!/bin/bash
# Automated setup script for Cursor MCP configuration

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_SERVER_PATH="$SCRIPT_DIR/mcp_server.py"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"

echo "🚀 Setting up YouTube Virality Detector MCP Server..."
echo ""
echo "📍 MCP Server Location: $MCP_SERVER_PATH"
echo "🐍 Python Environment: $VENV_PYTHON"
echo ""

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found at: $VENV_PYTHON"
    echo "Please run: python3.13 -m venv venv"
    exit 1
fi

# Check if MCP server file exists
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at: $MCP_SERVER_PATH"
    exit 1
fi

echo "✅ All files found!"
echo ""
echo "📋 Add this configuration to your Cursor MCP settings:"
echo ""
echo "============================================"
echo ""
echo "Name: youtube-virality-detector"
echo "Type: stdio"
echo "Command: $VENV_PYTHON"
echo "Args: [\"$MCP_SERVER_PATH\"]"
echo ""
echo "============================================"
echo ""
echo "📝 Or copy this JSON configuration:"
echo ""
cat << EOF
{
  "mcpServers": {
    "youtube-virality-detector": {
      "command": "$VENV_PYTHON",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here"
      }
    }
  }
}
EOF
echo ""
echo ""
echo "⚠️  IMPORTANT: Replace 'your-openai-api-key-here' with your actual OpenAI API key!"
echo ""
echo "📖 To add this to Cursor:"
echo "   1. Open Cursor Settings (Cmd+,)"
echo "   2. Search for 'MCP'"
echo "   3. Click 'Add MCP Server'"
echo "   4. Fill in the details from above"
echo ""
echo "✨ Done! Your MCP server is ready to use."
