from openai import OpenAI
from IPython import get_ipython
from scraper import fetch_website_contents
from IPython.display import Markdown, display

PROVIDER_MODEL = "llama3.2"  #"deepseek-r1:1.5b"
PROVIDER_API_KEY = "Ollama"  # It can be anything for Ollama
PROVIDER_BASE_URL = "http://localhost:11434/v1"


def show_summary(summary: str) -> None:
    if get_ipython() is not None:
        display(Markdown(summary))

    print(f"[INFO] Summary of the website: {summary}")


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
        print(f"[FAIL] {context} failed: response did not include choices.")
        return None

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message is None:
        print(f"[FAIL] {context} failed: response choice did not include message.")
        return None

    content = getattr(message, "content", None)
    if not content:
        print(f"[FAIL] {context} failed: response choice did not include content.")
        return None

    return content


def summarize(url, client):
    website_contents = fetch_website_contents(url)
    try:
        response = client.chat.completions.create(
            model=PROVIDER_MODEL,
            messages=messages_for(website_contents)
        )
    except Exception as exception:
        print(f"[FAIL] Summarization failed: {exception}")
        return None

    return extract_message_content(response, "Summarization")


def display_summary(url, client):
    """
    A function to display the summary nicely in the output, using Markdown
    """
    summary = summarize(url, client)
    if not summary:
        print("[FAIL] Summary was NOT generated.")
        return
    else:
        print(f"[INFO] Summarization successful")
    
    show_summary(summary)


def smoke_test_chat(client) -> bool:
    """
    Quick first message to verify chat completions is working.
    """
    message = "Hello! This is my first ever message to you! Hi!"

    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    try:
        response = client.chat.completions.create(
            model=PROVIDER_MODEL,
            messages=messages
        )
    except Exception as exception:
        print(f"[FAIL] Smoke-test chat failed with exception: {exception}")
        return False
    else:
        content = extract_message_content(response, "Smoke-test chat")
        if not content:
            return False

        print(f"[INFO] Smoke-test chat response: {content}")
        return True


def main():
    client = OpenAI(base_url=PROVIDER_BASE_URL, api_key=PROVIDER_API_KEY)
    if smoke_test_chat(client):
        display_summary("https://www.edwarddonner.com", client)
    else:
        print(f"[FAIL] Did NOT run summarization as smoke-test failed")


if __name__ == "__main__":
    main()
