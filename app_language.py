from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Get environment variables
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Validate environment variables
if not endpoint or not key:
    print("Error: Missing required environment variables!")
    print("Please set the following in your .env file:")
    print("  AZURE_LANGUAGE_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/")
    print("  AZURE_LANGUAGE_KEY=your_language_key_here")
    sys.exit(1)

# Initialize the client
client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)

def detect_language(text):
    """
    Detect the language of the given text using Azure AI Language service.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with language information
    """
    try:
        # Azure Text Analytics expects a list of documents
        documents = [text]
        
        # Detect language
        response = client.detect_language(documents=documents)
        
        # Process results
        for doc in response:
            if doc.is_error:
                print(f"Error: {doc.error.code} - {doc.error.message}")
                return None
            else:
                result = {
                    "detected_language": doc.primary_language.name,
                    "iso6391_name": doc.primary_language.iso6391_name,
                    "confidence_score": doc.primary_language.confidence_score,
                }
                return result
                
    except Exception as e:
        print(f"Encountered an error: {e}")
        return None

def main():
    # Example texts in different languages
    sample_texts = [
        "Hello, how are you today?",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "Guten Tag, wie geht es dir?",
        "مرحبا، كيف حالك؟",
        "こんにちは、元気ですか？",
    ]
    
    # If text is provided as command line argument, use it
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(f"Analyzing text: {text}\n")
        result = detect_language(text)
        if result:
            print(f"Detected Language: {result['detected_language']}")
            print(f"ISO 639-1 Code: {result['iso6391_name']}")
            print(f"Confidence Score: {result['confidence_score']:.2%}")
    else:
        # Run examples
        print("Azure AI Language Detection Examples\n" + "="*50)
        for text in sample_texts:
            print(f"\nText: {text}")
            result = detect_language(text)
            if result:
                print(f"  → Language: {result['detected_language']} ({result['iso6391_name']})")
                print(f"  → Confidence: {result['confidence_score']:.2%}")

if __name__ == "__main__":
    main()

