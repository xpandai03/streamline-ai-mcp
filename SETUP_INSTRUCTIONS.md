# YouTube Virality Detector MCP - Setup Guide

## ✅ Installation Complete!

All dependencies are installed and tested. The script successfully:
- Downloaded and transcribed a YouTube video
- Analyzed it for viral moments using AI
- Returned ranked viral clips with timestamps and hooks

## 🚀 Quick Start - Add to Cursor

### Step 1: Open Cursor MCP Settings
1. Open Cursor Settings: `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
2. Search for "MCP" in the settings
3. Click "Edit Config" or "Add MCP Server"

### Step 2: Add Configuration

Copy and paste this JSON into your Cursor MCP config:

```json
{
  "mcpServers": {
    "youtube-virality-detector": {
      "command": "/Users/raunekpratap/Desktop/CLIPPING MCP/venv/bin/python",
      "args": ["/Users/raunekpratap/Desktop/CLIPPING MCP/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here"
      }
    }
  }
}
```

### Step 3: Restart Cursor
After saving the config, restart Cursor for changes to take effect.

## 🎯 How to Use

Once configured, you can ask Cursor:

```
"Analyze this YouTube video for viral moments: https://www.youtube.com/watch?v=YOUR_VIDEO"
```

### Example Prompts:
- "Find viral clips in this video: [URL]"
- "Analyze this YouTube video and suggest 4 viral moments: [URL]"
- "What are the best short-form clips from this video: [URL]"

### Optional Parameters:
- `max_clips`: Number of clips to return (default: 4)
- `whisper_model`: Transcription quality - tiny/base/small/medium/large (default: base)

## 📋 What You Get

For each viral moment, you'll receive:
- **Rank**: Ordered by virality score
- **Hook**: Catchy title for the clip
- **Timestamp**: Exact start/end times (HH:MM:SS)
- **Duration**: Clip length in seconds
- **Virality Score**: 0.0-1.0 rating
- **Why It's Viral**: AI explanation of viral potential
- **Transcript Preview**: What's being said in that moment

## 🧪 Manual Testing (Optional)

If you want to test outside Cursor:

```bash
cd "/Users/raunekpratap/Desktop/CLIPPING MCP"
source venv/bin/activate
python test_script.py "https://www.youtube.com/watch?v=YOUR_VIDEO"
```

Results will be saved to `test_results.json`.

## 🛠️ Troubleshooting

### MCP Server Not Showing Up
1. Make sure Cursor is fully restarted
2. Check MCP settings to verify the server is listed
3. Look for error messages in Cursor's MCP logs

### "API Key Error"
- Verify the OpenAI API key in the config is correct
- Check that you have credits in your OpenAI account

### "Module Not Found" Errors
Run:
```bash
cd "/Users/raunekpratap/Desktop/CLIPPING MCP"
source venv/bin/activate
pip install yt-dlp openai-whisper openai tqdm
```

### Slow Processing
- Use `whisper_model: "tiny"` for faster transcription
- Larger models (base/small/medium/large) are more accurate but slower

## 📁 Project Structure

```
CLIPPING MCP/
├── youtube-virality-detector.py  # Core detection logic
├── mcp_server.py                  # MCP wrapper
├── test_script.py                 # Testing tool
├── venv/                          # Python environment
├── cursor_mcp_config.json         # Ready-to-use config
└── SETUP_INSTRUCTIONS.md          # This file
```

## 🎉 Next Steps

1. Add the MCP config to Cursor
2. Test with a YouTube video
3. Iterate on viral clip suggestions
4. Create actual clips from the timestamps!

## 💡 Tips for Best Results

- **Short videos (< 10 min)** process fastest
- **Clear speech** transcribes better
- **Engaging content** gets better viral scores
- **Educational/comedy/surprising** content works best for viral clips

---

**Need help?** Check the files in this directory:
- `test_script.py` - For standalone testing
- `cursor_mcp_config.json` - Copy-paste config
- `test_results.json` - Sample output from testing
