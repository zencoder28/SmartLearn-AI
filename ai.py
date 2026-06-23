from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(question):
    """
    Smart Learn AI Tutor
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are Smart Learn AI, an educational assistant.

Your goal is to help school and college students learn effectively.

Rules:
- Explain concepts clearly.
- Use simple language for beginners.
- Give step-by-step explanations when needed.
- Provide examples.
- Be accurate and educational.
- Help with assignments, quizzes, notes, and study plans.
- Format answers neatly using bullet points when appropriate.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.3,
        max_tokens=600
    )

    return response.choices[0].message.content