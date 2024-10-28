import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
from constants import TEXT_PATH, NOTES_PATH


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_detailed_notes(text):
    """Generates detailed, structured notes for an entire document using OpenAI's GPT-4o model."""
    messages = [
        {"role": "system", "content": (
            "You are an expert note-taker and educator. Create comprehensive, structured notes that thoroughly cover the provided text. "
            "These notes should be in-depth and help the reader understand, retain, and explore the material in depth. "
            "Structure the notes to include main headings, subheadings, and bullet points, with each point containing paragraph-length explanations where appropriate. "
            "For each key idea, include:\n"
            "- A clear definition or detailed explanation.\n"
            "- Historical and cultural context, especially if relevant to modern perspectives.\n"
            "- Examples, case studies, or illustrations of the concept.\n"
            "- Comparisons to related theories, ideas, or perspectives, especially contrasting modern interpretations.\n"
            "- Reflections on the implications of each concept for modern life, psychology, or culture.\n"
            "Conclude with an exhaustive list of key takeaways, questions to promote deep thinking, and any remaining ambiguities or open-ended questions related to the topics.\n"
            "Aim to create notes that could serve as a study guide for someone learning this material in detail."
            "Lastly, Below the notes provide a comprehensive and detailed summary of the full text."
        )},
        {"role": "user", "content": f"Text:\n{text}\n\nProvide the notes below in a structured, concise format:"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Use the GPT-4o model with the extended token limit
        messages=messages,
        max_tokens=16000,  # Maximize token usage for a comprehensive output
        temperature=0.4
    )
    
    return response.choices[0].message.content



# Load your full transcription
with open(f"{TEXT_PATH}/transcription.txt", "r") as f:
    transcription_text = f.read()

# Generate detailed notes for the full text
detailed_notes = generate_detailed_notes(transcription_text)

# Save the detailed notes to a file
with open(f"{NOTES_PATH}/detailed_notes.txt", "w") as f:
    f.write(detailed_notes)