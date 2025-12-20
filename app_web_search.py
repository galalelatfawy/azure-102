from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),

)



input = "What is the weather in Leipzig today?"

response = client.responses.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    input=input,
    temperature=0.0,
    tools=[
        {
            "type": "web_search",
        }
    ],
    # stream=False,
)

# Parse and print structured JSON
print(response.output_text)