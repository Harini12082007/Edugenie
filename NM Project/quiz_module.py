import json
import re

from gemini_client import ask_gemini


def clean_json(text: str) -> str:

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove ```
    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(passage: str):

    prompt = f"""
You are EduGenie quiz generator.

Create exactly 3 multiple-choice questions
from the following educational text.

TEXT:
{passage}

Return ONLY valid JSON.

Required format:

[
    {{
        "question": "Question 1",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Option A"
    }},
    {{
        "question": "Question 2",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Option B"
    }},
    {{
        "question": "Question 3",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Option C"
    }}
]

Rules:

- Exactly 3 questions.
- Exactly 4 options per question.
- answer must exactly match one option.
- Questions must be based on the supplied text.
- Do not add Markdown.
- Return JSON only.
"""

    raw_response = ask_gemini(prompt)

    cleaned = clean_json(raw_response)

    try:

        quiz = json.loads(cleaned)

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned invalid quiz format.",
            "raw_response": raw_response
        }

    if not isinstance(quiz, list):

        return {
            "error": "Quiz format is invalid."
        }

    if len(quiz) != 3:

        return {
            "error": "Quiz should contain exactly 3 questions."
        }

    for question in quiz:

        if "question" not in question:
            return {"error": "Question field missing."}

        if "options" not in question:
            return {"error": "Options field missing."}

        if "answer" not in question:
            return {"error": "Answer field missing."}

        if len(question["options"]) != 4:
            return {
                "error": "Each question must have exactly 4 options."
            }

        if question["answer"] not in question["options"]:
            return {
                "error": "Correct answer does not match options."
            }

    return quiz