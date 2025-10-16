### 1\. **Modular Architecture**

-   **YouTubeDownloader**: Uses yt-dlp to download audio efficiently
-   **WhisperTranscriber**: Handles transcription with automatic chunking for long videos
-   **ViralityAnalyzer**: Uses OpenAI GPT to identify viral moments
-   **ViralityDetector**: Orchestrates the entire pipeline

### 2\. **Smart Chunking**

-   Automatically splits audio longer than 10 minutes into chunks
-   Preserves accurate timestamps across chunks
-   Cleans up temporary files automatically

### 3\. **Viral Detection Logic**

The AI analyzes for:

-   Strong emotional impact (funny, surprising, inspiring)
-   Self-contained stories
-   Memorable quotes
-   Educational "aha" moments
-   Relatable situations

### 4\. **Rich Output Format**

Returns JSON with:

-   Ranked viral moments with timestamps
-   Virality scores (0.0-1.0)
-   Hook lines for each moment
-   Reasoning for virality
-   Full transcript with timestamps

Installation
------------

```
pip install yt-dlp openai-whisper openai pydub tqdm

```

You'll also need FFmpeg installed for audio processing.

Usage
-----

### Basic CLI Usage:

```
python virality_detector.py "https://youtube.com/watch?v=..." --api-key YOUR_OPENAI_KEY

```

### With options:

```
# Use larger Whisper model for better accuracy
python virality_detector.py URL --api-key KEY --whisper-model large

# Save to JSON file
python virality_detector.py URL --api-key KEY --output results.json

# Exclude full transcript from output
python virality_detector.py URL --api-key KEY --no-transcript

```

### Programmatic Usage:

```
from virality_detector import ViralityDetector

detector = ViralityDetector(openai_api_key="your-key")
results = detector.process_video("https://youtube.com/watch?v=...")

# Access viral moments
for moment in results["viral_moments"]:
    print(f"{moment['hook']} at {moment['timestamp']}")

```

Next Steps for Enhancement
--------------------------

1.  **Add Flask/FastAPI wrapper** for web service deployment
2.  **Add support for Claude API** as alternative to OpenAI
3.  **Export clips** - Add ffmpeg commands to actually cut the viral segments
4.  **Batch processing** - Process multiple URLs
5.  **Custom virality prompts** - Allow users to define what "viral" means for their use case
6.  **Video clip generation** - Auto-generate the actual video clips
