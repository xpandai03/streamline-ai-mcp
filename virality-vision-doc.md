# YouTube Virality Detector - Vision & Product Specification

## Executive Summary

Build an MCP (Model Context Protocol) tool that enables AI assistants like Claude to analyze YouTube videos and automatically identify viral-worthy moments. Users simply provide a YouTube URL, and the system returns timestamped clips with high viral potential, complete with hooks, scores, and explanations.

## Problem Statement

Content creators waste hours manually scrubbing through long-form videos to find shareable moments. They miss potential viral clips because:
- Manual review is time-consuming and tedious
- Human bias overlooks unexpected viral potential
- Lack of data-driven approach to content selection
- No systematic way to identify multiple clip opportunities

## Solution Vision

### Core Value Proposition
**"Turn any YouTube video into viral clips in minutes, not hours"**

An AI-powered tool that:
1. Takes a YouTube URL as input
2. Downloads and transcribes the full video
3. Analyzes content for viral potential using AI
4. Returns ranked, timestamped moments ready for clipping
5. Provides actionable insights on why each moment could go viral

### User Experience Flow

```
User: "Analyze this video for viral moments: youtube.com/watch?v=..."
↓
Assistant: "I'll analyze that video for viral potential..."
↓
[System processes in background]
↓
Assistant: "Found 5 viral moments! Here are the top clips:

1. 🔥 'The Unexpected Plot Twist' (2:34-3:15)
   - Hook: "You won't believe what happens when..."
   - Virality Score: 9.2/10
   - Perfect for: TikTok, YouTube Shorts
   
2. 😂 'The Comedy Gold Moment' (5:47-6:02)
   - Hook: "When you realize..."
   - Virality Score: 8.7/10
   - Perfect for: Instagram Reels
   
[...]"
```

## Target Users

### Primary Users
1. **Content Creators** - YouTubers repurposing long-form content
2. **Social Media Managers** - Finding clips for brand accounts
3. **Podcast Producers** - Extracting highlight reels
4. **Digital Marketers** - Creating engaging social content

### Use Cases
- **Podcast Highlights**: Extract best moments from 2-hour episodes
- **Educational Content**: Find teachable moments for micro-learning
- **Gaming Streams**: Identify epic plays and funny moments
- **Interviews**: Pull quotable soundbites and revelations
- **Tutorials**: Extract quick tips and hacks

## Core Features

### MVP (Minimum Viable Product)
1. **URL Input** - Accept any public YouTube video URL
2. **Automatic Transcription** - Full video with accurate timestamps
3. **AI Analysis** - Identify 5-10 viral moments per video
4. **Ranked Results** - Sort by viral potential score
5. **Timestamp Ranges** - Exact start/end times for clipping
6. **Hook Generation** - Catchy titles for each clip
7. **Platform Recommendations** - Suggest best platform for each clip

### Enhanced Features (Phase 2)
1. **Custom Criteria** - User-defined viral parameters
2. **Batch Processing** - Analyze multiple videos at once
3. **Clip Export** - Auto-generate actual video clips
4. **Trend Integration** - Compare against current viral trends
5. **A/B Testing** - Multiple hook variations per clip
6. **Analytics Prediction** - Estimated view/engagement counts

## Technical Integration

### MCP Tool Specification

```yaml
tool_name: youtube_virality_detector
description: Analyze YouTube videos to find viral clip opportunities
parameters:
  - url: YouTube video URL (required)
  - clip_duration: Target clip length in seconds (optional, default: 30)
  - platform: Target platform (optional: tiktok/reels/shorts/all)
  - style: Content style (optional: funny/educational/inspiring/shocking)
  - max_clips: Maximum clips to return (optional, default: 5)
```

### Expected MCP Response Format

```json
{
  "video_info": {
    "title": "Original Video Title",
    "duration": "20:34",
    "channel": "Channel Name",
    "url": "https://youtube.com/..."
  },
  "viral_clips": [
    {
      "rank": 1,
      "title": "Generated Viral Hook Title",
      "timestamp": "2:34-3:15",
      "duration_seconds": 41,
      "virality_score": 0.92,
      "platforms": ["tiktok", "reels"],
      "style": "funny",
      "hook": "Wait for it... you won't believe what happens next",
      "content_summary": "Brief description of what happens",
      "viral_factors": [
        "Unexpected twist",
        "Highly relatable",
        "Perfect length for TikTok"
      ],
      "suggested_caption": "Full caption text with hashtags",
      "thumbnail_timestamp": "2:47"
    }
  ],
  "summary": {
    "total_clips_found": 5,
    "total_viral_duration": "3:24",
    "best_platform": "TikTok",
    "dominant_style": "Comedy"
  }
}
```

## Virality Detection Algorithm

### Core Viral Indicators
1. **Emotional Triggers**
   - Surprise/shock value
   - Humor/comedy timing
   - Inspiration/motivation
   - Controversy/debate potential
   - Relatability/shared experiences

2. **Structural Elements**
   - Strong opening hook (first 3 seconds)
   - Clear story arc or punchline
   - Visual or audio climax
   - Satisfying conclusion
   - Memeable moments

3. **Content Patterns**
   - Quotable one-liners
   - "Wait for it" moments
   - Before/after transformations
   - Expert tips/life hacks
   - Fail/win moments

4. **Platform-Specific Optimization**
   - TikTok: 15-60 seconds, trend-aligned
   - Reels: 15-30 seconds, aesthetic focus
   - Shorts: 30-60 seconds, retention-optimized
   - Twitter: <2:20, discussion-worthy

### AI Prompt Engineering

```
You are a viral content expert who understands what makes videos explode on social media.

Analyze this transcript with timestamps and identify moments that would work as standalone viral clips.

For each viral moment, consider:
- Does it work without context?
- Is there a clear emotional hook?
- Would someone share this?
- Does it fit platform constraints?
- Is there a trending angle?

Score each moment 0-10 based on:
- Shareability (0-3 points)
- Emotional impact (0-3 points)  
- Completeness (0-2 points)
- Trendability (0-2 points)
```

## Success Metrics

### User Success Indicators
- **Time Saved**: 2 hours → 2 minutes per video
- **Clips Generated**: 5-10 high-quality clips per video
- **Engagement Rate**: 2-5x higher than random clips
- **Platform Performance**: Optimized for each platform's algorithm

### System Performance Targets
- **Processing Time**: <3 minutes for 30-minute video
- **Accuracy**: 80% of suggested clips perform above average
- **Coverage**: Catch 90% of potentially viral moments
- **Reliability**: 99.9% uptime for MCP tool

## Implementation Phases

### Phase 1: MCP Tool MVP (Week 1-2)
- Basic YouTube download and transcription
- Simple viral detection with GPT-4
- Return timestamps and descriptions via MCP
- Support single video analysis

### Phase 2: Enhanced Analysis (Week 3-4)
- Improved viral detection algorithm
- Platform-specific optimization
- Hook and caption generation
- Batch processing support

### Phase 3: Production Features (Week 5-6)
- Actual clip generation with ffmpeg
- Thumbnail extraction
- Trend analysis integration
- Performance analytics

### Phase 4: Scale & Optimize (Week 7-8)
- Caching layer for common videos
- Multi-language support
- Custom viral criteria
- API rate limit management

## User Interaction Examples

### Example 1: Basic Analysis
```
User: "Find viral moments in this video: [YouTube URL]"

Claude: "I'll analyze this 15-minute tutorial for viral clips...

Found 4 high-potential moments:

1. **The Mind-Blowing Trick** (3:24-3:52)
   💡 Perfect for: Educational TikTok
   🎯 Score: 8.9/10
   🎬 28 seconds of pure value
   
   This segment shows a counterintuitive solution that makes 
   viewers go 'Why didn't I think of that?' Great retention.

2. **The Funny Fail** (7:12-7:28)
   😂 Perfect for: Instagram Reels
   🎯 Score: 8.5/10
   🎬 16 seconds of comedy gold
   
   Classic expectation vs. reality moment. Highly relatable
   and memeable. Add text overlay for maximum impact.

Would you like me to generate the actual clips or provide more details?"
```

### Example 2: Platform-Specific Request
```
User: "What parts of this podcast would work best for TikTok?"

Claude: "Analyzing for TikTok-specific viral potential (15-60 sec clips)...

Top 3 TikTok-Ready Moments:

1. **The Controversial Take** (12:45-13:12)
   🔥 27 seconds
   Hook: "This CEO just said what everyone's thinking..."
   Why it works: Opens with shocking statement, builds tension
   Suggested hashtags: #BusinessTruth #CEOSays #RealTalk

2. **The Success Story** (34:20-34:58)
   📈 38 seconds  
   Hook: "From $7 to $7 million in 2 years"
   Why it works: Clear transformation story, inspirational
   Suggested hashtags: #SuccessStory #Entrepreneur #Motivation

Caption templates and optimal posting times included below..."
```

### Example 3: Content Creator Workflow
```
User: "I just uploaded a 45-minute gaming stream. Find the best clips for Shorts."

Claude: "Scanning your gaming stream for YouTube Shorts moments (30-60 sec)...

🎮 Found 6 Epic Moments:

1. **The Impossible Clutch** (8:34-9:23)
   - 49 seconds of pure adrenaline
   - Peak moment at 9:11 (use for thumbnail)
   - Estimated views: 50K-100K based on similar clips

2. **The Rage Quit Comedy** (15:45-16:12)
   - 27 seconds (loop it for 54 sec Short)
   - Add captions at 15:52 for emphasis
   - Perfect for gaming compilation channels

Quick Actions:
- [Download All Clips] 
- [Generate Thumbnails]
- [Create Upload Schedule]
- [A/B Test Titles]"
```

## Expected Outcomes

### For Content Creators
- **10x faster** content repurposing
- **3x more** content from same source
- **Data-driven** clip selection
- **Platform-optimized** content

### For End Users (Viewers)
- Higher quality short-form content
- More engaging social media feeds
- Better content discovery
- Reduced low-quality spam

### For Platforms
- Increased engagement metrics
- Better content diversity
- Higher user retention
- More viral moments

## Technical Requirements Summary

### Core Dependencies
- **MCP Integration**: Claude/ChatGPT compatible
- **YouTube Access**: yt-dlp for reliable downloading
- **Transcription**: Whisper for accurate timestamps
- **AI Analysis**: GPT-4/Claude for viral detection
- **Video Processing**: ffmpeg for clip generation

### Performance Requirements
- Process 30-min video in <3 minutes
- Handle videos up to 4 hours
- Support 100+ concurrent requests
- 99.9% availability

### Data Flow
```
YouTube URL → MCP Tool Request → Download Audio → Transcribe → 
AI Analysis → Viral Detection → Format Response → Return to User
```

## Risk Mitigation

### Technical Risks
- **API Rate Limits**: Implement caching and queuing
- **Large Files**: Stream processing and chunking
- **Accuracy**: Human feedback loop for improvement

### Content Risks
- **Copyright**: Only analyze, don't redistribute
- **Privacy**: No personal data storage
- **Misuse**: Rate limiting and usage policies

## Future Vision

### Advanced Features (6+ months)
- **AI Video Understanding**: Analyze visual elements, not just audio
- **Trend Prediction**: Identify tomorrow's viral formats
- **Auto-Publishing**: Direct upload to platforms
- **Performance Tracking**: Monitor actual clip performance
- **Custom AI Training**: Train on user's successful content

### Platform Expansion
- LinkedIn (professional highlights)
- Twitter/X (discussion starters)
- Snapchat (quick moments)
- Platform-agnostic export

### Integration Ecosystem
- Editing software plugins
- Social media schedulers
- Analytics platforms
- Content management systems

## Success Criteria

The tool is successful when:
1. Users consistently find 3+ usable clips per video
2. Processing time is under 3 minutes for standard videos
3. 80% of users return for multiple analyses
4. Generated clips outperform manually selected ones
5. The tool becomes part of creators' standard workflow

## Call to Action

This MCP tool will revolutionize how creators repurpose content, making viral clip creation accessible, data-driven, and efficient. By integrating directly with AI assistants, we remove friction and make the process as simple as sharing a URL.

**Next Steps:**
1. Implement core MCP tool structure
2. Integrate transcription pipeline
3. Develop viral detection prompts
4. Test with diverse video content
5. Deploy and iterate based on feedback