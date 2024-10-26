import yt_dlp
from constants import AUDIO_PATH

def download_audio(video_url, audio_path):
    """
    Downloads audio from a YouTube video and saves it as a .wav file.
    Arguments:
        video_url (str): The URL of the YouTube video to download.
    Returns:
        str: Path to the downloaded audio file.
    """
    # Define options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best audio format available
        'outtmpl': audio_path.replace('.wav', ''),       # Save in the path defined in constants
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use ffmpeg to extract the audio
            'preferredcodec': 'wav',      # Change to 'mp3' if needed
            'preferredquality': '192',    # Best audio quality
        }],
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {video_url}...")
        ydl.download([video_url])
        print(f"Audio downloaded and saved to {audio_path}")

    return AUDIO_PATH  # Return the path to the downloaded audio file
