# YouTube Virality Analyzer - ChatGPT App SDK Wrapper

TypeScript Express server that wraps the Python FastMCP backend and provides ChatGPT App integration with custom widgets.

## Architecture

```
ChatGPT → TypeScript Wrapper (port 3000) → Python FastMCP (port 8080)
```

## Features

- **MCP Protocol**: Implements Model Context Protocol using @modelcontextprotocol/sdk
- **Tool Proxying**: Forwards requests to Python backend for video processing
- **Custom Widgets**: Responsive UI components for ChatGPT interface
- **SSE Streaming**: Server-Sent Events for real-time communication

## Setup

### Prerequisites

- Node.js 20+ installed
- Python FastMCP backend running on port 8080 (or configured URL)
- AWS ECS deployment (optional, for production)

### Installation

```bash
cd typescript-sdk
npm install
```

### Configuration

Create `.env` file:

```bash
# Copy example file
cp .env.example .env

# Edit with your settings
PYTHON_BACKEND_URL=http://localhost:8080  # or AWS ECS URL
PORT=3000
NODE_ENV=development
```

### Development

```bash
# Start TypeScript wrapper
npm run dev

# In another terminal, expose via HTTPS
cloudflared tunnel --url http://localhost:3000
```

The server will start on `http://localhost:3000` with:
- SSE endpoint: `/sse`
- Health check: `/health`
- Tools list: `/mcp/tools`
- Widget files: `/widget/*`

## ChatGPT Integration

### 1. Expose via HTTPS

```bash
cloudflared tunnel --url http://localhost:3000
# Copy the HTTPS URL (e.g., https://xyz.trycloudflare.com)
```

### 2. Register in ChatGPT

1. Open ChatGPT → Settings → Apps & Connectors
2. Enable **Developer Mode**
3. Click **Create App**
4. Fill in:
   - Name: `YouTube Virality Analyzer`
   - Description: `Find viral moments in YouTube videos`
   - MCP Server URL: `https://xyz.trycloudflare.com` (your tunnel URL)
5. Click **Create**

### 3. Test the Tool

In ChatGPT, type:
```
Analyze this video for viral moments:
https://youtube.com/watch?v=dQw4w9WgXcQ
```

## Project Structure

```
typescript-sdk/
├── src/
│   ├── index.ts              # Main Express server
│   ├── tools/                # Tool definitions (future)
│   └── widgets/              # Widget components (future)
├── public/                   # Built widget files
├── dist/                     # Compiled TypeScript
├── package.json
├── tsconfig.json
└── .env
```

## API Endpoints

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "yt-mcp-typescript-wrapper",
  "python_backend": "http://localhost:8080",
  "version": "1.0.0"
}
```

### `GET /sse`
Server-Sent Events endpoint for MCP protocol

**Headers:**
```
Accept: text/event-stream
```

### `GET /mcp/tools`
List available tools (debug endpoint)

**Response:**
```json
{
  "tools": [
    {
      "name": "analyze_youtube_video",
      "description": "...",
      "inputSchema": {...}
    }
  ]
}
```

### `GET /widget/*`
Serve widget HTML/JS files

## Tool: analyze_youtube_video

Analyzes a YouTube video to find viral clip moments.

**Input Schema:**
```typescript
{
  url: string;          // YouTube video URL (required)
  max_clips?: number;   // Max clips to return (default: 4)
  whisper_model?: string; // Whisper model (default: "base")
}
```

**Output:**
```json
{
  "video_title": "...",
  "video_url": "...",
  "viral_clips_found": 4,
  "top_clips": [
    {
      "rank": 1,
      "hook": "...",
      "timestamp": "0:10-0:35",
      "virality_score": "0.92/1.0",
      "why_viral": "...",
      "transcript_preview": "..."
    }
  ]
}
```

## Troubleshooting

### ChatGPT App Connector Fails

1. **Check SSE endpoint:**
   ```bash
   curl -N -H "Accept: text/event-stream" http://localhost:3000/sse
   ```
   Should stream events, not return HTML

2. **Verify Python backend:**
   ```bash
   curl http://localhost:8080/health
   ```
   Should return `{"status": "healthy"}`

3. **Check logs:**
   ```bash
   npm run dev  # Watch console output
   ```

### Tool Not Discovered

1. **Test /mcp/tools endpoint:**
   ```bash
   curl http://localhost:3000/mcp/tools
   ```
   Should return tool list

2. **Verify HTTPS tunnel:**
   ```bash
   curl https://your-tunnel-url.trycloudflare.com/health
   ```

### Python Backend Timeout

1. **Increase timeout in src/index.ts:**
   ```typescript
   timeout: 300000  // 5 minutes
   ```

2. **Check Python backend logs:**
   ```bash
   aws logs tail /ecs/yt-mcp --follow
   ```

## Development Commands

```bash
# Install dependencies
npm install

# Run in development mode (with auto-reload)
npm run dev

# Build TypeScript to JavaScript
npm run build

# Run production build
npm start

# Build widget (future)
npm run build:widget
```

## Production Deployment

### Option 1: Standalone Node Server

```bash
# Build
npm run build

# Run
NODE_ENV=production PYTHON_BACKEND_URL=https://your-ecs-url.com npm start
```

### Option 2: Docker with Python Backend

See `IMPLEMENTATION_ROADMAP.md` Phase 4 for unified deployment strategy.

## Next Steps

1. ✅ Complete TypeScript wrapper scaffold
2. ⏳ Add widget UI components (clip-viewer)
3. ⏳ Test with Python backend locally
4. ⏳ Deploy unified stack to AWS
5. ⏳ Register in ChatGPT App Store

## Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [@modelcontextprotocol/sdk](https://github.com/modelcontextprotocol/typescript-sdk)
- [ChatGPT Apps SDK Docs](https://developers.openai.com/apps-sdk/build/mcp-server)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## License

MIT
