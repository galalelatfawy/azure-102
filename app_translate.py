from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text.models import InputTextItem
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()

# Get environment variables
key = os.getenv("AZURE_TRANSLATOR_KEY")
endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
region ="eastus"
credential = AzureKeyCredential(key)
source_language = "en"
target_language = "fr"
text = "Hello, world!"
document = InputTextItem(text=text)
client = TextTranslationClient(endpoint=endpoint, credential=credential, region=region)

# Translate text - correct API format
# body can be a list of strings or InputTextItem objects
response = client.translate(
    body=[document],
    to_language=[target_language],
)
# Print results
for translation in response:
    if translation.translations:
        for t in translation.translations:
            print(f"Original: {document.text}")
            print(f"Translated ({t.to}): {t.text}")
            print(f"Confidence: {t.confidence_score if hasattr(t, 'confidence_score') else 'N/A'}")