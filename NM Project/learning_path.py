from gemini_client import ask_gemini


def get_learning_recommendations(topic: str) -> str:

    prompt = f"""
You are EduGenie, an educational learning planner.

Create a step-by-step learning path for:

{topic}

Structure the answer as:

BEGINNER LEVEL
- Concepts to learn
- Practice

INTERMEDIATE LEVEL
- Concepts to learn
- Practice

ADVANCED LEVEL
- Concepts to learn
- Practice

PROJECTS
- Small project ideas

RESOURCES
- Documentation
- Videos
- Articles
- Books

FINAL GOAL
Explain what the learner should be able to do after completing the path.

Keep the plan practical and easy to follow.
"""

    return ask_gemini(prompt)