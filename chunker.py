from pydub import AudioSegment
import os

def split_audio(audio_path, chunk_length_ms, output_dir):
    """
    Splits an audio file into smaller chunks of a specified length.
    Arguments:
        audio_path (str): Path to the audio file to be split.
        chunk_length_ms (int): Length of each chunk in milliseconds.
        output_dir (str): Directory to save the audio chunks.
    Returns:
        list: Paths to the generated audio chunks.
    """
    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create chunks and save them
    chunk_paths = []
    for index, start_time in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk = audio[start_time:start_time + chunk_length_ms]
        chunk_path = os.path.join(output_dir, f"chunk_{index}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
        print(f"Chunk {index} saved as {chunk_path}")

    return chunk_paths  # Return a list of paths to the audio chunks