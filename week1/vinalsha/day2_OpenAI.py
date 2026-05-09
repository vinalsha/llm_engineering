### Agenda: How can we hit the OpenAI API endpoint (hence the LLM)
### with requests module and get a response?

import os
import requests
from dotenv import load_dotenv


def validate_api_key() -> str:
    """Load and validate OPENAI_API_KEY, then return it."""
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key is NOT found! Please check your .env")
    if not api_key.startswith("sk-proj-"):
        raise ValueError("API key is found, but it does NOT start with 'sk-proj-', please check")
    if api_key.strip() != api_key:
        raise ValueError("API key is found, but there are tabs/whitespaces around the key, please check")

    print("API key is found and it looks good!")
    return api_key


def main() -> None:
    """Send a simple chat completion request and print the model response."""
    api_key = validate_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "user",
            "content": "Hello GPT! This is my very first message to you! Hi!",
        }
    ]

    payload = {
        "model": "gpt-5-nano",
        "messages": messages,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
    except requests.exceptions.RequestException as exc:
        print("Request to OpenAI endpoint failed before receiving a response.")
        print(f"Error details: {exc}")
        raise SystemExit(1)

    if response.ok:
        print("Request to OpenAI endpoint is successful!")
        body = response.json()
        choices = body.get("choices", [])
        if not choices:
            print("Response did not include any choices.")
            raise SystemExit(1)

        content = choices[0].get("message", {}).get("content")
        if not content:
            print("Response choice did not include message content.")
            raise SystemExit(1)

        print(content)
    else:
        print("Request to OpenAI endpoint has failed!")
        print(
            f"status_code: {response.status_code}\n"
            f"reason: {response.reason}\n"
            f"text: {response.text}"
        )


if __name__ == "__main__":
    main()
