# Performance Optimization Guide

## Current Performance Baseline
- **10-minute video**: ~8-10 minutes processing time
- **5-minute video**: ~60-90 seconds processing time

## Processing Time Breakdown
1. **Audio Download**: 5-15 seconds (depends on YouTube servers)
2. **Whisper Transcription**: 60-80% of total time
3. **GPT-4 Analysis**: 10-20 seconds
4. **Formatting**: <1 second

---

## Cloud Deployment Optimizations

### 1. Use Faster Whisper Models (Huge Speed Boost)

**Current**: Using OpenAI Whisper (CPU-based, slow)
**Optimized**: Switch to Whisper API or faster-whisper library

#### Option A: OpenAI Whisper API (Recommended)
**Speed**: 10-20x faster than local Whisper
**Cost**: ~$0.006 per minute of audio

```python
# Replace WhisperTranscriber with API call
from openai import OpenAI

client = OpenAI(api_key=api_key)

def transcribe_with_api(audio_path):
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    return transcript.segments
```

**Expected improvement**:
- 10-min video: 8-10 min → **1-2 minutes**
- 5-min video: 60-90 sec → **15-30 seconds**

#### Option B: faster-whisper (CPU/GPU optimized)
**Speed**: 4-8x faster than standard Whisper
**Cost**: Free (runs on your infrastructure)

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

# Use GPU if available, else CPU with optimizations
model = WhisperModel("base", device="cuda", compute_type="float16")
# Or for CPU:
# model = WhisperModel("base", device="cpu", compute_type="int8")

segments, info = model.transcribe(audio_path, beam_size=5)
```

**Expected improvement**:
- 10-min video: 8-10 min → **2-4 minutes**
- 5-min video: 60-90 sec → **30-45 seconds**

---

### 2. Parallel Processing Architecture

**Current**: Sequential (download → transcribe → analyze)
**Optimized**: Parallel + streaming

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_video_optimized(url):
    # Download and transcribe can start immediately
    download_task = asyncio.create_task(download_audio(url))

    # Once download completes, start transcription
    audio_path = await download_task
    transcribe_task = asyncio.create_task(transcribe_audio(audio_path))

    # While transcribing, prefetch GPT-4 system prompt
    segments = await transcribe_task

    # Analyze immediately
    results = await analyze_segments(segments)
    return results
```

**Expected improvement**: 10-15% faster overall

---

### 3. GPU Acceleration (Cloud Infrastructure)

**For Cloud Deployment:**
- **AWS**: EC2 g4dn.xlarge (1x NVIDIA T4 GPU) - $0.526/hour
- **GCP**: n1-standard-4 + NVIDIA T4 - $0.50/hour
- **Azure**: NC4as_T4_v3 - $0.526/hour

**With GPU Whisper transcription:**
- 10-min video: **30-60 seconds** total
- 5-min video: **10-20 seconds** total

---

### 4. Use Smaller Whisper Model for Speed

**Trade-off**: Accuracy vs Speed

| Model  | Speed  | Accuracy | Recommended Use |
|--------|--------|----------|-----------------|
| tiny   | 10x    | 80%      | Quick previews  |
| base   | 5x     | 85%      | **Current default - balanced** |
| small  | 2x     | 90%      | High accuracy needed |
| medium | 1x     | 95%      | Professional use |
| large  | 0.5x   | 98%      | Maximum accuracy |

**For viral clips (where speed matters)**:
- Use `tiny` or `base` - viral moments don't need perfect transcription
- Viewers won't notice small transcription errors

---

### 5. Optimize GPT-4 Analysis

**Current**: Single GPT-4 call with full transcript
**Optimized**: Use GPT-4o-mini for initial filtering, GPT-4 for final ranking

```python
# Step 1: Quick scan with GPT-4o-mini (10x faster, 20x cheaper)
from openai import OpenAI
client = OpenAI(api_key=api_key)

# Use mini for finding candidate moments
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Fast pre-filtering
    messages=[...],
    temperature=0.7
)

# Step 2: Use GPT-4 only for final ranking of top 10 candidates
final_response = client.chat.completions.create(
    model="gpt-4-turbo-preview",  # Only for final selection
    messages=[...]
)
```

**Expected improvement**:
- Cost: -80%
- Speed: +40% faster

---

### 6. Caching Strategy

**For repeated analysis of popular videos:**

```python
import hashlib
import redis

# Setup Redis cache
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_analysis(url):
    cache_key = f"viral_moments:{hashlib.md5(url.encode()).hexdigest()}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

def cache_analysis(url, results):
    cache_key = f"viral_moments:{hashlib.md5(url.encode()).hexdigest()}"
    cache.setex(cache_key, 86400, json.dumps(results))  # 24hr TTL
```

**Expected improvement**: Instant response for cached videos

---

### 7. Pre-download Audio Only (Skip Video)

**Current**: Uses yt-dlp default settings
**Optimized**: Download audio-only, lowest quality sufficient

```python
ydl_opts = {
    'format': 'worstaudio/worst',  # Fastest download
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '64',  # Lower quality = faster (sufficient for transcription)
    }],
}
```

**Expected improvement**: 30-50% faster downloads

---

## Recommended Cloud Architecture

### Option 1: Serverless (AWS Lambda + API Gateway)
**Best for**: Occasional use, pay-per-request

```
User Request → API Gateway → Lambda (Whisper API + GPT-4) → Results
```

**Pros**:
- No infrastructure management
- Pay only for usage
- Auto-scaling

**Cons**:
- 15-minute Lambda timeout (limits long videos)
- Cold starts add 2-5 seconds

**Cost estimate**:
- Whisper API: $0.006/min audio
- GPT-4: ~$0.03 per analysis
- Lambda: $0.20 per 1M requests
- **Total per 10-min video: ~$0.10**

---

### Option 2: Container-based (Cloud Run / ECS)
**Best for**: High volume, consistent traffic

```
User Request → Load Balancer → Container (faster-whisper GPU + GPT-4) → Results
```

**Pros**:
- Full control over environment
- GPU support for faster-whisper
- No timeout limits

**Cons**:
- More expensive at low volume
- Requires infrastructure management

**Cost estimate** (with GPU):
- EC2 g4dn.xlarge: $0.526/hour
- Process ~120 videos/hour
- **Cost per video: ~$0.004** (excluding API costs)

---

### Option 3: Hybrid (Recommended)
**Best balance of cost and performance**

```
User Request → API Gateway → Lambda (coordinator)
                ↓
         Check Cache (Redis)
                ↓
    Queue Job (SQS) → EC2 Worker (GPU + faster-whisper)
                ↓
         Return Results + Cache
```

**Features**:
- Lambda handles requests, checks cache
- EC2 spot instances for heavy processing
- Auto-scaling based on queue depth
- Redis cache for popular videos

**Expected performance**:
- Cached videos: **<1 second**
- New 10-min video: **1-2 minutes** (with Whisper API)
- New 10-min video: **30-60 seconds** (with GPU faster-whisper)

**Cost estimate**:
- Most requests served from cache: **$0.001**
- New video analysis: **$0.06-0.10**

---

## Implementation Priority

### Phase 1: Quick Wins (Do First)
1. ✅ **Switch to Whisper API** - 10x speed improvement, minimal code change
2. ✅ **Use "tiny" or "base" model** - Already using base, could drop to tiny
3. ✅ **Optimize audio download** - Set to worst quality audio

**Expected improvement**: 10-min video → **1-2 minutes**

### Phase 2: Infrastructure (For Scale)
4. **Add Redis caching** - Instant results for popular videos
5. **Deploy to Cloud Run / Lambda** - Auto-scaling, pay-per-use
6. **Add queue system** - Handle concurrent requests

**Expected improvement**: Most requests < **5 seconds** (cached)

### Phase 3: Advanced (For High Volume)
7. **GPU workers with faster-whisper**
8. **GPT-4o-mini pre-filtering**
9. **Parallel processing pipeline**

**Expected improvement**: New videos → **30-60 seconds**

---

## Quick Implementation: Whisper API (Fastest ROI)

I can update the code right now to use Whisper API. Want me to do that?

**Changes needed**:
1. Update `WhisperTranscriber` class to use OpenAI API
2. Remove local Whisper model download
3. Update requirements.txt

**Benefits**:
- ✅ 10x faster transcription
- ✅ No GPU needed
- ✅ More accurate than tiny/base models
- ✅ ~$0.06 per 10-min video
- ✅ Works in any cloud environment

Would you like me to implement this optimization now?
