# AI Text Summarizer
Small web app to summarize text or URLs with a Transformer model.  
Also extracts top keywords using YAKE.

**Stack:** Python, Transformers (DistilBART), Gradio, YAKE  
**Deploy:** Hugging Face Spaces (serverless) · Docker (portable)

---

## Features
- Paste text **or** provide a URL
- Summarization with a lightweight Transformer pipeline
- Top-3 keywords with YAKE (language selectable)
- Simple, clean Gradio UI

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:7860


```

## Run with Docker

docker build -t ai-summarizer .
docker run -p 7860:7860 ai-summarizer
# open http://127.0.0.1:7860
