import os
import time

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Read model name
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Please create a .env file and add your Gemini API key."
    )


# Create Gemini client
client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt: str) -> str:

    # Try up to 3 times
    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.interactions.create(
                model=MODEL,
                input=prompt
            )

            answer = response.output_text

            if not answer:
                return "Gemini returned an empty response."

            return answer.strip()


        except Exception as e:

            error_message = str(e)
            error_lower = error_message.lower()


            # Network / DNS error
            if "getaddrinfo failed" in error_lower:

                return (
                    "Network error: Python cannot connect to Gemini API. "
                    "Please check your internet connection, DNS, firewall "
                    "or proxy settings."
                )


            # Gemini temporarily unavailable / high demand
            if (
                "503" in error_lower
                or "service_unavailable" in error_lower
                or "high demand" in error_lower
                or "temporarily unavailable" in error_lower
            ):

                if attempt < max_retries - 1:

                    wait_time = 3 * (attempt + 1)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                else:

                    return (
                        "Gemini is temporarily unavailable because "
                        "the service is experiencing high demand. "
                        "Please try again in a few moments."
                    )


            # Other API errors
            return f"Gemini API Error: {error_message}"


    return "Gemini request failed after multiple attempts."