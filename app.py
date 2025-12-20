from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),

)
# Upload the PDF file
with open("999930.pdf", "rb") as pdf_file:
    file = client.files.create(
        file=pdf_file,
        purpose="assistants",  # Valid values: "assistants", "fine-tune", or "batch"
    )

schema_prompt = """Extract the following JSON schema from the provided document.
Return ONLY valid JSON.
Schema:
{
  "summary": string,                  // concise 2-3 sentence summary
  "key_points": [string],             // bullet points of main points
  "action_items": [string],           // tasks or follow-ups, empty if none
  "citations": [                      // cite where you got the info
    {
      "page": integer,                // page number if known, else null
      "quote": string                 // supporting snippet
    }
  ]
}
"""

input = [
    {"role": "system", "content": schema_prompt},
    {
        "role": "user",
        "content": [
            {
                "type": "input_file",
                "file_id": file.id,
            },
            {
                "type": "input_text",
                "text": "Produce the JSON according to the schema."
            }
        ]
    },
]

response = client.responses.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    input=input,
    temperature=0.0,
    stream=False,
)

# Parse and print structured JSON
output_text = response.output_text
try:
    parsed = json.loads(output_text)
    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError:
    # Fallback: print raw text if not valid JSON
    print(output_text)
    