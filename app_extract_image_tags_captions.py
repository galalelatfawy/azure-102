from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = ImageAnalysisClient(
    endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_VISION_KEY")),
)
with open("image.png", "rb") as image_file:
    image = image_file.read()

response = client.analyze(
    image_data=image,
    visual_features=[VisualFeatures.TAGS,VisualFeatures.OBJECTS,VisualFeatures.CAPTION]
)

print(response.tags)
print(json.dumps(response.as_dict(), indent=2))