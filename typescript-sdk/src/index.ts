#!/usr/bin/env node
/**
 * YouTube Virality Analyzer - ChatGPT App SDK Wrapper
 *
 * This TypeScript Express server wraps the Python FastMCP backend and provides:
 * - MCP protocol implementation via @modelcontextprotocol/sdk
 * - Custom widgets for ChatGPT interface
 * - Tool proxying to Python backend
 */

import express from 'express';
import {Server} from '@modelcontextprotocol/sdk/server/index.js';
import {SSEServerTransport} from '@modelcontextprotocol/sdk/server/sse.js';
import {CallToolRequestSchema, ListToolsRequestSchema} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';
import dotenv from 'dotenv';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

// ES Module __dirname equivalent
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8080';

// Middleware
app.use(cors());
app.use(express.json());

// Create MCP Server
const mcpServer = new Server({
  name: 'youtube-virality-analyzer',
  version: '1.0.0'
}, {
  capabilities: {
    tools: {}
  }
});

// Tool definition
const analyzeVideoTool = {
  name: 'analyze_youtube_video',
  description: 'Analyze a YouTube video to find viral clip moments for TikTok, Reels, and Shorts. Returns timestamped clips with virality scores and engagement reasoning.',
  inputSchema: {
    type: 'object' as const,
    properties: {
      url: {
        type: 'string' as const,
        description: 'YouTube video URL'
      },
      max_clips: {
        type: 'number' as const,
        default: 4,
        description: 'Maximum number of viral clips to return (1-10)'
      },
      whisper_model: {
        type: 'string' as const,
        default: 'base',
        enum: ['tiny', 'base', 'small', 'medium'],
        description: 'Whisper transcription model size'
      }
    },
    required: ['url']
  }
};

// Register tool list handler
mcpServer.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [analyzeVideoTool]
}));

// Register tool call handler
mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'analyze_youtube_video') {
    try {
      console.log(`[MCP] Calling analyze_youtube_video with args:`, args);

      // Proxy request to Python FastMCP backend
      const response = await axios.post(
        `${PYTHON_BACKEND_URL}/analyze`,
        args,
        {
          headers: {
            'Content-Type': 'application/json',
            ...(process.env.API_KEY && { 'X-API-Key': process.env.API_KEY })
          },
          timeout: 300000 // 5 minute timeout for video processing
        }
      );

      console.log(`[MCP] Received response from Python backend:`, {
        status: response.status,
        clipsFound: response.data.viral_clips_found || 0
      });

      // Return response with widget metadata
      return {
        content: [
          {
            type: 'text' as const,
            text: JSON.stringify(response.data, null, 2)
          }
        ],
        _meta: {
          'openai/outputTemplate': 'ui://widget/clip-viewer.html'
        }
      };
    } catch (error: any) {
      console.error('[MCP] Error calling Python backend:', error.message);

      return {
        content: [
          {
            type: 'text' as const,
            text: JSON.stringify({
              error: 'Failed to analyze video',
              details: error.message,
              backend_url: PYTHON_BACKEND_URL
            }, null, 2)
          }
        ],
        isError: true
      };
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Health check (outside MCP router)
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'yt-mcp-typescript-wrapper',
    python_backend: PYTHON_BACKEND_URL,
    version: '1.0.0'
  });
});

// CORS preflight handlers (must be before router mounting)
app.options('/mcp', (req, res) => res.sendStatus(200));
app.options('/mcp/*', (req, res) => res.sendStatus(200));

// Create MCP router
const mcpRouter = express.Router();

// Base MCP endpoint (index) - must be in router to work correctly
mcpRouter.get('/', (req, res) => {
  res.json({
    service: 'YouTube Virality Analyzer MCP wrapper',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      tools: '/mcp/tools',
      messages: '/mcp/messages',
      widget: '/widget/clip-viewer.html'
    }
  });
});

// SSE endpoint for MCP protocol (ChatGPT expects /mcp base path)
mcpRouter.get('/messages', async (req, res) => {
  console.log('[SSE] New MCP connection established at /mcp/messages');

  // Set SSE headers with CORS for ChatGPT
  res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache, no-store, no-transform, must-revalidate');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  // CORS headers for ChatGPT Apps SDK
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization');
  res.setHeader('Access-Control-Expose-Headers', 'Content-Type');

  // Flush headers immediately to establish connection
  res.flushHeaders();

  // Send initial "open" event
  res.write('event: open\n');
  res.write('data: {}\n\n');
  console.log('[SSE] Sent event: open');

  // Send MCP initialization event with server info and tools
  const initData = {
    version: '2024-11-05',
    serverInfo: {
      name: 'youtube-virality-analyzer',
      version: '1.0.0'
    },
    capabilities: {
      tools: {}
    },
    tools: [analyzeVideoTool]
  };

  res.write('event: init\n');
  res.write(`data: ${JSON.stringify(initData)}\n\n`);
  console.log('[SSE] Sent event: init with tools:', initData.tools.map(t => t.name));

  // Now connect MCP SDK transport for ongoing communication
  try {
    const transport = new SSEServerTransport('/mcp/messages', res);
    await mcpServer.connect(transport);
    console.log('[SSE] MCP server transport connected');
  } catch (error: any) {
    console.error('[SSE] Error connecting MCP transport:', error.message);
  }

  // Keep connection alive - handle client disconnect
  req.on('close', () => {
    console.log('[SSE] Client disconnected from /mcp/messages');
  });
});

// Tools endpoint (for debugging)
mcpRouter.get('/tools', async (req, res) => {
  res.json({
    tools: [analyzeVideoTool]
  });
});

// Mount MCP router at /mcp
app.use('/mcp', mcpRouter);

// Legacy SSE endpoint (redirect to /mcp/messages)
app.get('/sse', (req, res) => {
  res.redirect(301, '/mcp/messages');
});

// Serve widget files (placeholder for now)
app.use('/widget', express.static(path.join(__dirname, '../public')));

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'YouTube Virality Analyzer - ChatGPT App',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      sse: '/sse (MCP protocol)',
      tools: '/mcp/tools (debug)',
      widget: '/widget/clip-viewer.html'
    },
    python_backend: PYTHON_BACKEND_URL
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║  YouTube Virality Analyzer - TypeScript MCP Wrapper      ║
╠════════════════════════════════════════════════════════════╣
║  🚀 Server running on: http://localhost:${PORT}           ║
║  🐍 Python backend: ${PYTHON_BACKEND_URL.padEnd(37)}║
║  📡 MCP SSE endpoint: http://localhost:${PORT}/sse       ║
║  🔧 Health check: http://localhost:${PORT}/health        ║
╚════════════════════════════════════════════════════════════╝
  `);

  console.log('\n[INFO] Ready to accept ChatGPT App connections');
  console.log('[INFO] Use Cloudflare Tunnel to expose HTTPS endpoint');
  console.log('\nNext steps:');
  console.log('1. Run: cloudflared tunnel --url http://localhost:3000');
  console.log('2. Copy the HTTPS URL');
  console.log('3. In ChatGPT → Settings → Apps → Create App → Paste URL');
  console.log('');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[INFO] SIGTERM received, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\n[INFO] SIGINT received, shutting down gracefully...');
  process.exit(0);
});
