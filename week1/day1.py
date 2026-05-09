### Imports 

import os 
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

### Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# print(f"OPENAI_API_KEY: {api_key}")

### Check the key

if not api_key:
    print(f"No API key was found - \
        please head over the trobleshooting notebook in this folder to identify and fix!")
elif not api_key.startswith("sk-proj-"):
    print(f"An API key was found, \
        but it does not start with 'sk-proj-'; \
        please check if you are using the right key - \
        see troubleshooting notebook")
elif api_key.strip() != api_key:
    print(f"An API key was found, \
        but it looks like it might have space or tab characters at the start or end - \
        please remove them - \
        see troubleshooting notebook")
else:
    print(f"API key found and looks good so far!")

### Calling OpenAI's Chat Completions API

# To give you a preview, calling OpenAI with these messages is this easy. 
# Any problems, head over to the troubleshooting notebook.

message = "Hello, GPT! This is my first ever message to you! Hi!"

messages = [
    {
        "role": "user",
        "content": message
    }
]

# print(messages)

openai = OpenAI()

# I do not have any API credits, so this is destined to fail
# Will give a shot with Gemini later

try:
    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )

except Exception as exception:
    print(f"Exception: {exception}")
    # print(dir(exception))
    print(f"> args: {exception.args}")
    print(f"> body: {exception.body}")
    print(f"> code: {exception.code}")
    print(f"> message: {exception.message}")
    print(f"> param: {exception.param}")
    print(f"> request: {exception.request}")
    print(f"> request_id: {exception.request_id}")
    print(f"> response: {exception.response}")
    print(f"> status_code: {exception.status_code}")
    print(f"> type: {exception.type}")
    print(f"> with_traceback: {exception.with_traceback}")

    ### Sample output for my reference:

    # API key found and looks good so far!
    # Exception: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
    # > args: ("Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}",)
    # > body: {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}
    # > code: insufficient_quota
    # > message: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
    # > param: None
    # > request: <Request('POST', 'https://api.openai.com/v1/chat/completions')>
    # > request_id: req_c930f5df2f564da4b119a0594d42071b
    # > response: <Response [429 Too Many Requests]>
    # > status_code: 429
    # > type: insufficient_quota
    # > with_traceback: <built-in method with_traceback of RateLimitError object at 0x1093d1470>

else:
    # print(f"Response: {response}")
    print(f"Response: {response.choices[0].message.content}")

ed = fetch_website_contents("https://edwarddonner.com")
# print(ed)

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


# print(messages_for(ed))

def summarize(url):
    website_contents = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages=messages_for(website_contents)
    )
    return response.choices[0].message.content

# summarize("https://www.edwarddonner.com")

def display_summary(url):
    """
    A function to display the summary nicely in the output, using Markdown
    """
    summary = summarize(url)
    display(Markdown(summary))

display_summary("https://www.edwarddonner.com")
