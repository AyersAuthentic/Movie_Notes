from moviepy.editor import VideoFileClip
from pathlib import Path
import os

def extract_audio_from_video(video_path, output_path=None):
    """
    Extracts audio from a local video file and saves it as a .wav file.
    
    Arguments:
        video_path (str): Path to the local video file
        output_path (str, optional): Path where the audio should be saved. 
                                   If None, saves in the same directory as video
    
    Returns:
        str: Path to the extracted audio file
    """
    try:
        # Convert string path to Path object
        video_path = Path(video_path)
        
        # If no output path is specified, use the same directory as video
        if output_path is None:
            output_path = video_path.with_suffix('.wav')
        
        # Load the video file
        video = VideoFileClip(str(video_path))
        
        # Extract the audio
        audio = video.audio
        
        print(f"Extracting audio from {video_path}...")
        
        # Write the audio file with balanced quality settings
        audio.write_audiofile(
            str(output_path),
            fps=16000,     # Reduced from 44100, still good for speech
            nbytes=2,      # 16-bit depth (CD quality) instead of 32-bit
            codec='pcm_s16le'  # Standard PCM format
        )
        
        # Close the video to free up resources
        video.close()
        audio.close()
        
        print(f"Audio extracted and saved to {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        raise 