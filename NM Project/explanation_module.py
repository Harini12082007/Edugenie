from gemini_client import ask_gemini


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie, a friendly teacher.

Explain the following topic to a beginner.

Topic:
{topic}

Use this structure:

1. Definition
2. Main idea
3. Important points
4. Simple example
5. Short recap

Use simple English.
Avoid unnecessarily difficult words.
"""

    return ask_gemini(prompt)