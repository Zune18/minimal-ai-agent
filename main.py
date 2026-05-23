import os

from dotenv import load_dotenv
from openai import OpenAI

from agent import Agent


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "google/gemini-3.5-flash"

agent = Agent(
    client=client,
    model=MODEL
)

agent.run("What's the weather in London?")