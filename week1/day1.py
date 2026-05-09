import os
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display


def validate_api_key():
    """Load and validate OPENAI_API_KEY"""
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "No API key was found - please head over to the troubleshooting notebook in this folder."
        )
    if not api_key.startswith("sk-proj-"):
        raise ValueError(
            "An API key was found, but it does not start with 'sk-proj-'; please check."
        )
    if api_key.strip() != api_key:
        raise ValueError(
            "API key has leading/trailing spaces or tabs; please remove them."
        )

    print("API key found and looks good so far!")


### Define our system prompt

# You can experiment with this later, changing the last sentence to "Respond in markdown in Spanish."

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in code block - just respond with the markdown.
"""

### Define our user prompt

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.
"""

def messages_for(website):
    """
    It returns the particular messages format required by Open AI API endpoint
    """
    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt_prefix + website
        }
    ]


def extract_message_content(response, context):
    """
    Validate response shape and return choices[0].message.content.
    """
    choices = getattr(response, "choices", None)
    if not choices:
        print(f"{context} failed: response did not include choices.")
        return None

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message is None:
        print(f"{context} failed: response choice did not include message.")
        return None

    content = getattr(message, "content", None)
    if not content:
        print(f"{context} failed: response choice did not include content.")
        return None

    return content


def summarize(url, client):
    website_contents = fetch_website_contents(url)
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages_for(website_contents)
        )
    except Exception as exception:
        print(f"Summarization failed: {exception}")
        return None

    return extract_message_content(response, "Summarization")


def display_summary(url, client):
    """
    A function to display the summary nicely in the output, using Markdown
    """
    summary = summarize(url, client)
    if not summary:
        print("Summary was not generated.")
        return
    display(Markdown(summary))


def smoke_test_chat(client) -> bool:
    """
    Quick first message to verify chat completions is working.
    """
    message = "Hello, GPT! This is my first ever message to you! Hi!"
    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages
        )
    except Exception as exception:
        print(f"Smoke-test chat failed with exception: {exception}")
        return False
    else:
        content = extract_message_content(response, "Smoke-test chat")
        if not content:
            return False

        print(f"Response: {content}")
        return True


def main():
    validate_api_key()
    client = OpenAI()
    if smoke_test_chat(client):
        display_summary("https://www.edwarddonner.com", client)
    else:
        print(f"Did NOT run summarization as smoke-test failed")


if __name__ == "__main__":
    main()
