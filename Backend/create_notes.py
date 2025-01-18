import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
from constants import TEXT_PATH, NOTES_PATH


load_dotenv()

## transcription of a lecture by Jordan Peterson on the psychological significance of the Bible. 

prompt = (
    """
You are an expert in structured summarization, note-taking, and knowledge distillation. Your task is to generate **detailed, comprehensive, and structured notes** from the following transcript. These notes should follow the **O1 reasoning model**, meaning they must focus on the most important insights while ensuring depth and clarity.

### **Instructions for Note Generation**:
1. **Comprehensive Summaries**:  
   - Summarize each major section in **as much detail as necessary** to fully capture key ideas.  
   - Provide full explanations, avoiding excessive brevity or information loss.  
   - Retain the logical flow of ideas while making the content easier to digest.  

2. **Structured Formatting**:  
   - Use **clear section headers** for different topics and subtopics.  
   - **Bullet points** should break down key concepts for readability.  
   - Include **diagrams, equations, or code snippets** if applicable.  

3. **Actionable Insights & Applications**:  
   - Extract practical takeaways and **decision-making frameworks** where relevant.  
   - Provide **real-world applications, examples, or case studies** to reinforce concepts.  

4. **Maintain Clarity Without Oversimplification**:  
   - Do not oversimplify complex ideas—**retain necessary depth and nuance**.  
   - Use technical explanations where appropriate, ensuring accuracy.  
   - Provide definitions or explanations for specialized terms as needed.  

---

### **Example Format for the Notes:**  

## **Topic: O1 Reasoning Model for Decision-Making**  

### **Overview & Core Concept**  
The **O1 reasoning model** is a structured approach to decision-making that focuses on **speed and efficiency** by leveraging heuristics, automation, and predefined frameworks. The term **O1** is derived from **constant-time complexity (O(1))** in computer science, where an operation executes in the same amount of time regardless of input size.  

By contrast, **O(n) reasoning** requires a more in-depth analysis, where effort scales with complexity. O(n) reasoning is useful for **high-stakes, novel, or uncertain situations** where deeper analysis is required, but for most daily decisions, O1 reasoning can save cognitive energy and improve efficiency.  

### **Key Insights**  

#### **1. When to Use O1 Reasoning**  
- **Routine or Repetitive Decisions**  
  - Decisions that occur frequently should be **automated or predefined** to avoid wasting time.  
  - Example: Choosing what to eat for breakfast—having a fixed meal plan removes daily decision-making friction.  

- **Time-Sensitive Situations**  
  - If a decision must be made quickly, **pre-established mental models** or rules can streamline the process.  
  - Example: A paramedic doesn’t deliberate over every possible treatment—protocols guide immediate action.  

- **High-Certainty, Low-Risk Decisions**  
  - If the stakes are low and the correct choice is obvious, O1 reasoning is preferable.  
  - Example: If your usual route to work is blocked, choosing the next fastest alternative doesn’t require deep analysis.  

#### **2. When NOT to Use O1 Reasoning**  
- **Complex, High-Stakes Decisions**  
  - Major career moves, financial investments, or architectural software design decisions often require O(n) reasoning.  
- **Novel Situations with Uncertain Variables**  
  - If no prior knowledge or heuristics exist, analysis and exploration are necessary.  

### **Practical Applications of O1 Reasoning**  

#### **A. Personal Productivity**  
1. **Predefine Your Workflows**  
   - Use checklists and decision trees for common tasks.  
   - Example: **“If an email takes <2 minutes to answer, respond immediately.”**  

2. **Use Heuristics for Daily Life**  
   - Example: Always choose the **healthiest available meal option** when unsure what to eat.  

#### **B. Machine Learning & AI Applications**  
1. **Automating Decision Processes**  
   - Many AI models operate on O1 reasoning principles by applying predefined rules to classify data rapidly.  
   - Example: A spam filter automatically categorizes an email based on trained heuristics.  

2. **O1 vs. O(n) in Algorithm Design**  
   - O(1) operations (like hash table lookups) are preferred for efficiency in data structures.  
   - Example: A caching system retrieves frequently accessed data in O(1) time rather than recalculating it.  

### **Actionable Steps**  
1. **Identify Repetitive Decisions**  
   - Write down decisions you make daily that could be automated or simplified.  

2. **Create Predefined Rules**  
   - Example: “If I need to buy something under $50 and I’ve already researched it, I don’t spend more than 5 minutes deciding.”  

3. **Use Decision Matrices for More Complex Choices**  
   - If a decision is semi-complex but still frequent, use a framework (e.g., Eisenhower Matrix for prioritization).  

4. **Automate or Delegate Whenever Possible**  
   - Use scheduling tools, automation scripts, or assistants for low-level tasks.  

---

### **Process:**  
Now, extract and structure the information from the following transcript:  
---  
 

"""
    

   
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_detailed_notes(text):
    """Generates detailed, structured notes for an entire document using OpenAI's GPT-4o model."""
    messages = [
            {
                "role": "user",
                "content": f"""
                    {prompt}

                    \n{text}\n\nComplete your task below:
                """
            }
        ]
    
    response = client.chat.completions.create(
        model="o1-mini-2024-09-12",  
        messages=messages,
        ##temperature=0.4
    )
    
    return response.choices[0].message.content



def read_transcription_file():
    """Reads the transcription file if it exists."""
    transcription_file_path = f"{TEXT_PATH}/transcription.txt"
    if not os.path.exists(transcription_file_path):
        raise FileNotFoundError(
            f"Transcription file not found at {transcription_file_path}. Ensure the file is created before running this script."
        )
    with open(transcription_file_path, "r") as f:
        return f.read()

def save_detailed_notes(notes):
    """Saves the generated detailed notes to a file."""
    os.makedirs(NOTES_PATH, exist_ok=True)
    detailed_notes_file_path = f"{NOTES_PATH}/detailed_notes.txt"
    with open(detailed_notes_file_path, "w") as f:
        f.write(notes)


