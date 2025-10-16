# YouTube Virality Detector - MCP Deployment Guide

## ✅ Status: Ready to Deploy

All code is tested and working! Your MCP server is ready to be added to Cursor.

---

## 🚀 Quick Deployment (2 Minutes)

### Step 1: Open Cursor MCP Settings

1. Open Cursor
2. Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
3. Search for "MCP" in the settings search bar
4. Click on "MCP Servers" section
5. Look for an "Edit Config" or "Configure" button

**OR**

1. In Cursor, go to: **Settings → Extensions → MCP**
2. Click "Edit in settings.json" or similar option

---

### Step 2: Add Your MCP Server Configuration

Copy the **ENTIRE contents** of this file:
```
/Users/raunekpratap/Desktop/CLIPPING MCP/cursor_mcp_config.json
```

And paste it into your Cursor MCP configuration.

**The configuration contains:**
- Python path to your virtual environment
- Path to the MCP server script
- Your OpenAI API key (already embedded)

---

### Step 3: Restart Cursor

1. **Completely quit** Cursor (not just close the window)
   - Mac: `Cmd + Q`
   - Windows/Linux: File → Exit
2. **Reopen** Cursor
3. The MCP server will load automatically

---

### Step 4: Verify It's Working

In Cursor's chat, type:
```
Analyze this YouTube video for viral moments: https://www.youtube.com/watch?v=iqNzfK4_meQ
```

**Expected result:**
- Cursor will download the video
- Transcribe it (takes 30-60 seconds)
- Return 3-4 viral clips with:
  - Timestamps (HH:MM:SS)
  - Duration (30-60 seconds)
  - Virality scores
  - Catchy hooks
  - Reasoning

---

## 📋 What You Get

Each viral moment includes:

| Field | Description |
|-------|-------------|
| **Rank** | Ordered by virality score (best first) |
| **Hook** | Catchy title for the clip (8-12 words) |
| **Timestamp** | Exact start/end times (HH:MM:SS format) |
| **Duration** | Clip length in seconds (30-60s range) |
| **Virality Score** | 0.0-1.0 rating (0.75+ recommended) |
| **Why Viral** | AI explanation of viral potential |
| **Transcript** | What's being said in that moment |

---

## 🎯 Example Usage in Cursor

### Basic Request:
```
Find viral clips in this video: [YouTube URL]
```

### With Custom Parameters:
```
Analyze this video for viral moments:
- URL: https://www.youtube.com/watch?v=YOUR_VIDEO
- I want 5 clips
- Use faster transcription (tiny model)
```

### Follow-up Iteration:
```
The first clip looks great! Can you analyze these moments more:
- Extend clip #2 by 10 seconds to capture the full story
- Find a shorter clip around the 5-minute mark
```

---

## 🛠️ Troubleshooting

### Issue: MCP Server Not Showing Up

**Solution:**
1. Check Cursor's MCP logs for errors
2. Verify the paths in your config are correct
3. Make sure you fully quit and restarted Cursor

**How to check:**
- Cursor Settings → MCP → View Logs (if available)
- Look for "youtube-virality-detector" in the logs

---

### Issue: "OPENAI_API_KEY not set" Error

**Solution:**
Your API key in the config file might be wrong or expired.

**Fix:**
1. Get your OpenAI API key from: https://platform.openai.com/api-keys
2. Open: `/Users/raunekpratap/Desktop/CLIPPING MCP/cursor_mcp_config.json`
3. Replace the `OPENAI_API_KEY` value
4. Restart Cursor

---

### Issue: "Module Not Found" Error

**Solution:**
The virtual environment might be broken.

**Fix:**
```bash
cd "/Users/raunekpratap/Desktop/CLIPPING MCP"
source venv/bin/activate
pip install --upgrade yt-dlp openai-whisper openai tqdm mcp
```

Then restart Cursor.

---

### Issue: Slow Processing

**Solution:**
Videos take time depending on length and Whisper model.

**Expected Processing Times:**
- 5-minute video: ~1-2 minutes (with `base` model)
- 10-minute video: ~2-3 minutes
- 20-minute video: ~4-5 minutes

**Speed it up:**
Ask Cursor to use a faster model:
```
Analyze this video with the tiny model for speed
```

---

## 🧪 Test Videos

Use these test URLs to verify everything works:

1. **Short (5 min):** https://www.youtube.com/watch?v=iqNzfK4_meQ
2. **Medium (11 min):** https://www.youtube.com/watch?v=o2s8I6yBrxE
3. **Long (20 min):** https://www.youtube.com/watch?v=DzjWEn2BS_k

---

## 📁 Project Files

All files are located in:
```
/Users/raunekpratap/Desktop/CLIPPING MCP/
```

**Key Files:**
- `mcp_server.py` - The MCP server (don't modify)
- `youtube-virality-detector.py` - Core detection logic
- `cursor_mcp_config.json` - Ready-to-use Cursor config
- `venv/` - Python virtual environment

---

## 🔄 Updating the System

If you need to update the prompt or improve detection:

1. Edit: `youtube-virality-detector.py` (lines 213-309)
2. Test changes: `python test_script.py "YOUR_VIDEO_URL"`
3. Restart Cursor (MCP will load the new version)

No need to modify `mcp_server.py` unless changing the API.

---

## 💡 Tips for Best Results

### Video Selection:
- ✅ Clear speech (good audio quality)
- ✅ Engaging content (educational, comedy, surprising moments)
- ✅ 5-30 minute videos work best
- ❌ Avoid music videos or very long (1hr+) videos

### Clip Quality:
- All clips are **30-60 seconds** (optimized for Reels/Shorts/TikTok)
- **Complete thoughts** - no mid-sentence cuts
- **Self-contained** - understandable without watching full video
- **Natural boundaries** - starts/ends at sentence breaks

### Iteration:
- Ask Cursor to refine clips: "Make clip #2 longer to include the punchline"
- Request specific moments: "Find a clip around the 8-minute mark"
- Change scoring: "Prioritize funny moments over educational ones"

---

## 🎉 You're All Set!

Once configured, you can:
1. Paste any YouTube URL into Cursor
2. Get 3-4 ready-to-clip viral moments
3. Use the timestamps to create actual video clips
4. Post to TikTok, Reels, and YouTube Shorts

**Next Steps:**
1. Add the MCP config to Cursor (Step 1-2 above)
2. Restart Cursor (Step 3)
3. Test with a video (Step 4)
4. Start finding viral moments! 🚀

---

## 📞 Need Help?

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Review the logs in Cursor's MCP settings
3. Test manually with: `python test_script.py "VIDEO_URL"`
4. Check that all dependencies are installed in the venv

Happy clipping! 🎬
