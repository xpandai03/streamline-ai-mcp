#!/usr/bin/env python3
"""
MCP Server for YouTube Viral Moment Detection
Wraps the virality detector functionality as an MCP tool
"""

import os
import json
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Import our existing virality detector (handles hyphenated filename)
import importlib.util
import sys as _sys
_spec = importlib.util.spec_from_file_location("youtube_virality_detector",
    os.path.join(os.path.dirname(__file__), "youtube-virality-detector.py"))
_module = importlib.util.module_from_spec(_spec)
_sys.modules["youtube_virality_detector"] = _module
_spec.loader.exec_module(_module)
from youtube_virality_detector import ViralityDetector


# Create MCP server instance
app = Server("youtube-virality-detector")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="analyze_youtube_video",
            description="Analyze a YouTube video to find viral clip moments. Downloads video, transcribes it, and uses AI to identify the most viral-worthy moments (30-60s clips) for creating short-form content for TikTok, Reels, and Shorts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL (required)"
                    },
                    "max_clips": {
                        "type": "integer",
                        "description": "Maximum number of viral clips to return (default: 4)",
                        "default": 4
                    },
                    "whisper_model": {
                        "type": "string",
                        "description": "Whisper model size for transcription: tiny (fastest), base, small, medium, large (most accurate). Default: base",
                        "enum": ["tiny", "base", "small", "medium", "large"],
                        "default": "base"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""

    if name != "analyze_youtube_video":
        raise ValueError(f"Unknown tool: {name}")

    # Get parameters
    url = arguments.get("url")
    max_clips = arguments.get("max_clips", 4)
    whisper_model = arguments.get("whisper_model", "base")

    if not url:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": "URL parameter is required"})
        )]

    # Get OpenAI API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": "OPENAI_API_KEY environment variable not set. Please configure it in your MCP settings."
            })
        )]

    try:
        # Initialize detector (blocking operation, but MCP handles this)
        detector = ViralityDetector(api_key, whisper_model)

        # Process video
        results = detector.process_video(url)

        # Limit to requested number of clips
        results["viral_moments"] = results["viral_moments"][:max_clips]

        # Remove full transcript to reduce output size
        if "full_transcript" in results:
            del results["full_transcript"]

        # Format output for better readability
        output = {
            "video_title": results["video"]["title"],
            "video_url": results["video"]["url"],
            "video_duration": f"{results['video']['duration']} seconds",
            "channel": results["video"]["channel"],
            "viral_clips_found": len(results["viral_moments"]),
            "top_clips": []
        }

        for moment in results["viral_moments"]:
            output["top_clips"].append({
                "rank": moment["rank"],
                "hook": moment["hook"],
                "timestamp": moment["timestamp"],
                "start_seconds": moment["start_seconds"],
                "end_seconds": moment["end_seconds"],
                "duration": f"{moment['duration']:.1f} seconds",
                "virality_score": f"{moment['virality_score']:.2f}/1.0",
                "why_viral": moment["reasoning"],
                "transcript_preview": moment["transcript"][:200] + "..." if len(moment["transcript"]) > 200 else moment["transcript"]
            })

        return [types.TextContent(
            type="text",
            text=json.dumps(output, indent=2)
        )]

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": f"Failed to process video: {str(e)}",
                "url": url
            })
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
