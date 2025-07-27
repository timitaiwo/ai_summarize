import os
from openai import OpenAI

from .scraper import main

# Setup env
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL: str = os.getenv("GEMINI_BASE_API")
GEMINI_CLIENT: OpenAI = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)

base_url: str = os.getenv("ROOT_URL_LINK")


if __name__ == "__main__":
    main(base_url)
