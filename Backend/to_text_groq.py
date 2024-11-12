from groq import Groq 
import os
import glob
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from the .env file
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  

def transcribe_audio_chunk(file_path):
    """
    Transcribes a single audio chunk using Groq’s transcription model.
    Arguments:
        file_path (str): Path to the audio file to transcribe.
    Returns:
        tuple: (file_path, transcribed text) or None if an error occurs.
    """
    try:
        # Read the file and send it to Groq's transcription API
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
              file=(file_path, audio_file.read()), # Required audio file
              model="whisper-large-v3-turbo", # Required model to use for transcription
            )
        return transcript.text
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
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(transcribe_audio_chunk, path): i for i, path in enumerate(chunk_paths)}
        
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                index = futures[future]
                transcriptions.append((index, result))
    
    # Sort by index to ensure order is maintained
    transcriptions.sort(key=lambda x: x[0])
    ordered_texts = [text for _, text in transcriptions]
    
    return ordered_texts

def save_transcriptions(transcriptions, output_dir):
    """
    Saves a list of transcriptions to a text file.
    Arguments:
        transcriptions (list): List of transcribed text from audio chunks.
        output_dir (str): Directory to save the transcription file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "transcription.txt")
    with open(output_path, "w") as f:
        for text in transcriptions:
            f.write(text + "\n")
    print(f"Transcriptions saved to {output_path}")