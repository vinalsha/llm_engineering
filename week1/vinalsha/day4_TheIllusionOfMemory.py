import os 
from dotenv import load_dotenv
from openai import OpenAI

GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(f"API key is NOT found!")
if not api_key.startswith("AIz"):
    raise ValueError(f"API key does NOT start with 'AIz', please check!")
if not api_key.strip() == api_key:
    raise ValueError(f"API key contains tabs/whitespaces around it, please check!")

print(f"[DEBUG] API key looks good!")

client = OpenAI(base_url=GEMINI_BASE_URL, api_key=api_key)

messages1 = [
    {
        "role": "system",
        "content": "You are a helpful assistant"
    },
    {
        "role": "user",
        "content": "Hi! I'm Ed!"
    }
]

print(f"[INFO] First user-prompt: Hi! I'm Ed!")

response1 = client.chat.completions.create(
    model=GEMINI_MODEL,
    messages=messages1
)

content1 = response1.choices[0].message.content

print(f"[INFO] First response from LLM: {content1}")

messages2 = [
    {
        "role": "system",
        "content": "You are a helpful assistant!"
    },
    {
        "role": "user",
        "content": "What is my name?"
    }
]

print(f"[INFO] Second user-prompt: What is my name?")

response2 = client.chat.completions.create(
    model=GEMINI_MODEL,
    messages=messages2
)

content2 = response2.choices[0].message.content

print(f"[INFO] Second response from LLM: {content2}")

print(f"[INFO] Me: What?! I just told you my name?!")

print(f"[INFO] Every call to an LLM is completely STATELESS. It's a totally new call, every single time")
print(f"[INFO] As AI engineers, it's OUR JOB to devise techniques to give the impression that the LLM has a 'memory'")

print(f"[INFO] Third user-prompt: Gave both first & second user prompts in one call, this is the trick!")

messages3 = [
    {
        "role": "system",
        "content": "You are a helpful assistant"
    },
    {
        "role": "user",
        "content": "Hi! I am Ed!"
    },
    {
        "role": "assistant",
        "content": "Hi Ed! How can I help you today?"
    },
    {
        "role": "user",
        "content": "What is my name?"
    }
]

response3 = client.chat.completions.create(
    model=GEMINI_MODEL,
    messages=messages3
)

content3 = response3.choices[0].message.content

print(f"[INFO] Third response from LLM: {content3}")


