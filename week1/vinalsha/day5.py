import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from scraper import fetch_website_links, fetch_website_contents

GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(f"[ERROR] API key is NOT found, please check!")
if not api_key.startswith("AIz"):
    raise ValueError(f"[ERROR] API key does NOT starting with 'AIz', please check!")
if not api_key.strip() == api_key:
    raise ValueError(f"[ERROR] API key contains tabs/whitespaces around it, please check!")

print(f"[INFO] API key looks good!")

client = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=api_key
)

links = fetch_website_links("https://www.edwarddonner.com")

# print(f"Links: {links}")

link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links will be most relevant to include in a brochure abour the company.
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {
            "type": "About page",
            "url": "https://full.url/goes/here/about"
        },
        {
            "type": "Careers page",
            "url": "https://another.full.url/careers"
        }
    ]
}
"""

def get_links_user_prompt(url):
    user_prompt = """
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company,
respond with full https URL in JSON format.
Do not include Terms of Service, Privacy, Email links.

Links (some might be relative links): 
"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


# print(get_links_user_prompt("https://www.edwarddonner.com"))

def select_relevant_links(url):
    print(f"Selecting relevant links from the {url} by calling {GEMINI_MODEL}")
    messages = [
        {
            "role": "system",
            "content": link_system_prompt
        },
        {
            "role": "user",
            "content": get_links_user_prompt(url)
        }
    ]

    response = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=messages,
        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    # print(content)

    links = json.loads(content).get("links", None)

    return links

# select_relevant_links("https://www.edwarddonner.com")

def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n### Relevant Links:\n"
    for link in relevant_links:
        result += f"\n\n### Link: {link["type"]}\n"
        result += fetch_website_contents(link["url"])
    return result

# print(fetch_page_and_all_relevant_links("https://www.edwarddonner.com"))

brochure_system_prompt = """
You are an assistant that analyses the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
Use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[0:5000]  # Truncate if more than 5000 characters
    return user_prompt

# get_brochure_user_prompt("HuggingFace", "https://www.huggingface.co")

def create_brochure(company_name, url):
    messages = [
        {
            "role": "system",
            "content": brochure_system_prompt
        },
        {
            "role": "user",
            "content": get_brochure_user_prompt("HuggingFace", "https://www.huggingface.co")
        }
    ]

    response = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=messages
    )

    print(response.choices[0].message.content)

create_brochure("HuggingFace", "https://www.huggingface.co")