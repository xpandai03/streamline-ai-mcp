# YouTube Viral Moments MCP

An MCP (Model Context Protocol) server that analyzes YouTube videos to identify viral-worthy moments for short-form content creation (TikTok, Reels, Shorts).

## Features

- **Smart Clip Detection**: Uses OpenAI GPT-4 to identify 3-4 viral moments per video
- **CLEAR Framework**: Implements structured prompting for consistent, high-quality results
- **Duration Enforcement**: Ensures all clips are 25-65 seconds (optimal for short-form platforms)
- **Complete Thoughts**: Clips always start/end at natural sentence boundaries
- **Rich Metadata**: Returns timestamps, hooks, virality scores, and reasoning for each clip
- **⚡ Optimized for Speed**: Uses Whisper API for 10x faster transcription (1-2 min for 10-min videos)
- **Fallback Support**: Automatically falls back to local Whisper if API fails or file >25MB

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- FFmpeg (for audio processing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/raunekp/yt-viral-moments-mcp.git
cd yt-viral-moments-mcp
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Standalone Usage

Run the detector directly from command line:

```bash
python youtube-virality-detector.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --api-key "your-openai-api-key" \
  --whisper-model base
```

### Use with Cursor (MCP Integration)

1. **Configure MCP Settings**

   Open Cursor and navigate to: `Settings → MCP & Tools`

   Add this configuration:
   ```json
   {
     "mcpServers": {
       "youtube-virality-detector": {
         "command": "/absolute/path/to/venv/bin/python",
         "args": ["/absolute/path/to/mcp_server.py"],
         "env": {
           "OPENAI_API_KEY": "your-openai-api-key-here"
         }
       }
     }
   }
   ```

2. **Restart Cursor**

   Completely quit (Cmd+Q on Mac) and reopen Cursor.

3. **Test the Tool**

   In Cursor's chat, type:
   ```
   Analyze this YouTube video for viral moments: https://www.youtube.com/watch?v=VIDEO_ID
   ```

## How It Works

### Architecture

```
YouTube URL → Download Audio → Transcribe (Whisper) → Analyze (GPT-4) → Viral Clips
```

1. **Download**: Uses `yt-dlp` to extract audio from YouTube
2. **Transcribe**: OpenAI Whisper converts audio to timestamped text
3. **Analyze**: GPT-4 identifies viral moments using CLEAR framework
4. **Validate**: Enforces 25-65 second duration and complete thoughts
5. **Rank**: Returns top clips sorted by virality score

### CLEAR Framework

The AI uses a structured prompt framework:
- **Clarity**: Clear objective and scope
- **Logic**: Decision rules and validation steps
- **Examples**: Positive/negative examples for guidance
- **Adaptation**: Quality check protocols
- **Results**: Structured JSON output format

### Virality Scoring

Each clip receives a 0.0-1.0 score based on:
- **Emotional Impact** (30%): Hook strength, surprise factor
- **Shareability** (30%): Standalone value, relatability
- **Completeness** (20%): Natural boundaries, self-contained
- **Platform Fit** (20%): Optimal length, trending format

## Example Output

```json
{
  "video_title": "Using OpenAI Codex CLI with GPT-5",
  "viral_clips_found": 4,
  "top_clips": [
    {
      "rank": 1,
      "hook": "Recapping Codex CLI's Impact: From Concept to Deployment",
      "timestamp": "0:04:50 - 0:05:36",
      "duration": "46.0 seconds",
      "virality_score": "0.90/1.0",
      "why_viral": "Comprehensive recap with strong emotional arc...",
      "transcript_preview": "So to recap, we modified a Pong game..."
    }
  ]
}
```

## Configuration

### Transcription Method

**Default: Whisper API (Recommended)**
- ⚡ 10-20x faster than local Whisper
- Higher accuracy (uses large-v3 model)
- Cost: ~$0.006/minute (~$0.06 for 10-min video)
- **Performance**: 10-min video in ~1-2 minutes

**Fallback: Local Whisper**
- Automatically used if API fails or file >25MB
- Slower but free
- Models: tiny (fastest), base (default), small, medium, large (most accurate)
- **Performance**: 10-min video in ~8-10 minutes

### Parameters

- `max_clips`: Number of clips to return (default: 4)
- `whisper_model`: Transcription model size (default: "base")

## Files

- `mcp_server.py`: MCP server wrapper for Cursor integration
- `youtube-virality-detector.py`: Core detection logic
- `test_script.py`: Standalone testing script
- `DEPLOYMENT_GUIDE.md`: Detailed setup instructions
- `QUICK_START.txt`: 3-step deployment guide

## Troubleshooting

### Common Issues

**MCP not showing in Cursor:**
- Verify paths in `~/.cursor/mcp.json` are absolute
- Check Cursor logs: Settings → MCP & Tools → View Logs
- Ensure virtual environment has all dependencies

**Transcription fails:**
- Install FFmpeg: `brew install ffmpeg` (Mac) or `apt install ffmpeg` (Linux)
- Check Whisper model is downloaded

**API errors:**
- Verify OpenAI API key is valid
- Check API key has sufficient credits
- Ensure key has access to GPT-4

### Manual Test

Run the test script to verify setup:
```bash
cd "/path/to/CLIPPING MCP"
source venv/bin/activate
python test_script.py "https://www.youtube.com/watch?v=iqNzfK4_meQ"
```

Expected: 4 clips, all 25-65 seconds, with scores 0.82-0.90

## Requirements

See `requirements.txt` for full dependency list. Key packages:
- `mcp>=1.0.0`: Model Context Protocol SDK
- `openai>=1.0.0`: OpenAI API client
- `openai-whisper`: Audio transcription
- `yt-dlp`: YouTube download

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built using [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by OpenAI Whisper and GPT-4
- Uses `yt-dlp` for reliable YouTube downloads

## Support

For issues or questions:
- Open a GitHub issue
- Check `DEPLOYMENT_GUIDE.md` for detailed troubleshooting
- Review test examples in `test-yt-urls.md`

---

**Made with Claude Code** 🤖
