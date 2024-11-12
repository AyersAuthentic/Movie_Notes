import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
from constants import TEXT_PATH, NOTES_PATH


load_dotenv()


prompt = (
    "You will be provided with a transcription of a lecture by Jordan Peterson on the psychological significance of the Bible. "
    "Your task is to create a comprehensive, structured study guide that allows readers to thoroughly understand, retain, and reflect on the material.\n\n"
    
    "You are a skilled note-taker, analyst, and educator. Approach this task with the goal of creating in-depth notes and summaries that explore each key idea and support long-term learning. "
    "Organize the notes into clear sections with main headings, subheadings, and bullet points, and paragraph form summaries.\n\n"
    
    "For each main section, provide:\n"
    "- A set of detailed notes exploring the ideas presented, structured to help readers engage with the material.\n"
    "- A concise summary of each section directly below the heading, distilling the main points covered in that section.\n\n"
    
    "Within each key idea, include:\n"
    "- **Precise Definitions or In-Depth Explanations**: Clearly define or explain each concept in a way that is accurate and accessible.\n"
    "- **Historical and Cultural Context**: Highlight relevant historical or cultural information, especially when it adds depth or modern relevance.\n"
    "- **Illustrative Examples or Analogies**: Use concrete examples, case studies, or relatable analogies to reinforce understanding.\n"
    "- **Comparative Analysis**: Offer comparisons with related theories or ideas, emphasizing differences and connections to modern perspectives.\n"
    "- **Reflections on Broader Implications**: Discuss the significance of each concept as it relates to contemporary psychology, culture, or personal well-being.\n\n"
    
    "After the main content, conclude with:\n"
    "- **Key Takeaways**: Summarize the core themes or principles for quick reference.\n"
    "- **Thought-Provoking Questions**: Pose questions that encourage the reader to think more deeply about the content.\n"
    "- **Unresolved Ambiguities or Open-Ended Topics**: Identify any lingering ambiguities or open questions that invite further exploration.\n\n"
    
    "Lastly, write a **comprehensive multi-paragraph summary** of the entire lecture. This summary should capture the full scope and complexity of the material, covering the main arguments, themes, and insights in a way that provides a clear, insightful overview. Do not restrict the summary to a single paragraph; use as many paragraphs as needed to cover the content effectively.\n\n"
    
    "Focus on creating a study guide that maximizes understanding and engagement, providing readers with a tool to explore the material in depth."
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_detailed_notes(text):
    """Generates detailed, structured notes for an entire document using OpenAI's GPT-4o model."""
    messages = [
        {"role": "system", "content": prompt },
        {"role": "user", "content": f"Lecture Transcription:\n{text}\n\nComplete your task below:"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",  # Use the GPT-4o model with the extended token limit
        messages=messages,
        max_tokens=16000,  # Maximize token usage for a comprehensive output
        ##temperature=0.4
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