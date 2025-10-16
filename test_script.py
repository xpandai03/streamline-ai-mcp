#!/usr/bin/env python3
"""
Test script for YouTube Virality Detector
"""

import os
import sys

# Set API key (replace with your actual key or pass via environment variable)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

import importlib.util
import sys

# Import module with hyphens in filename
spec = importlib.util.spec_from_file_location("youtube_virality_detector", "youtube-virality-detector.py")
module = importlib.util.module_from_spec(spec)
sys.modules["youtube_virality_detector"] = module
spec.loader.exec_module(module)

from youtube_virality_detector import ViralityDetector
import json

def test_video(url: str):
    """Test the virality detector on a YouTube URL"""
    print(f"🎬 Testing with URL: {url}")
    print("=" * 60)

    try:
        # Initialize detector with smaller model for faster testing
        print("\n📥 Initializing detector (using 'tiny' model for speed)...")
        detector = ViralityDetector(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            whisper_model="tiny"  # Fastest model for testing
        )

        # Process video
        print("\n🔄 Processing video (this may take a few minutes)...")
        results = detector.process_video(url)

        # Display results
        print("\n" + "=" * 60)
        print("✅ RESULTS")
        print("=" * 60)
        print(f"\n📹 Video: {results['video']['title']}")
        print(f"📺 Channel: {results['video']['channel']}")
        print(f"⏱️  Duration: {results['video']['duration']} seconds")
        print(f"\n🔥 Found {len(results['viral_moments'])} viral moments:\n")

        for moment in results['viral_moments'][:4]:  # Show top 4
            print(f"#{moment['rank']}: {moment['hook']}")
            print(f"   ⏰ Time: {moment['timestamp']}")
            print(f"   📊 Score: {moment['virality_score']:.2f}/1.0")
            print(f"   💡 Why: {moment['reasoning'][:100]}...")
            print(f"   ⏳ Duration: {moment['duration']:.1f}s")
            print()

        # Save full results
        output_file = "test_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"💾 Full results saved to: {output_file}")
        print("\n✨ Test completed successfully!")

        return True

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test with a short video (easier/faster for testing)
    # You can replace this with any YouTube URL

    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    else:
        # Default test video - a short one for quick testing
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with actual test URL
        print("⚠️  No URL provided. Using default test video.")
        print("💡 Usage: python test_script.py <youtube_url>")
        print()

    test_video(test_url)
