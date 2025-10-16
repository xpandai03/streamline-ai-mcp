#!/usr/bin/env python3
"""
YouTube Video Virality Detector
Analyzes YouTube videos to identify high-virality moments using transcription and AI analysis.
"""

import os
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import timedelta
import tempfile
import subprocess
import sys

# Third-party imports
try:
    import yt_dlp
    import whisper
    from openai import OpenAI
    from tqdm import tqdm
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install yt-dlp openai-whisper openai tqdm")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TranscriptSegment:
    """Represents a transcribed segment with timing information."""
    text: str
    start: float
    end: float
    
    def to_timestamp(self) -> str:
        """Convert seconds to readable timestamp format."""
        return f"{self._seconds_to_time(self.start)} - {self._seconds_to_time(self.end)}"
    
    @staticmethod
    def _seconds_to_time(seconds: float) -> str:
        """Convert seconds to HH:MM:SS format."""
        return str(timedelta(seconds=int(seconds)))


@dataclass
class ViralMoment:
    """Represents a potential viral moment in the video."""
    start_time: float
    end_time: float
    transcript: str
    hook: str
    virality_score: float
    reasoning: str
    
    def to_timestamp(self) -> str:
        """Convert to readable timestamp range."""
        return f"{TranscriptSegment._seconds_to_time(self.start_time)} - {TranscriptSegment._seconds_to_time(self.end_time)}"


class YouTubeDownloader:
    """Handles YouTube video downloading and audio extraction."""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path(tempfile.gettempdir())
        self.output_dir.mkdir(exist_ok=True)
        
    def download_audio(self, url: str) -> Path:
        """Download audio from YouTube video."""
        logger.info(f"Downloading audio from: {url}")
        
        output_path = self.output_dir / "%(title)s.%(ext)s"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info['title']
            # Get the actual downloaded file path
            audio_file = self.output_dir / f"{video_title}.mp3"
            
        logger.info(f"Audio downloaded: {audio_file}")
        return audio_file, info


class WhisperTranscriber:
    """Handles audio transcription using OpenAI Whisper."""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model.
        
        Args:
            model_size: Size of Whisper model (tiny, base, small, medium, large)
        """
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        self.max_chunk_duration = 600  # 10 minutes in seconds
        
    def transcribe(self, audio_path: Path) -> List[TranscriptSegment]:
        """
        Transcribe audio file with timestamps.

        Args:
            audio_path: Path to audio file

        Returns:
            List of TranscriptSegment objects
        """
        logger.info(f"Transcribing: {audio_path}")
        return self._transcribe_single(audio_path)
    
    def _transcribe_single(self, audio_path: Path) -> List[TranscriptSegment]:
        """Transcribe a single audio file."""
        result = self.model.transcribe(
            str(audio_path),
            verbose=False,
            language="en",  # Auto-detect if needed
            task="transcribe"
        )
        
        segments = []
        for segment in result["segments"]:
            segments.append(TranscriptSegment(
                text=segment["text"].strip(),
                start=segment["start"],
                end=segment["end"]
            ))
        
        return segments


class ViralityAnalyzer:
    """Analyzes transcript for viral moments using AI."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for analysis
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def analyze(self, segments: List[TranscriptSegment], video_info: Dict) -> List[ViralMoment]:
        """
        Analyze transcript segments for viral potential.
        
        Args:
            segments: List of transcript segments
            video_info: Metadata about the video
            
        Returns:
            List of ViralMoment objects
        """
        logger.info("Analyzing for viral moments...")
        
        # Prepare transcript with timestamps
        transcript_with_times = self._format_transcript(segments)
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(transcript_with_times, video_info)
        
        # Get AI analysis
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at identifying viral video moments. Analyze transcripts to find highly engaging, shareable moments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Parse response
        try:
            analysis = json.loads(response.choices[0].message.content)
            return self._parse_viral_moments(analysis, segments)
        except json.JSONDecodeError:
            logger.error("Failed to parse AI response")
            return []
    
    def _format_transcript(self, segments: List[TranscriptSegment]) -> str:
        """Format transcript with timestamps for analysis."""
        lines = []
        for segment in segments:
            timestamp = f"[{segment.start:.1f}s - {segment.end:.1f}s]"
            lines.append(f"{timestamp} {segment.text}")
        return "\n".join(lines)
    
    def _create_analysis_prompt(self, transcript: str, video_info: Dict) -> str:
        """Create the prompt for viral moment analysis using CLEAR framework."""
        return f"""You are a viral video clip expert helping content creators identify high-performing short-form content from long-form videos.

=== CLARITY ===
Problem: Extract 3-4 viral-worthy clips from this YouTube video that will perform on TikTok, Reels, and Shorts.

Video Context:
- Title: {video_info.get('title', 'Unknown')}
- Channel: {video_info.get('channel', 'Unknown')}
- Duration: {video_info.get('duration', 0)} seconds

Objective: Identify clips with 0.75+ virality scores that capture COMPLETE thoughts/stories.

Scope:
✅ IN: Self-contained moments with natural beginning/end, complete narrative arcs, full back-and-forths
❌ OUT: Mid-sentence cuts, incomplete thoughts, clips requiring prior context

=== LOGIC ===
Clip Selection Process:
1) Scan transcript for high-energy moments (hooks, punchlines, reveals, reactions)
2) Expand boundaries to capture COMPLETE thought (30-60 seconds optimal, 25-65 acceptable)
3) Ensure clip starts at natural sentence/idea beginning and ends at natural conclusion
4) Verify clip is self-contained (understandable without watching full video)
5) Assign virality score based on emotional impact + shareability + completeness

Decision Rules:
- Duration: 30-60s target (25-65s acceptable range)
- NEVER cut mid-sentence or mid-thought
- If punchline exists, MUST include full setup + delivery
- If dialogue/exchange, capture BOTH sides completely
- Prefer natural pauses/transitions as boundaries

=== EXAMPLES ===

POSITIVE Examples (from successful viral clips):
✅ "So one of the first thing according to the SEC..." [40s] - Complete accusation explanation + personal take
✅ "What happened was he was starting a private equity fund..." [35s] - Full story arc: setup → brands → conclusion
✅ "At the end of all these events he would say..." [30s] - Complete concept with context + definition

EDGE CASES:
- Fast-paced dialogue: Ensure both question AND answer included
- Multi-part stories: Capture one complete chapter, not fragments
- Technical explanations: Include setup + explanation + implication

COUNTEREXAMPLE (what NOT to do):
❌ Starting with "...and that's why" (missing context)
❌ Ending mid-explanation "So basically you need to..." (incomplete)
❌ Cutting off punchline or response in dialogue

=== ADAPTATION ===
Quality Check Protocol:
- Read clip transcript aloud - does it make sense standalone?
- Check boundaries - natural pause at start/end?
- Verify duration - 30-60s sweet spot achieved?
- If clip feels incomplete, extend 5-10s in needed direction

=== RESULTS ===
Return JSON with this EXACT structure:
{{
    "viral_moments": [
        {{
            "start_time": <float seconds - find natural sentence start>,
            "end_time": <float seconds - find natural sentence end>,
            "hook": "<8-12 word catchy title capturing the moment>",
            "virality_score": <0.0-1.0 based on: 0.3=emotional impact, 0.3=shareability, 0.2=completeness, 0.2=platform fit>,
            "reasoning": "<2-3 sentences: WHY viral + WHAT makes it complete + WHERE it fits>",
            "transcript_excerpt": "<first 10-15 words to verify clip content>"
        }}
    ]
}}

TRANSCRIPT WITH TIMESTAMPS:
{transcript}

SUCCESS CRITERIA:
✅ 3-4 clips total
✅ Each 30-60 seconds (strict: no <25s or >65s)
✅ Each starts/ends at sentence boundaries
✅ Each self-contained (test: "Can viewer understand without context?")
✅ Highest virality score moments prioritized
✅ No overlapping clips

DURATION ENFORCEMENT (CRITICAL):
⚠️ REJECT any clip <25 seconds - it's incomplete by definition
⚠️ REJECT any clip >65 seconds - it's too long for short-form platforms
⚠️ If a moment seems viral but is <25s, EXPAND to capture more context
⚠️ If a moment is >65s, either SPLIT into multiple clips OR TRIM to capture the core moment
⚠️ MANDATORY: Calculate end_time - start_time and verify it's between 25-65 BEFORE including in output

GUARDRAILS:
- NEVER cut mid-sentence
- NEVER omit punchline/conclusion
- NEVER create clips requiring prior knowledge
- NEVER accept clips outside 25-65s duration range
- ALWAYS verify natural speaking rhythm preserved
- ALWAYS extend short clips to capture complete context"""
    
    def _parse_viral_moments(self, analysis: Dict, segments: List[TranscriptSegment]) -> List[ViralMoment]:
        """Parse AI analysis into ViralMoment objects with duration validation."""
        moments = []
        MIN_DURATION = 25  # seconds
        MAX_DURATION = 65  # seconds

        for moment_data in analysis.get("viral_moments", []):
            # Find relevant transcript text
            start = moment_data["start_time"]
            end = moment_data["end_time"]
            duration = end - start

            # ENFORCE DURATION CONSTRAINTS - skip clips outside range
            if duration < MIN_DURATION or duration > MAX_DURATION:
                logger.warning(f"Skipping clip with invalid duration: {duration:.1f}s (must be {MIN_DURATION}-{MAX_DURATION}s)")
                continue

            relevant_text = " ".join([
                seg.text for seg in segments
                if seg.start <= end and seg.end >= start
            ])

            moment = ViralMoment(
                start_time=start,
                end_time=end,
                transcript=relevant_text[:500],  # Limit length
                hook=moment_data.get("hook", ""),
                virality_score=moment_data.get("virality_score", 0.5),
                reasoning=moment_data.get("reasoning", "")
            )
            moments.append(moment)

        # Sort by virality score
        moments.sort(key=lambda x: x.virality_score, reverse=True)
        return moments


class ViralityDetector:
    """Main orchestrator for the virality detection pipeline."""
    
    def __init__(self, openai_api_key: str, whisper_model: str = "base"):
        self.downloader = YouTubeDownloader()
        self.transcriber = WhisperTranscriber(whisper_model)
        self.analyzer = ViralityAnalyzer(openai_api_key)
        
    def process_video(self, url: str) -> Dict:
        """
        Process a YouTube video end-to-end.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary containing full results
        """
        try:
            # Step 1: Download audio
            logger.info("Step 1/4: Downloading audio...")
            audio_path, video_info = self.downloader.download_audio(url)
            
            # Step 2: Transcribe
            logger.info("Step 2/4: Transcribing audio...")
            segments = self.transcriber.transcribe(audio_path)
            
            # Step 3: Analyze for virality
            logger.info("Step 3/4: Analyzing for viral moments...")
            viral_moments = self.analyzer.analyze(segments, video_info)
            
            # Step 4: Format results
            logger.info("Step 4/4: Formatting results...")
            results = self._format_results(video_info, segments, viral_moments)
            
            # Cleanup
            audio_path.unlink()
            
            return results
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise
    
    def _format_results(self, video_info: Dict, segments: List[TranscriptSegment], 
                       viral_moments: List[ViralMoment]) -> Dict:
        """Format all results into a structured dictionary."""
        return {
            "video": {
                "title": video_info.get("title"),
                "url": video_info.get("webpage_url"),
                "duration": video_info.get("duration"),
                "channel": video_info.get("channel"),
            },
            "viral_moments": [
                {
                    "rank": i + 1,
                    "timestamp": moment.to_timestamp(),
                    "start_seconds": moment.start_time,
                    "end_seconds": moment.end_time,
                    "duration": moment.end_time - moment.start_time,
                    "hook": moment.hook,
                    "virality_score": moment.virality_score,
                    "reasoning": moment.reasoning,
                    "transcript": moment.transcript
                }
                for i, moment in enumerate(viral_moments)
            ],
            "full_transcript": [
                {
                    "timestamp": segment.to_timestamp(),
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                }
                for segment in segments
            ]
        }


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Detect viral moments in YouTube videos")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--whisper-model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size")
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument("--no-transcript", action="store_true", 
                       help="Exclude full transcript from output")
    
    args = parser.parse_args()
    
    # Set up API key
    os.environ["OPENAI_API_KEY"] = args.api_key
    
    # Process video
    detector = ViralityDetector(args.api_key, args.whisper_model)
    results = detector.process_video(args.url)
    
    # Remove transcript if requested
    if args.no_transcript:
        del results["full_transcript"]
    
    # Output results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to: {args.output}")
    else:
        # Print to console
        print("\n" + "="*50)
        print("VIRAL MOMENTS DETECTED")
        print("="*50)
        
        for moment in results["viral_moments"]:
            print(f"\n#{moment['rank']} - {moment['hook']}")
            print(f"   Timestamp: {moment['timestamp']}")
            print(f"   Score: {moment['virality_score']:.2f}")
            print(f"   Why: {moment['reasoning']}")
            print(f"   Duration: {moment['duration']:.1f} seconds")
            print("-"*50)
        
        print(f"\nFull results: {len(results['viral_moments'])} moments found")


if __name__ == "__main__":
    main()