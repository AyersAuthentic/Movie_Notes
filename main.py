import os
from fetch_audio import download_audio  # Import from fetch_audio.py
from chunker import split_audio  # Import from chunker.py
from to_text import transcribe_chunks, save_transcriptions  # Import from to_text.py
import argparse

from constants import AUDIO_PATH, CHUNK_PATH, CHUNK_LENGTH_MS, TEXT_PATH

def main(video_url):

    print(f"Beginning download from {video_url}...")
 
 
    transcription_output = "transcription.txt"  # Path for the final transcription text

    # Step 1: Download Audio
    print("Step 1: Downloading audio from YouTube...")
    download_audio(video_url, AUDIO_PATH)

    # Step 2: Chunk Audio
    print("Step 2: Splitting audio into smaller chunks...")
    if not os.path.exists(CHUNK_PATH):
        os.makedirs(CHUNK_PATH)
    
    split_audio(AUDIO_PATH, CHUNK_LENGTH_MS, CHUNK_PATH)
    
    # Step 3: Transcribe Chunks
    print("Step 3: Transcribing audio chunks...")
    transcriptions = transcribe_chunks(CHUNK_PATH)  # This should be a function in to_text.py

    # Step 4: Save Transcriptions
    print("Saving transcriptions to file...")
    save_transcriptions(transcriptions, TEXT_PATH)  # Also a function in to_text.py

    print(f"Transcription complete! Output saved to {transcription_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch audio from YouTube video")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video to fetch audio from")
    args = parser.parse_args()
    
    main(args.video_url)