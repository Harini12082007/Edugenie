from gemini_client import ask_gemini


def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie.

Summarize the following educational text.

TEXT:
{text}

Requirements:

- Keep important information.
- Remove repetition.
- Use simple language.
- Use bullet points where appropriate.
- Do not add unrelated information.
- Make it useful for exam revision.
"""

    return ask_gemini(prompt)