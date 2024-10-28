from openai import OpenAI
import os
import glob
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from the .env file
load_dotenv()

# Load API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio_chunk(file_path):
    """
    Transcribes a single audio chunk using OpenAI's Whisper model.
    Arguments:
        file_path (str): Path to the audio file to transcribe.
    Returns:
        tuple: (file_path, transcribed text) or None if an error occurs.
    """
    try:
        # Read the file and send to Whisper
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return file_path, transcript.text
    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")
        return None

def transcribe_chunks(chunk_dir):
    """
    Transcribes all audio chunks in a specified directory concurrently.
    Arguments:
        chunk_dir (str): Directory containing audio chunks.
    Returns:
        list: List of transcriptions for each audio chunk in sorted order.
    """
    # Custom sort key to sort chunk files by numeric order
    def sort_key(path):
        match = re.search(r"chunk_(\d+)\.wav", path)
        return int(match.group(1)) if match else float('inf')

    # Sort chunk files in the directory
    chunk_paths = sorted(glob.glob(f"{chunk_dir}/chunk_*.wav"), key=sort_key)
    
    transcriptions = []
    
    # Use ThreadPoolExecutor to transcribe files concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers based on your system's capacity
        futures = {executor.submit(transcribe_audio_chunk, path): path for path in chunk_paths}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                _, text = result
                transcriptions.append(text)
    
    return transcriptions

def save_transcriptions(transcriptions, output_dir):
    """
    Saves a list of transcriptions to a text file.
    Arguments:
        transcriptions (list): List of transcribed text from audio chunks.
        output_dir (str): Directory to save the transcription file.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the transcriptions to a file
    output_path = os.path.join(output_dir, "transcription.txt")
    with open(output_path, "w") as f:
        for text in transcriptions:
            f.write(text + "\n")
    print(f"Transcriptions saved to {output_path}")