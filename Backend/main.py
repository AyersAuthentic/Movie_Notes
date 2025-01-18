import os
from fetch_audio import download_audio
from extract_audio import extract_audio_from_video
from chunker import split_audio
from to_text import transcribe_chunks, save_transcriptions
from create_notes import generate_detailed_notes, read_transcription_file, save_detailed_notes
import argparse

from constants import AUDIO_PATH, CHUNK_PATH, CHUNK_LENGTH_MS, TEXT_PATH, NOTES_PATH

def main(source, is_local=False):
    print(f"Beginning {'extraction' if is_local else 'download'} from {source}...")
 
    transcription_output = "transcription.txt"

    # Step 1: Get Audio (either download or extract)
    print(f"Step 1: {'Extracting' if is_local else 'Downloading'} audio...")
    if is_local:
        extract_audio_from_video(source, AUDIO_PATH)
    else:
        download_audio(source, AUDIO_PATH)

    # Step 2: Chunk Audio
    print("Step 2: Splitting audio into smaller chunks...")
    if not os.path.exists(CHUNK_PATH):
        os.makedirs(CHUNK_PATH)
    
    split_audio(AUDIO_PATH, CHUNK_LENGTH_MS, CHUNK_PATH)
    
    # Step 3: Transcribe Chunks
    print("Step 3: Transcribing audio chunks...")
    transcriptions = transcribe_chunks(CHUNK_PATH)

    # Step 4: Save Transcriptions
    print("Saving transcriptions to file...")
    save_transcriptions(transcriptions, TEXT_PATH)

    print(f"Transcription complete! Output saved to {transcription_output}")

    # Load full transcription
    transcription_text = read_transcription_file()

    print("Step 4: Generating detailed notes...")
    detailed_notes = generate_detailed_notes(transcription_text)
    save_detailed_notes(detailed_notes)

    # Play completion sound
    try:
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    except Exception as e:
        print(f"Could not play completion sound: {e}")

    print(f"Notes complete! Output saved to {NOTES_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video to generate notes")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--youtube", "-yt", type=str, 
                      help="URL of the YouTube video to fetch audio from")
    group.add_argument("--local", "-l", type=str,
                      help="Path to local video file to extract audio from")
    args = parser.parse_args()
    
    if args.youtube:
        main(args.youtube, is_local=False)
    else:
        main(args.local, is_local=True)