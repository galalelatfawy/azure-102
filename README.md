## Azure PDF Extraction with OpenAI (Azure)

This project uploads a PDF to Azure OpenAI, asks the model to extract structured JSON according to a fixed schema, and prints the parsed result.

### Prerequisites
- Python 3.13+ (managed via `uv` in this repo)
- Azure OpenAI resource with a deployed model
- An API key with access to that deployment

### Setup
1) Install/refresh the env:
```bash
uv sync
```

2) Configure environment variables in `.env` (file is git-ignored):
```
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
```

3) Place your PDF at the project root as `999930.pdf` (or adjust the path in `app.py`).

### Run
```bash
uv run python app.py
```
The script:
- Uploads the PDF (`purpose="assistants"`).
- Prompts the model to produce JSON matching the schema.
- Parses and pretty-prints the JSON (falls back to raw text if parsing fails).

### Notes
- Streaming is disabled for predictable JSON parsing.
- `.env` is ignored by git; keep secrets there.
- Update `AZURE_OPENAI_DEPLOYMENT_NAME` to the exact deployment name (case-sensitive) from your Azure OpenAI resource.


